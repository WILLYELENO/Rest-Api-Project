"""
blocklist.py

Este archivo solo contiene la lista de bloqueo de los tokens JWT. Será importado por
aplicación y el recurso de cierre de sesión para que los tokens se puedan agregar a la lista de bloqueo cuando el
el usuario cierra la sesión.

Esto es solo de prueba, lo ideal sería almacenar estos tokens en la base de datos porque
cuando reiniciemos la aplicacion, se perderan los tokens alamacenados, ya que no deja de ser
una lista.

"""

BLOCKLIST = set()
