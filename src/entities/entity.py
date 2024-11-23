from typing import Tuple, Optional
import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2

class Entity(Sprite):
    """Base class for all game entities"""

    def __init__(
        self,
        position: Tuple[float, float],
        size: Tuple[int, int],
        speed: float = 0.0
    ) -> None:
        """Initialize the entity.

        Args:
            position: Initial (x, y) position
            size: Width and height of the entity
            speed: Initial movement speed
        """
        super().__init__()

        # Position and movement
        self._position: Vector2 = Vector2(position)
        self._velocity: Vector2 = Vector2(0, 0)
        self.speed: float = speed

        # Collision and rendering
        self.image: pygame.Surface = pygame.Surface(size)
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = (int(self._position.x), int(self._position.y))

        # State
        self.active: bool = True
        self.visible: bool = True

    @property
    def position(self) -> Tuple[float, float]:
        """Get the current position"""
        return (self._position.x, self._position.y)

    @position.setter
    def position(self, value: Tuple[float, float]) -> None:
        """Set the position"""
        self._position = Vector2(value)
        self.rect.topleft = (int(self._position.x), int(self._position.y))

    @property
    def velocity(self) -> Tuple[float, float]:
        """Get the current velocity"""
        return (self._velocity.x, self._velocity.y)

    @velocity.setter
    def velocity(self, value: Tuple[float, float]) -> None:
        """Set the velocity"""
        self._velocity = Vector2(value)

    def update(self, dt: float) -> None:
        """Update entity state.

        Args:
            dt: Time delta in seconds
        """
        # Update position based on velocity
        self._position += self._velocity * dt
        self.rect.topleft = (int(self._position.x), int(self._position.y))

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the entity if visible.

        Args:
            surface: Surface to draw on
        """
        if self.visible:
            surface.blit(self.image, self.rect)
