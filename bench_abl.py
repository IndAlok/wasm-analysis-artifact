#!/usr/bin/env python3
"""Ablation benchmarks: each variant = PR head with ONE change disabled.
Modules: dotnet.wasm (cap 600) and rust-1267866 (cap 180). 3 reps, fresh
process per run, same command as the main campaign. Resumable."""
import json, os, resource, subprocess, time
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "results-ablation.jsonl"
REPS = 3
JOBS = [
    ("noindex", ROOT / "rizin-pr" / "abl-noindex" / "build-abl" / "binrz" / "rizin" / "rizin"),
    ("nocall", ROOT / "rizin-pr" / "abl-nocall" / "build-abl" / "binrz" / "rizin" / "rizin"),
    ("noaav", ROOT / "rizin-pr" / "abl-noaav" / "build-abl" / "binrz" / "rizin" / "rizin"),
]
MODULES = [
    ("dotnet.wasm", ROOT / "testbins" / "wasm" / "dotnet.wasm", 600),
    ("rust-1267866-42c27146", ROOT / "corpus" / "rust-1267866-42c27146.wasm", 180),
]

def run(binary, mod, timeout):
    t0 = time.perf_counter(); timeout_flag = False; out = ""
    try:
        p = subprocess.run([str(binary), "-qq", "-c", "aaa; aflc", str(mod)],
                           capture_output=True, text=True, timeout=timeout)
        out = p.stdout
    except subprocess.TimeoutExpired:
        timeout_flag = True
    dt = time.perf_counter() - t0
    rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    aflc = None
    if out.strip():
        try: aflc = int(out.strip().splitlines()[-1])
        except ValueError: pass
    return {"seconds": round(min(dt, timeout), 3) if timeout_flag else round(dt, 3),
            "timeout": timeout_flag, "aflc": aflc, "maxrss_kb_cum": rss}

def load_done():
    done = {}
    if OUT.exists():
        for line in open(OUT):
            if line.strip():
                r = json.loads(line); done.setdefault((r["variant"], r["module"]), []).append(r)
    return done

def main():
    done = load_done()
    for variant, binary in JOBS:
        if not binary.exists():
            print(f"SKIP {variant}: binary missing", flush=True); continue
        for name, mod, cap in MODULES:
            rows = done.get((variant, name), [])
            if any(r["timeout"] for r in rows):
                print(f"SKIP {variant} {name}: timeout recorded", flush=True); continue
            for rep in range(len(rows) + 1, REPS + 1):
                r = run(binary, mod, cap)
                r.update({"variant": variant, "module": name, "rep": rep})
                with open(OUT, "a") as f: f.write(json.dumps(r) + "\n")
                print(f"{variant} {name} rep{rep}: {r['seconds']}s timeout={r['timeout']} aflc={r['aflc']}", flush=True)
                if r["timeout"]: break
    print("ABLATION DONE", flush=True)

if __name__ == "__main__":
    main()
