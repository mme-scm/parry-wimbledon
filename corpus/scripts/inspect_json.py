"""Print the structure of a JSON file: top-level type, length, keys of first records."""
import json, sys

def describe(obj, depth=0, maxdepth=4):
    pad = "  " * depth
    if isinstance(obj, dict):
        print(f"{pad}dict with {len(obj)} keys: {list(obj.keys())[:20]}")
        if depth < maxdepth:
            for k in list(obj.keys())[:8]:
                print(f"{pad} key {k!r}:")
                describe(obj[k], depth + 1, maxdepth)
    elif isinstance(obj, list):
        print(f"{pad}list len {len(obj)}")
        if obj and depth < maxdepth:
            describe(obj[0], depth + 1, maxdepth)
    else:
        s = repr(obj)
        print(f"{pad}{type(obj).__name__}: {s[:200]}")

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    data = json.load(f)
describe(data, maxdepth=int(sys.argv[2]) if len(sys.argv) > 2 else 4)
