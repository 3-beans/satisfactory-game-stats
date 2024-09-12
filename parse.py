from collections import defaultdict
import json
from pathlib import Path

import satisfactory_save as s

# Load a save game
gamefile = Path("games/Crush Life_autosave_0.sav")
save = s.SaveGame(gamefile)

stats = {}
found = defaultdict(int)
# counts = defaultdict(set)

objs = save.persistentAndRuntimeData().save_objects

stats["total_objects"] = len(objs)

for obj in objs:
    if not obj.ClassName.startswith("/Game/FactoryGame/Buildable/Factory/"):
        continue

    class_name = "".join(obj.ClassName.split("/")[5])
    found[class_name] += 1

    # if not class_name.startswith("ConveyorBeltMk"):
    #     continue

    # if not hasattr(obj, "child_references"):
    #     continue

    # for x in obj.child_references:
    #     counts[class_name].add(x.PathName)

# counts = { k: len(v) for k, v in counts.items() }

stats_file = "output/stats.json"
stats_output = Path(stats_file)
stats_output.parent.mkdir(parents=True, exist_ok=True)
with stats_output.open("wt") as f:
    json.dump(stats, f, indent=4, sort_keys=True)

found_file = "output/found.json"
found_output = Path(found_file)
found_output.parent.mkdir(parents=True, exist_ok=True)
with found_output.open("wt") as f:
    json.dump(found, f, indent=4, sort_keys=True)
