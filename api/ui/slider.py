from pygame import Surface
import pygame
from api.ui.ui_element_base import UIElementBase
import utils.utils

class Slider(UIElementBase):
    def __init__(self, screen: Surface, rel_x: float, rel_y: float, width: int, height: int, **kwargs):
        """
        Creates a slider.

        Parameters:
            screen (Surface): The screen to draw the slider on.
            rel_x (float): The x-coordinate of the slider relative to the size of the screen.
            rel_y (float): The y-coordinate of the slider relative to the size of the screen.
            width (int): The width of the slider.
            height (int): The height of the slider.
            **kwargs: Additional arguments to pass to the UIElementBase class.
        """

        self.min = kwargs.get("min", 0)
        self.max = kwargs.get("max", 100)
        self.step = kwargs.get("step", 1)
        self.value =  utils.utils.clamp(kwargs.get("initial_value", 0), self.min, self.max)

        self.selected = False

        self.blob_image = kwargs.get("handle_image", None)
        self.handle_image = kwargs.get("handle_image", None)

        super().__init__(screen, rel_x, rel_y, width, height)


    def update_events(self, pygame_events) -> None:
        """
        Updates the slider.

        Parameters:
            pygame_events (list): The list of pygame events.
        """

        mouse_pos = pygame.mouse.get_pos()

        if self.contains(mouse_pos[0], mouse_pos[1]):
            if pygame.mouse.get_pressed()[0]:
                self.selected = True

        for event in pygame_events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.selected = False

        if self.selected:
            self.value = utils.utils.round((mouse_pos[0] - self._x) / self._width * (self.max - self.min) + self.min)
            self.value = max(min(self.value, self.max), self.min)

        return super().update_events(pygame_events)