<<<<<<< HEAD

<h1 align="center">🚗 Sistema de Renta de Autos con RMI (Pyro) 🚗</h1>

<p align="center">
<b>Proyecto para la materia de <i>Sistemas de Cómputo Paralelo y Distribuido</i></b><br>
Simulación de renta de autos usando llamadas remotas RMI/RPC en Python con Pyro5.
</p>

---

## Conceptos Clave

### RPC (Remote Procedure Call)
Permite que un cliente ejecute funciones en un servidor remoto como si fueran locales. El cliente espera la respuesta del servidor (llamada síncrona). Ideal para funciones rápidas y directas.

### RMI (Remote Method Invocation)
Permite invocar métodos de objetos que residen en otro servidor (por ejemplo, usando Pyro en Python). Permite transferir objetos complejos, no solo datos simples.

---

## 📝 Actividad
Implementa un sistema de renta de autos para el mes de marzo usando llamadas RPC o RMI. El sistema debe:

- Permitir al usuario rentar diferentes tipos de vehículos:
  - **Auto 4 puertas**
  - **Camioneta 4 puertas**
  - **Camioneta 3 puertas**
  - El usuario proporciona la cantidad de ocupantes y los días a rentar.
- El servidor debe mostrar los tipos de vehículos, sus características (cupo, costo, días disponibles), recibir solicitudes de al menos 3 usuarios y verificar:
  - Disponibilidad del vehículo
  - Que no se exceda el cupo máximo
  - Que los días solicitados estén disponibles
  - Confirmar la renta y calcular el monto a pagar
- Un usuario puede rentar hasta 3 vehículos.

### Tabla de Vehículos Disponibles

| Vehículo              | Cupo Máx. | Costo por Día | Unidades Disponibles | Días Disponibles     |
|-----------------------|-----------|---------------|---------------------|---------------------|
| Auto 4 puertas        | 4         | $600          | 5                   | Lunes a Domingo     |
| Camioneta 4 puertas   | 5         | $750          | 5                   | Martes a Domingo    |
| Camioneta 3 puertas   | 10        | $1200         | 3                   | Lunes a Domingo     |

---

## ⚙️ Ejecución

1. **Instalar herramienta de entornos virtuales:**
  ```bash
  sudo apt update
  sudo apt install python3-venv
  ```
2. **Crear el entorno virtual (llamado `entorno_dist`):**
  ```bash
  python3 -m venv entorno_dist
  ```
3. **Activar el entorno:**
  ```bash
  source entorno_dist/bin/activate
  ```
4. **Instalar Pyro5:**
  ```bash
  pip install Pyro5
  ```
=======
# Llamada-Remota-Distribuida
Llamadas RCP y RMI, esta llamada es RMI con Pyro5 de Python, es de la clase "Computo paralelo y distribuido" 8°Semestre
>>>>>>> dee7ad6e95769935dd57b38ddb9b72227ccb372c
