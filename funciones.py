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
