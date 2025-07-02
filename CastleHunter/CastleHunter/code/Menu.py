#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import WIN_WIDTH, C_ORANGE, MENU_OPTION, C_WHITE, C_YELLOW


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/MenuBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        self.volume_on = True # Estado inicial do volume (ligado)
        self.music_volume = 0.3 # Volume padrão da música

    def run(self):
        menu_option = 0
        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.set_volume(self.music_volume) # Define o volume inicial
        pygame.mixer_music.play(-1)
        while True:
            # DRAW IMAGES
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, "CastleHunter", C_ORANGE, ((WIN_WIDTH / 2), 70))

            for i in range(len(MENU_OPTION)):
                option_text = MENU_OPTION[i]
                if option_text == 'VOLUME':
                    status = "ON" if self.volume_on else "OFF"
                    option_text = f"VOLUME: {status}"

                # --- LINHA MODIFICADA AQUI: 200 para 170 ---
                if i == menu_option:
                    self.menu_text(20, option_text, C_YELLOW, ((WIN_WIDTH / 2), 170 + 25 * i)) # Posição Y ajustada
                else:
                    self.menu_text(20, option_text, C_WHITE, ((WIN_WIDTH / 2), 170 + 25 * i)) # Posição Y ajustada
                # --- FIM DA MODIFICAÇÃO ---

            pygame.display.flip()

            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:
                        if MENU_OPTION[menu_option] == 'VOLUME':
                            self.volume_on = not self.volume_on
                            if self.volume_on:
                                pygame.mixer_music.set_volume(self.music_volume)
                            else:
                                pygame.mixer_music.set_volume(0)
                        else:
                            return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)