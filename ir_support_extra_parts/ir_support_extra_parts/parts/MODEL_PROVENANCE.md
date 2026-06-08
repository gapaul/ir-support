# Model Provenance

This optional parts pack contains visually useful scene objects and teaching props that are not required by the core 41013 lab exercises, quizzes, or assignments.

Current source:

- Older UTS MATLAB Robotics Toolbox parts and object models, made by UTS staff and students between about 2016 and 2022, then ported from the local MATLAB toolbox archive into Python/Swift-ready DAE assets.
- Student Assignment 2 object models from 2023S, 2024S, and 2025S, converted or cleaned into Python/Swift-ready DAE assets. These are intended as optional teaching props rather than verified reference CAD.

These models are useful teaching assets, but they should not be treated as manufacturer-verified or dimensionally guaranteed reference models.

## Student Object Batch 1

Attempted move into `ir_support_extra_parts` on 2026-06-07. Robot link meshes, full environments, duplicated existing parts, and oversized scene models were excluded from this batch.

- `Workbench` from `A2_Khoa_57_HongLinhN_NhatMinhV`, 2025S; original stem `Workbench`; scaled from millimetres and converted to DAE.
- `GlassBottle` from `Khoa_A2_10`, 2024S; original stem `glass_bottle`; retained as a small DAE drinkware prop.
- `PintCup` from `Khoa_A2_10`, 2024S; original stem `pint_cup`; retained as a small DAE drinkware prop.
- `ShotGlass` from `Khoa_A2_10`, 2024S; original stem `shot_glass`; retained as a small DAE drinkware prop.
- `WineCup` from `Khoa_A2_10`, 2024S; original stem `wine_cup`; retained as a small DAE drinkware prop.
- `WineBottle` from `Khoa_A2_10`, 2024S; original stem `wine_bottle`; retained as a small DAE drinkware prop.
- `Plate` from `A2_Adam_60_BenjaminH_NathanaelJ_JarrelR`, 2025S; original stem `plate`; scaled from millimetres and converted to DAE.
- `SafetyHelmet` from `Group_114`, 2023S; original stem `safetyhat`; converted from PLY to DAE.
- `WarningSign` from `Group_114`, 2023S; original stem `warningsign`; converted from PLY to DAE.
- `WetFloorSign` from `Group_38`, 2023S; original stem `wetsign`; converted from PLY to DAE.
- `BlueBin` from `Group_16`, 2023S; original stem `BlueBin`; converted from PLY to DAE.
- `Apple` from `Group_74`, 2023S; original stem `apple`; converted from PLY to DAE.
- `MilkPitcher` from `Group_2`, 2023S; original stem `MilkPitcher`; converted from PLY to DAE.
- `CardboardBox` from `A2_Louis_30_LukeK_LukeH_VyasaKarthikP`, 2025S; original stem `cardboard_box_1`; converted from STL to DAE.
- `MilkCarton` from `A2_Louis_30_LukeK_LukeH_VyasaKarthikP`, 2025S; original stem `milk_carton_1`; converted from STL to DAE.
- `BananaPeel` from `A2_Louis_30_LukeK_LukeH_VyasaKarthikP`, 2025S; original stem `banana_peel_1`; converted from STL to DAE.
- `SauceBottle` from `A2_Richardo_34_EmilyW_ThomaisP_MarkL`, 2025S; original stem `Sauce_Bottle1`; converted from STL to DAE.

Rejected after Swift inspection:

- `CupHolder` from `A2_AnhMinh_42_DaniyaS_ZainK`, 2025S; original stem `cupholder1`; too specific and unlikely to be reusable.
- `BlueCan` from `Group_16`, 2023S; original stem `BlueCanV2`; visually low-value compared with other reusable objects.
- `BoxAssembly` from `Group_36`, 2023S; original stem `Box Assembly B`; unclear object purpose and not useful enough as a general teaching prop.

## Student Object Batch 2

Attempted move into ir_support_extra_parts on 2026-06-08. Robot link meshes, full environments, duplicated existing parts, and oversized scene models were excluded from this batch. All accepted objects were converted or normalised to DAE for Swift inspection.

- `TrafficCone` from `A2_AnhMinh_43_LouannM_StellaM_KatiaS`, 2025S; original stem `traffic_cone2`; scaled from millimetres and normalised as a DAE prop.
- `BeerBottle` from `Khoa_A2_10`, 2024S; original stem `beer_bottle`; retained as a DAE prop, normalised for Swift, and given a simple beer label.
- `SpiritBottle` from `Khoa_A2_10`, 2024S; original stem `spirit_bottle`; retained as a DAE prop, normalised for Swift, and given a simple spirits label.
- `SafetyRailing` from `Mahdi_A2_4`, 2024S; original stem `Safety Railing`; retained as a DAE prop and scaled to approximately 1.05 m high for Swift.
- `LegoMan` from `A2_AnhMinh_40_WilliamL_JohnM`, 2025S; original stem `LEGOMAN`; scaled from millimetres, made double-sided, and normalised as a DAE prop.
- `SafetyPerson` from `A2_AnhMinh_43_LouannM_StellaM_KatiaS`, 2025S; original stem `safetyman`; scaled from millimetres and normalised as a DAE prop.
- `StencilPlate` from `A2_Khoa_52_BenH_JaydnT_NguyenH`, 2025S; original stem `Stencil_Plate`; scaled from millimetres and normalised as a DAE prop.
- `Toolbox` from `Sheila_A2_3`, 2024S; original stem `toolbox`; converted from PLY to DAE.
- `GreenBin` from `Group_16`, 2023S; original stem `GreenBin`; converted from PLY to DAE.
- `RedBin` from `Group_16`, 2023S; original stem `RedBin`; converted from PLY to DAE.
- `Tray` from `Group_51`, 2023S; original stem `tray`; converted from PLY to DAE.
- `WateringCan` from `Group_75`, 2023S; original stem `Watering_can`; converted from PLY to DAE.
- `FireBlanket` from `Group_70`, 2023S; original stem `fireBlanket`; converted from PLY to DAE and given simple front-panel text.
- `BarcodeScanner` from `Group_39`, 2023S; original stem `barcodescanner5`; converted from PLY to DAE.
- `FoodTrayBlue` from `Group_4`, 2023S; original stem `Food_Tray_Blue2`; converted from PLY to DAE.
- `JuiceBoxOrange` from `Group_47`, 2023S; original stem `JuiceBoxOrange`; converted from PLY to DAE, made double-sided, and given simple juice labels.
- `Lunchbox` from `Group_47`, 2023S; original stem `MealBoxMeat`; converted from PLY to DAE, made double-sided, and renamed for clearer general use.
- `Monitor` from `Group_68`, 2023S; original stem `MonitorDesign`; converted from PLY to DAE.
- `SafetyLight` from `Group_68`, 2023S; original stem `SafetyLightDesign`; converted from PLY to DAE.
- `WallShelf` from `Group_68`, 2023S; original stem `WShelfDesign`; converted from PLY to DAE.

Future additions:

When parts or scene objects are moved in from 2023 and later Assignment 2 submissions, add a reference entry here for each asset or related group of assets. Include the part name, student group or submission identifier, teaching session, original file stem if useful, and any notable cleanup or conversion work.



