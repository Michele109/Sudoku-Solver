import pandas as pd  # Necessario per gestire le righe del dataset

from src.utils.loaders import load_csv
from src.utils.validation import verify_sudoku_solution

# Paths e configurazioni (rimangono simili ai tuoi)
DATA_PATH_9x9 = "data/9x9sudoku.csv"
DATA_PATH_16x16 = "data/16x16sudoku.csv"

GRID_CONFIG = {
    9: {"path": DATA_PATH_9x9, "column": "quizzes", "sol_col": "solutions"},  # Aggiunta colonna soluzione
    16: {"path": DATA_PATH_16x16, "column": "Sudoku", "sol_col": "solution"},
}

def prompt_grid_size() -> int:
    """Prompt the user to choose between 9x9 and 16x16."""
    while True:
        raw = input("Select grid size — enter 9 (Standard) or 16 (Hexadoku): ").strip()
        if raw in ("9", "16"):
            return int(raw)
        print("  Invalid input. Please enter 9 or 16.")


def prompt_sample_size() -> int:
    """Prompt the user for the number of puzzle instances to process."""
    while True:
        raw = input("Enter the number of puzzles to process (n > 0): ").strip()
        if raw.isdigit() and int(raw) > 0:
            return int(raw)
        print("  Invalid input. Please enter a positive integer.")


def prompt_execution_mode() -> str:
    """Prompt the user to choose random or static execution mode."""
    while True:
        raw = input(
            "Select execution mode — enter R (Random) or S (Static): "
        ).strip().upper()
        if raw in ("R", "S"):
            return raw
        print("  Invalid input. Please enter R or S.")

def load_puzzles_df(grid_size: int):
    """Carica l'intero DataFrame per avere sia quiz che soluzioni."""
    config = GRID_CONFIG[grid_size]
    df = load_csv(config["path"])
    return df


def run_benchmark(df: pd.DataFrame, n: int, mode: str, grid_size: int) -> None:
    if df is None or df.empty:
        print("Errore: il dataset è vuoto.")
        return

    config = GRID_CONFIG[grid_size]

    # Selezione dei dati
    if mode == "R":
        n = min(n, len(df))
        selected_data = df.sample(n)
    else:
        # Prende una riga a caso e la ripete n volte
        single_row = df.sample(1)
        selected_data = pd.concat([single_row] * n)

    valid_count = 0
    total_nodes = 0
    max_mem_reached = 0

    print(f"\nEsecuzione di {n} puzzle su griglia {grid_size}x{grid_size} ...\n")

    for _, row in selected_data.iterrows():
        # Adattiamo i nomi delle colonne per la funzione verify_sudoku_solution
        # che si aspetta 'Sudoku' e 'solution'
        row_to_verify = pd.Series({
            'Sudoku': row[config["column"]],
            'solution': row[config["sol_col"]]
        })

        # Usiamo la tua nuova funzione di validazione
        is_correct, nodes, memory = verify_sudoku_solution(row_to_verify)

        if is_correct:
            valid_count += 1
            total_nodes += nodes
            max_mem_reached = max(max_mem_reached, memory)
            print(".", end="", flush=True)  # Feedback visivo
        else:
            print("x", end="", flush=True)

    validation_pct = (valid_count / n) * 100
    avg_nodes = total_nodes / n if n > 0 else 0

    print("\n\n" + "=" * 45)
    print("  RIEPILOGO BENCHMARK")
    print("=" * 45)
    print(f"  Dimensione Griglia : {grid_size}x{grid_size}")
    print(f"  Soluzioni Valide   : {valid_count}/{n} ({validation_pct:.1f}%)")
    print(f"  Nodi Medi Espansi  : {avg_nodes:.2f}")
    print(f"  Profondità Massima : {max_mem_reached}")
    print("=" * 45)


def main() -> None:
    print("\n=== Sudoku Solver Benchmarking Suite ===\n")
    grid_size = prompt_grid_size()
    n = prompt_sample_size()
    mode = prompt_execution_mode()

    df = load_puzzles_df(grid_size)
    if df is None:
        print("Impossibile caricare il dataset. Uscita.")
        return

    run_benchmark(df, n, mode, grid_size)


if __name__ == "__main__":
    main()