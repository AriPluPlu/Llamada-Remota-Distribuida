import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import Pyro5.api

# Configuración básica de la apariencia
ctk.set_appearance_mode("dark")  # Modo oscuro
ctk.set_default_color_theme("blue")  # Tema de color por defecto

class AplicacionRentaAutos(ctk.CTk):
    def __init__(self, uri):
        super().__init__()

        self.title("Sistema de Renta de Autos")
        self.geometry("850x600")
        self.resizable(False, False) #bloquear  el redimensionamiento de la ventana

        # Conectar con el servidor
        try:
            self.renta_autos = Pyro5.api.Proxy(uri)
            #obtener el catálogo de vehículos desde el servidor para mostrarlo en la interfaz
            self.catalogo = self.renta_autos.obtener_catalogo()
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor.\n{e}")
            self.destroy()
            return
        

        #Lienzo del tamaño definido de la ventana
        self.canvas = tk.Canvas(self, width=850, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True) #fill both para que ocupe todo el espacio disponible, expand true para que se ajuste al redimensionar (aunque en este caso no se puede redimensionar)

        # Dibujar el degradado de fondo y el título
        self.dibujar_fondo_y_titulo()

        #Colocar nuestras tajertas izquierda y derecha encima de lo dibujado en el lienzo
        self.crear_interfaz_sobre_canvas()
        
        
    def dibujar_fondo_y_titulo(self):
        # Aquí recreamos tu CSS: linear-gradient(90deg, c1 0%, c2 75%, c3 100%)
        width, height = 850, 600
        img = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(img)

        # Tus colores CSS convertidos a formato RGB (Red, Green, Blue)
        c1 = (195, 214, 224) # 0%
        c2 = (145, 161, 167) # 75%
        c3 = (83, 99, 105)   # 100%

        # Dibujamos línea por línea de izquierda a derecha para hacer el degradado
        for y in range(height):
            p = y / height # Porcentaje del ancho (0.0 a 1.0)
            
            if p <= 0.75:
                # Transición del 0 al 75% (De C1 a C2)
                p_norm = p / 0.75
                r = int(c1[0] + (c2[0] - c1[0]) * p_norm)
                g = int(c1[1] + (c2[1] - c1[1]) * p_norm)
                b = int(c1[2] + (c2[2] - c1[2]) * p_norm)
            else:
                # Transición del 75% al 100% (De C2 a C3)
                p_norm = (p - 0.75) / 0.25
                r = int(c2[0] + (c3[0] - c2[0]) * p_norm)
                g = int(c2[1] + (c3[1] - c2[1]) * p_norm)
                b = int(c2[2] + (c3[2] - c2[2]) * p_norm)

            # Dibujamos una línea horizontal del color calculado
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Convertimos la imagen generada a algo que Tkinter entienda y la ponemos de fondo
        self.bg_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        
        # Dibujamos el título directo en el fondo para que no tenga cuadros feos
        self.canvas.create_text(425, 40, text="RENTA DE AUTOS", font=("Arial", 26, "bold"), fill="#111111")

    def crear_interfaz_sobre_canvas(self):
        # TARJETA IZQUIERDA: Vehículos Disponibles
        left_frame = ctk.CTkFrame(self.canvas, fg_color="#222222", corner_radius=18, width=380, height=480)
        left_frame.pack_propagate(False) #tamaño fijo
        self.canvas.create_window(30, 80, anchor="nw", window=left_frame)

        lbl_vehiculos = ctk.CTkLabel(left_frame, text="Vehículos Disponibles", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        lbl_vehiculos.pack(pady=20)

        self.vehiculo_seleccionado = ctk.StringVar(value="")

        # Generar radiobuttons dinámicos
        # self.catalogo es lo que nos envio el server
        for clave, vehiculo in self.catalogo.items():
            texto_info = f"{vehiculo['nombre']}\nCupo: {vehiculo['cupo']}\nCosto: ${vehiculo['costo']} por día\nDisp: {vehiculo['dias_disp']}"
            
            rb = ctk.CTkRadioButton(
                left_frame, 
                text=texto_info, 
                variable=self.vehiculo_seleccionado, 
                #value es el valor que se asignará a self.vehiculo_seleccionado cuando este radiobutton esté seleccionado, en este caso la clave del vehículo (ej. "auto_4puertas")
                value=clave,
                font=ctk.CTkFont(size=14),
                text_color="#D9D9D9",
                fg_color="#91A1A7", 
                hover_color="#737373"
            )
            rb.pack(anchor="w", padx=30, pady=15)

        # ==========================================
        # TARJETA DERECHA: Datos del Usuario
        right_frame = ctk.CTkFrame(self.canvas, fg_color="#222222", corner_radius=18, width=380, height=480)
        right_frame.pack_propagate(False)
        self.canvas.create_window(440, 80, anchor="nw", window=right_frame)

        lbl_datos = ctk.CTkLabel(right_frame, text="Datos", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        lbl_datos.pack(pady=(20, 5))

        lbl_instruccion = ctk.CTkLabel(right_frame, text="Ingrese los datos solicitados", font=ctk.CTkFont(size=12), text_color="#B3BDC0")
        lbl_instruccion.pack(anchor="w", padx=30, pady=(0, 15))

        # --- Nombre ---
        ctk.CTkLabel(right_frame, text="Nombre", font=ctk.CTkFont(size=14), text_color="white").pack(anchor="w", padx=30)
        #self.entry_nombre es el campo de texto donde el usuario ingresará su nombre, lo guardamos como atributo para poder acceder a su valor luego cuando se presione el botón de solicitar
        self.entry_nombre = ctk.CTkEntry(right_frame, placeholder_text="Ej. Pepito", fg_color="#1A1A1A", border_color="#555555", text_color="white", width=320)
        self.entry_nombre.pack(padx=30, pady=(0, 15))

        # --- Pasajeros ---
        ctk.CTkLabel(right_frame, text="Número de pasajeros", font=ctk.CTkFont(size=14), text_color="white").pack(anchor="w", padx=30)
        self.entry_pasajeros = ctk.CTkEntry(right_frame, placeholder_text="Ej. 2", fg_color="#1A1A1A", border_color="#555555", text_color="white", width=320)
        self.entry_pasajeros.pack(padx=30, pady=(0, 15))

        # --- Días de Renta (Checkboxes) ---
        #.pack(anchor="w", padx=30) para que el label quede alineado a la izquierda con un margen de 30 píxeles
        ctk.CTkLabel(right_frame, text="Días de Renta", font=ctk.CTkFont(size=14), text_color="white").pack(anchor="w", padx=30, pady=(5, 5))
        # Creamos un frame para contener los checkboxes de los días, esto nos ayudará a organizarlos mejor y a posicionarlos debajo del label
        dias_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        dias_frame.pack(fill="x", padx=30)

        dias_semana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        #{} diccionario para guardar las variables asociadas a cada checkbox, la clave será el nombre del día y el valor será la variable StringVar que indica si ese día está seleccionado o no
        self.variables_dias = {}

        for i, dia in enumerate(dias_semana):
            var = ctk.StringVar(value="off")
            #aqui guardamos la variable asociada a ese día en el diccionario para luego poder revisar cuáles días fueron seleccionados cuando se presione el botón de solicitar
            self.variables_dias[dia] = var
            #hacemos el checkbox
            cb = ctk.CTkCheckBox(
                #.capitalize() para que el texto del día se vea con la primera letra mayúscula
                #onvalue="on" significa que cuando el checkbox esté seleccionado, la variable asociada (var) tomará el valor "on", y offvalue="off" significa que cuando no esté seleccionado, la variable tomará el valor "off"
                #inicia en off 
                #y cuando se presione el botón de solicitar, revisaremos cuáles variables tienen el valor "on" para saber qué días seleccionó el usuario
                dias_frame, text=dia.capitalize(), variable=var, onvalue="on", offvalue="off",
                text_color="#D9D9D9", fg_color="#91A1A7", hover_color="#737373"
            )
            cb.grid(row=i % 4, column=i // 4, sticky="w", padx=(0, 15), pady=5)

        # --- Botón Solicitar ---
        btn_solicitar = ctk.CTkButton(
            right_frame, text="Solicitar Auto", font=ctk.CTkFont(size=17, weight="bold"),
            fg_color="transparent", border_width=1, border_color="#737373", text_color="white",
            hover_color="#333333", command=self.enviar_solicitud, width=320, height=50
        )
        # Lo posicionamos hasta abajo de la tarjeta
        btn_solicitar.pack(side="bottom", pady=20)

    def enviar_solicitud(self):
        #obtenido de la linea usuario = self.entry_nombre.get().strip() y las siguientes, aquí estamos obteniendo los datos ingresados por el usuario en la interfaz para luego enviarlos al servidor
        usuario = self.entry_nombre.get().strip()
        print(f"Usuario ingresado: '{usuario}'")
        #obtenido de la linea tipo_vehiculo = self.vehiculo_seleccionado.get() y las siguientes, aquí estamos obteniendo los datos ingresados por el usuario en la interfaz para luego enviarlos al servidor
        tipo_vehiculo = self.vehiculo_seleccionado.get()
        print(f"Tipo de vehículo seleccionado: '{tipo_vehiculo}'")
        #lo mismo
        pasajeros_txt = self.entry_pasajeros.get().strip()
        print(f"Número de pasajeros ingresado: '{pasajeros_txt}'")
        #aquí estamos revisando cuáles días fueron seleccionados por el usuario, recorriendo 
        # el diccionario de variables de los días y guardando en una lista los nombres de los días que tienen

        dias_seleccionados = [dia for dia, var in self.variables_dias.items() if var.get() == "on"]
        #obtenemos la cantidad de dias por la longitud de la lista de días seleccionados, por ejemplo si el usuario seleccionó lunes, miércoles y viernes, entonces dias_seleccionados tendrá 3 elementos y cantidad_dias será 3
        cantidad_dias = len(dias_seleccionados)
        print(f"Días seleccionados: {dias_seleccionados} (Cantidad: {cantidad_dias})")
        #quitar espacios y poner en minúscula para que el formato sea consistente, por ejemplo "Lunes, Martes" se convertirá en "lunes, martes"
        dia_semana_str = ", ".join(dias_seleccionados)

#validaciones antes de enviar al server
        if not usuario:
            messagebox.showwarning("Faltan datos", "Por favor ingresa tu nombre.")
            return
        if not tipo_vehiculo:
            messagebox.showwarning("Faltan datos", "Por favor selecciona un vehículo de la lista.")
            return
        if not pasajeros_txt.isdigit():
            messagebox.showwarning("Error", "El número de pasajeros debe ser un número entero.")
            return
        if cantidad_dias == 0:
            messagebox.showwarning("Faltan datos", "Por favor selecciona al menos un día de renta.")
            return

        ocupantes = int(pasajeros_txt)

        try:
            respuesta = self.renta_autos.solicitar_renta(usuario, tipo_vehiculo, ocupantes, cantidad_dias, dia_semana_str)
            
            if "Error" in respuesta or "Lo sentimos" in respuesta or "Que mal" in respuesta or "excedió" in respuesta:
                messagebox.showwarning("Respuesta del Servidor", respuesta)
            else:
                messagebox.showinfo("¡Éxito!", respuesta)
                self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error de Comunicación", f"Hubo un problema con el servidor:\n{e}")

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, ctk.END)
        self.entry_pasajeros.delete(0, ctk.END)
        for var in self.variables_dias.values():
            var.set("off")
        self.vehiculo_seleccionado.set("")

if __name__ == "__main__":
    dialogo_inicial = ctk.CTk()
    dialogo_inicial.withdraw() 
    
    dialogo = ctk.CTkInputDialog(text="Pega la URI del servidor PYRO:", title="Conexión al Servidor")
    uri_ingresada = dialogo.get_input()
    
    dialogo_inicial.destroy()
    if uri_ingresada:
        app = AplicacionRentaAutos(uri_ingresada)
        app.mainloop()
    else:
        print("No se ingresó ninguna URI. Cerrando.")