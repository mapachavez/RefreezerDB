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
    
def gestionClientes(conexion):
    opc = ""
    while (opc != "5"):
        cursor = conexion.cursor()
        print("\n1. Insertar datos")
        print("2. Consultar datos")
        print("3. Modificar datos")
        print("4. Eliminar datos")
        print("5. Regresar")
        
        opc = input("\nIntroduce el número de opción: ")
        
        if opc == "1":
            print("\n------\t Insertar nuevos clientes \t------")
            try:
                conexion.start_transaction()
                
                nombre = input("\nIntroduzca el nombre: ")
                direccion = input("Introduzca la direccion: ")
                mail = input("Introduzca el correo: ")
                telf = input("Introduzca el telefono: ")
                
                query_c = "INSERT INTO cliente (nombre, direccion, correo, telefono) VALUES (%s, %s, %s, %s)"
                val_c = (nombre, direccion, mail, telf)
                cursor.execute(query_c, val_c)
                
                id_cliente = cursor.lastrowid
                
                tipo = ""
                while tipo == "":
                    tipo = input("""\n\t\tTipo de cliente:
                                
                            1. Cliente natural
                            2. Cliente empresa
                            
                        Inserte tipo de cliente: """)
                    
                    if tipo == "1":
                        cedula = input("Ingrese el numero de cedula: ")
                        query_cn = "INSERT INTO cliente_natural (ID_cliente, Cedula) VALUES (%s, %s)"
                        val_cn = (id_cliente, cedula)
                        cursor.execute(query_cn,val_cn)
                    elif tipo == "2":
                        ruc = input("Ingrese el ruc de la empresa: ")
                        query_ce = "INSERT INTO cliente_empresa (ID_cliente, RUC) VALUES (%s, %s)"
                        val_ce = (id_cliente, ruc)
                        cursor.execute(query_ce,val_ce)
                    else:
                        input("Opcion no válida. Intente nuevamente...")
                        tipo = ""
                
                # Confirmar la transacción si ambas inserciones son exitosas
                conexion.commit()
                input("\nINFO: Cliente insertado correctamente...\n")
            
            except mysql.connector.Error as err:
                print(f"Error: {err} \n")
                # Deshacer la transacción si ocurre un error
                conexion.rollback()
            finally:
                cursor.close()
        elif opc == "2":
            ocon = ""
            while ocon != "3":
                print("\n------\t Consulta de clientes \t------")
                print("1. Clientes naturales")
                print("2. Clientes empresa")
                print("3. Regresar")
                ocon = input("\nIngrese una opcion: ")
                
                if ocon == "1":
                    print("\n---------- \t\t Consulta de clientes naturales \t\t----------\n")
                    query_ccn = "SELECT * FROM cliente c JOIN cliente_natural USING(ID_cliente)"
                    
                    try:
                        cursor.execute(query_ccn)
                        rescn = cursor.fetchall()

                        for fila in rescn:
                            print(f"ID: {fila[0]}| Nombre: {fila[1]}| Direccion: {fila[2]}| Correo: {fila[3]}| Teléfono: {fila[4]}| Cédula: {fila[5]}\n")
                        
                        input("\nConsulta exitosa! \nPresione enter para continuar...")

                    except mysql.connector.Error as err:
                        print(f"Error: {err}")
                elif ocon == "2":
                    print("\n---------- \t\t Consulta de clientes empresa \t\t----------\n")
                    query_cce = "SELECT * FROM cliente c JOIN cliente_empresa USING(ID_cliente)"
                    
                    try:
                        cursor.execute(query_cce)
                        resce = cursor.fetchall()

                        for fila in resce:
                            print(f"ID: {fila[0]}| Nombre: {fila[1]}| Direccion: {fila[2]}| Correo: {fila[3]}| Teléfono: {fila[4]}| RUC: {fila[5]}\n")

                        input("\nConsulta exitosa! \nPresione enter para continuar...")
                        
                    except mysql.connector.Error as err:
                        print(f"Error: {err}")
                elif ocon =="3":
                    input("Regresando al menú anterior...\n")
                else:
                    input("Opcion no válida. Intente nuevamente...")
                    ocon = ""
                    
            cursor.close()
        elif opc == "3":
            print("\n------\t Modificar datos de clientes \t------")
            while True:
                print("\nSeleccione el tipo de cliente:")
                print("1. Cliente Natural")
                print("2. Cliente Empresa")
                
                tipo_cliente = input("\nIngrese el número correspondiente al tipo de cliente: ")
                
                if tipo_cliente in ['1', '2']:
                    break
                else:
                    print("Selección inválida. Por favor, intente de nuevo.")
            
            id_cliente = input("Ingrese el ID del cliente: ")
            
            # Selección de la tabla a modificar
            while True:
                print("\nSeleccione la tabla que desea modificar:")
                print("1. Tabla CLIENTE")
                print("2. Tabla CLIENTE_NATURAL o CLIENTE_EMPRESA")
                
                tabla_seleccionada = input("Ingrese el número correspondiente a la tabla: ")
                
                if tabla_seleccionada in ['1', '2']:
                    break
                else:
                    print("Selección inválida. Por favor, intente de nuevo.")
                    
            if tabla_seleccionada == '1':
                # Modificación en la tabla CLIENTE
                while True:
                    print("\nSeleccione el campo a modificar en la tabla CLIENTE:")
                    print("1. Nombre")
                    print("2. Dirección")
                    print("3. Correo")
                    print("4. Teléfono")
                    
                    campo_seleccionado = input("Ingrese el número correspondiente al campo: ")
                    
                    campos = {
                        '1': 'nombre',
                        '2': 'direccion',
                        '3': 'correo',
                        '4': 'telefono'
                    }
                    
                    campo = campos.get(campo_seleccionado)
                    
                    if campo:
                        nuevo_valor = input(f"Ingrese el nuevo valor para {campo}: ")
                        consulta = f"UPDATE CLIENTE SET {campo} = %s WHERE ID_cliente = %s"
                        cursor.execute(consulta, (nuevo_valor, id_cliente))
                        print(f"\nRegistro en la tabla CLIENTE con ID {id_cliente} actualizado correctamente.")
                        break
                    else:
                        print("Selección de campo inválida. Por favor, intente de nuevo.")
            
            elif tabla_seleccionada == '2':
                # Modificación en la tabla CLIENTE_NATURAL o CLIENTE_EMPRESA
                if tipo_cliente == '1':
                    while True:
                        print("\nSeleccione el campo a modificar en la tabla CLIENTE_NATURAL:")
                        print("1. Cédula")
                        
                        seleccion = input("Ingrese el número correspondiente al campo: ")
                        
                        if seleccion == '1':
                            campo = 'Cedula'
                            tabla = 'CLIENTE_NATURAL'
                            break
                        else:
                            print("Selección de campo inválida. Por favor, intente de nuevo.")
                
                elif tipo_cliente == '2':
                    while True:
                        print("\nSeleccione el campo a modificar en la tabla CLIENTE_EMPRESA:")
                        print("1. RUC")
                        
                        seleccion = input("Ingrese el número correspondiente al campo: ")
                        
                        if seleccion == '1':
                            campo = 'RUC'
                            tabla = 'CLIENTE_EMPRESA'
                            break
                        else:
                            print("Selección de campo inválida. Por favor, intente de nuevo.")

                nuevo_valor = input(f"Ingrese el nuevo valor para {campo}: ")
                consulta = f"UPDATE {tabla} SET {campo} = %s WHERE ID_cliente = %s"
                cursor.execute(consulta, (nuevo_valor, id_cliente))
                print(f"\nRegistro en la tabla {tabla} con ID {id_cliente} actualizado correctamente.")
            #Aplicar los cambios
            conexion.commit()
            cursor.close()
            input("Aplicando cambios... \nPulse enter para continuar...")
        elif opc == "4":
            print("\n------\t Eliminar datos de clientes \t------")
            while True:
                print("\nSeleccione el tipo de cliente:")
                print("1. Cliente Natural")
                print("2. Cliente Empresa")
                
                tipo_cliente = input("\nIngrese el número correspondiente al tipo de cliente: ")
                
                if tipo_cliente in ['1', '2']:
                    break
                else:
                    print("Selección inválida. Por favor, intente de nuevo.")
            
            id_cliente = input("Ingrese el ID del cliente: ")

            # Determinar la tabla específica según el tipo de cliente
            if tipo_cliente == '1':
                tabla_especifica = "CLIENTE_NATURAL"
            elif tipo_cliente == '2':
                tabla_especifica = "CLIENTE_EMPRESA"

            try:
                # Eliminar primero de la tabla específica
                consulta_especifica = f"DELETE FROM {tabla_especifica} WHERE ID_cliente = %s"
                cursor.execute(consulta_especifica, (id_cliente,))
                
                # Luego eliminar de la tabla CLIENTE
                consulta_cliente = "DELETE FROM CLIENTE WHERE ID_cliente = %s"
                cursor.execute(consulta_cliente, (id_cliente,))
                
                print(f"Cliente con ID {id_cliente} eliminado correctamente de las tablas CLIENTE y {tabla_especifica}.")

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                
            #Aplicar los cambios
            conexion.commit()
            cursor.close()
            input("Aplicando cambios... \nPulse enter para continuar...")
        elif opc == "5":
            cursor.close()
            input("\nRegresando al menú principal... \nPresione enter para continuar...")
        else:
            input("\nOpcion no válida. Intente nuevamente...")
            opc = ""
            cursor.close()
            
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
        gestionClientes(conexion)
    
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
        print("\nOpcion 9")
        input("Presione enter para continunar...\n")
    elif (opc == "10"):
        conexion.close()
        input("Presione enter para cerrar...\n")
    else:
        print("No existe esa opcion. Intente nuevamente")
        input("Presione enter para continunar...\n")