import pygame
import math

from config import *
from vetor import Vetor2D
from game_object import GameObject

class OVNIProjetil(GameObject):
    def __init__(self, posicao: Vetor2D, velocidade: Vetor2D, imagem_path: str):
        super().__init__(posicao, velocidade, 4)
        self.__tempo_criacao = pygame.time.get_ticks()
        self.__imagem_path = imagem_path
        try:
            self.original_image = pygame.image.load(self.__imagem_path).convert_alpha()
        except pygame.error:
            self.original_image = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(self.original_image, VERMELHO, (4, 4), 4)
        angulo = math.degrees(math.atan2(-velocidade.get_y(), velocidade.get_x())) + 90
        self.image = pygame.transform.rotate(self.original_image, -angulo)
        self.rect = self.image.get_rect(center=posicao.para_tupla())
        self.mask = pygame.mask.from_surface(self.image)

    def atualizar(self, delta_tempo: float) -> None:
        super().atualizar(delta_tempo)
        if pygame.time.get_ticks() - self.__tempo_criacao > 3000:
            self.set_ativo(False)

    def to_dict(self) -> dict:
        data = self.to_dict_base()
        data["tempo_criacao_relativo_ms"] = pygame.time.get_ticks() - self.__tempo_criacao
        data["imagem_path"] = self.__imagem_path
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'OVNIProjetil':
        obj = cls(Vetor2D.from_dict(data["posicao"]), Vetor2D.from_dict(data["velocidade"]), data["imagem_path"])
        obj.restaurar_estado_base(data)
        obj.__tempo_criacao = pygame.time.get_ticks() - data.get("tempo_criacao_relativo_ms", 0)
        return obj
