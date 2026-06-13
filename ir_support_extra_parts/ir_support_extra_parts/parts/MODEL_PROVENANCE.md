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

## Student Object Batch 3

Attempted move into ir_support_extra_parts on 2026-06-08. Robot link meshes, full environments, duplicated existing parts, and oversized scene models were excluded from this batch. A malformed source `table1.dae` and several PLY files that Blender could not import cleanly were skipped in favour of cleaner DAE candidates.

- `BarTable` from `Khoa_A2_10`, 2024S; original stem `bartable`; retained as a DAE prop and normalised for Swift.
- `RobotTable` from `A2_Khoa_52_BenH_JaydnT_NguyenH`, 2025S; original stem `Robottable`; scaled from millimetres and normalised as a DAE prop.
- `OfficeDesk` from `Group_42`, 2023S; original stem `desk`; corrected after Swift inspection because it had been scaled too small, then normalised as a DAE prop.
- `SimpleTable` from `A2_Khoa_52_BenH_JaydnT_NguyenH`, 2025S; original stem `GenericDeskFinal`; scaled from millimetres, normalised as a DAE prop, and renamed from `GenericDesk` after Swift inspection.
- `DishRack` from `A2_AnhMinh_46_PhuTrungN_NhatThienM_MohammadFaiyadH`, 2025S; original stem `Dish_Holder`; scaled from millimetres and normalised as a DAE prop.
- `BoxBin` from `A2_AnhMinh_44_LachlanC_ZacharyO_NathanielG`, 2025S; original stem `Box_Bin`; retained as a DAE prop, scaled down to a reusable bin-sized object, and normalised for Swift.
- `SuctionCup` from `A2_Richardo_35_LewisW_EdenL`, 2025S; original stem `suction_cup`; corrected after Swift inspection because it had been scaled too small, then normalised as a DAE prop.
- `PrintBin` from `A2_Louis_26_AdamS_JacobB_JordanR`, 2025S; original stem `print_bin`; corrected after Swift inspection because the imported DAE mesh was extremely small, then normalised as a DAE prop.
- `BuildPlateWorkbench` from `A2_Louis_26_AdamS_JacobB_JordanR`, 2025S; original stem `build_plate_table`; corrected after Swift inspection because the imported DAE mesh was extremely small, then normalised as a DAE prop and renamed from `BuildPlateTable` without clashing with the existing `Workbench` asset.
- `CerealBoxGreen` from `Karlos_A2_4`, 2024S; original stem `CerealBox_Green`; converted from PLY to DAE and given front/back CEREAL labels with corrected text orientation.
- `FireAlarm` from `Group_40`, 2023S; original stem `FireAlarm`; converted from PLY to DAE.
- `TakeawayCup` from `A2_Tony_21_JackH_SaiS_LiamD`, 2025S; original stem `Mcdonalds Cup`; retained as a DAE prop and normalised for Swift.
- `PlateFixture` from `A2_AnhMinh_46_PhuTrungN_NhatThienM_MohammadFaiyadH`, 2025S; original stem `Plate_Fix`; scaled from millimetres, decimated, and normalised as a DAE prop.
- `StandingBarTable` from `A2_Khoa_57_HongLinhN_NhatMinhV`, 2025S; original stem `tableunderbox`; scaled from millimetres, normalised as a DAE prop, and renamed from `UnderBoxTable` after Swift inspection.
- `PushButton` from `A2_Louis_26_AdamS_JacobB_JordanR`, 2025S; original stem `Button`; corrected after Swift inspection because it had been scaled too small, then decimated, normalised, and recoloured with a red push dome and dark grey base.

Rejected after Swift inspection:

- `BlackjackTable` from `A2_Tony_18_JoshuaI_MunirA_IsabelleW`, 2025S; original stem `blackjack_table`; remained invisible/unusable in Swift and was removed from batch 3.
- `ComputerTable` from `Karlos_A2_4`, 2024S; original stem `ComputerTable`; not a useful general computer table prop and removed from batch 3.
- `FridgeCabinetTop` from `A2_AnhMinh_46_PhuTrungN_NhatThienM_MohammadFaiyadH`, 2025S; original stem `Fridge_Cabinet_Top`; too specific for the reusable object pack.
- `PrintBed` from `Group_79`, 2023S; original stem `moddedprintbed`; too specific for the reusable object pack.
- `TopCabinet` from `A2_AnhMinh_46_PhuTrungN_NhatThienM_MohammadFaiyadH`, 2025S; original stem `Top_Cabinet_W_Beefs`; 

## Student Object Batch 4

Attempted move into ir_support_extra_parts on 2026-06-09. Robot link meshes, full environments, duplicated existing parts, oversized scene models, malformed candidate meshes, and objects that were too specific for general teaching use were excluded. Several accepted assets were recoloured, labelled, reoriented, or renamed after Swift inspection.

- `FoodCan` from `Katia_A2_2`, 2024S; original stem `Can_Of_Food_Spam`; converted from PLY to DAE and given a simple food label.
- `Pallet` from `Katia_A2_7`, 2024S; original stem `pallet`; scaled from millimetres, reoriented flat on the floor, given a timber-like material, and converted from PLY to DAE.
- `SmallShippingBox` from `Katia_A2_9`, 2024S; original stem `IndividualBox`; scaled from millimetres, reoriented, converted from PLY to DAE, and renamed for clearer general use.
- `BlueSyrupBottle` from `Khoa_A2_5`, 2024S; original stem `BlueSyrupBottle`; converted from PLY to DAE and given a simple syrup label.
- `TestTubeHolder` from `Khoa_A2_5`, 2024S; original stem `SpatulaHolder`; converted from PLY to DAE and renamed after Swift inspection because the object is more useful as a test tube holder.
- `BottleCrate` from `Mahdi_A2_6`, 2024S; original stem `Bottle Crate`; scaled from millimetres, simplified, recoloured grey, and converted from PLY to DAE.
- `PlateRack` from `Quang_A2_1`, 2024S; original stem `plateRack`; converted from PLY to DAE.
- `SafetyGate` from `Sheila_A2_1`, 2024S; original stem `Safety Gate`; scaled from millimetres, simplified, reoriented upright, material-flattened, and converted from PLY to DAE.
- `DumplingTray` from `Sheila_A2_2`, 2024S; original stem `dumpling_tray`; converted from PLY to DAE.
- `BottleSixPack` from `Mahdi_A2_6`, 2024S; original stem `Bottle 6 Pack Fixed`; scaled from millimetres, simplified, reoriented upright, recoloured, and converted from PLY to DAE.
- `CandyJar` from `Sheila_A2_3`, 2024S; original stem `greenappleJar`; simplified, material-flattened, labelled, and converted from PLY to DAE.
- `MustardBottle` from `Tony_A2_2`, 2024S; original stem `MustardBottle`; converted from PLY to DAE and given a simple mustard label.
- `TomatoSauceBottle` from `Tony_A2_2`, 2024S; original stem `TomatoSauceBottle`; converted from PLY to DAE and given a simple tomato sauce label.
- `MilkCrate` from `Group_54`, 2023S; original stem `MilkCrate`; converted from PLY to DAE and recoloured for Swift inspection.
- `SafetyLightCurtain` from `Group_51`, 2023S; original stem `Safety Light Curtain`; converted from PLY to DAE and recoloured for Swift inspection.
- `PlateStacker` from `Group_65`, 2023S; original stem `plateStacker`; converted from PLY to DAE.
- `FireExtinguisher` from `Quang_A2_7`, 2024S; original stem `Fire`; retained as a fire-extinguisher-style prop, scaled from millimetres, simplified, reoriented, labelled, and converted from PLY to DAE. Renamed from `Flame` after Swift inspection because the mesh is a fire extinguisher, not a flame.
- `BeerGlass` from `Group_45`, 2023S; original stem `BeerGlasses`; scaled from millimetres, simplified, reoriented upright, converted from PLY to DAE, and renamed to singular after Swift inspection.
- `PizzaPeel` from `Group_60`, 2023S; original stem `PizzaPeel`; converted from PLY to DAE and recoloured.

Rejected after Swift inspection:

- `DiscHolder` from `Sheila_A2_5`, 2024S; original stem `DiscHolderv3`; removed because it was too specific and unlikely to be useful as a general teaching prop.

Rejected before Swift inspection:

- `CandyBox` from `Sheila_A2_3`, 2024S; original stem `candyBox`; source PLY had malformed face records and could not be imported cleanly.
- `Shoebox` from `A2_Louis_30_LukeK_LukeH_VyasaKarthikP`, 2025S; original stem `shoebox`; source PLY had malformed face records and could not be imported cleanly.

## Student Object Batch 5

Attempted move into ir_support_extra_parts on 2026-06-11, with final Swift review cleanup on 2026-06-12. This small batch deliberately targeted the thinner controls/sensors category while keeping the total extra-parts catalogue near 100 objects. Robot link meshes, full environments, duplicated existing parts, and oversized scene models were excluded. Accepted objects were normalised to metre-scale DAE assets, placed on the ground plane, made double-sided, and recoloured or labelled where the source material was too plain.

- `LightTower` from `Group_39`, 2023S; original stem `LightTower`; converted from PLY to DAE and recoloured as a red/amber/green indicator tower.
- `ControlPanel` from `Group_41`, 2023S; original stem `control panel C`; scaled from centimetre-like source units, converted from PLY to DAE, and given a dark panel, screen, buttons, and simple text.
- `MagneticSwitch` from `Group_76`, 2023S; original stem `magnetic_switch_w_leads`; converted from PLY to DAE and recoloured as a dark switch body with cable and blue sensor tip.
- `ProximitySensor` from `Mahdi_A2_6`, 2024S; original stem `Proximity Sensor`; scaled from centimetre-like source units, decimated below the target DAE size, converted from PLY to DAE, and recoloured as a metallic sensor.
- `Camera` from `Group_10`, 2023S; original stem `camera`; scaled to a plausible workcell-camera size, converted from PLY to DAE, recoloured with a dark body, and cleaned after Swift inspection to remove generated floating lens-detail geometry.
- `TrafficLight` from `A2_Richardo_32_DiL_KhiladA_RobeerO`, 2025S; original stem `Traffic_Light`; scaled from source units and converted from STL to a dark DAE prop. Generated red/amber/green panels were removed after Swift inspection because they did not align with the source mesh.
- `CautionSign` from `Group_39`, 2023S; original stem `CautionSign`; converted from PLY to DAE, recoloured yellow, and given face-aligned CAUTION text on both sides after Swift inspection.

Rejected after Swift inspection:

- `CutterHolder` from `Group_18`, 2023S; original stem `cutter holder`; removed because the object purpose was unclear and it was not useful enough as a reusable teaching prop.

Future additions:

When parts or scene objects are moved in from 2023 and later Assignment 2 submissions, add a reference entry here for each asset or related group of assets. Include the part name, student group or submission identifier, teaching session, original file stem if useful, and any notable cleanup or conversion work.














