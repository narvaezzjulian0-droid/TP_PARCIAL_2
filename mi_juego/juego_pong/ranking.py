import os

# ---------------------------------------------
#  ARCHIVO: ranking.py
#  FUNCIÓN: Guardar y cargar puntajes del juego
# ---------------------------------------------

# Obtenemos la ruta base del proyecto.
# __file__ apunta al archivo actual (ranking.py)
# dirname(dirname(__file__)) sube dos carpetas:
#   /mi_juego/juego_pong   → sube a /mi_juego
CARPETA_BASE = os.path.dirname(os.path.dirname(__file__))

# Archivo donde se guardará el ranking.
# Se creará automáticamente si no existe.
RUTA_RANKING = os.path.join(CARPETA_BASE, "ranking.txt")


def guardar_score(nombre, puntaje):
    """
    Guarda un puntaje en el archivo ranking.txt.

    Formato de guardado:
        nombre:puntos

    Ejemplo:
        Julián:7
        IA:3

    Se usa modo "a" para agregar líneas sin borrar las anteriores.
    """

    linea = f"{nombre}:{puntaje}\n"

    # Abrimos en modo append (agregar al final)
    with open(RUTA_RANKING, "a", encoding="utf-8") as f:
        f.write(linea)



def cargar_ranking():
    """
    Carga todas las puntuaciones del archivo ranking.txt.

    Retorna una lista de tuplas:
        [(nombre, puntaje), (nombre, puntaje), ...]

    También ordena los puntajes de mayor a menor para mostrar ranking real.
    """

    # Si nunca se jugó y el archivo no existe → ranking vacío
    if not os.path.exists(RUTA_RANKING):
        return []

    ranking = []

    # Abrimos para leer línea por línea
    with open(RUTA_RANKING, "r", encoding="utf-8") as f:
        for linea in f:

            # Validamos que el formato sea correcto "nombre:puntos"
            if ":" in linea:
                nombre, pts = linea.strip().split(":")

                try:
                    # Convertimos el puntaje a entero
                    ranking.append((nombre, int(pts)))
                except:
                    # Si falla (por datos corruptos) simplemente se ignora esa línea
                    pass

    # Ordenamos la lista: el mejor puntaje primero
    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking


