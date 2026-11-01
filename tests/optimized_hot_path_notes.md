# Integrated conversion optimization

Production changes are in `opencc_purepy/core.py` and
`opencc_purepy/starter_union.py`.

StarterUnion builds a private map of starting characters to descending distinct
key lengths alongside its original BMP/astral indexes. Identical length tuples
are shared. Greedy matching iterates cached lengths rather than trimming masks
and selecting/clearing bits for every candidate.

Serial conversion and workers process their ranges with one output list and one
loop, slicing only candidate words. Existing range generation is retained so
get_split_ranges behavior, delimiters, and custom range handling remain intact.
The 10,000-character splitting threshold and the >1,000-ranges / >=1,000,000-
characters multiprocessing conditions remain unchanged, as do four-worker
chunking and Pool lifecycle. The legacy mask path supports duck-typed unions and
older indexed objects without the private index. Public method and constructor
signatures, dictionary precedence, and short-text behavior are preserved.

The range kernel is a module-level `convert_union_ranges_indexed` function so
worker code does not access a protected class member. Profiling candidate
adapters reuse this kernel instead of duplicating its matching loop. Cached
length annotations use `Sequence[int]`; stored patterns remain immutable tuples.
The earlier experiment reports record measurements before this adapter cleanup.

## Final warm benchmarks

The harness `benchmark_optimized_hot_path.py` compares the integrated converter
against core.py from commit `5a6f35d34c25b2f126912deeb11496be598037e4`.
It uses the same dictionaries, prewarms indexes, randomizes path order, and
checks every result against the original output. The small sample uses 15
batches of 20 conversions; the 100k prefix uses seven trials; full-file and
double-file cases use five. Multiprocessing includes Pool startup and payload
serialization on every call. The benchmark's baseline module registration in
spawned interpreters introduces some common harness startup work for both paths.

| Case | Python 3.8 original / optimized, ms | Less time | Python 3.13 original / optimized, ms | Less time |
| --- | ---: | ---: | ---: | ---: |
| sample_hans.txt, 7,735 chars | 7.48 / 4.40 | 41.1% | 5.94 / 4.49 | 24.4% |
| ChangFeng 100k prefix | 95.78 / 58.40 | 39.0% | 80.21 / 60.80 | 24.2% |
| ChangFeng full file, serial | 1,050.75 / 667.76 | 36.4% | 889.43 / 716.91 | 19.4% |
| ChangFeng full file, automatic multiprocessing | 599.72 / 506.12 | 15.6% | 562.04 / 521.24 | 7.3% |
| ChangFeng doubled, 2,217,180 chars, automatic multiprocessing | 985.57 / 776.76 | 21.2% | 898.92 / 802.68 | 10.7% |

The two raw runtime reports are `benchmark_optimized_hot_path_py38.json` and
`benchmark_optimized_hot_path_py313.json`. Earlier experiment harnesses remain
anchored to the pre-refactor core so they still measure the original candidates.

## Index cost

Nine fresh-index measurements on Python 3.8, using an already merged S2T map,
gave original index build median 9.84 ms versus 17.41 ms with cached lengths:
about 7.58 ms additional one-time work per newly indexed S2T union. These are
index-only measurements, excluding dictionary loading/merging and array
allocation. Existing indexed unions reuse the cached index.

The S2T length map contains 6,244 starters and 205 distinct shared tuples.
Its approximate reachable size including keys and unique tuples, excluding
shared integer objects, is 789,936 bytes (~771 KiB). Some referenced objects
may already be shared, so this is not a measured RSS increase. The serialized
union payload increases from roughly 1.57 MB to 1.64 MB (about 69 KB / 4.4%).
The measured parallel improvements already include that extra payload cost.
Raw index measurements are in `benchmark_hot_path_index_cost.json`.

## Validation

- Full pytest suite: 86 passed on Python 3.8.10 and 86 on Python 3.7.9.
- Standard-library unittest discovery: 60 passed on Python 3.13.16. Pytest is
  not installed for that interpreter, so this excludes function-style tests.
- New regression tests cover constructor compatibility, lazy index reuse,
  longest matching, precedence, empty replacements, astral starters, 63/64/65/
  70/120-character keys, cap limits, randomized comparisons with the original
  mask loop, all configs and punctuation settings, pickling, old/duck-typed
  unions, range offsets/gaps/negative bounds, and the unchanged thresholds.
- Real Windows spawned-worker conversion matched the original on both the
  1.1-million-character file and the doubled 2.2-million-character input.
- `git diff --check` passed. Tracked bytecode generated during validation was
  restored; only intended source changes and profiling/test artifacts remain.
