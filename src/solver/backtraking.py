from src.utils.constants import char_to_int, int_to_char

class SudokuSolver:
    def __init__(self, sudoku_string: str):
        self.BOARD_SIZE = int(len(sudoku_string)**0.5)
        self.BLOCK_SIZE = int(self.BOARD_SIZE**0.5)
        self.grid = self._parse_sudoku_string(sudoku_string)
        self.expanded_nodes = 0
        self.max_memory_nodes = 0
        self.current_recursion_depth = 0
        # Apply initial constraint propagation
        self._initial_propagation_result = self._apply_constraint_propagation()

    def _parse_sudoku_string(self, sudoku_string):
        # Ensure the string is the correct length
        if len(sudoku_string) != self.BOARD_SIZE * self.BOARD_SIZE:
            raise ValueError(f"Sudoku string must be {self.BOARD_SIZE*self.BOARD_SIZE} characters long.")

        grid = []
        for i in range(self.BOARD_SIZE):
            row_str = sudoku_string[i*self.BOARD_SIZE : (i+1)*self.BOARD_SIZE]
            grid.append([char_to_int(char) for char in row_str])
        return grid

    def _is_valid(self, board, row, col, num):
        # Check row
        if num in board[row]:
            return False

        # Check column
        for r_idx in range(self.BOARD_SIZE):
            if board[r_idx][col] == num:
                return False

        # Check 4x4 block
        start_row = (row // self.BLOCK_SIZE) * self.BLOCK_SIZE
        start_col = (col // self.BLOCK_SIZE) * self.BLOCK_SIZE
        for r_idx in range(start_row, start_row + self.BLOCK_SIZE):
            for c_idx in range(start_col, start_col + self.BLOCK_SIZE):
                if board[r_idx][c_idx] == num:
                    return False
        return True

    def _get_possible_values(self, row, col):
        """Returns a list of possible numbers for a given cell."""
        possible = []
        for num in range(1, self.BOARD_SIZE + 1):
            if self._is_valid(self.grid, row, col, num):
                possible.append(num)
        return possible

    def _get_all_empty_cells_with_possibilities(self):
        """Returns a dict of {(r, c): [possible_nums]} for all empty cells, or False if contradiction found."""
        empty_cells_possibilities = {}
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                if self.grid[r][c] == 0:
                    possibles = self._get_possible_values(r, c)
                    if not possibles: # Contradiction: an empty cell has no possible values
                        return False
                    empty_cells_possibilities[(r, c)] = possibles
        return empty_cells_possibilities

    def _apply_constraint_propagation(self):
        """Applies Naked Single and Hidden Single rules iteratively until no more progress is made.
        Returns False if a contradiction is found, True otherwise.
        """
        while True:
            made_progress_in_this_iteration = False

            empty_cells_possibilities = self._get_all_empty_cells_with_possibilities()
            if empty_cells_possibilities is False: # Contradiction detected during possibilities refresh
                return False
            if not empty_cells_possibilities: # Board is full
                return True

            # Naked Singles: If a cell has only one possible value, fill it.
            naked_single_found = False
            for (r, c), possibles in list(empty_cells_possibilities.items()):
                if len(possibles) == 1:
                    self.grid[r][c] = possibles[0]
                    self.expanded_nodes += 1 # Count as a fixed node by propagation
                    naked_single_found = True
                    break # Found a Naked Single, re-evaluate all rules from scratch

            if naked_single_found:
                made_progress_in_this_iteration = True
                continue # Restart outer while loop

            # Hidden Singles: If a number can only go in one cell within a unit (row/col/block), fill that cell.
            hidden_single_found = False

            # Rows
            for r in range(self.BOARD_SIZE):
                digit_to_locations = {num: [] for num in range(1, self.BOARD_SIZE + 1)}
                for c in range(self.BOARD_SIZE):
                    if self.grid[r][c] == 0:
                        for num in empty_cells_possibilities.get((r, c), []):
                            digit_to_locations[num].append((r, c))

                for num, locations in digit_to_locations.items():
                    if len(locations) == 1: # Hidden Single found
                        cell_r, cell_c = locations[0]
                        if self.grid[cell_r][cell_c] == 0: # Ensure it's still empty
                            self.grid[cell_r][cell_c] = num
                            self.expanded_nodes += 1
                            hidden_single_found = True
                            break # Found a Hidden Single, re-evaluate all rules
                if hidden_single_found: break # Break from row loop

            if hidden_single_found:
                made_progress_in_this_iteration = True
                continue # Restart outer while loop

            # Columns
            for c in range(self.BOARD_SIZE):
                digit_to_locations = {num: [] for num in range(1, self.BOARD_SIZE + 1)}
                for r in range(self.BOARD_SIZE):
                    if self.grid[r][c] == 0:
                        for num in empty_cells_possibilities.get((r, c), []):
                            digit_to_locations[num].append((r, c))

                for num, locations in digit_to_locations.items():
                    if len(locations) == 1: # Hidden Single found
                        cell_r, cell_c = locations[0]
                        if self.grid[cell_r][cell_c] == 0:
                            self.grid[cell_r][cell_c] = num
                            self.expanded_nodes += 1
                            hidden_single_found = True
                            break
                if hidden_single_found: break # Break from col loop

            if hidden_single_found:
                made_progress_in_this_iteration = True
                continue # Restart outer while loop

            # Blocks
            for block_row_start in range(0, self.BOARD_SIZE, self.BLOCK_SIZE):
                for block_col_start in range(0, self.BOARD_SIZE, self.BLOCK_SIZE):
                    digit_to_locations = {num: [] for num in range(1, self.BOARD_SIZE + 1)}
                    for r in range(block_row_start, block_row_start + self.BLOCK_SIZE):
                        for c in range(block_col_start, block_col_start + self.BLOCK_SIZE):
                            if self.grid[r][c] == 0:
                                for num in empty_cells_possibilities.get((r, c), []):
                                    digit_to_locations[num].append((r, c))

                    for num, locations in digit_to_locations.items():
                        if len(locations) == 1: # Hidden Single found
                            cell_r, cell_c = locations[0]
                            if self.grid[cell_r][cell_c] == 0:
                                self.grid[cell_r][cell_c] = num
                                self.expanded_nodes += 1
                                hidden_single_found = True
                                break
                if hidden_single_found: break # Break from inner block loop
            if hidden_single_found: # Break from outer block loop
                made_progress_in_this_iteration = True
                continue # Restart outer while loop

            if not made_progress_in_this_iteration:
                break # No progress was made in this iteration, exit loop
        return True # Propagation completed without contradiction

    def _find_empty(self, board):
        """Finds the empty cell with the Minimum Remaining Values (MRV heuristic)."""
        min_possible_count = self.BOARD_SIZE + 1
        best_empty_cell = None

        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                if board[r][c] == 0:
                    possible_values = self._get_possible_values(r, c)
                    num_possible = len(possible_values)

                    # If a cell has 0 possible values, this path is invalid.
                    # The solve function will backtrack when it tries to fill this cell.
                    # We still need to find the cell with minimum *positive* possibilities.
                    if num_possible < min_possible_count:
                        min_possible_count = num_possible
                        best_empty_cell = (r, c)
                        # Optimization: if a cell has only one possible value, it's the best choice.
                        if num_possible == 1:
                            return best_empty_cell[0], best_empty_cell[1]

        if best_empty_cell:
            return best_empty_cell[0], best_empty_cell[1]
        return None, None # No empty cell found (board is full)

    def solve(self):
        if not self._initial_propagation_result: # If initial propagation failed, puzzle is unsolvable
            return False

        self.current_recursion_depth += 1
        self.max_memory_nodes = max(self.max_memory_nodes, self.current_recursion_depth)

        row, col = self._find_empty(self.grid) # Uses MRV to select the next cell

        if row is None: # No empty cells, Sudoku is solved
            self.current_recursion_depth -= 1
            return True

        self.expanded_nodes += 1 # Increment expanded nodes for each decision point

        # Try numbers only from the pre-calculated possible values for this cell
        possible_values_for_cell = self._get_possible_values(row, col)

        for num in possible_values_for_cell:
            self.grid[row][col] = num
            if self.solve():
                return True
            # Backtrack
            self.grid[row][col] = 0

        self.current_recursion_depth -= 1
        return False # No number worked in this cell or an earlier decision was wrong

    def get_solution(self):
        """Returns the solved Sudoku grid in character format and as a single string."""
        solved_grid_chars = []
        for r in range(self.BOARD_SIZE):
            solved_grid_chars.append(''.join([int_to_char(num) for num in self.grid[r]]))
        found_solution_str = ''.join(solved_grid_chars)
        return [solved_grid_chars, found_solution_str]