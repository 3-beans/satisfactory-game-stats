# ruff: noqa: T201

from math import inf, sqrt

import satisfactory_save as s


def print_property(p: s.Property, indent=1):
    space = "  " * indent
    print(f"{space}{p.Name.toString()} ({p.Type.toString()})")
    if isinstance(p, s.FloatProperty):
        print(f"{space}  {p.Value}")
    elif isinstance(p, s.ObjectProperty):
        print(f"{space}  Lvl: {p.Value.LevelName}")
        print(f"{space}  Path: {p.Value.PathName}")
    elif isinstance(p, s.StructProperty):
        print(f"{space}  StructName: {p.StructName.toString()}")
        struct = p.Value
        if isinstance(struct, s.PropertyStruct):
            for struct_member in struct.Data:
                print_property(struct_member, indent + 2)
        else:
            print(f"{space}    -- todo --")
    else:
        print(f"{space}  -- todo --")


def print_object(obj: s.SaveObjectBase):
    print("TOC:")
    print(f"  isActor: {obj.isActor()}")
    print(f"  ClassName: {obj.ClassName}")
    print(f"  Reference.LevelName: {obj.Reference.LevelName}")
    print(f"  Reference.PathName: {obj.Reference.PathName}")
    if obj.isActor():
        print(f"  NeedTransform: {obj.NeedTransform}")
        rot = obj.Transform.Rotation
        trans = obj.Transform.Translation
        scale = obj.Transform.Scale3D
        print(f"  Transform.Rotation: [X:{rot.X} Y:{rot.Y} Z:{rot.Z} W:{rot.W}]")
        print(f"  Transform.Translation: [X:{trans.X} Y:{trans.Y} Z:{trans.Z}]")
        print(f"  Transform.Scale3D: [X:{scale.X} Y:{scale.Y} Z:{scale.Z}]")
        print(f"  WasPlacedInLevel: {obj.WasPlacedInLevel}")
    else:
        print(f"  OuterPathName: {obj.OuterPathName}")
    print("Data:")
    print(f"  SaveVersion: {obj.SaveVersion}")
    print(f"  ShouldMigrateObjectRefsToPersistent: {obj.ShouldMigrateObjectRefsToPersistent}")
    if obj.isActor():
        print(f"  parent_reference.LevelName: {obj.parent_reference.LevelName}")
        print(f"  parent_reference.PathName: {obj.parent_reference.PathName}")
        print(f"  child_references: {list(obj.child_references)}")
    print("  Properties:")
    for p in obj.Properties:
        print_property(p, 2)
    print(f"  Guid: {obj.Guid}")
    print(f"  ExtraProperties: {obj.ExtraProperties}")


def calculate_belt_distance(obj: s.SaveObjectBase):
    """
    Calculates a basic distance (in 3d space) for a belt.

    Does NOT take into account spline pathing yet, so the calculation is not very accurate.

    Returns -inf if the passed object is not a conveyor belt, or the spline data property
    can't be found.
    """
    class_name = "".join(obj.ClassName.split("/")[5])
    if not class_name.startswith("ConveyorBeltMk"):
        return -inf

    for p in obj.Properties:
        if p.Name.Name == "mSplineData":
            # all "location" points
            locations = [v.Data[0].Value.Data for v in p.Value.Values]

            distances = []
            for j in range(0, len(locations) - 1):
                distances.append(
                    sqrt(
                        (locations[j + 1].X - locations[j].X) ** 2
                        + (locations[j + 1].Y - locations[j].Y) ** 2
                        + (locations[j + 1].Z - locations[j].Z) ** 2
                    )
                )

            return sum(distances)

    return -inf
