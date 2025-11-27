# main.py
# ------------------------------------------
# Este archivo es el punto de entrada del juego.
# Es decir, cuando ejecutás "python main.py", lo primero
# que se corre es este archivo.
# ------------------------------------------

# Importamos el archivo "menu.py"
# Esto nos permite usar su función principal: main_menu()
import menu

# Esta condición se ejecuta SOLO cuando este archivo
# es ejecutado directamente desde la terminal.
# Si algún otro archivo importara main.py,
# este bloque NO se ejecutaría.
#
# Sirve para evitar que el juego se abra automáticamente
# cuando se hagan importaciones internas en Python.
if __name__ == "__main__":
    
    # Llamamos a la función principal del menú.
    # Esto inicia la pantalla del menú de inicio del juego.
    menu.main_menu()
