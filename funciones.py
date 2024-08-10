def gestionCertificado(conexion):
    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Certificados ---")
        print("1. Añadir nuevo Certificado")
        print("2. Consultar Certificados")
        print("3. Editar Certificado")
        print("4. Eliminar Certificado")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir nuevo certificado
            descripcion = input("Ingrese la descripción del certificado: ")
            fecha_vigencia = input("Ingrese la fecha de vigencia (YYYY-MM-DD): ")
            nombre = input("Ingrese el nombre del certificado: ")
            id_empleado = input("Ingrese el ID del empleado: ")

            query = """
            INSERT INTO certificado (descripcion, fecha_vigencia, nombre, ID_Empleado)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (descripcion, fecha_vigencia, nombre, id_empleado))
            conexion.commit()
            print("Certificado añadido exitosamente.")

        elif opcion == '2':
            # Consultar certificados
            query = "SELECT * FROM certificado"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Certificados ---")
                for fila in resultados:
                    id_certificado = fila[0]
                    descripcion = fila[1]
                    fecha_vigencia = fila[2]
                    nombre = fila[3]
                    id_empleado = fila[4]
                    print(f"ID: {id_certificado} | Descripción: {descripcion} | Fecha de Vigencia: {fecha_vigencia} | Nombre: {nombre} | ID Empleado: {id_empleado}")
            else:
                print("No se encontraron certificados.")

        elif opcion == '3':
            # Editar certificado
            id_certificado = input("Ingrese el ID del certificado que desea editar: ")
            nueva_descripcion = input("Ingrese la nueva descripción: ")
            query = "UPDATE certificado SET descripcion = %s WHERE ID_Certificado = %s"
            cursor.execute(query, (nueva_descripcion, id_certificado))
            conexion.commit()
            print("Certificado actualizado exitosamente.")

        elif opcion == '4':
            # Eliminar certificado
            id_certificado = input("Ingrese el ID del certificado que desea eliminar: ")
            query = "DELETE FROM certificado WHERE ID_Certificado = %s"
            cursor.execute(query, (id_certificado,))
            conexion.commit()
            print("Certificado eliminado exitosamente.")

        elif opcion == '5':
            # Salir
            print("Saliendo del sistema de gestión de certificados...")
            break
        else:
            print("Opción inválida...")

    cursor.close()

def gestionproyecto(conexion):
    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Proyectos ---")
        print("1. Añadir nuevo Proyecto")
        print("2. Consultar proyectos")
        print("3. Editar proyecto")
        print("4. Eliminar proyecto")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir un nuevo proyecto
            nombre = input("Ingrese el nombre del proyecto: ")
            fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
            fecha_fin = input("Ingrese la fecha de finalización (YYYY-MM-DD): ")
            
            query = """
            INSERT INTO proyecto (nombre, fecha_inicio, fecha_fin)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (nombre, fecha_inicio, fecha_fin))
            conexion.commit()
            input("Proyecto añadido exitosamente.")
        
        elif opcion == '2':
            # Mostrar los proyectos
            query = "SELECT * FROM proyecto"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Proyectos Creados ---")
                for fila in resultados:
                    id_proyecto = fila[0]
                    nombre = fila[1]
                    fecha_inicio = fila[2].strftime("%Y-%m-%d")
                    fecha_fin = fila[3].strftime("%Y-%m-%d")
                    
                    print(f"ID: {id_proyecto} | Nombre: {nombre} "
                          f"Fecha de Inicio: {fecha_inicio} | Fecha de Fin: {fecha_fin}\n")
                input("Consulta realizada correctamente...")
            else:
                print("No se encontraron proyectos.")
        
        elif opcion == '3':
            id_proyecto = input("Ingrese el ID del proyecto que desea editar: ")
            print("Seleccione el campo que desea editar:")
            print("1. Nombre del Proyecto")
            print("2. Fecha de Inicio")
            print("3. Fecha de Fin")
            campo = input("Opción: ")

            if campo == '1':
                nuevo_valor = input("Ingrese el nuevo nombre del proyecto: ")
                query = "UPDATE proyecto SET nombre = %s WHERE ID_Proyecto = %s"
            elif campo == '2':
                nuevo_valor = input("Ingrese la nueva fecha de inicio (YYYY-MM-DD): ")
                query = "UPDATE proyecto SET fecha_inicio = %s WHERE ID_Proyecto = %s"
            elif campo == '3':
                nuevo_valor = input("Ingrese la nueva fecha de fin (YYYY-MM-DD): ")
                query = "UPDATE proyecto SET fecha_fin = %s WHERE ID_Proyecto = %s"
            else:
                print("Opción incorrecta...")
                continue

            cursor.execute(query, (nuevo_valor, id_proyecto))
            conexion.commit()
            input("Proyecto actualizado exitosamente...")
        
        elif opcion == '4':
            # Eliminar el proyecto 
            id_proyecto = input("Ingrese el ID del proyecto que desea eliminar: ")
            query = "DELETE FROM proyecto WHERE ID_Proyecto = %s"
            cursor.execute(query, (id_proyecto,))
            conexion.commit()
            input("El proyecto se ha eliminado exitosamente...")
        
        elif opcion == '5':
            # Salir
            input("Saliendo del sistema de gestión de proyectos...")
            break
        else: 
            print("Opción inválida...")
    
    cursor.close()

def gestionempleados(conexion):
    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Empleados ---")
        print("1. Añadir nuevo empleado")
        print("2. Consultar empleados")
        print("3. Editar empleado")
        print("4. Eliminar empleado")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir nuevo empleado
            nombre = input("Ingrese el nombre del empleado: ")
            cargo = input("Ingrese el cargo del empleado: ")
            correo = input("Ingrese el correo del empleado: ")

            query = """
            INSERT INTO empleado (nombre, cargo, correo)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (nombre, cargo, correo))
            conexion.commit()
            input("Empleado añadido exitosamente.")

        elif opcion == '2':
            # Consultar empleados (mostrar todos)
            query = "SELECT * FROM empleado"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Empleados Registrados ---")
                for row in resultados:
                    id_empleado = row[0]
                    nombre = row[1]
                    cargo = row[2]
                    correo = row[3]

                    print(f"ID: {id_empleado} | Nombre: {nombre} | Cargo: {cargo} | Correo: {correo}\n")
                input("Consulta realizada correctamente...")
            else:
                print("No se encontraron empleados.")

        elif opcion == '3':
            # Editar empleado
            id_empleado = input("Ingrese el ID del empleado que desea editar: ")
            print("Seleccione el campo que desea editar:")
            print("1. Nombre")
            print("2. Cargo")
            print("3. Correo")
            campo = input("Opción: ")

            if campo == '1':
                nuevo_valor = input("Ingrese el nuevo nombre del empleado: ")
                query = "UPDATE empleado SET nombre = %s WHERE ID_Empleado = %s"
            elif campo == '2':
                nuevo_valor = input("Ingrese el nuevo cargo del empleado: ")
                query = "UPDATE empleado SET cargo = %s WHERE ID_Empleado = %s"
            elif campo == '3':
                nuevo_valor = input("Ingrese el nuevo correo del empleado: ")
                query = "UPDATE empleado SET correo = %s WHERE ID_Empleado = %s"
            else:
                print("Opción no válida.")
                continue

            cursor.execute(query, (nuevo_valor, id_empleado))
            conexion.commit()
            input("Empleado actualizado exitosamente...")

        elif opcion == '4':
            # Eliminar empleado
            id_empleado = input("Ingrese el ID del empleado que desea eliminar: ")
            query = "DELETE FROM empleado WHERE ID_Empleado = %s"
            cursor.execute(query, (id_empleado,))
            conexion.commit()
            input("Empleado eliminado exitosamente...")

        elif opcion == '5':
            # Salir
            input("Saliendo del sistema de gestión de empleados...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

    cursor.close()

def gestion_inventario(conexion):

    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Inventario ---")
        print("1. Añadir nuevo producto")
        print("2. Consultar productos")
        print("3. Editar producto")
        print("4. Eliminar producto")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Add a new product
            stock = int(input("Ingrese la cantidad en stock: "))
            nombre = input("Ingrese el nombre del producto: ")
            marca = input("Ingrese la marca: ")
            precio_unidad = float(input("Ingrese el precio unitario: "))

            query = """
            INSERT INTO inventario (stock, nombre, marca, precio_unidad)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (stock, nombre, marca, precio_unidad))
            conexion.commit()
            print("Producto añadido exitosamente.")

        elif opcion == '2':
            # Show products
            query = "SELECT * FROM inventario"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Productos ---")
                for fila in resultados:
                    id_inventario, stock, nombre, marca, precio_unidad = fila
                    print(f"ID: {id_inventario} | Stock: {stock} | Nombre: {nombre} | Marca: {marca} | Precio: {precio_unidad}")
            else:
                print("No se encontraron productos.")

        elif opcion == '3':
            # Edit product
            id_inventario = int(input("Ingrese el ID del producto a editar: "))
            campo = input("Seleccione el campo a editar (stock, nombre, marca, precio_unidad): ")
            nuevo_valor = input(f"Ingrese el nuevo valor para {campo}: ")

            query = f"UPDATE inventario SET {campo} = %s WHERE ID_Inventario = %s"
            cursor.execute(query, (nuevo_valor, id_inventario))
            conexion.commit()
            print("Producto actualizado exitosamente.")

        elif opcion == '4':
            # Delete product
            id_inventario = int(input("Ingrese el ID del producto a eliminar: "))
            query = "DELETE FROM inventario WHERE ID_Inventario = %s"
            cursor.execute(query, (id_inventario,))
            conexion.commit()
            print("Producto eliminado exitosamente.")

        elif opcion == '5':
            # Exit
            print("Saliendo del sistema de gestión de inventario...")
            break
        else:
            print("Opción inválida.")

    cursor.close()

def gestion_proveedor(conexion):
    """
    Función para gestionar las operaciones CRUD en la tabla 'proveedor'.

    Args:
        conexion: Conexión a la base de datos.
    """

    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Proveedores ---")
        print("1. Añadir nuevo Proveedor")
        print("2. Consultar Proveedores")
        print("3. Editar Proveedor")
        print("4. Eliminar Proveedor")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir un nuevo proveedor
            nombre = input("Ingrese el nombre del proveedor: ")
            correo = input("Ingrese el correo electrónico: ")
            telefono = input("Ingrese el número de teléfono: ")
            disponibilidad = input("Ingrese la disponibilidad: ")

            query = """
            INSERT INTO proveedor (nombre, correo, telefono, disponibilidad)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, correo, telefono, disponibilidad))
            conexion.commit()
            print("Proveedor añadido exitosamente.")

        elif opcion == '2':
            # Consultar proveedores
            query = "SELECT * FROM proveedor"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Proveedores ---")
                for fila in resultados:
                    id_proveedor, nombre, correo, telefono, disponibilidad = fila
                    print(f"ID: {id_proveedor} | Nombre: {nombre} | Correo: {correo} | Teléfono: {telefono} | Disponibilidad: {disponibilidad}")
            else:
                print("No se encontraron proveedores.")

        elif opcion == '3':
            # Editar proveedor
            id_proveedor = input("Ingrese el ID del proveedor a editar: ")
            campo = input("Seleccione el campo a editar (nombre, correo, telefono, disponibilidad): ")
            nuevo_valor = input(f"Ingrese el nuevo valor para {campo}: ")

            query = f"UPDATE proveedor SET {campo} = %s WHERE ID = %s"
            cursor.execute(query, (nuevo_valor, id_proveedor))
            conexion.commit()
            print("Proveedor actualizado exitosamente.")

        elif opcion == '4':
            # Eliminar proveedor
            id_proveedor = input("Ingrese el ID del proveedor a eliminar: ")
            query = "DELETE FROM proveedor WHERE ID = %s"
            cursor.execute(query, (id_proveedor,))
            conexion.commit()
            print("Proveedor eliminado exitosamente.")

        elif opcion == '5':
            # Salir
            print("Saliendo del sistema de gestión de proveedores...")
            break
        else:
            print("Opción inválida.")

    cursor.close()
