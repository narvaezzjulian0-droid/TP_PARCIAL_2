# --------------------------------------------------------------
# menu.py — Menú principal del juego PONG
# Contiene:
#  - Música del menú
#  - Opciones
#  - Selector de dificultad
#  - Ranking
#  - Créditos
#  - Navegación hacia el juego
# --------------------------------------------------------------

import pygame
import sys
import game
import os
import ranking
import config

# Carpeta base: obtiene la carpeta raíz del proyecto (mi_juego)
CARPETA_BASE = os.path.dirname(os.path.dirname(__file__))

# Carpeta donde se guardan los sonidos
CARPETA_SONIDOS = os.path.join(CARPETA_BASE, "sounds")

pygame.init()
pygame.mixer.init()

# --------------------------------------------------------------
# Función para cargar sonidos del menú
# Retorna un objeto pygame.mixer.Sound si existe
# Caso contrario no rompe el juego, devuelve None
# --------------------------------------------------------------
def cargar_sound(nombre):
    ruta = os.path.join(CARPETA_SONIDOS, nombre)
    try:
        s = pygame.mixer.Sound(ruta)
        # Aplica el volumen global (ON/OFF)
        s.set_volume(config.VOLUMEN if config.SONIDO_ACTIVO else 0.0)
        return s
    except Exception as e:
        print("No se pudo cargar sonido de menú:", ruta, e)
        return None

# Carga y reproduce la música del menú (en loop infinito)
sonido_menu = cargar_sound("menu.mp3")
if sonido_menu:
    sonido_menu.play(-1)

# Tamaño de la ventana del menú
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menu Principal - Pong")

# Colores usados
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Fuentes principales del menú
fuente = pygame.font.Font(None, 60)
fuente_peque = pygame.font.Font(None, 40)

# Dificultad por defecto
DIFICULTAD = "Normal"

# --------------------------------------------------------------
# Dibuja un texto centrado automáticamente en x,y
# --------------------------------------------------------------
def dibujar_texto(texto, fuente, color, x, y):
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(x, y))
    pantalla.blit(render, rect)

# --------------------------------------------------------------
# Muestra el ranking guardado en el archivo ranking.txt
# Se puede volver con ESC
# --------------------------------------------------------------
def mostrar_ranking():
    while True:
        pantalla.fill((5, 5, 5))

        dibujar_texto("RANKING", fuente, BLANCO, ANCHO // 2, 80)

        # Carga lista de [(nombre, puntos)]
        datos = ranking.cargar_ranking()

        if len(datos) == 0:
            dibujar_texto("No hay puntuaciones guardadas", fuente_peque, BLANCO, ANCHO // 2, 300)
        else:
            y = 180
            # Muestra solo los mejores 10
            for nombre, puntos in datos[:10]:
                dibujar_texto(f"{nombre} - {puntos}", fuente_peque, BLANCO, ANCHO // 2, y)
                y += 45

        dibujar_texto("ESC para volver", fuente_peque, BLANCO, ANCHO // 2, 550)

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return  # vuelve al menú

        pygame.display.flip()

# --------------------------------------------------------------
# Submenú de opciones
# Permite:
#  1) Activar/Desactivar sonido
#  2) Cambiar dificultad
#  3) Volver
# --------------------------------------------------------------
def menu_opciones():
    while True:
        pantalla.fill((20, 20, 20))

        dibujar_texto("OPCIONES", fuente, BLANCO, ANCHO // 2, 100)
        dibujar_texto("1 - Sonido ON/OFF (M)", fuente_peque, BLANCO, ANCHO // 2, 250)
        dibujar_texto("2 - Selector de dificultad", fuente_peque, BLANCO, ANCHO // 2, 320)
        dibujar_texto("3 - Volver", fuente_peque, BLANCO, ANCHO // 2, 390)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                # Alternar sonido
                if evento.key == pygame.K_1:
                    config.SONIDO_ACTIVO = not config.SONIDO_ACTIVO
                    vol = config.VOLUMEN if config.SONIDO_ACTIVO else 0.0
                    if sonido_menu:
                        sonido_menu.set_volume(vol)

                # Abrir menú de dificultad
                if evento.key == pygame.K_2:
                    menu_dificultad()

                # Volver
                if evento.key == pygame.K_3:
                    return

        pygame.display.flip()

# --------------------------------------------------------------
# Selector de dificultad
# Cambia la variable global DIFICULTAD
# --------------------------------------------------------------
def menu_dificultad():
    global DIFICULTAD

    while True:
        pantalla.fill((15, 15, 15))

        dibujar_texto("DIFICULTAD", fuente, BLANCO, ANCHO // 2, 100)
        dibujar_texto("1 - Fácil", fuente_peque, BLANCO, ANCHO // 2, 240)
        dibujar_texto("2 - Normal", fuente_peque, BLANCO, ANCHO // 2, 310)
        dibujar_texto("3 - Difícil", fuente_peque, BLANCO, ANCHO // 2, 380)
        dibujar_texto("4 - Volver", fuente_peque, BLANCO, ANCHO // 2, 450)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                # Cambia dificultad global
                if evento.key == pygame.K_1:
                    DIFICULTAD = "Facil"
                    return
                if evento.key == pygame.K_2:
                    DIFICULTAD = "Normal"
                    return
                if evento.key == pygame.K_3:
                    DIFICULTAD = "Dificil"
                    return
                if evento.key == pygame.K_4:
                    return  # volver sin cambiar

        pygame.display.flip()

# --------------------------------------------------------------
# Menú principal del juego
# Contiene todas las opciones principales
# --------------------------------------------------------------
def main_menu():
    while True:
        pantalla.fill(NEGRO)

        # Títulos y opciones
        dibujar_texto("PONG", fuente, BLANCO, ANCHO // 2, 120)
        dibujar_texto("1 - Jugar", fuente_peque, BLANCO, ANCHO // 2, 250)
        dibujar_texto("2 - Opciones", fuente_peque, BLANCO, ANCHO // 2, 320)
        dibujar_texto("3 - Score guardado / Ranking", fuente_peque, BLANCO, ANCHO // 2, 390)
        dibujar_texto("4 - Créditos", fuente_peque, BLANCO, ANCHO // 2, 460)
        dibujar_texto("5 - Salir", fuente_peque, BLANCO, ANCHO // 2, 530)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                # 1 - Iniciar juego
                if evento.key == pygame.K_1:
                    # Detiene música del menú antes de entrar al juego
                    if sonido_menu:
                        sonido_menu.stop()

                    # Ejecuta el juego usando la dificultad actual
                    game.jugar(DIFICULTAD)

                    # Al volver del juego, si el sonido está activo, reproduce música del menú de nuevo
                    if sonido_menu and config.SONIDO_ACTIVO:
                        sonido_menu.play(-1)

                # 2 - Opciones
                if evento.key == pygame.K_2:
                    menu_opciones()

                # 3 - Ranking
                if evento.key == pygame.K_3:
                    mostrar_ranking()

                # 4 - Créditos
                if evento.key == pygame.K_4:
                    mostrar_creditos()

                # 5 - Salir del juego
                if evento.key == pygame.K_5:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# --------------------------------------------------------------
# Pantalla de créditos
# --------------------------------------------------------------
def mostrar_creditos():
    while True:
        pantalla.fill((10, 10, 10))

        dibujar_texto("CRÉDITOS", fuente, BLANCO, ANCHO // 2, 100)
        dibujar_texto("Juego creado por Julián", fuente_peque, BLANCO, ANCHO // 2, 260)
        dibujar_texto("ESC para volver", fuente_peque, BLANCO, ANCHO // 2, 400)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return  # vuelve al menú principal

        pygame.display.flip()
