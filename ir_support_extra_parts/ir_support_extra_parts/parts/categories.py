"""Category groupings for the optional IR Support extra parts.

These groupings are intentionally practical rather than taxonomic. They are
aimed at helping students find useful scene props for industrial robotics
assignments without having to scan one long list of mesh filenames.
"""


PART_CATEGORIES = {
    "Manipulable Objects": (
        "Apple",
        "BananaPeel",
        "brick",
        "DishRack",
        "DumplingTray",
        "hand",
        "LegoMan",
        "MilkPitcher",
        "PizzaPeel",
        "Plate",
        "PlateFixture",
        "PlateRack",
        "PlateStacker",
        "pen0.9x0.8x7.7m",
        "StencilPlate",
        "SuctionCup",
        "TestTubeHolder",
        "Toolbox",
        "Tray",
        "WateringCan",
    ),
    "Food And Packaging Props": (
        "BeerBottle",
        "BeerGlass",
        "BlueSyrupBottle",
        "BottleSixPack",
        "CandyJar",
        "CardboardBox",
        "CerealBoxGreen",
        "FoodCan",
        "FoodTrayBlue",
        "GlassBottle",
        "JuiceBoxOrange",
        "Lunchbox",
        "MilkCarton",
        "MustardBottle",
        "PintCup",
        "SauceBottle",
        "ShotGlass",
        "SmallShippingBox",
        "SpiritBottle",
        "TakeawayCup",
        "TomatoSauceBottle",
        "WineBottle",
        "WineCup",
    ),
    "Workcell Fixtures": (
        "BarTable",
        "BlueBin",
        "bookcaseTwoShelves0.5x0.2x0.5m",
        "BottleCrate",
        "BoxBin",
        "BuildPlateWorkbench",
        "chair",
        "drum",
        "GreenBin",
        "MilkCrate",
        "OfficeDesk",
        "Pallet",
        "PrintBin",
        "printer",
        "RedBin",
        "RobotTable",
        "SimpleTable",
        "StandingBarTable",
        "tableBlue1x1x0.5m",
        "tableBrown2.1x1.4x0.5m",
        "tableRound0.3x0.3x0.3m",
        "WallShelf",
        "Workbench",
    ),
    "Safety Objects": (
        "baby",
        "barrier1.5x0.2x1m",
        "fenceAssemblyGreenRectangle4x8x2.5m",
        "fenceFinal",
        "FireBlanket",
        "FireExtinguisher",
        "fireExtinguisherElevated",
        "personFemaleBusiness",
        "personMaleCasual",
        "personMaleConstruction",
        "personMaleOld",
        "SafetyGate",
        "SafetyHelmet",
        "SafetyPerson",
        "SafetyRailing",
        "TrafficCone",
        "WarningSign",
        "WetFloorSign",
    ),
    "Controls And Sensors": (
        "BarcodeScanner",
        "emergencyStopButton",
        "emergencyStopWallMounted",
        "FireAlarm",
        "Monitor",
        "PushButton",
        "SafetyLightCurtain",
        "SafetyLight",
    ),
}


def category_names():
    """Return the available category names in display order."""

    return tuple(PART_CATEGORIES.keys())


def parts_by_category(category):
    """Return the part names in a category."""

    if category not in PART_CATEGORIES:
        available = ", ".join(category_names())
        raise ValueError(f"Unknown part category '{category}'. Available: {available}")
    return PART_CATEGORIES[category]


def category_summary():
    """Return ``(category, count)`` pairs in display order."""

    return tuple((category, len(parts)) for category, parts in PART_CATEGORIES.items())


__all__ = [
    "PART_CATEGORIES",
    "category_names",
    "parts_by_category",
    "category_summary",
]
