from typing import Optional
import pygame
import random

from config import *
from vetor import Vetor2D
from game_object import GameObject
from ovni_projetil import OVNIProjetil



class OVNI(GameObject):
    def __init__(self, imagem_path: str, posicao: Optional[Vetor2D] = None, velocidade: Optional[Vetor2D] = None):
        raio_ovni = 20
        if posicao is None or velocidade is None:
            direcao = random.choice([-1, 1])
            pos_x = -raio_ovni if direcao == 1 else LARGURA_TELA + raio_ovni
            pos_y = random.uniform(ALTURA_TELA * 0.1, ALTURA_TELA * 0.6)
            posicao_final = Vetor2D(pos_x, pos_y)
            velocidade_final = Vetor2D(VELOCIDADE_OVNI * direcao, 0)
        else:
            posicao_final, velocidade_final = posicao, velocidade
        
        super().__init__(posicao_final, velocidade_final, raio_ovni)
        
        self.__direcao_horizontal = 1 if self.get_velocidade().get_x() > 0 else -1
        self.__ultimo_tiro_tempo_ms = pygame.time.get_ticks()
        
        try:
            self.image = pygame.image.load(imagem_path).convert_alpha()
            self.rect = self.image.get_rect(center=self.get_posicao().para_tupla())
            self.mask = pygame.mask.from_surface(self.image)
        except pygame.error:
            self.image, self.rect, self.mask = None, None, None

    def atualizar(self, delta_tempo: float) -> None:
        super().atualizar(delta_tempo)
        pos_x = self.get_posicao().get_x()
        raio = self.get_raio()
        if (self.__direcao_horizontal == 1 and pos_x > LARGURA_TELA + raio) or \
           (self.__direcao_horizontal == -1 and pos_x < -raio):
            self.set_ativo(False)

    def tentar_atirar(self, posicao_nave: Vetor2D) -> list: return []

    def to_dict(self) -> dict:
        data = self.to_dict_base()
        data.update({"ultimo_tiro_tempo_ms_relativo": max(0, pygame.time.get_ticks() - self.__ultimo_tiro_tempo_ms)})
        return data

    @classmethod
    def _restaurar_estado_ovni(self, data: dict):
        self.__ultimo_tiro_tempo_ms = pygame.time.get_ticks() - data.get("ultimo_tiro_tempo_ms_relativo", 0)

