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
# ----------------- MAIN ------------------ #

conexion = conectar() 
opc = 0
while(opc != 10):
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

    opc = int(input("Ingrese una opcion: "))
    
    if (opc == 1):
        print("\nOpcion 1")
        input("Presione enter para continunar...\n")
    
    elif (opc == 2):
        print("\nOpcion 2")
        input("Presione enter para continunar...\n")
    elif (opc == 3):
        print("\nOpcion 3")
        input("Presione enter para continunar...\n")
    elif (opc == 4):
        print("\nOpcion 4")
        input("Presione enter para continunar...\n")
    elif (opc == 5):
        print("\nOpcion 5")
        input("Presione enter para continunar...\n")
    elif (opc == 6):
        print("\nOpcion 6")
        input("Presione enter para continunar...\n")
    elif (opc == 7):
        print("\nOpcion 7")
        input("Presione enter para continunar...\n")
    elif (opc == 8):
        print("\nOpcion 8")
        input("Presione enter para continunar...\n")
    elif (opc == 9):
        print("\nOpcion 9")
        input("Presione enter para continunar...\n")
    elif (opc == 10):
        print("\nOpcion 10")
        input("Presione enter para cerrar...\n")
    else:
        print("No existe esa opcion. Intente nuevamente")
        input("Presione enter para continunar...\n")