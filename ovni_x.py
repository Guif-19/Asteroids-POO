from typing import Optional, List
import pygame

from config import *
from vetor import Vetor2D
from ovni import OVNI
from ovni_projetil import OVNIProjetil 

class OvniX(OVNI):
    def __init__(self, posicao: Optional[Vetor2D] = None, velocidade: Optional[Vetor2D] = None):
        super().__init__(IMAGEM_OVNI_X, posicao, velocidade)

    def tentar_atirar(self, posicao_nave: Vetor2D) -> list[OVNIProjetil]:
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self._OVNI__ultimo_tiro_tempo_ms > COOLDOWN_TIRO_OVNI_MS:
            self._OVNI__ultimo_tiro_tempo_ms = tempo_atual
            projeteis = []
            direcoes = [Vetor2D(1, 1).normalizar(), Vetor2D(-1, 1).normalizar(), Vetor2D(1, -1).normalizar(), Vetor2D(-1, -1).normalizar()]
            for direcao in direcoes:
                projeteis.append(OVNIProjetil(self.get_posicao() + direcao * self.get_raio(), direcao * VELOCIDADE_PROJETIL_OVNI, IMAGEM_PROJETIL_OVNI_X))
            return projeteis
        return []
