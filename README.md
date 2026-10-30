# Artifact: Fast static analysis of WebAssembly binaries with a per-function scope index

## Contents
- `rizin-wasm-scope-index.patch`: the full change against Rizin dev commit
  33c209ec826a75bb4d712742454db0dedf9b027d (the parent of the pull request
  merge). Apply with `git apply` on a checkout of that commit.
- `bench.py`, `bench_abl.py`: the timing scripts. Fresh process per run,
  `rizin -qq -c "aaa; aflc"`, timeouts 180 s (600 s for dotnet.wasm and
  AngryBots13.wasm, 900 s for the 75 MB module rerun).
- `results-linux.jsonl`: raw rows of the Linux campaign (834 runs).
- `results-linux-extra.jsonl`: the 75 MB module at the 900 s timeout.
- `results-ablation.jsonl`: raw ablation rows.
- `summary-linux.md`, `stats10.md`: medians and ranges computed from the rows.
- `module-list.md`: the 32 modules with byte sizes.
- `machine.txt`: the Linux machine and build record.

## Corpus
30 modules from the filtered WasmBench release (8,461 modules), sampled by
producer group across file size with picker seed 1, plus dotnet.wasm and
AngryBots13.wasm from the Rizin test binaries. The two constructed modules
(brif.wasm, calls.wasm) were measured on the Windows machine only and are
described in the paper.

## Build
meson setup build --buildtype=release -Duse_sys_capstone=disabled
ninja -C build

## Tests
test/unit/test_wasm_scope (29 tests) and test/unit/test_event (8 tests) pass
on the patched build.
