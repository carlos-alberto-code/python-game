from typing import Tuple
from .entity import Entity
import pygame

class Player(Entity):
    def __init__(
        self,
        position: Tuple[float, float],
        size: Tuple[int, int] = (32, 32),
        speed: float = 200.0
    ) -> None:
        super().__init__(position, size, speed)
        self.image.fill((0, 255, 0))  # Temporary green color
        self.jumping: bool = False
        self.jump_force: float = 400.0
        self.gravity: float = 800.0

    def handle_input(self, dt: float) -> None:
        """Handle player input.

        Args:
            dt: Time delta in seconds
        """
        keys = pygame.key.get_pressed()
        move_x = 0.0

        if keys[pygame.K_LEFT]:
            move_x = -self.speed
        if keys[pygame.K_RIGHT]:
            move_x = self.speed

        if keys[pygame.K_SPACE] and not self.jumping:
            self._velocity = pygame.Vector2(self._velocity.x, -self.jump_force)
            self.jumping = True

        self._velocity = pygame.Vector2(move_x, self._velocity.y)

    def update(self, dt: float) -> None:
        """Update player state.

        Args:
            dt: Time delta in seconds
        """
        # Apply gravity
        self._velocity = pygame.Vector2(self._velocity.x, self._velocity.y + self.gravity * dt)

        # Update position
        super().update(dt)

        # Simple ground collision
        if self.rect.bottom > 240:  # Screen height
            self.rect.bottom = 240
            self._position.y = float(self.rect.top)
            self._velocity = pygame.Vector2(self._velocity.x, 0)
            self.jumping = False
