#!/usr/bin/env python3
"""Download the Perseus TEI XML of the Iliad and Odyssey, pinned to a commit.

The files go to corpus/raw/perseus/ (gitignored, never committed).  The commit
hash, file SHA-256 and fetch date are written to homer/source.json, which IS
committed, so that every later step can be traced to an exact upstream state.

Usage:
    python homer/fetch_text.py                 # use the pinned commit below
    python homer/fetch_text.py --commit master # re-resolve (updates source.json)
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "corpus" / "raw" / "perseus"
SOURCE_JSON = ROOT / "homer" / "source.json"
REPO = "PerseusDL/canonical-greekLit"
# master of PerseusDL/canonical-greekLit on 2026-10-07 (git ls-remote)
PINNED_COMMIT = "01b725d835e6e733062ffd79e0efdbae1ba06e5c"
FILES = {
    "Il": "data/tlg0012/tlg001/tlg0012.tlg001.perseus-grc2.xml",
    "Od": "data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml",
}
# Last upstream commit that touched each file at PINNED_COMMIT, and the git blob
# id of the file, determined with a blobless clone:
#   git clone --filter=blob:none --no-checkout https://github.com/PerseusDL/canonical-greekLit
#   git log -1 --format=%H -- <path>;  git rev-parse HEAD:<path>
LAST_COMMIT = {
    "Il": ("ceeb60d9e9e0ebefd0f22b536e03a67084d2452a", "2026-09-18",
           "bd2fdecd37f336c0f7a55650e35ad20f43165ef9"),
    "Od": ("b864b282e1689a2c2a1ebb59ff8aa2b773cb50c1", "2026-09-15",
           "e799b82a372f2612ab1b05c67a015fbef04fe261"),
}


def git_blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def resolve(ref: str) -> str:
    if len(ref) == 40 and all(c in "0123456789abcdef" for c in ref):
        return ref
    out = subprocess.run(
        ["git", "ls-remote", f"https://github.com/{REPO}.git", f"refs/heads/{ref}"],
        capture_output=True, text=True, check=True).stdout.split()
    if not out:
        sys.exit(f"cannot resolve {ref}")
    return out[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", default=PINNED_COMMIT)
    args = ap.parse_args()
    commit = resolve(args.commit)
    RAW.mkdir(parents=True, exist_ok=True)
    record = {"repository": f"https://github.com/{REPO}", "commit": commit,
              "fetched": datetime.date.today().isoformat(), "files": {}}
    for work, path in FILES.items():
        url = f"https://raw.githubusercontent.com/{REPO}/{commit}/{path}"
        dest = RAW / pathlib.Path(path).name
        r = requests.get(url, timeout=120)
        r.raise_for_status()
        dest.write_bytes(r.content)
        sha = hashlib.sha256(r.content).hexdigest()
        blob = git_blob_id(r.content)
        record["files"][work] = {"path": path, "url": url, "local": str(dest.relative_to(ROOT)),
                                 "sha256": sha, "git_blob": blob, "bytes": len(r.content)}
        if commit == PINNED_COMMIT:
            lc, date, expected_blob = LAST_COMMIT[work]
            record["files"][work]["last_commit_touching_file"] = lc
            record["files"][work]["last_commit_date"] = date
            if blob != expected_blob:
                sys.exit(f"{work}: git blob {blob} != expected {expected_blob}")
        print(f"{work}: {url} -> {dest} ({len(r.content)} bytes, sha256 {sha[:12]}...)")
    if SOURCE_JSON.exists():
        old = json.loads(SOURCE_JSON.read_text())
        for work, info in record["files"].items():
            prev = old.get("files", {}).get(work, {})
            if prev.get("sha256") and prev["sha256"] != info["sha256"]:
                print(f"WARNING: {work} sha256 differs from recorded {prev['sha256']}")
    SOURCE_JSON.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
