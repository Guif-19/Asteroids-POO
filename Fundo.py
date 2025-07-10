import pygame
import random

from config import *

class FundoEstrelado:
    def __init__(self):
        self.__estrelas_lentas = [[random.randrange(LARGURA_TELA), random.randrange(ALTURA_TELA), 1] for _ in range(NUM_ESTRELAS_LENTAS)]
        self.__estrelas_rapidas = [[random.randrange(LARGURA_TELA), random.randrange(ALTURA_TELA), 2] for _ in range(NUM_ESTRELAS_RAPIDAS)]

    def atualizar(self, delta_tempo: float):
        for estrela in self.__estrelas_lentas: estrela[1] = (estrela[1] + VELOCIDADE_ESTRELAS_LENTA * delta_tempo * FPS) % ALTURA_TELA
        for estrela in self.__estrelas_rapidas: estrela[1] = (estrela[1] + VELOCIDADE_ESTRELAS_RAPIDA * delta_tempo * FPS) % ALTURA_TELA

    def desenhar(self, tela: pygame.Surface):
        for x, y, tamanho in self.__estrelas_lentas: pygame.draw.circle(tela, (150, 150, 150), (int(x), int(y)), max(1, tamanho // 2))
        for x, y, tamanho in self.__estrelas_rapidas: pygame.draw.circle(tela, COR_ESTRELA, (int(x), int(y)), tamanho)
