from src.utils import visualizer
from src.utils import loaders

DATA_PATH9x9 = '../data/9x9sudoku.csv'
DATA_PATH16x16 = '../data/16x16sudoku.csv'

dataset9x9 = loaders.load_csv(DATA_PATH9x9)
dataset16x16 = loaders.load_csv(DATA_PATH16x16)

print ("Testing print_sudoku_grid with samples Sudoku grids:")

sample_sudoku_str1 = dataset16x16['Sudoku'][0]  # Get the first Sudoku grid from the 16x16 dataset
sample_sudoku_str2 = dataset9x9['quizzes'][0]  # Get the first Sudoku grid from the 9x9 dataset
visualizer.print_sudoku_grid(sample_sudoku_str1, GRID_SIZE=16)
visualizer.print_sudoku_grid(sample_sudoku_str2, GRID_SIZE=9)

print("Testing prepare_grid_from_string with a samples Sudoku grids:")

sample_sudoku_grid1 = visualizer.prepare_grid_from_string(sample_sudoku_str1, GRID_SIZE=16)
sample_sudoku_grid2 = visualizer.prepare_grid_from_string(sample_sudoku_str2, GRID_SIZE=9)

print("---9x9 Sudoku Grid---")
print(sample_sudoku_grid1)
print("---16x16 Sudoku Grid---")
print(sample_sudoku_grid2)