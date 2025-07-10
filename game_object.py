from typing import Optional
import pygame
from config import *
from vetor import Vetor2D


class GameObject:
    def __init__(self, posicao: Vetor2D, velocidade: Vetor2D, raio: float):
        self.__posicao = posicao
        self.__velocidade = velocidade
        self.__raio = raio
        self.__ativo = True
        self.image: pygame.Surface | None = None
        self.rect: pygame.Rect | None = None
        self.mask: pygame.mask.Mask | None = None

    def get_posicao(self) -> Vetor2D: return self.__posicao
    def get_velocidade(self) -> Vetor2D: return self.__velocidade
    def get_raio(self) -> float: return self.__raio
    def is_ativo(self) -> bool: return self.__ativo
    def get_rect(self) -> Optional[pygame.Rect]: return self.rect

    def set_posicao(self, nova_posicao: Vetor2D): self.__posicao = nova_posicao
    def set_velocidade(self, nova_velocidade: Vetor2D): self.__velocidade = nova_velocidade
    def set_ativo(self, estado: bool): self.__ativo = estado

    def atualizar(self, delta_tempo: float) -> None:
        posicao_atual = self.get_posicao()
        velocidade_atual = self.get_velocidade()
        raio = self.get_raio()

        nova_posicao = posicao_atual + velocidade_atual * delta_tempo * FPS
        
        self.set_posicao(nova_posicao)
        
        # wrap-around
        if nova_posicao.get_x() < -raio: nova_posicao.set_x(LARGURA_TELA + raio)
        elif nova_posicao.get_x() > LARGURA_TELA + raio: nova_posicao.set_x(-raio)
        if nova_posicao.get_y() < -raio: nova_posicao.set_y(ALTURA_TELA + raio)
        elif nova_posicao.get_y() > ALTURA_TELA + raio: nova_posicao.set_y(-raio)

        if self.rect:
            self.rect.center = nova_posicao.para_tupla()

    def desenhar(self, tela: pygame.Surface) -> None:
        if self.is_ativo() and self.image and self.rect:
            tela.blit(self.image, self.rect)

    def colide_com(self, outro_objeto: 'GameObject') -> bool:
        if not self.is_ativo() or not outro_objeto.is_ativo(): return False
        r1, r2 = self.get_rect(), outro_objeto.get_rect()
        if not r1 or not r2: return False
        if not r1.colliderect(r2): return False
        
        mask_self, mask_outro = getattr(self, 'mask', None), getattr(outro_objeto, 'mask', None)
        if not mask_self or not mask_outro: return False
        
        offset = (r2.x - r1.x, r2.y - r1.y)
        return mask_self.overlap(mask_outro, offset) is not None

    def to_dict_base(self) -> dict:
        return {"classe_tipo": self.__class__.__name__, "posicao": self.get_posicao().to_dict(), "velocidade": self.get_velocidade().to_dict(), "raio": self.get_raio(), "ativo": self.is_ativo()}

    def restaurar_estado_base(self, data: dict):
        self.set_ativo(data.get("ativo", True))
