#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys

import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import C_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME, C_GREEN, C_CYAN, EVENT_TIMEOUT, \
    TIMEOUT_STEP, TIMEOUT_LEVEL, C_RED  # Adicionado C_RED para a barra de vida dos inimigos
from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.timeout = TIMEOUT_LEVEL
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []

        # Carregue o background estático apropriado para o nível
        if self.name == 'Level1':
            self.background_image = pygame.image.load('./asset/Level1Static.png').convert_alpha()
        elif self.name == 'Level2':
            self.background_image = pygame.image.load('./asset/Level2Static.png').convert_alpha()
        else:
            self.background_image = None

        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]
        self.entity_list.append(player)
        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]
            self.entity_list.append(player)
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)  # 100ms

    def run(self, player_score: list[int]):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.set_volume(0.3)
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)

            # Desenhe o background estático no início de cada frame
            if self.background_image:
                self.window.blit(source=self.background_image, dest=(0, 0))

            for ent in self.entity_list:
                # Apenas desenhe as entidades que não são o background
                if not isinstance(ent,
                                  type(self.background_image)):  # Esta linha pode ser removida se o background_image nunca for uma "Entity"
                    self.window.blit(source=ent.surf, dest=ent.rect)

                ent.move()

                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

                    # --- NOVO CÓDIGO: Desenhar barra de vida ---
                    self.draw_health_bar(ent)  # Chama o novo método para desenhar a barra de vida
                    # --- FIM NOVO CÓDIGO ---

                if ent.name == 'Player1':
                    self.level_text(14, f'Player1 - Health: {ent.health} | Score: {ent.score}', C_GREEN, (10, 25))
                if ent.name == 'Player2':
                    self.level_text(14, f'Player2 - Health: {ent.health} | Score: {ent.score}', C_CYAN, (10, 45))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout == 0:
                        for ent in self.entity_list:
                            if isinstance(ent, Player) and ent.name == 'Player1':
                                player_score[0] = ent.score
                            if isinstance(ent, Player) and ent.name == 'Player2':
                                player_score[1] = ent.score
                        return True

                found_player = False
                for ent in self.entity_list:
                    if isinstance(ent, Player):
                        found_player = True

                if not found_player:
                    return False

            # printed text
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', C_WHITE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps():.0f}', C_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades: {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 20))
            pygame.display.flip()
            # Collisions
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)

    # --- NOVO MÉTODO: Desenha a barra de vida ---
    def draw_health_bar(self, entity: Entity):
        if not hasattr(entity, 'max_health'):  # Garante que a entidade tem vida máxima definida
            return

        bar_width = entity.rect.width  # Largura da barra baseada na largura da entidade
        bar_height = 5  # Altura da barra de vida
        bar_offset_y = 10  # Distância acima da entidade

        # Posição da barra de vida acima da entidade
        bar_x = entity.rect.x
        bar_y = entity.rect.y - bar_height - bar_offset_y

        # Calcula a porcentagem de vida
        health_percentage = entity.health / entity.max_health
        current_bar_width = int(bar_width * health_percentage)

        # Cor da barra de vida
        if isinstance(entity, Player):
            health_color = C_GREEN
        elif isinstance(entity, Enemy):
            health_color = C_RED
        else:
            health_color = C_WHITE  # Cor padrão se não for player nem inimigo

        # Desenha o fundo da barra (preto para contraste)
        pygame.draw.rect(self.window, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Desenha a barra de vida atual
        pygame.draw.rect(self.window, health_color, (bar_x, bar_y, current_bar_width, bar_height))
    # --- FIM NOVO MÉTODO ---