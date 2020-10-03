from graphics import *


COLS = 48
ROWS = 48
CELL_SIZE = 20
PADDING = 4
WIDTH = COLS * (CELL_SIZE + PADDING) + PADDING
HEIGHT = ROWS * (CELL_SIZE + PADDING) + PADDING
BG_COLOR = color_rgb(50, 50, 50)
DEAD_COLOR = color_rgb(0, 0, 0)
LIVE_COLOR = color_rgb(245, 245, 0)  # cadmium yellow
SLEEP_TIME = 0.1  # Duration in seconds between each iteration


class Cell:
    def __init__(self, row, col):
        self.rect = Rectangle(
            Point(col * (CELL_SIZE + PADDING) + PADDING, row * (CELL_SIZE + PADDING) + PADDING),
            Point(col * (CELL_SIZE + PADDING) + PADDING + CELL_SIZE, row * (CELL_SIZE + PADDING) + CELL_SIZE + PADDING)
        )
        self.rect.setFill(DEAD_COLOR)
        # Current state
        self.alive = False
        # placeholder for next iteration's state
        self.next_value = False

    def go_to_next_state(self):
        # Only need to take action if the state has changed
        if self.alive and not self.next_value:
            # This cell has died
            self.alive = self.next_value
            self.rect.setFill(DEAD_COLOR)
        elif not self.alive and self.next_value:
            # This cell has come to life
            self.alive = self.next_value
            self.rect.setFill(LIVE_COLOR)


class Grid:
    def __init__(self, rows, cols, win, wrap=False):
        self.cols = cols
        self.rows = rows
        self.wrap = wrap
        self.grid = [[
             Cell(row, col) for row in range(rows)
        ] for col in range(cols)]
        for col in self.grid:
            for cell in col:
                cell.rect.setFill(DEAD_COLOR)
                cell.rect.draw(win)

    def get_alive(self, row, col):
        if not self.wrap and any([
            row == -1,
            row == self.rows,
            col == -1,
            col == self.cols
        ]):
            return False
        return self.grid[col % self.cols][row % self.rows].alive

    def activate(self, col, row):
        self.grid[col][row].alive = True
        self.grid[col][row].rect.setFill(LIVE_COLOR)

    def deactivate(self, row, col):
        self.grid[col][row].alive = False
        self.grid[col][row].rect.setFill(DEAD_COLOR)

    def iterate(self):
        # Determine next state of grid
        for col in range(0, self.cols):
            for row in range(0, self.rows):
                live_neighbors = sum((
                    1 for r in range(row-1, row+2) for c in range(col-1, col+2)
                    if self.get_alive(r, c) and not (c == col and r == row)
                ))
                # No need to make a call to self.get_alive here because we know we're not potentially wrapping
                if self.grid[col][row].alive:
                    if live_neighbors == 2 or live_neighbors == 3:
                        self.grid[col][row].next_value = True
                    else:
                        self.grid[col][row].next_value = False
                else:
                    if live_neighbors == 3:
                        self.grid[col][row].next_value = True
                    else:
                        self.grid[col][row].next_value = False

        # Update the current state of the grid to be the next state
        for col in self.grid:
            for cell in col:
                cell.go_to_next_state()


def main(initial_grid=None):
    win = GraphWin("Conway's Game of Life", WIDTH, HEIGHT)
    win.setBackground(BG_COLOR)
    grid = Grid(ROWS, COLS, win)

    if initial_grid:
        for (x, y) in initial_grid:
            grid.activate(x, y)

    while win.checkMouse() is None:
        time.sleep(SLEEP_TIME)
        grid.iterate()

    win.close()
