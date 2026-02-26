#importamos pyro para poder conectarnos al servidor y hacer solicitudes remotas
import Pyro5.api

#función que simula a los 3 clienets
def simular_clientes():
    #Ejecutamos el cliente y solicitamos la URI del servidor para conectarnos
    uri_servidor ="PYRO:obj_5cffbbf20bf64a14abe0c7d5c00269c6@localhost:33483"
    
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
    
    print("\n========== ENVIAR SOLICITUDES DE 3 USUARIOS ==========")
    # Caso 1
    res1 = renta_autos.solicitar_renta("Usuario 1", "auto_4puertas", 3, 4, "martes")
    print(res1)
    res1 = renta_autos.solicitar_renta("Usuario 1", "auto_4puertas", 3, 4, "martes")
    print(res1)
    res1 = renta_autos.solicitar_renta("Usuario 1", "auto_4puertas", 3, 4, "martes")
    print(res1)
    res1 = renta_autos.solicitar_renta("Usuario 1", "auto_4puertas", 3, 4, "martes")
    print(res1)
    
    #Intenta rentar Camioneta de 4 puertas en Lunes (Debe fallar)
    res2 = renta_autos.solicitar_renta("Usuario 2", "cam_4puertas", 4, 2, "lunes")
    print(res2)
    
    # Intenta meter 12 personas en Camioneta 3 puertas (Excede cupo)
    res3 = renta_autos.solicitar_renta("Usuario 3", "cam_3puertas", 12, 5, "viernes")
    print(res3)

    # Usuario 2 hace un segundo intento correcto (Pueden rentar hasta 3 vehículos)
    res4 = renta_autos.solicitar_renta("Usuario 2", "cam_4puertas", 4, 2, "miercoles")
    print(res4)

if __name__ == "__main__":
    simular_clientes()