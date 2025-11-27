# config.py
# -----------------------------------------------
# Este archivo funciona como un módulo de configuración global.
# Guarda variables simples que son usadas por distintos archivos,
# como `menu.py` y `game.py`, sin generar problemas de importación circular.
# -----------------------------------------------

# SONIDO_ACTIVO:
# Esta variable indica si el sonido del juego está encendido o apagado.
# Se modifica desde el menú (tecla M o menú de opciones).
# - True  → el sonido está activado.
# - False → el sonido está silenciado.
SONIDO_ACTIVO = True


# VOLUMEN:
# Controla el volumen general del juego.
# Es un valor entre 0.0 y 1.0:
# - 1.0  → volumen máximo
# - 0.0  → silencio total
# El menú y el juego usan esta variable para ajustar el volumen
# al cambiar el audio o silenciarlo.
VOLUMEN = 1.0  # rango permitido: 0.0 a 1.0
