from ir_support.functions import swift_video_capture_example as capture_example


def test_swift_video_capture_example_cli_defaults():
    args = capture_example.parse_args([])

    assert args.output == "swift_ur3e_capture_example.mp4"
    assert args.frames == 72
    assert args.fps == 12
    assert args.width == 960
    assert args.height == 540
    assert not args.visible


def test_swift_video_capture_example_cli_overrides():
    args = capture_example.parse_args(
        [
            "--output",
            "demo.mp4",
            "--frames",
            "5",
            "--fps",
            "24",
            "--width",
            "640",
            "--height",
            "360",
            "--visible",
        ]
    )

    assert args.output == "demo.mp4"
    assert args.frames == 5
    assert args.fps == 24
    assert args.width == 640
    assert args.height == 360
    assert args.visible
