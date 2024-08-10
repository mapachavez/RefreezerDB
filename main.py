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
    
            
def gestionProformas(conexion):
    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Proformas ---")
        print("1. Añadir nueva proforma")
        print("2. Consultar proformas")
        print("3. Editar proforma")
        print("4. Eliminar proforma")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir nueva proforma
            fecha_emision = input("Ingrese la fecha de emisión (YYYY-MM-DD): ")
            costo_mano_obra = input("Ingrese el costo de mano de obra: ")
            subtotal = input("Ingrese el subtotal: ")
            
            while True:
                estado_aprobacion = input("Ingrese el estado de aprobación (Aprobado/No Aprobado) [Enter para 'No Aprobado']: ")
                if estado_aprobacion == "":
                    estado_aprobacion = "No Aprobado"
                if estado_aprobacion in ["Aprobado", "No Aprobado"]:
                    break
                print("Entrada no válida. Intente nuevamente.")

            calle = input("Ingrese la calle: ")
            manzana = input("Ingrese la manzana: ")
            ciudad = input("Ingrese la ciudad: ")
            visita_fecha = input("Ingrese la fecha de visita (YYYY-MM-DD): ")
            visita_hora = input("Ingrese la hora de visita (HH:MM:SS): ")
            visita_observacion = input("Ingrese observaciones de la visita (puede dejarlo vacío): ")

            id_cliente = input("Ingrese el ID del cliente: ")
            id_proyecto = input("Ingrese el ID del proyecto (opcional): ")

            query = """
            INSERT INTO proforma (fecha_emision, costo_mano_obra, subtotal, estado_aprobacion, calle, manzana, ciudad, visita_fecha, visita_hora, visita_observacion, ID_Cliente, ID_Proyecto)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (fecha_emision, costo_mano_obra, subtotal, estado_aprobacion, calle, manzana, ciudad, visita_fecha, visita_hora, visita_observacion, id_cliente, id_proyecto if id_proyecto else None))
            conexion.commit()
            input("Proforma añadida exitosamente.")

        elif opcion == '2':
            # Consultar proformas (mostrar todas)
            query = "SELECT * FROM proforma"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Proformas Creadas ---")
                for row in resultados:
                    id_proforma = row[0]
                    fecha_emision = row[1].strftime("%Y-%m-%d")
                    costo_mano_obra = row[2]
                    subtotal = row[3]
                    estado_aprobacion = row[4]
                    calle = row[5]
                    manzana = row[6]
                    ciudad = row[7]
                    visita_fecha = row[8].strftime("%Y-%m-%d")
                    visita_hora = str(row[9])  # Convertir TIME a string
                    visita_observacion = row[10] if row[10] else 'N/A'
                    id_cliente = row[11]
                    id_proyecto = row[12] if row[12] else 'N/A'

                    print(f"ID: {id_proforma} | Fecha Emisión: {fecha_emision} | Costo Mano de Obra: {costo_mano_obra} | Subtotal: {subtotal} | "
                          f"Estado Aprobación: {estado_aprobacion} | Dirección: {calle}, {manzana}, {ciudad} | "
                          f"Fecha Visita: {visita_fecha} | Hora Visita: {visita_hora} | Observaciones: {visita_observacion} | "
                          f"ID Cliente: {id_cliente} | ID Proyecto: {id_proyecto}\n")
                input("Consulta realizada correctamente...")
            else:
                print("No se encontraron proformas.")
            

        elif opcion == '3':
            # Editar proforma
            id_proforma = input("Ingrese el ID de la proforma que desea editar: ")
            print("Seleccione el campo que desea editar:")
            print("1. Fecha de Emisión")
            print("2. Costo Mano de Obra")
            print("3. Subtotal")
            print("4. Estado de Aprobación")
            print("5. Calle")
            print("6. Manzana")
            print("7. Ciudad")
            print("8. Fecha de Visita")
            print("9. Hora de Visita")
            print("10. Observaciones de la Visita")
            print("11. ID Cliente")
            print("12. ID Proyecto")
            campo = input("Opción: ")

            if campo == '1':
                nuevo_valor = input("Ingrese la nueva fecha de emisión (YYYY-MM-DD): ")
                query = "UPDATE proforma SET fecha_emision = %s WHERE ID_Proforma = %s"
            elif campo == '2':
                nuevo_valor = input("Ingrese el nuevo costo de mano de obra: ")
                query = "UPDATE proforma SET costo_mano_obra = %s WHERE ID_Proforma = %s"
            elif campo == '3':
                nuevo_valor = input("Ingrese el nuevo subtotal: ")
                query = "UPDATE proforma SET subtotal = %s WHERE ID_Proforma = %s"
            elif campo == '4':
                while True:
                    nuevo_valor = input("Ingrese el nuevo estado de aprobación (Aprobado/No Aprobado) [Enter para 'No Aprobado']: ")
                    if nuevo_valor == "":
                        nuevo_valor = "No Aprobado"
                    if nuevo_valor in ["Aprobado", "No Aprobado"]:
                        break
                    print("Entrada no válida. Intente nuevamente.")
                query = "UPDATE proforma SET estado_aprobacion = %s WHERE ID_Proforma = %s"
            elif campo == '5':
                nuevo_valor = input("Ingrese la nueva calle: ")
                query = "UPDATE proforma SET calle = %s WHERE ID_Proforma = %s"
            elif campo == '6':
                nuevo_valor = input("Ingrese la nueva manzana: ")
                query = "UPDATE proforma SET manzana = %s WHERE ID_Proforma = %s"
            elif campo == '7':
                nuevo_valor = input("Ingrese la nueva ciudad: ")
                query = "UPDATE proforma SET ciudad = %s WHERE ID_Proforma = %s"
            elif campo == '8':
                nuevo_valor = input("Ingrese la nueva fecha de visita (YYYY-MM-DD): ")
                query = "UPDATE proforma SET visita_fecha = %s WHERE ID_Proforma = %s"
            elif campo == '9':
                nuevo_valor = input("Ingrese la nueva hora de visita (HH:MM:SS): ")
                query = "UPDATE proforma SET visita_hora = %s WHERE ID_Proforma = %s"
            elif campo == '10':
                nuevo_valor = input("Ingrese las nuevas observaciones de la visita: ")
                query = "UPDATE proforma SET visita_observacion = %s WHERE ID_Proforma = %s"
            elif campo == '11':
                nuevo_valor = input("Ingrese el nuevo ID del cliente: ")
                query = "UPDATE proforma SET ID_Cliente = %s WHERE ID_Proforma = %s"
            elif campo == '12':
                nuevo_valor = input("Ingrese el nuevo ID del proyecto (puede dejarlo vacío): ")
                query = "UPDATE proforma SET ID_Proyecto = %s WHERE ID_Proforma = %s"
            else:
                print("Opción no válida.")
                continue

            cursor.execute(query, (nuevo_valor, id_proforma))
            conexion.commit()
            input("Proforma actualizada exitosamente...")

        elif opcion == '4':
            # Eliminar proforma
            id_proforma = input("Ingrese el ID de la proforma que desea eliminar: ")
            query = "DELETE FROM proforma WHERE ID_Proforma = %s"
            cursor.execute(query, (id_proforma,))
            conexion.commit()
            input("Proforma eliminada exitosamente...")

        elif opcion == '5':
            # Salir
            input("Saliendo del sistema de gestión de proformas...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

    cursor.close()
        
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
        gestionProformas(conexion)
        
    elif (opc == "3"):
        fu.gestionproyecto(conexion)
    elif (opc == "4"):
        print("\nOpcion 4")
        input("Presione enter para continunar...\n")
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