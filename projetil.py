from typing import Optional
import pygame
import math
import random
from enum import Enum, auto

from config import *
from vetor import Vetor2D
from game_object import GameObject


class Projetil(GameObject):
    def __init__(self, posicao: Vetor2D, velocidade: Vetor2D):
        super().__init__(posicao, velocidade, 3)
        self.__frames_vividos = 0
        try:
            self.original_image = pygame.image.load(IMAGEM_PROJETIL_JOGADOR).convert_alpha()
        except pygame.error:
            self.original_image = pygame.Surface((5, 10), pygame.SRCALPHA)
            pygame.draw.rect(self.original_image, BRANCO, (0, 0, 5, 10))
        angulo = math.degrees(math.atan2(-velocidade.get_y(), velocidade.get_x())) + 90
        
        self.image = pygame.transform.rotate(self.original_image, -angulo)
        self.rect = self.image.get_rect(center=posicao.para_tupla())
        self.mask = pygame.mask.from_surface(self.image)

    def atualizar(self, delta_tempo: float) -> None:
        super().atualizar(delta_tempo); self.__frames_vividos += 1
        if self.__frames_vividos > DURACAO_PROJETIL: self.set_ativo(False)

    def to_dict(self) -> dict:
        data = self.to_dict_base()
        data["frames_vividos"] = self.__frames_vividos
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Projetil':
        obj = cls(
            Vetor2D.from_dict(data["posicao"]),
            Vetor2D.from_dict(data["velocidade"])
        )
        obj.restaurar_estado_base(data)
        obj.__frames_vividos = data.get("frames_vividos", 0)
        return obj
