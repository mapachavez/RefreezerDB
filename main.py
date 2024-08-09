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
            print("INFO: Conexión exitosa a la base de datos\n")
            return conexion
        
    except mysql.connector.Error as err:
        print(f"Error: {err} \n")
        return None
    
def gestionClientes(conexion):
    cursor = conexion.cursor()
    opc = "0"
    while (opc != "5"):
        print("1. Insertar datos")
        print("2. Consultar datos")
        print("3. Modificar datos")
        print("4. Eliminar datos")
        print("5. Salir")
        
        opc = input("\nIntroduce el número de opción: ")
        
        if opc == "1":
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
# ----------------- MAIN ------------------ #

conexion = conectar() 
opc = ""
while(opc != "10"):
    print(""" ----- MENÚ PRINCIPAL DE REFREEZER -----
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
        print("\nOpcion 10")
        conexion.close()
        input("Presione enter para cerrar...\n")
    else:
        print("No existe esa opcion. Intente nuevamente")
        input("Presione enter para continunar...\n")