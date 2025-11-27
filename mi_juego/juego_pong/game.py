# game.py
import pygame
from pygame.locals import *
import random
import os
import ranking
import config

# --------------------------------------------------------------
# RUTAS DE ARCHIVOS
# --------------------------------------------------------------

# Obtiene la carpeta base (donde está tu proyecto "mi_juego")
CARPETA_BASE = os.path.dirname(os.path.dirname(__file__))

# Carpeta donde guardás las imágenes (assets/)
CARPETA_ASSETS = os.path.join(CARPETA_BASE, "assets")

# Carpeta donde guardás los sonidos (sounds/)
CARPETA_SONIDOS = os.path.join(CARPETA_BASE, "sounds")

# --------------------------------------------------------------
# CONSTANTES
# --------------------------------------------------------------

VENTANA_HORI = 800
VENTANA_VERTI = 600
FPS = 60
COLOR = (255, 255, 255)
NEGRO = (0, 0, 0)

# --------------------------------------------------------------
# SONIDOS
# --------------------------------------------------------------

pygame.mixer.init()

# Función para cargar un sonido sin que el juego se rompa si falta un archivo
def cargar_sound(nombre):
    ruta = os.path.join(CARPETA_SONIDOS, nombre)
    try:
        s = pygame.mixer.Sound(ruta)
        # Respeta si el sonido está activado o muteado (config.py)
        s.set_volume(config.VOLUMEN if config.SONIDO_ACTIVO else 0.0)
        return s
    except Exception as e:
        print("No se pudo cargar sonido:", ruta, e)
        return None

# Cargar sonidos del juego
sonido_rebote = cargar_sound("rebote.mp3")
sonido_punto = cargar_sound("punto.mp3")
sonido_victoria = cargar_sound("victoria.mp3")
sonido_derrota = cargar_sound("derrota.mp3")


# --------------------------------------------------------------
# CLASE PELOTA
# --------------------------------------------------------------
class PelotaPong:
    def __init__(self, nombre_imagen):

        # Carga la imagen de la pelota
        ruta_imagen = os.path.join(CARPETA_ASSETS, nombre_imagen)
        original = pygame.image.load(ruta_imagen).convert_alpha()

        # Achica la pelota a 30x30
        self.imagen = pygame.transform.scale(original, (30, 30))
        self.ancho, self.alto = self.imagen.get_size()

        # Posición inicial al centro
        self.x = VENTANA_HORI / 2 - self.ancho / 2
        self.y = VENTANA_VERTI / 2 - self.alto / 2

        # Movimiento inicial random
        self.dir_x = random.choice([-5, 5])
        self.dir_y = random.choice([-5, 5])

        # Puntajes
        self.puntuacion = 0
        self.puntuacion_ia = 0

    # Mueve la pelota cada frame
    def mover(self):
        self.x += self.dir_x
        self.y += self.dir_y

    # Revisa rebotes y puntos
    def rebotar(self):

        # ⚠ CORREGIDO: ahora cuenta bien los puntos
        # Si sale por la izquierda → punto para IA
        if self.x <= 0:
            self.reiniciar()
            self.puntuacion_ia += 1
            if sonido_punto:
                sonido_punto.play()

        # Si sale por la derecha → punto para jugador
        if self.x + self.ancho >= VENTANA_HORI:
            self.reiniciar()
            self.puntuacion += 1
            if sonido_punto:
                sonido_punto.play()

        # Rebotes arriba/abajo
        if self.y <= 0 or self.y + self.alto >= VENTANA_VERTI:
            self.dir_y = -self.dir_y
            if sonido_rebote:
                sonido_rebote.play()

    # Reinicia pelota tras un punto
    def reiniciar(self):
        self.x = VENTANA_HORI / 2 - self.ancho / 2
        self.y = VENTANA_VERTI / 2 - self.alto / 2

        # Invierte la dirección para variar
        self.dir_x = -self.dir_x
        self.dir_y = random.choice([-5, 5])


# --------------------------------------------------------------
# CLASE RAQUETA
# --------------------------------------------------------------
class Raquetapong:
    def __init__(self):

        # Cargar imagen de la raqueta
        ruta_raqueta = os.path.join(CARPETA_ASSETS, "raqueta.png")
        self.imagen = pygame.image.load(ruta_raqueta).convert_alpha()

        self.ancho, self.alto = self.imagen.get_size()

        # Posición inicial a mitad de pantalla
        self.x = 0
        self.y = VENTANA_VERTI / 2 - self.alto / 2

        self.dir_y = 0

    # Mover raqueta del jugador
    def mover(self):
        self.y += self.dir_y

        # Limites de pantalla
        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= VENTANA_VERTI:
            self.y = VENTANA_VERTI - self.alto

    # Mover raqueta de la IA
    def mover_ia(self, pelota, velocidad):
        if self.y > pelota.y:
            self.dir_y = -velocidad
        elif self.y < pelota.y:
            self.dir_y = velocidad
        else:
            self.dir_y = 0

        self.y += self.dir_y

    # Detecta colisión con la pelota
    def colision(self, pelota):

        if (
            pelota.x < self.x + self.ancho
            and pelota.x + pelota.ancho > self.x
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x

            # Evita múltiples colisiones seguidas
            if pelota.x < VENTANA_HORI / 2:
                pelota.x = self.x + self.ancho
            else:
                pelota.x = self.x - pelota.ancho

            if sonido_rebote:
                sonido_rebote.play()


# --------------------------------------------------------------
# PEDIR NOMBRE AL JUGAR
# --------------------------------------------------------------
def pedir_nombre(ventana, fuente):
    nombre = ""
    activo = True
    clock = pygame.time.Clock()

    while activo:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return "Jugador"
            if ev.type == pygame.KEYDOWN:

                # ENTER confirma
                if ev.key == pygame.K_RETURN:
                    return nombre.strip() if nombre.strip() != "" else "Jugador"

                # Borrar letra
                if ev.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]

                # Carga letras tipeadas
                else:
                    if len(nombre) < 12 and ev.unicode.isprintable():
                        nombre += ev.unicode

        # Fondo
        ventana.fill((20, 20, 40))

        # Texto superior
        titulo = fuente.render("Ingresa tu nombre (ENTER):", True, (255, 255, 255))
        ventana.blit(titulo, (VENTANA_HORI // 2 - titulo.get_width() // 2, 140))

        # Caja de texto
        caja = pygame.Rect(VENTANA_HORI // 2 - 200, 260, 400, 60)
        pygame.draw.rect(ventana, (230, 230, 230), caja)

        texto = fuente.render(nombre, True, (10, 10, 10))
        ventana.blit(texto, (caja.x + 10, caja.y + 10))

        ayuda = pygame.font.Font(None, 24).render("Max 12 chars", True, (180, 180, 180))
        ventana.blit(ayuda, (VENTANA_HORI // 2 - ayuda.get_width() // 2, caja.y + 70))

        pygame.display.flip()
        clock.tick(30)


# --------------------------------------------------------------
# ANIMACIÓN FINAL (VICTORIA / GAME OVER)
# --------------------------------------------------------------
def animacion_final(ventana, texto, subtitulo=None, sonido=None):

    clock = pygame.time.Clock()
    fuente_big = pygame.font.Font(None, 120)
    fuente_small = pygame.font.Font(None, 36)

    # Reproducir sonido final
    if sonido and config.SONIDO_ACTIVO:
        try:
            sonido.play()
        except:
            pass

    # Animación: fade + zoom
    for alpha in range(0, 256, 8):
        ventana.fill((0, 0, 0))
        surf = fuente_big.render(texto, True, (255, 255, 255))
        surf.set_alpha(alpha)
        rect = surf.get_rect(center=(VENTANA_HORI // 2, VENTANA_VERTI // 2 - 30))
        ventana.blit(surf, rect)

        if subtitulo:
            sub = fuente_small.render(subtitulo, True, (200, 200, 200))
            sub.set_alpha(alpha)
            rect2 = sub.get_rect(center=(VENTANA_HORI // 2, VENTANA_VERTI // 2 + 50))
            ventana.blit(sub, rect2)

        pygame.display.flip()
        clock.tick(60)

    pygame.time.delay(800)

    # Menú final
    while True:
        ventana.fill((10, 10, 10))
        ventana.blit(surf, rect)
        if subtitulo:
            ventana.blit(sub, rect2)

        info = fuente_small.render(
            "R - Reintentar    |    ESC - Volver al menú",
            True,
            (230, 230, 230)
        )
        vent_rect = info.get_rect(center=(VENTANA_HORI // 2, VENTANA_VERTI - 80))
        ventana.blit(info, vent_rect)

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return "menu"

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    return "retry"
                if ev.key == pygame.K_ESCAPE:
                    return "menu"

        clock.tick(30)


# --------------------------------------------------------------
# LOOP PRINCIPAL DEL JUEGO
# --------------------------------------------------------------
def game_loop(dificultad):

    pygame.init()
    ventana = pygame.display.set_mode((VENTANA_HORI, VENTANA_VERTI))
    pygame.display.set_caption("Pong")

    # Cargar fondo
    ruta_fondo = os.path.join(CARPETA_ASSETS, "fondo.png")
    fondo = pygame.image.load(ruta_fondo).convert()
    fondo = pygame.transform.scale(fondo, (VENTANA_HORI, VENTANA_VERTI))

    fuente = pygame.font.Font(None, 60)

    # Pedir nombre del jugador
    nombre_jugador = pedir_nombre(ventana, fuente)

    pelota = PelotaPong("pelota.png")

    # -------- CONFIGURAR DIFICULTAD --------
    if dificultad == "Facil":
        ia_vel = 3
        velocidad_base = 4
    elif dificultad == "Normal":
        ia_vel = 5
        velocidad_base = 6
    else:
        ia_vel = 7
        velocidad_base = 7

    # Ajusta velocidad real de la pelota
    pelota.dir_x = velocidad_base if pelota.dir_x > 0 else -velocidad_base
    pelota.dir_y = velocidad_base if pelota.dir_y > 0 else -velocidad_base

    # Raqueta jugador (izquierda)
    raqueta_1 = Raquetapong()
    raqueta_1.x = 60

    # Raqueta IA (derecha)
    raqueta_2 = Raquetapong()
    raqueta_2.x = VENTANA_HORI - 60 - raqueta_2.ancho

    clock = pygame.time.Clock()

    # Loop para permitir "reintentar"
    while True:

        pelota.puntuacion = 0
        pelota.puntuacion_ia = 0
        pelota.reiniciar()

        jugando = True

        # Loop principal
        while jugando:

            # Movimiento y colisiones
            pelota.mover()
            pelota.rebotar()
            raqueta_1.mover()
            raqueta_2.mover_ia(pelota, ia_vel)
            raqueta_1.colision(pelota)
            raqueta_2.colision(pelota)

            # Dibujar elementos
            ventana.blit(fondo, (0, 0))
            ventana.blit(pelota.imagen, (pelota.x, pelota.y))
            ventana.blit(raqueta_1.imagen, (raqueta_1.x, raqueta_1.y))
            ventana.blit(raqueta_2.imagen, (raqueta_2.x, raqueta_2.y))

            # Puntaje
            izq = fuente.render(str(pelota.puntuacion), True, NEGRO)
            der = fuente.render(str(pelota.puntuacion_ia), True, NEGRO)
            sep = fuente.render(":", True, NEGRO)

            xc = VENTANA_HORI // 2
            ventana.blit(izq, (xc - 50, 40))
            ventana.blit(sep, (xc - 12, 40))
            ventana.blit(der, (xc + 30, 40))

            # ---------------- GANAR O PERDER ----------------

            if pelota.puntuacion >= 7:
                ranking.guardar_score(nombre_jugador, pelota.puntuacion)
                accion = animacion_final(
                    ventana,
                    "VICTORIA",
                    f"{nombre_jugador} {pelota.puntuacion} pts",
                    sonido_victoria
                )
                if accion == "retry":
                    break
                else:
                    return  # Volver al menú

            if pelota.puntuacion_ia >= 7:
                ranking.guardar_score("IA", pelota.puntuacion_ia)
                accion = animacion_final(
                    ventana,
                    "GAME OVER",
                    f"IA {pelota.puntuacion_ia} pts",
                    sonido_derrota
                )
                if accion == "retry":
                    break
                else:
                    return

            # ---------------- EVENTOS ----------------
            for event in pygame.event.get():

                if event.type == QUIT:
                    return

                if event.type == pygame.KEYDOWN:

                    # Tecla M → silenciar
                    if event.key == pygame.K_m:
                        config.SONIDO_ACTIVO = not config.SONIDO_ACTIVO
                        vol = config.VOLUMEN if config.SONIDO_ACTIVO else 0.0

                        # Modificar volumen de todos los sonidos cargados
                        for s in (sonido_rebote, sonido_punto, sonido_victoria, sonido_derrota):
                            if s:
                                try:
                                    s.set_volume(vol)
                                except:
                                    pass

                    # ESC → volver al menú
                    if event.key == pygame.K_ESCAPE:
                        return

                    # Movimiento jugador
                    if event.key == pygame.K_w:
                        raqueta_1.dir_y = -5
                    if event.key == pygame.K_s:
                        raqueta_1.dir_y = 5

                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_w, pygame.K_s):
                        raqueta_1.dir_y = 0

            pygame.display.flip()
            clock.tick(FPS)


def jugar(dificultad):
    game_loop(dificultad)
