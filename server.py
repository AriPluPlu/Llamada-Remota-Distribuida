# Servidor para el sistema de renta de autos utilizando Pyro5
#importamos la biblioteca Pyro5 para crear un servidor de objetos remotos
import Pyro5.api

#@Pyro5.api.expose es un decorador que indica que la clase sera invocable remotamente a través de Pyro
@Pyro5.api.expose
#Definimos la clase del sistema de renta de autos
#Contiene el inventario,reglas de negocio y métodos para obtener el catálogo y solicitar una renta

#object es la clase de Python que se hereda para crear una clase nueva, en este caso SistemaRentaAutos
class SistemaRentaAutos(object):
#definimos el constructor de la clase
    def __init__(self):#self es una referencia a la instancia actual de la clase, se utiliza para acceder a las variables y métodos de la clase
        # unidades disponibles de cada tipo de vehículo
        self.unidades = {"auto_4puertas": 5, "cam_4puertas": 5, "cam_3puertas": 3}
        # catálogo de vehículos con sus características
        self.catalogo = {
            "auto_4puertas": {"nombre": "Auto 4 puertas", "cupo": 4, "costo": 600, "dias_disp": "Lunes a Domingo"},
            "cam_4puertas": {"nombre": "Camioneta 4 puertas", "cupo": 5, "costo": 750, "dias_disp": "Martes a Domingo"},
            "cam_3puertas": {"nombre": "Camioneta 3 puertas", "cupo": 10, "costo": 1200, "dias_disp": "Lunes a Domingo"}
        }
        #diccionario de usuarios y su número de rentas simultáneas
        self.rentas_usuario = {}

#funcon que devuelve el catálogo de vehículos disponibles para renta
    def obtener_catalogo(self):
        return self.catalogo
#funcion que "procesa" la solicitud de renta
#Recibe el nombre del usuario,tipo de vehículo
#número de ocupantes, días de renta y día de la semana
    def solicitar_renta(self, usuario, tipo_vehiculo, ocupantes, dias, dia_semana):
        # 1. Verificar si existe el vehículo con su nombre
        if tipo_vehiculo not in self.catalogo:
            return f"[{usuario}] , El vehículo no se ha encontrado."
            
        # si esta, obtenemos la información del vehículo del catálogo
        vehiculo = self.catalogo[tipo_vehiculo]
        
        # Verificar cupo
        if ocupantes > vehiculo["cupo"]:
            return f"[{usuario}], El cupo máximo para {vehiculo['nombre']} es de {vehiculo['cupo']} personas, ya se excedió."
            
        # --- NUEVA VALIDACIÓN DE DÍAS EXACTOS ---
        # Convertimos el texto "domingo, lunes" en una lista quitando espacios y poniendo minúsculas
        lista_dias = [dia.strip().lower() for dia in dia_semana.split(',')]
        
        # Validar que la cantidad de días de renta coincida con los días ingresados
        if len(lista_dias) != dias:
            return f"[{usuario}] , Error: Pediste rentar por {dias} días, pero ingresaste {len(lista_dias)} días ({dia_semana}). Deben coincidir."
            
        # Verificar disponibilidad de días para la camioneta 4 puertas
        if tipo_vehiculo == "cam_4puertas" and "lunes" in lista_dias:
            return f"[{usuario}] , Lo sentimos, pero la {vehiculo['nombre']} no se puede rentar ni usar los lunes. (Días solicitados: {dia_semana})"
        # ----------------------------------------
            
        # Verificar inventario
        if self.unidades[tipo_vehiculo] <= 0:
            return f"[{usuario}], Lo sentimos pero no hay unidades disponibles de {vehiculo['nombre']}."

        # verificar que el usuario no exceda el límite de 3 rentas simultáneas
        rentas_actuales = self.rentas_usuario.get(usuario, 0)
        if rentas_actuales >= 3:
            return f"[{usuario}] , Que mal, has alcanzado el límite de 3 rentas simultáneas."
            
        # si aun no ha alcanzado el límite, incrementamos su contador de rentas
        self.rentas_usuario[usuario] = rentas_actuales + 1

        # Confirmar renta y descontar inventario
        self.unidades[tipo_vehiculo] -= 1
        monto_total = vehiculo["costo"] * dias
        
        return f"[{usuario}] , La renta de {vehiculo['nombre']} ha sido confirmada por {dias} días ({dia_semana}).\n Con un total a pagar de: ${monto_total}."
# Configuración del servidor Pyro
def iniciar_servidor():
    # Creamos un daemon de Pyro
    #es importante por que escucha las solicitudes entrantes
    #y las dirige al objeto registrado
    daemon = Pyro5.api.Daemon()          
    #uri es la dirección que los clientes usarán para conectarse al servidor  
    #registramos la clase SistemaRentaAutos en el daemon y obtenemos su URI
    # funciona como un ID del objeto remoto, permitiendo a los clientes localizarlo y comunicarse con él 
    uri = daemon.register(SistemaRentaAutos) 
    #imprime la URI para que los clientes puedan conectarse al servidor
    print("Servidor listo. La URI para conectarse es:")
    print(uri)
    #iniciamos el ciclo para esperar que se conecten los clientes
    daemon.requestLoop()                    

#main que inicia el servidor cuando se ejecuta el script
if __name__ == "__main__":
    iniciar_servidor()