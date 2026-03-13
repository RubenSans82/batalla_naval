import pygame
import os

class SoundManager:
    def __init__(self):
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        pygame.mixer.init()
        print("Audio dummy inicializado (instantáneo).")
        
        # 2. Intentar activar audio real SIN bloquear
        try:
            # Intento de re-inicializar con audio real
            # Quitamos el dummy y probamos
            del os.environ["SDL_AUDIODRIVER"]
            pygame.mixer.quit()
            pygame.mixer.init()
            print("Audio real inicializado correctamente.")

        except pygame.error:
            # Si falla, volvemos al dummy sin demoras
            os.environ["SDL_AUDIODRIVER"] = "dummy"
            pygame.mixer.quit()
            pygame.mixer.init()
            print("No hay audio real. Continuando con dummy sin demoras.")

        self.snd_miss = pygame.mixer.Sound("assets/sounds/miss.wav")
        self.snd_hit  = pygame.mixer.Sound("assets/sounds/hit.wav")
        self.snd_sunk = pygame.mixer.Sound("assets/sounds/sunk.wav")

    def play_miss(self):
        pygame.time.delay(300)
        self.snd_miss.play()

    def play_hit(self):
        pygame.time.delay(300)
        self.snd_hit.play()

    def play_sunk(self):
        pygame.time.delay(300)
        self.snd_sunk.play()