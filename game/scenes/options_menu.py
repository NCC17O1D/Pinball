from pathlib import Path
import sys
from pygame import Color, Surface
import pygame
from api.management.scene import BaseDisplay
from pygame.event import Event
from pygame.freetype import Font
from api.ui.button import Button
from api.ui.button_style import ButtonStyle
from api.ui.slider import Slider
from api.ui.text import Text
from api.ui.ui_element_base import UIElementBase

from constants import ASSETS_PATH, PROJECT_PATH, SCREEN_WIDTH
from dynamic_parameters import MASTER_VOLUMNE, MUSIC_VOLUME


class OptionsMenu(BaseDisplay):
    def __init__(self, screen: Surface, scene_manager) -> None:
        self.button_style = ButtonStyle(ASSETS_PATH / Path("buttons/default_style"))

        self.font = Font(ASSETS_PATH / Path("fonts/Tektur-Regular.ttf"), 75)
        self.ui_elements: list[UIElementBase] = []

        super().__init__(screen, scene_manager)

    def awake(self) -> None:
        button_width = 250
        button_height = 125

        text_relativ_x = .05
        text_font_size = 40


        self.title = Text(self.screen, (.5, .05), (.5, 0), text="Options", width=SCREEN_WIDTH-SCREEN_WIDTH/8, font=self.font)
        self.ui_elements.append(self.title)

        # Sliders
        slider_relativ_x = .75
        slider_width = 250

        self.ui_elements.append(Text(self.screen, (.5, .25), (.5, .5), text="Resolution", font=self.font, font_size=text_font_size*2))

        self.ui_elements.append(Text(self.screen, (text_relativ_x, .35), (0, .5), text="Global Scale", font=self.font, font_size=text_font_size))
        gloabl_scale_slider = Slider(self.screen, (slider_relativ_x, .4), (.5, .5), slider_width, 50, min=0.5, max=2.0, step=0.5, initial_value=1)
        gloabl_scale_slider.value.subscribe(lambda value: self.set_global_scale(value))
        self.ui_elements.append(gloabl_scale_slider)


        self.ui_elements.append(Text(self.screen, (.5, .5), (.5, .5), text="Sound", font=self.font, font_size=text_font_size*2))
        
        self.ui_elements.append(Text(self.screen, (text_relativ_x, .6), (0, .5), text="Master Volume", font=self.font, font_size=text_font_size))
        master_volume_slider = Slider(self.screen, (slider_relativ_x, .6), (.5, .5), slider_width, 50, min=0, max=100, step=1, initial_value=50)
        master_volume_slider.value.subscribe(lambda value: self.set_master_volume(value))
        self.ui_elements.append(master_volume_slider)

        self.ui_elements.append(Text(self.screen, (text_relativ_x, .7), (0, .5), text="Music Volume", font=self.font, font_size=text_font_size))
        music_volume_slider = Slider(self.screen, (slider_relativ_x, .7), (.5, .5), slider_width, 50, min=0, max=100, step=1, initial_value=50)
        music_volume_slider.value.subscribe(lambda value: self.set_music_volume(value))
        self.ui_elements.append(music_volume_slider)

        self.ui_elements.append(Text(self.screen, (text_relativ_x, .8), (0, .5), text="SFX Volume", font=self.font, font_size=text_font_size))
        sfx_volume_slider = Slider(self.screen, (slider_relativ_x, .8), (.5, .5), slider_width, 50, min=0, max=100, step=1, initial_value=50)
        sfx_volume_slider.value.subscribe(lambda value: self.set_sfx_volume(value))
        self.ui_elements.append(sfx_volume_slider)

        back_button = self.button_style.create_button_set((button_width, button_height), 0.03, 3, left_sided=True, bottom_sided=True)
        apply_button = self.button_style.create_button_set((button_width, button_height), 0.03, 3, right_sided=True, bottom_sided=True)


        self.ui_elements.append(Button(self.screen, (0, 1), (0, 1), button_width, button_height,
                                  inactive_button=back_button[0], hover_button=back_button[1], pressed_button=back_button[2], 
                                  text="Back", font_size=50, on_click=lambda: self.scene_manager.change_scene("main_menu")))

        self.ui_elements.append(Button(self.screen, (1, 1), (1, 1), button_width, button_height,
                            inactive_button=apply_button[0], hover_button=apply_button[1], pressed_button=apply_button[2], 
                            text="Apply", font_size=50, on_click=lambda: self._apply_changes()))

        return super().awake()

    def update(self, delta_time: float, events: list[Event]) -> None:
        for element in self.ui_elements:
            element.draw()
            element.update_events(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        return super().update(delta_time, events)

    def set_master_volume(self, value: float) -> None:
        MASTER_VOLUMNE = value

    def set_music_volume(self, value: float) -> None:
        MUSIC_VOLUME = value
    
    def set_sfx_volume(self, value: float) -> None:
        SFX_VOLUME = value

    def set_global_scale(self, value: float) -> None:
        print(value)
        pass

    def _apply_changes(self):
        pass