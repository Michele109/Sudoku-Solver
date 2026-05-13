# Sudoku-Solver

Sudoku benchmark and validation project with support for both **9x9** and **16x16** grids.

## Solver architecture

The solver combines:

- **MRV (Minimum Remaining Values)** to pick the next empty cell.
- **Constraint propagation** before/during search:
  - Naked Singles
  - Hidden Singles (row, column, block)
- **Backtracking** when propagation alone is not enough.

## Performance metrics

The benchmark reports:

- **Expanded Nodes** (`expanded_nodes`): number of search decision points plus assignments made by constraint propagation.
- **Max Memory Nodes** (`max_memory_nodes`): maximum recursion depth reached by the backtracking search.

Interpretation:

- Lower expanded nodes usually indicate stronger pruning/propagation.
- Higher max memory nodes indicates deeper search was required for that puzzle set.

## Run benchmark

```bash
python main.py
```

Then choose:

1. Grid size (`9` or `16`)
2. Number of puzzles (`n > 0`)
3. Mode:
   - `R` random samples
   - `S` static repetition of one sampled puzzle
