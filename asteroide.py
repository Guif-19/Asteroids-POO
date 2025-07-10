from typing import Optional
import pygame
import math
import random
from enum import Enum, auto

from config import *
from vetor import Vetor2D
from game_object import GameObject

class Asteroide(GameObject):
    TAMANHOS = {"grande": (35, PONTOS_ASTEROIDE_GRANDE), "medio": (25, PONTOS_ASTEROIDE_MEDIO), "pequeno": (12, PONTOS_ASTEROIDE_PEQUENO)}
    def __init__(self, posicao: Vetor2D, tamanho_str="grande", velocidade: Vetor2D = None):
        raio, pontos = self.TAMANHOS[tamanho_str]
        vel = velocidade if velocidade is not None else Vetor2D(random.uniform(VEL_MIN_ASTEROIDE, VEL_MAX_ASTEROIDE) * random.choice([-1, 1]), random.uniform(VEL_MIN_ASTEROIDE, VEL_MAX_ASTEROIDE) * random.choice([-1, 1]))
        super().__init__(posicao, vel, raio)
        self.__tamanho_str, self.__pontos, self.__angulo_rotacao, self.__velocidade_rotacao = tamanho_str, pontos, random.uniform(0, 360), random.uniform(-1, 1)
        
        imagem_path = {"grande": IMAGEM_ASTEROIDE_GRANDE, "medio": IMAGEM_ASTEROIDE_MEDIO, "pequeno": IMAGEM_ASTEROIDE_PEQUENO}[tamanho_str]
        try:
            self.original_image = pygame.image.load(imagem_path).convert_alpha()
        except pygame.error:
            self.original_image = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.original_image, CINZA_CLARO, (raio, raio), raio, 1)
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=posicao.para_tupla())
        self.mask = pygame.mask.from_surface(self.image)

    def get_tamanho_str(self) -> str: return self.__tamanho_str
    def get_pontos(self) -> int: return self.__pontos

    def atualizar(self, delta_tempo: float) -> None:
        self.__angulo_rotacao = (self.__angulo_rotacao + self.__velocidade_rotacao) % 360
        self.image = pygame.transform.rotate(self.original_image, self.__angulo_rotacao)
        self.rect = self.image.get_rect(center=self.get_posicao().para_tupla())
        self.mask = pygame.mask.from_surface(self.image)
        super().atualizar(delta_tempo)

    def dividir(self) -> list['Asteroide']:
        if self.get_tamanho_str() == "pequeno": self.set_ativo(False); return []
        self.set_ativo(False)
        proximo_tamanho = "medio" if self.get_tamanho_str() == "grande" else "pequeno"
        novos = []
        for i in range(2):
            vel_base = self.get_velocidade()
            if vel_base.magnitude() < 0.1: vel_base = Vetor2D(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
            offset_dir = vel_base.normalizar().rotacionar(math.radians(90))
            offset = offset_dir * (self.get_raio() / 1.5) * (1 if i == 0 else -1)
            pos_frag = self.get_posicao() + offset
            vel_frag = vel_base.rotacionar(math.radians(random.uniform(20, 50) * (1 if i == 0 else -1)))
            novos.append(Asteroide(pos_frag, proximo_tamanho, vel_frag))
        return novos

    def to_dict(self) -> dict:
        data = self.to_dict_base()
        data.update({
            "tamanho_str": self.get_tamanho_str(),
            "pontos": self.get_pontos(),
            "angulo_rotacao": self.__angulo_rotacao,
            "velocidade_rotacao": self.__velocidade_rotacao
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Asteroide':
        obj = cls(
            Vetor2D.from_dict(data["posicao"]),
            data.get("tamanho_str", "grande"),
            Vetor2D.from_dict(data["velocidade"])
        )
        obj.restaurar_estado_base(data)
        
        obj.__pontos = data.get("pontos", cls.TAMANHOS[obj.get_tamanho_str()][1])
        obj.__angulo_rotacao = data.get("angulo_rotacao", 0)
        obj.__velocidade_rotacao = data.get("velocidade_rotacao", random.uniform(-1, 1))
        
        return obj
