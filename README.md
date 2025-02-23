Sistema de Gestión de Inventarios Mejorado
Descripción:
Este repositorio contiene un proyecto en Python que implementa un sistema de gestión de inventarios mejorado. La aplicación permite gestionar productos (añadir, actualizar, eliminar y consultar) a través de una interfaz de línea de comandos y utiliza un archivo de texto (inventario.txt) para almacenar de manera persistente la información del inventario. Además, incorpora manejo de excepciones para garantizar la robustez del sistema durante las operaciones de lectura y escritura en archivos.

Características Principales:

Almacenamiento en Archivos:
Cada modificación en el inventario (creación, actualización o eliminación de productos) se refleja automáticamente en el archivo inventario.txt, garantizando que los datos se conserven entre ejecuciones.

Recuperación Automática:
Al iniciar el programa, se carga la información almacenada en inventario.txt para reconstruir el inventario, permitiendo continuar la gestión de productos sin pérdida de información.

Manejo de Excepciones:
El sistema implementa bloques try/except para capturar y manejar errores comunes como FileNotFoundError y PermissionError, entre otros, mejorando la estabilidad y la experiencia del usuario.

Interfaz de Usuario en Consola:
Un menú interactivo guía al usuario en la realización de operaciones sobre el inventario, notificando el éxito o fallo de cada acción.