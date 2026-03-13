import pygame
import os

class SoundManager:
    def __init__(self):
        # 1. Inicializar siempre en dummy (instantáneo)
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        pygame.mixer.init()
        print("Audio dummy inicializado.")

        # Cargar sonidos (funcionan igual en dummy)
        self.snd_miss = pygame.mixer.Sound("assets/sounds/miss.wav")
        self.snd_hit  = pygame.mixer.Sound("assets/sounds/hit.wav")
        self.snd_sunk = pygame.mixer.Sound("assets/sounds/sunk.wav")

        # 2. Intentar activar audio real SIN bloquear
        try:
            pygame.mixer.quit()
            del os.environ["SDL_AUDIODRIVER"]
            pygame.mixer.init()
            print("Audio real inicializado correctamente.")
        except pygame.error:
            pygame.mixer.quit()
            os.environ["SDL_AUDIODRIVER"] = "dummy"
            pygame.mixer.init()
            print("Audio dummy inicializado.")
            print("No hay audio real. Continuando con dummy.")

    def play_miss(self):
        self.snd_miss.play()

    def play_hit(self):
        self.snd_hit.play()

    def play_sunk(self):
        self.snd_sunk.play()



class ImageManager:
    #pasamos el tamaño de celda como parámetro para evitar un "import circular" y el errror de carga
    def __init__(self,cell_size):
        # Cargar las imágenes con atributos privados para evitar acceso directo desde fuera de la clase
        
        self._img_miss = pygame.image.load("assets/images/miss.png").convert_alpha()
        self._img_hit  = pygame.image.load("assets/images/hit.png").convert_alpha()
        self._img_sunk = pygame.image.load("assets/images/sunk.png").convert_alpha()


        # Escalar las imágenes al tamaño de la celda de tu tablero (50x50)
        tamano = (cell_size, cell_size)

        self._img_miss = pygame.transform.scale(self._img_miss, tamano)
        self._img_hit  = pygame.transform.scale(self._img_hit, tamano)
        self._img_sunk = pygame.transform.scale(self._img_sunk, tamano)

    '''   
    los métodos getter rompen la encapsulación y no aportan valor real, ya que las imágenes 
    son atributos públicos y pueden ser accedidos directamente. 
    En lugar de eso, es mejor proporcionar métodos de acción que utilicen estas imágenes 
    para dibujarlas en la pantalla, manteniendo así una interfaz más limpia y orientada a la funcionalidad.
    

     def get_miss(self):
        return self.img_miss

    def get_hit(self):
        return self.img_hit

    def get_sunk(self):
        return self.
    '''    

    # Creamos métodos de ACCIÓN (Comportamiento)
    def draw_miss(self, surface, x, y):
        surface.blit(self._img_miss, (x, y))

    def draw_hit(self, surface, x, y):
        surface.blit(self._img_hit, (x, y))

    def draw_sunk(self, surface, x, y):
        surface.blit(self._img_sunk, (x, y))