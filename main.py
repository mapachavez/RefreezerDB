# --------------- LIBRERIAS --------------- #
import mysql.connector
# --------------- FUNCIONES --------------- #
def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost', # Cambiar por la dirección de tu servidor
            port = 9999, # Cambiar por el puerto de tu servidor
            user='user',   # Cambiar por tu nombre de usuario
            password='password',  # Cambiar por tu contraseña
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
                            print(f"ID: {fila[0]}| Nombre: {fila[1]}| Direccion: {fila[2]}| Correo: {fila[3]}| Teléfono: {fila[4]}| Cédula: {fila[5]}")
                        
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
                            print(f"ID: {fila[0]}| Nombre: {fila[1]}| Direccion: {fila[2]}| Correo: {fila[3]}| Teléfono: {fila[4]}| RUC: {fila[5]}")

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
        print("\nOpcion 2")
        input("Presione enter para continunar...\n")
    elif (opc == "3"):
        print("\nOpcion 3")
        input("Presione enter para continunar...\n")
    elif (opc == "4"):
        print("\nOpcion 4")
        input("Presione enter para continunar...\n")
    elif (opc == "5"):
        print("\nOpcion 5")
        input("Presione enter para continunar...\n")
    elif (opc == "6"):
        print("\nOpcion 6")
        input("Presione enter para continunar...\n")
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