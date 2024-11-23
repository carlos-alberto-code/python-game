from typing import List, Tuple, Optional

import pygame
from pygame.surface import Surface
from dataclasses    import dataclass


@dataclass
class Cell:
    """Represents a single cell in the game grid."""
    width: int
    height: int
    position: Tuple[int, int]  # (x, y) position in pixels

    def get_rect(self) -> pygame.Rect:
        """Returns the rectangular bounds of the cell."""
        return pygame.Rect(self.position[0], self.position[1], self.width, self.height)


class Grid:
    """Manages the game's 3x3 grid system."""

    def __init__(self, width: int, height: int, fps: int) -> None:
        self._width = width
        self._height = height
        self._fps = fps
        self._cells: List[List[Cell]] = []
        self._initialize_pygame()
        self._create_grid()

    def _initialize_pygame(self) -> None:
        """Initialize Pygame and create the game window."""
        pygame.init()
        pygame.display.set_caption("Grid Knight")
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._clock = pygame.time.Clock()

    def _create_grid(self) -> None:
        """Create the 3x3 grid of cells."""
        cell_width = self._width // 3
        cell_height = self._height // 3

        self._cells = []
        for row in range(3):
            cell_row = []
            for col in range(3):
                position = (col * cell_width, row * cell_height)
                cell = Cell(cell_width, cell_height, position)
                cell_row.append(cell)
            self._cells.append(cell_row)

    def get_cell_at_position(self, pos: Tuple[int, int]) -> Optional[Cell]:
        """Returns the cell at the given screen position."""
        x, y = pos
        for row in self._cells:
            for cell in row:
                if cell.get_rect().collidepoint(x, y):
                    return cell
        return None

    def draw_grid(self) -> None:
        """Draw the grid lines."""
        for i in range(1, 3):
            # Vertical lines
            pygame.draw.line(
                self._screen,
                (255, 255, 255),
                (i * self._width // 3, 0),
                (i * self._width // 3, self._height)
            )
            # Horizontal lines
            pygame.draw.line(
                self._screen,
                (255, 255, 255),
                (0, i * self._height // 3),
                (self._width, i * self._height // 3)
            )

    def update(self) -> None:
        """Update the game state and render."""
        self._screen.fill((0, 0, 0))  # Clear screen
        self.draw_grid()
        pygame.display.flip()
        self._clock.tick(self._fps)

    @property
    def screen(self) -> Surface:
        return self._screen


def main() -> None:
    """Main game loop."""
    WIDTH, HEIGHT = 256 * 3, 240 * 3  # Using the specified retro resolution
    FPS = 60
    grid = Grid(WIDTH, HEIGHT, FPS)

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Debug: Print cell information when clicked
                cell = grid.get_cell_at_position(pygame.mouse.get_pos())
                if cell:
                    print(f"Clicked cell at position: {cell.position}")

        grid.update()

    pygame.quit()


if __name__ == "__main__":
    main()
