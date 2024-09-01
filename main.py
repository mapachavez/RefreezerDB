# --------------- LIBRERIAS --------------- #
import mysql.connector
import funciones as fu
# --------------- FUNCIONES --------------- #
def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost', # Cambiar por la dirección de tu servidor
            port = 3306, # Cambiar por el puerto de tu servidor
            user='root',   # Cambiar por tu nombre de usuario
            password='admin',  # Cambiar por tu contraseña
            database='refreezerdb'
            )
        
        if conexion.is_connected():
            print("INFO: Conexión exitosa a la base de datos")
            return conexion
        
    except mysql.connector.Error as err:
        print(f"Error: {err} \n")
        return None
    

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
        print("\n-----\t Gestión de proformas \t-----")
        fu.gestionProformas(conexion)
        
    elif (opc == "3"):
        print("\n-----\t Gestión de proyectos \t-----")
        fu.gestionproyecto(conexion)
    elif (opc == "4"):
        print("\n-----\t Gestión de servicios \t-----")
        fu.gestionServicios(conexion)
    elif (opc == "5"):
        print("\n-----\t Gestión de empleados \t-----")
        fu.gestionempleados(conexion)
    elif (opc == "6"):
        print("\n-----\t Gestión de certificados \t-----")
        fu.gestionCertificado(conexion)
    elif (opc == "7"):
        print("\n-----\t Gestión de materiales \t-----")
        fu.gestionMateriales(conexion)
    elif (opc == "8"):
        print("\n-----\t Gestión de inventario \t-----")
        fu.gestionInventario(conexion)
    elif (opc == "9"):
        print("\n-----\t Gestión de proveedores \t-----")
        fu.gestion_proveedor(conexion)
    elif (opc == "10"):
        conexion.close()
        input("Presione enter para cerrar...\n")
    else:
        print("No existe esa opcion. Intente nuevamente")
        input("Presione enter para continunar...\n")