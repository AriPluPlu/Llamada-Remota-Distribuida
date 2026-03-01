#importamos pyro para poder conectarnos al servidor y hacer solicitudes remotas
import Pyro5.api

#función que simula a los 3 clienets
def simular_clientes():
    #Ejecutamos el cliente y solicitamos la URI del servidor para conectarnos
    uri_servidor ="PYRO:obj_38a380b502124dceb96351cac5109b2a@localhost:37469"
    
    # Nos conectamos al objeto remoto
    #renta_autos es lo que nos permite llamar a los métodos del servidor como si fueran locales
    renta_autos = Pyro5.api.Proxy(uri_servidor)
    
    #Obtenemos el catálogo de vehículos disponibles para renta y lo imprimimos
    print("\n========== CATÁLOGO DE VEHÍCULOS ========== ")
    #obtener.catalogo es la funcion que esta en el servidor
    catalogo = renta_autos.obtener_catalogo()
    #key es en este caso el nombre del vehículo y val es un diccionario con sus características
    #en el server ejmpluo. auto_4puertas": {"nombre": "Auto 4 puertas", "cupo": 4, "costo": 600, "dias_disp": "Lunes a Domingo"}
    for key, val in catalogo.items():
        print(f"{val['nombre']} | Cupo: {val['cupo']} | Costo: ${val['costo']}por día | Disp: {val['dias_disp']}")
    
    while True:
        print("\n========== NUEVA SOLICITUD DE RENTA ==========")
        usuario = input("Ingresa tu nombre (o escribe 'salir' para terminar): ")
        
        # Condición para romper el ciclo y cerrar el cliente
        if usuario.lower() == 'salir':
            print("Cerrando el sistema de rentas. ¡Hasta luego!")
            break
            
        tipo_vehiculo = input("Ingresa la clave del tipo de auto (auto_4puertas, cam_4puertas, cam_3puertas): ")
        
        # Usamos un try-except por si el usuario escribe letras en lugar de números
        try:
            ocupantes = int(input("Ingresa el número de ocupantes: "))
            dias = int(input("Ingresa los días de renta: "))
        except ValueError:
            print("\n[ERROR] Por favor, ingresa solo números para los ocupantes y los días. Intenta de nuevo.")
            continue # Regresa al inicio del ciclo
            
        dia_semana = input("Ingresa los días de la semana (ej. Lunes, Martes): ")
        
        # Hacemos la llamada remota al servidor con los datos que ingresó el usuario
        print("\nEnviando solicitud al servidor...")
        respuesta = renta_autos.solicitar_renta(usuario, tipo_vehiculo, ocupantes, dias, dia_semana)
        
        # Imprimimos lo que nos contestó el servidor
        print(">>> RESPUESTA DEL SERVIDOR:")
        print(respuesta)

if __name__ == "__main__":
    simular_clientes()