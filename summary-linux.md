| Module | Bytes | Before (median s) | After (median s) | Speedup | aflc before | aflc after |
|---|---|---|---|---|---|---|
| c-cpp-213-b3d4b933 | 213 | 0.031 | 0.026 | 1.2x | 1 | 1 |
| c-cpp-11747-437bbb52 | 11747 | 0.179 | 0.058 | 3.1x | 36 | 37 |
| c-cpp-31686-cdad54c2 | 31686 | 0.601 | 0.099 | 6.1x | 72 | 74 |
| c-cpp-36406-e4167165 | 36406 | 0.804 | 0.122 | 6.6x | 88 | 88 |
| c-cpp-36872-ae8c6272 | 36872 | 0.972 | 0.153 | 6.4x | 92 | 93 |
| c-cpp-37790-df16c5df | 37790 | 1.080 | 0.117 | 9.2x | 103 | 104 |
| c-cpp-43445-e4167c64 | 43445 | 1.408 | 0.140 | 10.1x | 113 | 114 |
| c-cpp-10259914-e7b1931d | 10259914 | timeout | 16.554 | >36x (timeout) | None | 7241 |
| rust-237-50611fcb | 237 | 0.026 | 0.024 | 1.1x | 4 | 4 |
| rust-19678-3964ca44 | 19678 | 1.018 | 0.092 | 11.1x | 113 | 98 |
| rust-44828-a7cbf271 | 44828 | 4.435 | 0.141 | 31.5x | 167 | 174 |
| rust-82857-cd105621 | 82857 | 16.879 | 0.232 | 72.8x | 235 | 245 |
| rust-180545-2e660083 | 180545 | 48.848 | 0.464 | 105.3x | 424 | 433 |
| rust-371209-766b2e4e | 371209 | timeout | 1.508 | >398x (timeout) | None | 1759 |
| rust-1267866-42c27146 | 1267866 | timeout | 3.002 | >200x (timeout) | None | 3732 |
| rust-23333735-5c8b3eea | 23333735 | timeout | 41.882 | >14x (timeout) | None | 9871 |
| go-1342329-cf7706e2 | 1342329 | timeout | 2.108 | >285x (timeout) | None | 996 |
| go-3820022-8c756e33 | 3820022 | timeout | 11.391 | >53x (timeout) | None | 2460 |
| go-7275141-bf1b4a57 | 7275141 | timeout | 17.751 | >34x (timeout) | None | 4439 |
| go-75106654-8673de74 | 75106654 | timeout | timeout |  | None | None |
| unknown-41-086919d5 | 41 | 0.023 | 0.025 | 0.9x | 3 | 3 |
| unknown-3278-e087012b | 3278 | 0.031 | 0.030 | 1.0x | 4 | 4 |
| unknown-14024-fc225b48 | 14024 | 0.507 | 0.079 | 6.4x | 47 | 48 |
| unknown-25781-b8cbef60 | 25781 | 0.534 | 0.142 | 3.8x | 49 | 49 |
| unknown-48024-c9050a67 | 48024 | 5.849 | 0.188 | 31.1x | 106 | 110 |
| unknown-92239-222494ac | 92239 | 13.647 | 0.374 | 36.5x | 156 | 169 |
| unknown-433848-c461fd74 | 433848 | timeout | 1.144 | >524x (timeout) | None | 1275 |
| unknown-65864037-6cc2f3fa | 65864037 | timeout | 169.907 | >4x (timeout) | None | 89911 |
| rust-1013270-a7e8869e | 1013270 | timeout | 2.252 | >266x (timeout) | None | 1699 |
| rust-1025155-ee6b4e75 | 1025155 | timeout | 2.832 | >212x (timeout) | None | 1674 |
| dotnet.wasm | 2812058 | timeout | 7.968 | >75x (timeout) | None | 12257 |
| AngryBots13.wasm | 10566769 | timeout | 31.883 | >19x (timeout) | None | 31584 |

aflc mismatches before vs after (both finished): [('c-cpp-11747-437bbb52', 36, 37), ('c-cpp-31686-cdad54c2', 72, 74), ('c-cpp-36872-ae8c6272', 92, 93), ('c-cpp-37790-df16c5df', 103, 104), ('c-cpp-43445-e4167c64', 113, 114), ('rust-19678-3964ca44', 113, 98), ('rust-44828-a7cbf271', 167, 174), ('rust-82857-cd105621', 235, 245), ('rust-180545-2e660083', 424, 433), ('unknown-14024-fc225b48', 47, 48), ('unknown-48024-c9050a67', 106, 110), ('unknown-92239-222494ac', 156, 169)]

Peak RSS (patched build, isolated single runs): dotnet.wasm 203 MB, rust-1267866 66 MB, go-3820022 185 MB, unknown-65864037 about 1,891 MB, go-75106654 about 1,657 MB (max over its 3 runs).
go-75106654 after medians come from results-linux-extra.jsonl (900 s timeout): 809.068 / 794.831 / 794.403 s, aflc 46,368.
