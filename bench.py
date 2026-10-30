#!/usr/bin/env python3
"""Linux rerun of the Wasm paper campaign.

Method matches the Windows campaign in the paper: fresh process per run,
`rizin -qq -c "aaa; aflc" module.wasm`, wall clock timing.
Differences, all recorded in the output: Linux machine, 3 repetitions for
runs that finish, and a run that hits the timeout is not repeated (a second
600 s wait adds no information). Timeouts: 180 s default, 600 s for
dotnet.wasm and AngryBots13.wasm.
"""
import json, os, resource, subprocess, sys, time, pathlib

ROOT = pathlib.Path(__file__).parent
RESULTS = ROOT / "results-linux.jsonl"
import os
REPS = int(os.environ.get("BENCH_REPS", "3"))

MODULES = []
paper = (ROOT.parent / "paper.md").read_text()
import re
for name, size in re.findall(r"^\| ((?:c-cpp|rust|go|unknown)-[0-9]+-[0-9a-f]{8}) \| ([0-9]+) \|", paper, re.M):
    MODULES.append((name, ROOT / "corpus" / f"{name}.wasm"))
MODULES.append(("dotnet.wasm", ROOT / "testbins" / "wasm" / "dotnet.wasm"))
MODULES.append(("AngryBots13.wasm", ROOT / "testbins" / "wasm" / "AngryBots13.wasm"))

TIMEOUTS = {"dotnet.wasm": 600, "AngryBots13.wasm": 600}
BUILDS = {
    "before": ROOT / "rizin-base" / "build-base" / "binrz" / "rizin" / "rizin",
    "after": ROOT / "rizin-pr" / "build-pr" / "binrz" / "rizin" / "rizin",
}

def done_keys():
    keys = set()
    if RESULTS.exists():
        for line in RESULTS.read_text().splitlines():
            try:
                r = json.loads(line)
                keys.add((r["module"], r["build"], r["rep"]))
            except Exception:
                pass
    return keys

def timed_out(build, module):
    if not RESULTS.exists():
        return False
    for line in RESULTS.read_text().splitlines():
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r["module"] == module and r["build"] == build and r.get("timeout"):
            return True
    return False

def run_one(binary, path, timeout):
    start = time.perf_counter()
    try:
        p = subprocess.run([str(binary), "-qq", "-c", "aaa; aflc", str(path)],
                           capture_output=True, text=True, timeout=timeout)
        secs = time.perf_counter() - start
        out = p.stdout.strip().splitlines()
        aflc = None
        for line in reversed(out):
            if line.strip().isdigit():
                aflc = int(line.strip()); break
        return {"seconds": round(secs, 3), "timeout": False, "aflc": aflc,
                "rc": p.returncode}
    except subprocess.TimeoutExpired:
        return {"seconds": float(timeout), "timeout": True, "aflc": None, "rc": None}

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    keys = done_keys()
    with open(RESULTS, "a") as fh:
        for name, path in MODULES:
            if only and only not in name:
                continue
            for build, binary in BUILDS.items():
                if not binary.exists():
                    print(f"SKIP {build}: binary missing", flush=True); continue
                if timed_out(build, name):
                    continue
                for rep in range(1, REPS + 1):
                    if (name, build, rep) in keys:
                        continue
                    t = TIMEOUTS.get(name, 180)
                    r = run_one(binary, path, t)
                    r.update({"module": name, "bytes": path.stat().st_size,
                              "build": build, "rep": rep,
                              "maxrss_kb": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
                    fh.write(json.dumps(r) + "\n"); fh.flush()
                    print(f"{name} {build} rep{rep}: {r['seconds']}s timeout={r['timeout']} aflc={r['aflc']}", flush=True)
                    if r["timeout"]:
                        break
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
