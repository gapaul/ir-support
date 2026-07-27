"""Capture a short MP4 from a real Swift browser scene.

This is an optional worked example for staff, advanced students, or automated
workflows that need frames from the actual Peter Corke Swift WebGL canvas. The
public Swift API can save screenshots through the browser, but it does not
provide a convenient Python-owned frame stream. This example uses Chrome
DevTools to capture the WebGL canvas after each Swift step.

Before running this script, patch the installed Swift package:

    python -m ir_support.doctor --patch-advanced-swift-capture

Google Chrome must be installed. The packages used here are normally installed
by `ir-support-full`; if you use a smaller environment, install missing
packages reported by the script.

Run from a terminal with your virtual environment active:

    python -m ir_support.functions.swift_video_capture_example

Useful options:

    python -m ir_support.functions.swift_video_capture_example --output demo.mp4
    python -m ir_support.functions.swift_video_capture_example --frames 120 --fps 24
    python -m ir_support.functions.swift_video_capture_example --visible

The default scene uses only core dependencies: a UR3e robot and a simple orange
Cuboid object. The output video is written to the current working directory.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import json
import math
import os
from io import BytesIO
from pathlib import Path
import shutil
import socket
import subprocess
import time
from typing import Callable, Iterable
from urllib.parse import quote
import uuid
import webbrowser

import numpy as np


FrameStep = Callable[[object, dict, int], None]


class SwiftCaptureError(RuntimeError):
    """Raised when the Swift browser capture plumbing cannot complete."""


def _capture_imports():
    try:
        from PIL import Image
        import requests
        import swift
        import websockets
    except ModuleNotFoundError as exc:
        raise SwiftCaptureError(
            "Missing optional Swift capture dependency. Install ir-support-full "
            "or install the missing package, then try again."
        ) from exc

    return Image, requests, swift, websockets


def _opencv_import():
    try:
        import cv2
    except ModuleNotFoundError as exc:
        raise SwiftCaptureError(
            "OpenCV is required to write MP4 files. Install ir-support-full "
            "or install opencv-python, then try again."
        ) from exc

    return cv2


def _debug_log(message: str) -> None:
    if os.environ.get("IR_SUPPORT_SWIFT_CAPTURE_DEBUG") != "1":
        return

    log_path = Path(os.environ.get("IR_SUPPORT_SWIFT_CAPTURE_LOG", "swift_capture_debug.log"))
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"{time.time():.3f} {message}\n")


def _find_chrome_path() -> str:
    chrome = shutil.which("chrome") or shutil.which("chrome.exe")
    if chrome:
        return chrome

    candidates = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    raise SwiftCaptureError("Could not find Google Chrome for Swift canvas capture.")


def _free_local_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class _CaptureChrome:
    def __init__(
        self,
        debug_port: int,
        profile_dir: Path,
        *,
        window_size: tuple[int, int],
        headless: bool,
    ) -> None:
        self.debug_port = debug_port
        self.profile_dir = profile_dir
        self.window_size = window_size
        self.headless = headless
        self.process: subprocess.Popen | None = None
        self.url: str | None = None

    def open_new_tab(self, url: str) -> bool:
        self.url = url
        width, height = self.window_size
        command = [
            _find_chrome_path(),
            f"--remote-debugging-port={self.debug_port}",
            f"--user-data-dir={self.profile_dir}",
            "--no-first-run",
            "--disable-default-apps",
            f"--window-size={width},{height}",
        ]

        if self.headless:
            command.extend(["--headless=new", "--use-gl=swiftshader", url])
        else:
            command.append(f"--app={url}")

        self.process = subprocess.Popen(command)
        return True

    open = open_new_tab
    open_new = open_new_tab

    def close(self) -> None:
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=4)
            except subprocess.TimeoutExpired:
                self.process.kill()


def _get_debug_ws_url(
    requests_module,
    debug_port: int,
    *,
    target_url: str | None,
    timeout: float = 20.0,
) -> str:
    deadline = time.time() + timeout
    last_error: Exception | None = None
    target_created = False

    while time.time() < deadline:
        try:
            tabs = requests_module.get(f"http://127.0.0.1:{debug_port}/json", timeout=1).json()
            for tab in tabs:
                if "localhost" in tab.get("url", "") and tab.get("webSocketDebuggerUrl"):
                    return str(tab["webSocketDebuggerUrl"])

            if target_url and not target_created:
                created = requests_module.put(
                    f"http://127.0.0.1:{debug_port}/json/new?{quote(target_url, safe='')}",
                    timeout=2,
                ).json()
                target_created = True
                if created.get("webSocketDebuggerUrl"):
                    return str(created["webSocketDebuggerUrl"])
        except Exception as exc:  # pragma: no cover - diagnostic path.
            last_error = exc
            _debug_log(f"DevTools poll error: {type(exc).__name__}: {exc}")

        time.sleep(0.2)

    raise SwiftCaptureError(f"Could not find the Swift tab in Chrome DevTools: {last_error}")


class _CdpSession:
    def __init__(self, websocket) -> None:
        self.websocket = websocket
        self._next_id = 0

    async def call(self, method: str, params: dict | None = None) -> dict:
        self._next_id += 1
        message_id = self._next_id
        await self.websocket.send(
            json.dumps({"id": message_id, "method": method, "params": params or {}})
        )

        while True:
            message = json.loads(await self.websocket.recv())
            if message.get("id") == message_id:
                if "error" in message:
                    raise SwiftCaptureError(str(message["error"]))
                return message.get("result", {})


def _decode_canvas_data_url(image_module, data_url: str) -> np.ndarray:
    if not isinstance(data_url, str) or "," not in data_url:
        raise SwiftCaptureError("Chrome DevTools did not return a canvas data URL.")

    encoded = data_url.split(",", 1)[1]
    image = image_module.open(BytesIO(base64.b64decode(encoded))).convert("RGB")
    return np.asarray(image)


async def _capture_canvas_sequence(
    websockets_module,
    image_module,
    ws_url: str,
    env,
    scene_state: dict,
    frame_steps: list[FrameStep],
    *,
    dt: float,
    wait_after_step: float,
    viewport_size: tuple[int, int],
) -> list[np.ndarray]:
    width, height = viewport_size
    frames: list[np.ndarray] = []
    expression = (
        "(() => { const c = document.querySelector('canvas'); "
        "return c ? c.toDataURL('image/png') : null; })()"
    )

    async with websockets_module.connect(ws_url, max_size=50_000_000) as websocket:
        cdp = _CdpSession(websocket)
        await cdp.call("Page.enable")
        await cdp.call("Runtime.enable")
        await cdp.call(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": width,
                "height": height,
                "deviceScaleFactor": 1,
                "mobile": False,
            },
        )
        await asyncio.sleep(0.25)

        for index, step_fn in enumerate(frame_steps):
            step_fn(env, scene_state, index)
            env.step(dt, render=True)
            if wait_after_step:
                await asyncio.sleep(wait_after_step)

            result = await cdp.call(
                "Runtime.evaluate",
                {
                    "expression": expression,
                    "returnByValue": True,
                    "awaitPromise": True,
                },
            )
            frames.append(_decode_canvas_data_url(image_module, result["result"]["value"]))

    return frames


def capture_swift_scene_frames(
    setup_scene: Callable[[object], dict],
    frame_steps: Iterable[FrameStep],
    *,
    dt: float = 1 / 12,
    wait_after_step: float = 0.03,
    warmup_steps: int = 20,
    window_size: tuple[int, int] = (1280, 720),
    headless: bool = True,
    realtime: bool = False,
    comms: str = "websocket",
    profile_root: str | Path | None = None,
    cleanup_profile: bool = True,
) -> list[np.ndarray]:
    """Launch Swift and capture real browser-canvas frames.

    `setup_scene(env)` should add robots, objects, and camera settings, then
    return any scene state required by frame callbacks. Each callback receives
    `(env, scene_state, index)`, updates the scene, and then this helper steps
    Swift and captures the visible browser canvas.
    """

    image_module, requests_module, swift_module, websockets_module = _capture_imports()

    if profile_root is None:
        profile_root = Path.cwd() / ".ir_support_swift_capture_profiles"
    profile_root = Path(profile_root)
    profile_root.mkdir(parents=True, exist_ok=True)

    profile_dir = profile_root / f"swift_capture_{uuid.uuid4().hex}"
    profile_dir.mkdir(parents=True, exist_ok=True)

    debug_port = _free_local_port()
    browser_name = f"ir_support_swift_capture_{uuid.uuid4().hex}"
    browser = _CaptureChrome(
        debug_port,
        profile_dir,
        window_size=window_size,
        headless=headless,
    )
    webbrowser.register(browser_name, None, browser)

    env = swift_module.Swift()
    try:
        _debug_log("before env.launch")
        env.launch(realtime=realtime, comms=comms, browser=browser_name)
        _debug_log(f"after env.launch browser.url={browser.url}")
        ws_url = _get_debug_ws_url(requests_module, debug_port, target_url=browser.url)
        time.sleep(float(os.environ.get("IR_SUPPORT_SWIFT_CAPTURE_PAGE_READY_WAIT", "2.0")))

        scene_state = setup_scene(env)
        for _ in range(warmup_steps):
            env.step(dt, render=True)
            time.sleep(min(wait_after_step, 0.03))

        return asyncio.run(
            _capture_canvas_sequence(
                websockets_module,
                image_module,
                ws_url,
                env,
                scene_state,
                list(frame_steps),
                dt=dt,
                wait_after_step=wait_after_step,
                viewport_size=window_size,
            )
        )
    except Exception as exc:
        if isinstance(exc, SwiftCaptureError):
            raise
        raise SwiftCaptureError(
            "Swift capture failed. Make sure Chrome is installed and run "
            "`python -m ir_support.doctor --patch-advanced-swift-capture` "
            "in this environment before trying again."
        ) from exc
    finally:
        try:
            env.close()
        except Exception:
            pass
        browser.close()
        if cleanup_profile:
            shutil.rmtree(profile_dir, ignore_errors=True)


def write_frames_to_mp4(frames: Iterable[np.ndarray], output_path: str | Path, fps: int = 12) -> Path:
    """Write RGB frames to an MP4 file using OpenCV."""

    cv2 = _opencv_import()
    frame_list = list(frames)
    if not frame_list:
        raise ValueError("No frames were provided.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    height, width = frame_list[0].shape[:2]
    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        float(fps),
        (width, height),
    )
    if not writer.isOpened():
        raise SwiftCaptureError(f"Could not open MP4 writer for {output_path}.")

    try:
        for frame in frame_list:
            if frame.shape[:2] != (height, width):
                raise ValueError("All frames must have the same dimensions.")
            writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    finally:
        writer.release()

    return output_path


def make_ur3e_moving_block_frames(
    *,
    frame_count: int = 72,
    window_size: tuple[int, int] = (960, 540),
    headless: bool = True,
) -> list[np.ndarray]:
    """Capture frames for the built-in UR3e plus moving block example."""

    from ir_support.robots import UR3e
    from spatialgeometry import Cuboid
    from spatialmath import SE3

    frame_count = max(2, int(frame_count))
    q_start = np.array([0.0, -math.pi / 2, math.pi / 3, -math.pi / 2, -math.pi / 4, 0.0])
    q_goal = np.array([0.45, -1.15, 0.55, -1.25, 0.45, 0.35])

    def setup_scene(env) -> dict:
        robot = UR3e()
        robot.q = q_start.copy()
        add_to_env = getattr(robot, "add_to_env", None)
        if callable(add_to_env):
            add_to_env(env)
        else:
            env.add(robot)

        block = Cuboid(
            scale=[0.08, 0.08, 0.08],
            color=[1.0, 0.55, 0.05, 1.0],
            pose=SE3(0.25, -0.25, 0.08),
        )
        env.add(block)
        env.set_camera_pose([1.25, -1.3, 0.85], [0.15, 0.0, 0.25])
        return {"robot": robot, "block": block}

    def step_scene(_env, scene_state: dict, index: int) -> None:
        progress = index / max(1, frame_count - 1)
        eased = 0.5 - 0.5 * math.cos(2 * math.pi * progress)
        scene_state["robot"].q = (1 - eased) * q_start + eased * q_goal
        scene_state["block"].T = SE3(
            0.25,
            -0.25 + 0.5 * progress,
            0.08 + 0.12 * math.sin(math.pi * progress),
        )

    return capture_swift_scene_frames(
        setup_scene,
        [step_scene for _ in range(frame_count)],
        dt=1 / 12,
        wait_after_step=0.02,
        warmup_steps=12,
        window_size=window_size,
        headless=headless,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture a short Swift MP4 showing a core UR3e and moving block."
    )
    parser.add_argument(
        "--output",
        default="swift_ur3e_capture_example.mp4",
        help="Output MP4 path. Default: swift_ur3e_capture_example.mp4",
    )
    parser.add_argument("--frames", type=int, default=72, help="Number of frames to capture.")
    parser.add_argument("--fps", type=int, default=12, help="Output video frames per second.")
    parser.add_argument("--width", type=int, default=960, help="Captured canvas width.")
    parser.add_argument("--height", type=int, default=540, help="Captured canvas height.")
    parser.add_argument(
        "--visible",
        action="store_true",
        help="Show the Chrome app window instead of running headless.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> Path:
    args = parse_args(argv)
    print("Capturing Swift scene frames...")
    frames = make_ur3e_moving_block_frames(
        frame_count=args.frames,
        window_size=(args.width, args.height),
        headless=not args.visible,
    )
    output_path = write_frames_to_mp4(frames, args.output, fps=args.fps)
    print(f"Wrote {len(frames)} frames to {output_path}")
    return output_path


if __name__ == "__main__":
    main()
