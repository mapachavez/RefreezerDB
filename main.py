# --------------- LIBRERIAS --------------- #
import mysql.connector
import funciones as fu
# --------------- FUNCIONES --------------- #
def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost', # Cambiar por la dirección de tu servidor
            port = 9999, # Cambiar por el puerto de tu servidor
            user='root',   # Cambiar por tu nombre de usuario
            password='lol',  # Cambiar por tu contraseña
            database='refreezerdb'
            )
        
        if conexion.is_connected():
            print("INFO: Conexión exitosa a la base de datos")
            return conexion
        
    except mysql.connector.Error as err:
        print(f"Error: {err} \n")
        return None
    
            

        
def gestionProyectos(conexion):
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
            #añadir un nuevo proyecto
            nombre_proyecto = input("Ingrese el nombre del proyecto: ")
            fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
            fecha_fin = input("Ingrese la fecha de finalizacion (YYYY-MM-DD): ")
            
            query = """
            INSERT INTO proyecto (nombre_proyecto, fecha_inicio, fecha_fin)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (nombre_proyecto, fecha_inicio, fecha_fin))
            conexion.commit()
            input("Proyecto añadido exitosamente.")
        elif opcion == '2':
            #Mostrar los proyectos
            query = "SELECT * FROM proyecto"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Proyectos Creados ---")
                for fila in resultados:
                    id_proyecto = fila[0]
                    nombre_proyecto = fila[1]
                    fecha_inicio = fila[2].strftime("%Y-%m-%d")
                    fecha_fin = fila[3].strftime("%Y-%m-%d")
                    
                    print(f"ID: {id_proyecto} | Nombre: {nombre_proyecto} "
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
                query = "UPDATE proyecto SET nombre_proyecto = %s WHERE ID_Proyecto = %s"
            elif campo == '2':
                nuevo_valor = input("Ingrese la nueva fecha de inicio (YYYY-MM-DD): ")
                query = "UPDATE proyecto SET fecha_inicio = %s WHERE ID_Proyecto = %s"
            elif campo == '3':
                nuevo_valor = input("Ingrese la nueva fecha de fin (YYYY-MM-DD): ")
                query = "UPDATE proyecto SET fecha_fin = %s WHERE ID_Proyecto = %s"
            else:
                print("Opcion incorrecta...")
                continue

            cursor.execute(query, (nuevo_valor, id_proyecto))
            conexion.commit()
            input("Proyecto actualizado exitosamente...")
        elif opcion == '4':
            #dar de baja el proyecto 
            id_proyecto = input("Ingrese el ID del proyecto que desea eliminar: ")
            query = "DELETE FROM proyecto WHERE ID_Proyecto = %s"
            cursor.execute(query, (id_proyecto,))
            conexion.commit()
            input("El proyecto se ha eliminado exitosamente...")

        elif opcion == '5':
            # pa salir
            input("Saliendo del sistema de gestión de proyectos...")
            break
        else: 
            print("Opcion invalida...")
    cursor.close()

#ponle 10 centavos de fe mijo
def gestionServicios(conexion):
    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Servicios ---")
        print("1. Añadir nuevo Servicio")
        print("2. Consultar Servicios")
        print("3. Editar Servicio")
        print("4. Eliminar Servicio")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir nuevo servicio
            descripcion = input("Ingrese la descripción del servicio: ")
            costo_servicio = input("Ingrese el costo del servicio: ")
            estado = input("Ingrese el estado del servicio: ")
            garantia = input("Ingrese la garantía (en meses): ")
            fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
            fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
            id_cliente = input("Ingrese el ID del cliente: ")

            query = """
            INSERT INTO SERVICIO (descripcion, costo_servicio, estado, garantia, Fecha_inicio, Fecha_fin, ID_cliente)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (descripcion, costo_servicio, estado, garantia, fecha_inicio, fecha_fin, id_cliente))
            conexion.commit()

            id_servicio = cursor.lastrowid

            print("\nSeleccione el tipo de servicio que desea añadir:")
            print("1. Diseño y Fabricación")
            print("2. Mantenimiento")
            print("3. Instalación y Montaje")
            print("4. Servicio Técnico")
            tipo_servicio = input("Opción: ")

            if tipo_servicio == '1':
                tipo_diseno = input("Ingrese el tipo de diseño: ")
                query_tipo = """
                INSERT INTO diseño_y_fabricacion (ID_Servicio, tipo_diseno)
                VALUES (%s, %s)
                """
                cursor.execute(query_tipo, (id_servicio, tipo_diseno))

            elif tipo_servicio == '2':
                tipo_mantenimiento = input("Ingrese el tipo de mantenimiento: ")
                name_unidad_maquinaria = input("Ingrese el nombre de la unidad/maquinaria: ")
                query_tipo = """
                INSERT INTO mantenimiento (ID_Servicio, Tipo_Mantenimiento, Name_Unidad_Maquinaria)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query_tipo, (id_servicio, tipo_mantenimiento, name_unidad_maquinaria))

            elif tipo_servicio == '3':
                tipo_instalacion = input("Ingrese el tipo de instalación: ")
                query_tipo = """
                INSERT INTO instalacion_y_montaje (ID_Servicio, tipo_instalacion)
                VALUES (%s, %s)
                """
                cursor.execute(query_tipo, (id_servicio, tipo_instalacion))

            elif tipo_servicio == '4':
                tipo_servicio_tecnico = input("Ingrese el tipo de servicio técnico: ")
                query_tipo = """
                INSERT INTO servicio_tecnico (ID_Servicio, tipo_servicio)
                VALUES (%s, %s)
                """
                cursor.execute(query_tipo, (id_servicio, tipo_servicio_tecnico))

            else:
                print("Opción no válida. Servicio no registrado en una tabla específica.")
                continue

            conexion.commit()
            input("Servicio añadido exitosamente.")

        elif opcion == '2':
            # Consultar servicios en general de la tabla servicio
            query = "SELECT * FROM SERVICIO"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Servicios ---")
                for row in resultados:
                    id_servicio = row[0]
                    descripcion = row[1]
                    costo_servicio = row[2]
                    estado = row[3]
                    garantia = row[4]
                    fecha_inicio = row[5].strftime("%Y-%m-%d")
                    fecha_fin = row[6].strftime("%Y-%m-%d")
                    id_cliente = row[7]

                    print(f"ID: {id_servicio} | Descripción: {descripcion} | Costo: {costo_servicio} | "
                          f"Estado: {estado} | Garantía: {garantia} meses | "
                          f"Fecha de Inicio: {fecha_inicio} | Fecha de Fin: {fecha_fin} | ID Cliente: {id_cliente}\n")
                input("Consulta realizada correctamente...")
            else:
                print("No se encontraron servicios.")

        elif opcion == '3':
            # modificar servicio
            id_servicio = input("Ingrese el ID del servicio que desea editar: ")

            print("\nSeleccione el tipo de servicio que desea editar:")
            print("1. Diseño y Fabricación")
            print("2. Mantenimiento")
            print("3. Instalación y Montaje")
            print("4. Servicio Técnico")
            tipo_servicio = input("Ingrese el numero de la opcion: ")

            if tipo_servicio == '1':
                nuevo_tipo_diseno = input("Ingrese el nuevo tipo de diseño: ")
                query_tipo = "UPDATE DISENO_Y_FABRICACION SET tipo_diseno = %s WHERE ID_Servicio = %s"
                cursor.execute(query_tipo, (nuevo_tipo_diseno, id_servicio))

            elif tipo_servicio == '2':
                nuevo_tipo_mantenimiento = input("Ingrese el nuevo tipo de mantenimiento: ")
                nuevo_name_unidad_maquinaria = input("Ingrese el nuevo nombre de la unidad/maquinaria: ")
                query_tipo = """
                UPDATE MANTENIMIENTO 
                SET Tipo_Mantenimiento = %s, Name_Unidad_Maquinaria = %s 
                WHERE ID_Servicio = %s
                """
                cursor.execute(query_tipo, (nuevo_tipo_mantenimiento, nuevo_name_unidad_maquinaria, id_servicio))

            elif tipo_servicio == '3':
                nuevo_tipo_instalacion = input("Ingrese el nuevo tipo de instalación: ")
                query_tipo = "UPDATE INSTALACION_Y_MONTAJE SET tipo_instalacion = %s WHERE ID_Servicio = %s"
                cursor.execute(query_tipo, (nuevo_tipo_instalacion, id_servicio))

            elif tipo_servicio == '4':
                nuevo_tipo_servicio_tecnico = input("Ingrese el nuevo tipo de servicio técnico: ")
                query_tipo = "UPDATE SERVICIO_TECNICO SET tipo_servicio = %s WHERE ID_Servicio = %s"
                cursor.execute(query_tipo, (nuevo_tipo_servicio_tecnico, id_servicio))

            else:
                print("Opción no válida.")
                continue

            print("Seleccione el campo que desea editar:")
            print("1. Descripción")
            print("2. Costo del Servicio")
            print("3. Estado")
            print("4. Garantía")
            print("5. Fecha de Inicio")
            print("6. Fecha de Fin")
            print("7. ID Cliente")
            campo = input("Opción: ")

            if campo == '1':
                nuevo_valor = input("Ingrese la nueva descripción: ")
                query = "UPDATE SERVICIO SET descripcion = %s WHERE ID_Servicio = %s"
            elif campo == '2':
                nuevo_valor = input("Ingrese el nuevo costo del servicio: ")
                query = "UPDATE SERVICIO SET costo_servicio = %s WHERE ID_Servicio = %s"
            elif campo == '3':
                nuevo_valor = input("Ingrese el nuevo estado: ")
                query = "UPDATE SERVICIO SET estado = %s WHERE ID_Servicio = %s"
            elif campo == '4':
                nuevo_valor = input("Ingrese la nueva garantía (en meses): ")
                query = "UPDATE SERVICIO SET garantia = %s WHERE ID_Servicio = %s"
            elif campo == '5':
                nuevo_valor = input("Ingrese la nueva fecha de inicio (YYYY-MM-DD): ")
                query = "UPDATE SERVICIO SET Fecha_inicio = %s WHERE ID_Servicio = %s"
            elif campo == '6':
                nuevo_valor = input("Ingrese la nueva fecha de fin (YYYY-MM-DD): ")
                query = "UPDATE SERVICIO SET Fecha_fin = %s WHERE ID_Servicio = %s"
            elif campo == '7':
                nuevo_valor = input("Ingrese el nuevo ID del cliente: ")
                query = "UPDATE SERVICIO SET ID_cliente = %s WHERE ID_Servicio = %s"
            else:
                print("Opción no válida.")
                continue

            cursor.execute(query, (nuevo_valor, id_servicio))
            conexion.commit()
            input("Servicio actualizado exitosamente...")

        elif opcion == '4':
            # Eliminar servicio
            id_servicio = input("Ingrese el ID del servicio que desea eliminar: ")
            #eliminacion por tablas de servicio especificas
            tablas_servicios = ["DISEÑO_Y_FABRICACION", "MANTENIMIENTO", "INSTALACION_Y_MONTAJE", "SERVICIO_TECNICO"]
            for tabla in tablas_servicios:
                query = f"DELETE FROM {tabla.lower} WHERE ID_Servicio = %s"
                cursor.execute(query, (id_servicio,))
            #eliminacion de la tabla servicio general
            query = "DELETE FROM SERVICIO WHERE ID_Servicio = %s"
            cursor.execute(query, (id_servicio,))
            conexion.commit()
            input("Servicio eliminado exitosamente de todas las tablas correspondientes...")

        elif opcion == '5':
            # Salir
            input("Saliendo del sistema de gestión de servicios...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

    cursor.close()

# ----------------- MAIN ------------------ #

conexion = conectar() 
opc = ""
while(opc != "10"):
    print("""\n ----- MENÚ PRINCIPAL DE REFREEZER -----
        1. Gestión de clientes
        2. Gestión de proformas
        3. Gestión de proyectos
        4. Gestión de servicios
        5. Gestión de empleados
        6. Gestión de certificados
        7. Gestión de materiales
        8. Gestión de inventario
        9. Gestión de proveedores
        10. Salir
    -----------------------------------------""")

    opc = input("Ingrese una opcion: ")
    
    if (opc == "1"):
        print("\n-----\t Gestión de clientes \t-----")
        fu.gestionClientes(conexion)
    
    elif (opc == "2"):
        fu.gestionProformas(conexion)
        
    elif (opc == "3"):
        fu.gestionproyecto(conexion)
    elif (opc == "4"):
        print("\nOpcion 4")
        gestionServicios(conexion)
    elif (opc == "5"):
        print("\n-----\t Gestión de empleados \t-----")
        fu.gestionempleados(conexion)
    elif (opc == "6"):
        fu.gestionCertificado(conexion)
    elif (opc == "7"):
        print("\nOpcion 7")
        input("Presione enter para continunar...\n")
    elif (opc == "8"):
        print("\nOpcion 8")
        input("Presione enter para continunar...\n")
    elif (opc == "9"):
        fu.gestion_proveedor(conexion)
    elif (opc == "10"):
        conexion.close()
        input("Presione enter para cerrar...\n")
    else:
        print("No existe esa opcion. Intente nuevamente")
        input("Presione enter para continunar...\n")