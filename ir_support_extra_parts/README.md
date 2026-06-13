# IR Support Extra Parts

Optional parts and scene-object model pack for `ir-support`.

This package contains DAE assets and helper functions for loading UTS parts
into Swift or other `spatialgeometry` scenes. These are nice-to-have visual
models, not required core lab dependencies.

## Why The Parts Are Categorised

The extra parts package is intended to support industrial robotics assignment
scenes rather than act as a general 3D asset library. The most useful objects
are things that students can place in a workcell, manipulate with a robot, use
as safety context, or use as simple controls and sensors.

The package is therefore organised into a small number of practical categories.
This keeps the list browsable as the package grows and helps avoid turning the
library into a long unsorted list of meshes.

Current category counts, 99 parts total:

| Category | Count | Use this for |
| --- | ---: | --- |
| Manipulable Objects | 20 | Small objects, tools, trays, fixtures, and props that a robot may pick, place, or interact with. |
| Food And Packaging Props | 23 | Bottles, cartons, cans, boxes, cups, and packaged products for sorting and packing demos. |
| Workcell Fixtures | 23 | Tables, benches, bins, crates, pallets, shelves, and larger layout objects. |
| Safety Objects | 19 | Barriers, signs, helmets, people, cones, extinguishers, and workcell safety props. |
| Controls And Sensors | 14 | Buttons, emergency stops, scanners, lights, light curtains, and display/control objects. |

The current collection is deliberately kept just under about 100 objects so it remains
browsable. It is strongest in food/packaging props and workcell fixtures, with
controls and sensors now represented by a smaller but useful set of cameras,
switches, indicators, panels, scanners, buttons, and light curtains.

## Parts By Category

### Manipulable Objects

`Apple`, `BananaPeel`, `brick`, `DishRack`, `DumplingTray`, `hand`, `LegoMan`, `MilkPitcher`, `PizzaPeel`, `Plate`, `PlateFixture`, `PlateRack`, `PlateStacker`, `pen0.9x0.8x7.7m`, `StencilPlate`, `SuctionCup`, `TestTubeHolder`, `Toolbox`, `Tray`, `WateringCan`.

### Food And Packaging Props

`BeerBottle`, `BeerGlass`, `BlueSyrupBottle`, `BottleSixPack`, `CandyJar`,
`CardboardBox`, `CerealBoxGreen`, `FoodCan`, `FoodTrayBlue`, `GlassBottle`,
`JuiceBoxOrange`, `Lunchbox`, `MilkCarton`, `MustardBottle`, `PintCup`,
`SauceBottle`, `ShotGlass`, `SmallShippingBox`, `SpiritBottle`, `TakeawayCup`,
`TomatoSauceBottle`, `WineBottle`, `WineCup`.

### Workcell Fixtures

`BarTable`, `BlueBin`, `bookcaseTwoShelves0.5x0.2x0.5m`, `BottleCrate`,
`BoxBin`, `BuildPlateWorkbench`, `chair`, `drum`, `GreenBin`, `MilkCrate`,
`OfficeDesk`, `Pallet`, `PrintBin`, `printer`, `RedBin`, `RobotTable`,
`SimpleTable`, `StandingBarTable`, `tableBlue1x1x0.5m`,
`tableBrown2.1x1.4x0.5m`, `tableRound0.3x0.3x0.3m`, `WallShelf`,
`Workbench`.

### Safety Objects

`baby`, `barrier1.5x0.2x1m`, `CautionSign`, `fenceAssemblyGreenRectangle4x8x2.5m`, `fenceFinal`, `FireBlanket`, `FireExtinguisher`, `fireExtinguisherElevated`, `personFemaleBusiness`, `personMaleCasual`, `personMaleConstruction`, `personMaleOld`, `SafetyGate`, `SafetyHelmet`, `SafetyPerson`, `SafetyRailing`, `TrafficCone`, `WarningSign`, `WetFloorSign`.

### Controls And Sensors

`BarcodeScanner`, `Camera`, `ControlPanel`, `emergencyStopButton`, `emergencyStopWallMounted`, `FireAlarm`, `LightTower`, `MagneticSwitch`, `Monitor`, `ProximitySensor`, `PushButton`, `SafetyLightCurtain`, `SafetyLight`, `TrafficLight`.

## Loading Parts

```python
import swift
from ir_support_extra_parts.parts import part_mesh, part_names

env = swift.Swift()
env.launch(realtime=True)

print(part_names())
box = part_mesh("CardboardBox")
env.add(box)
env.step()
```

## Browsing By Category

The repository includes a Swift inspection script that loads one category at a
time, arranges the objects in a grid, and animates them slowly so they can be
checked visually:

```bash
python tests/view_extra_parts_by_category_swift.py --category "Safety Objects"
```

When running directly from an IDE, edit `CATEGORY_NAME` near the top of
`tests/view_extra_parts_by_category_swift.py`.





