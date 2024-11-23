from abc import ABC, abstractmethod
from typing import Optional
import pygame

class GameState(ABC):
    def __init__(self) -> None:
        self.next_state: Optional[GameState] = None

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update the state logic"""
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the state"""
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events"""
        pass

    def switch_to(self, state: 'GameState') -> None:
        """Switch to a new state"""
        self.next_state = state

    def get_next_state(self) -> Optional['GameState']:
        """Get the next state if exists"""
        return self.next_state
