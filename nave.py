from typing import Optional
import pygame
import math
import random
from enum import Enum, auto

from config import *
from vetor import Vetor2D
from game_object import GameObject
from projetil import Projetil


class Nave(GameObject):
    def __init__(self, posicao: Vetor2D):
        super().__init__(posicao, Vetor2D(), 15)
        self.__angulo_graus = 0.0
        self.__rotacionando_esquerda, self.__rotacionando_direita, self.__acelerando = False, False, False
        self.__ultimo_tiro_tempo, self.__tem_tiro_triplo, self.__tempo_fim_tiro_triplo, self.__tempo_invulneravel_fim = 0, False, 0, 0
        try:
            self.original_image = pygame.image.load(IMAGEM_NAVE).convert_alpha()
        except pygame.error:
            self.original_image = pygame.Surface((self.get_raio() * 2, self.get_raio() * 2), pygame.SRCALPHA)

        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.get_posicao().para_tupla())
        self.mask = pygame.mask.from_surface(self.image)

    def get_angulo(self) -> float: return self.__angulo_graus
    def set_angulo(self, angulo: float): self.__angulo_graus = angulo
    def set_rotacao(self, direcao: str, estado: bool):
        if direcao == 'esquerda': self.__rotacionando_esquerda = estado
        elif direcao == 'direita': self.__rotacionando_direita = estado
    def set_acelerando(self, estado: bool): self.__acelerando = estado
    def get_invulneravel_fim(self) -> int: return self.__tempo_invulneravel_fim
    def set_invulneravel_fim(self, tempo: int): self.__tempo_invulneravel_fim = tempo
    def tem_tiro_triplo(self) -> bool: return self.__tem_tiro_triplo
    def set_tem_tiro_triplo(self, estado: bool): self.__tem_tiro_triplo = estado
    def set_tempo_fim_tiro_triplo(self, tempo: int): self.__tempo_fim_tiro_triplo = tempo
    def is_invulneravel(self) -> bool: return pygame.time.get_ticks() < self.get_invulneravel_fim()

    def desenhar(self, tela: pygame.Surface) -> None:
        if not self.is_ativo(): return
        if self.is_invulneravel() and (pygame.time.get_ticks() // 100) % 2 == 0: return
        super().desenhar(tela)
        if self.__acelerando:
            angulo_rad = math.radians(self.get_angulo())
            pos, raio = self.get_posicao(), self.get_raio()
            tras, esq, dir_ = Vetor2D(0, raio * 1.2).rotacionar(angulo_rad), Vetor2D(-raio * 0.3, raio * 0.8).rotacionar(angulo_rad), Vetor2D(raio * 0.3, raio * 0.8).rotacionar(angulo_rad)
            fogo = [(pos + tras).para_tupla(), (pos + esq).para_tupla(), (pos + dir_).para_tupla()]
            pygame.draw.polygon(tela, VERMELHO, fogo, 0)

    def atualizar(self, delta_tempo: float) -> None:
        if self.tem_tiro_triplo() and pygame.time.get_ticks() >= self.__tempo_fim_tiro_triplo: self.set_tem_tiro_triplo(False)
        if self.__rotacionando_esquerda: self.set_angulo(self.get_angulo() - VELOCIDADE_ROTACAO_NAVE)
        if self.__rotacionando_direita: self.set_angulo(self.get_angulo() + VELOCIDADE_ROTACAO_NAVE)
        if self.__acelerando:
            angulo_rad = math.radians(self.get_angulo() - 90)
            direcao = Vetor2D(math.cos(angulo_rad), math.sin(angulo_rad))
            self.set_velocidade(self.get_velocidade() + direcao * ACELERACAO_NAVE)
        self.set_velocidade(self.get_velocidade() * FRICCAO_NAVE)
        self.image = pygame.transform.rotate(self.original_image, -self.get_angulo())
        self.rect = self.image.get_rect(center=self.get_posicao().para_tupla())
        self.mask = pygame.mask.from_surface(self.image)
        super().atualizar(delta_tempo)

    def atirar(self) -> list['Projetil']:
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.__ultimo_tiro_tempo <= COOLDOWN_TIRO: return []
        self.__ultimo_tiro_tempo = tempo_atual
        angulo_rad = math.radians(self.get_angulo() - 90)
        direcao = Vetor2D(math.cos(angulo_rad), math.sin(angulo_rad))
        pos = self.get_posicao() + direcao * self.get_raio()
        vel = direcao * VELOCIDADE_PROJETIL + self.get_velocidade()
        projeteis = [Projetil(pos, vel)]
        if self.tem_tiro_triplo() and tempo_atual < self.__tempo_fim_tiro_triplo:
            for offset in [-ANGULO_TIRO_TRIPLO_GRAUS, ANGULO_TIRO_TRIPLO_GRAUS]:
                d = direcao.rotacionar(math.radians(offset))
                projeteis.append(Projetil(self.get_posicao() + d * self.get_raio(), d * VELOCIDADE_PROJETIL + self.get_velocidade()))
        return projeteis

    def ativar_tiro_triplo(self, duracao_segundos: int) -> None:
        if self.is_ativo(): self.set_tem_tiro_triplo(True); self.set_tempo_fim_tiro_triplo(pygame.time.get_ticks() + duracao_segundos * 1000)
    
    def to_dict(self) -> dict:  
        data = self.to_dict_base()
        data.update({"angulo_graus": self.get_angulo(), "tem_tiro_triplo": self.tem_tiro_triplo(), "tempo_fim_tiro_triplo_restante_ms": max(0, self.__tempo_fim_tiro_triplo - pygame.time.get_ticks()) if self.tem_tiro_triplo() else 0, "invulneravel_fim_restante_ms": max(0, self.get_invulneravel_fim() - pygame.time.get_ticks())})
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Nave':
        obj = cls(Vetor2D.from_dict(data["posicao"]))
        obj.set_velocidade(Vetor2D.from_dict(data["velocidade"])); obj.restaurar_estado_base(data); obj.set_angulo(data.get("angulo_graus", 0.0))
        obj.set_tem_tiro_triplo(data.get("tem_tiro_triplo", False))
        if obj.tem_tiro_triplo(): obj.set_tempo_fim_tiro_triplo(pygame.time.get_ticks() + data.get("tempo_fim_tiro_triplo_restante_ms", 0))
        tempo_inv_restante = data.get("invulneravel_fim_restante_ms", 0)
        if tempo_inv_restante > 0: obj.set_invulneravel_fim(pygame.time.get_ticks() + tempo_inv_restante)
        return obj
