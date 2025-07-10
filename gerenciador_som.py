import pygame
from typing import Optional

from config import *

class GerenciadorSom:
    def __init__(self):
        self.__volume_musica = VOLUME_MUSICA_PADRAO
        self.__volume_sfx = VOLUME_SFX_PADRAO
        try:
            self.__som_tiro = pygame.mixer.Sound(SOM_TIRO)
            self.__som_explosao_asteroide = pygame.mixer.Sound(SOM_EXPLOSAO_ASTEROIDE)
            self.__som_explosao_nave = pygame.mixer.Sound(SOM_EXPLOSAO_NAVE)
            self.__som_ovni_movendo = pygame.mixer.Sound(SOM_OVNI_MOVENDO)
            self.__som_ovni_tiro = pygame.mixer.Sound(SOM_OVNI_TIRO)
            self.__som_fantasma_invisivel = pygame.mixer.Sound(SOM_FANTASMA_INVISIVEL)
            self.atualizar_volumes_sfx()
            print("Efeitos sonoros carregados.")
        except pygame.error as e:
            print(f"AVISO: Não foi possível carregar um ou mais arquivos de som: {e}")
            dummy_sound = type('DummySound', (), {'play': lambda s, *a, **kw: None, 'stop': lambda s: None, 'set_volume': lambda s, v: None})()
            self.__som_tiro, self.__som_explosao_asteroide, self.__som_explosao_nave, self.__som_ovni_movendo, self.__som_ovni_tiro, self.__som_fantasma_invisivel = (dummy_sound,) * 6

    def get_volume_musica(self) -> float:
        return self.__volume_musica

    def get_volume_sfx(self) -> float:
        return self.__volume_sfx

    def tocar_musica_fundo(self, tipo_musica: str = 'menu'):
        pygame.mixer.music.stop()
        try:
            arquivo_musica = MUSICA_FUNDO_MENU if tipo_musica == 'menu' else MUSICA_FUNDO_JOGO
            pygame.mixer.music.load(arquivo_musica)
            pygame.mixer.music.set_volume(self.__volume_musica)
            pygame.mixer.music.play(-1)  # -1 para loop infinito
        except pygame.error as e:
            print(f"AVISO: Não foi possível tocar a música '{tipo_musica}': {e}")

    def parar_musica(self):
        pygame.mixer.music.stop()

    def tocar_som(self, nome_som: str, loop=0):
        if nome_som == 'tiro': self.__som_tiro.play()
        elif nome_som == 'explosao_asteroide': self.__som_explosao_asteroide.play()
        elif nome_som == 'explosao_nave': self.__som_explosao_nave.play()
        elif nome_som == 'ovni_tiro': self.__som_ovni_tiro.play()
        elif nome_som == 'ovni_movendo': self.__som_ovni_movendo.play(loops=loop)
        elif nome_som == 'fantasma_invisivel': self.__som_fantasma_invisivel.play(loops=loop)

    def parar_som(self, nome_som: str):
        if nome_som == 'ovni_movendo': self.__som_ovni_movendo.stop()
        elif nome_som == 'fantasma_invisivel': self.__som_fantasma_invisivel.stop()

    def set_volume_musica(self, volume, *args):
        novo_volume = float(volume) / 100.0
        self.__volume_musica = max(0.0, min(1.0, novo_volume))
        pygame.mixer.music.set_volume(self.__volume_musica)

    def set_volume_sfx(self, volume, *args):
        novo_volume = float(volume) / 100.0
        self.__volume_sfx = max(0.0, min(1.0, novo_volume))
        self.atualizar_volumes_sfx()

    def atualizar_volumes_sfx(self):
        self.__som_tiro.set_volume(self.__volume_sfx)
        self.__som_explosao_asteroide.set_volume(self.__volume_sfx)
        self.__som_explosao_nave.set_volume(self.__volume_sfx)
        self.__som_ovni_movendo.set_volume(self.__volume_sfx * 0.3)
        self.__som_ovni_tiro.set_volume(self.__volume_sfx)
        self.__som_fantasma_invisivel.set_volume(self.__volume_sfx * 0.6)

