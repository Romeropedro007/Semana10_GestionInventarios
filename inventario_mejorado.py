import os

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = round(precio, 2)  # Asegurar que el precio siempre tenga dos decimales

    def get_id(self):
        return self.id_producto

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    def set_cantidad(self, nueva_cantidad):
        self.cantidad = nueva_cantidad

    def set_precio(self, nuevo_precio):
        self.precio = round(nuevo_precio, 2)  # Aplicar redondeo también al actualizar

    def __str__(self):
        return f"ID: {self.id_producto} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"


class Inventario:
    def __init__(self, archivo='inventario.txt'):
        """
        Inicializa el inventario y carga los productos desde el archivo especificado.
        """
        self.archivo = archivo
        self.productos = {}
        self.cargar_inventario()

    def cargar_inventario(self):
        """
        Carga los productos desde el archivo de texto (self.archivo).
        Si el archivo no existe, se crea vacío.
        Maneja excepciones de permisos y formato.
        """
        if not os.path.exists(self.archivo):
            # Crear el archivo si no existe
            try:
                with open(self.archivo, 'w') as f:
                    pass
                print(f"[INFO] El archivo '{self.archivo}' no existía. Se ha creado uno nuevo.")
            except PermissionError:
                print(f"[ERROR] No tienes permiso para crear el archivo '{self.archivo}'.")
                return

        try:
            with open(self.archivo, 'r') as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue  # Saltar líneas vacías
                    partes = linea.split(';')
                    # Se asume formato: ID;NOMBRE;CANTIDAD;PRECIO
                    if len(partes) == 4:
                        id_prod, nombre, cant_str, precio_str = partes
                        try:
                            cantidad = int(cant_str)
                            precio = float(precio_str)
                            # Crear el objeto Producto y guardarlo en el diccionario
                            producto = Producto(id_prod, nombre, cantidad, precio)
                            self.productos[id_prod] = producto
                        except ValueError:
                            print(f"[ERROR] Error de formato en la línea: '{linea}'. Se ignora.")
                    else:
                        print(f"[ERROR] Formato inválido en la línea: '{linea}'. Se ignora.")
        except FileNotFoundError:
            print(f"[ERROR] El archivo '{self.archivo}' no existe.")
        except PermissionError:
            print(f"[ERROR] No tienes permiso para leer el archivo '{self.archivo}'.")

    def guardar_inventario(self):
        """
        Sobrescribe el archivo con los datos actuales del inventario.
        Maneja excepciones de permisos u otros errores de escritura.
        """
        try:
            with open(self.archivo, 'w') as f:
                for p in self.productos.values():
                    f.write(f"{p.get_id()};{p.get_nombre()};{p.get_cantidad()};{p.get_precio()}\n")
            # Notifica en consola que se guardó
            print("[INFO] Inventario guardado exitosamente.")
        except PermissionError:
            print(f"[ERROR] No tienes permisos para escribir en el archivo '{self.archivo}'.")
        except Exception as e:
            print(f"[ERROR] Ocurrió un error al guardar el inventario: {e}")

    def agregar_producto(self, producto):
        """
        Agrega un nuevo producto al inventario y actualiza el archivo.
        Retorna un mensaje de éxito o error.
        """
        if producto.get_id() in self.productos:
            return "[ERROR] El ID ya existe."
        self.productos[producto.get_id()] = producto
        self.guardar_inventario()
        return "[OK] Producto agregado correctamente."

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto por ID y actualiza el archivo.
        Retorna un mensaje de éxito o error.
        """
        if id_producto in self.productos:
            del self.productos[id_producto]
            self.guardar_inventario()
            return "[OK] Producto eliminado correctamente."
        return "[ERROR] El producto no existe."

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        """
        Actualiza la cantidad y/o precio de un producto existente.
        Si alguno de los campos es None, no se modifica.
        Retorna un mensaje de éxito o error.
        """
        if id_producto not in self.productos:
            return "[ERROR] Producto no encontrado."

        producto = self.productos[id_producto]
        if cantidad is not None:
            producto.set_cantidad(cantidad)
        if precio is not None:
            producto.set_precio(precio)

        self.guardar_inventario()
        return "[OK] Producto actualizado correctamente."

    def buscar_por_nombre(self, nombre):
        """
        Retorna una lista de productos cuyo nombre contenga la cadena buscada (ignorando mayúsculas/minúsculas).
        """
        return [p for p in self.productos.values() if nombre.lower() in p.get_nombre().lower()]

    def mostrar_productos(self):
        """
        Retorna un string con la representación de todos los productos o un mensaje si está vacío.
        """
        if not self.productos:
            return "[INFO] El inventario está vacío."
        return "\n".join(str(p) for p in self.productos.values())


if __name__ == "__main__":
    inventario = Inventario()

    while True:
        print("\n--- Sistema de Gestión de Inventarios ---")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id_producto = input("ID del producto: ")
            nombre = input("Nombre del producto: ")
            try:
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                mensaje = inventario.agregar_producto(Producto(id_producto, nombre, cantidad, precio))
                print(mensaje)
            except ValueError:
                print("[ERROR] Ingrese valores numéricos válidos para cantidad y precio.")

        elif opcion == "2":
            id_producto = input("ID del producto a eliminar: ")
            print(inventario.eliminar_producto(id_producto))

        elif opcion == "3":
            id_producto = input("ID del producto a actualizar: ")
            cant_input = input("Nueva cantidad (dejar en blanco para no cambiar): ")
            prec_input = input("Nuevo precio (dejar en blanco para no cambiar): ")

            # Validar la entrada y convertir a int/float si corresponde
            cantidad = None
            precio = None
            if cant_input.strip():
                if cant_input.isdigit():
                    cantidad = int(cant_input)
                else:
                    print("[ERROR] La cantidad debe ser un número entero.")
                    continue

            if prec_input.strip():
                try:
                    precio = float(prec_input)
                except ValueError:
                    print("[ERROR] El precio debe ser un número decimal.")
                    continue

            print(inventario.actualizar_producto(id_producto, cantidad, precio))

        elif opcion == "4":
            nombre_buscar = input("Nombre del producto a buscar: ")
            productos_encontrados = inventario.buscar_por_nombre(nombre_buscar)
            if productos_encontrados:
                for p in productos_encontrados:
                    print(p)
            else:
                print("[INFO] No se encontraron productos con ese nombre.")

        elif opcion == "5":
            print(inventario.mostrar_productos())

        elif opcion == "6":
            print("[INFO] Saliendo del sistema.")
            break

        else:
            print("[ERROR] Opción no válida. Intente de nuevo.")
