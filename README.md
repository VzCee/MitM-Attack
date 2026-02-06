##  MitM Using Protocol ARP
- Este proyecto está basado en una práctica realizada con fines educativos, en la cual realizamos un ataque de Man-in-the-Middle (MitM) mediante ARP Spoofing utilizando un script basado en Scapy en el lenguaje Python.


## Función Del Script
- Este script de Python utiliza la librería scapy para realizar un ataque de ARP Spoofing. El objetivo es posicionarse como un "hombre en el medio" entre una víctima y el gateway de la red. Al lograrlo, todo el tráfico entre la víctima e Internet pasará a través de la máquina del atacante, permitiendo su escucha, manipulación o filtrado.

## Video de Demostracion

- **https://youtu.be/x_7e8e8Rmms**

## Topologia en PNETLab
<img width="536" height="553" alt="image" src="https://github.com/user-attachments/assets/b888fd6e-2f8e-496f-a4b4-092bfa749b67" />

**En la topologia utilizamos las siguientes conexiones en la topologia;**
##Router conexion hacia el **Switch** e0/0 > e0/0
- **Router**

Conexion hacia el **Switch** e0/0 > e0/0

Conexion hacia el **Net** > e0/0


- **Atacante**
Conexión con **Net** > etho1

Conexión con **Switch** etho0 > e0/1


- **Victima**
Conexión con **Switch** etho0 > e0/2




## Configuración del Script
- El script no utiliza parámetros de línea de comandos. La configuración se realiza editando directamente las siguientes variables al inicio del archivo arp_spoof.py:

`VICTIMA_IP = "23.72.0.3"`

`GATEWAY_IP = "23.72.0.1"`

`INTERFACE = "eth0"`


## Requisitos para utilizar la herramienta
- Python 3.8+
- Librería `scapy`
- Acceso a internet
- Acceso root o privilegios de administrador para manipular paquetes de red.

## Medidas de mitigación
- Static ARP Entries: Configurar entradas ARP estáticas en dispositivos críticos.

- Dynamic ARP Inspection (DAI): Habilitar en switches para validar paquetes ARP.

- Monitoreo de red: Detectar anomalías en tráfico ARP.

- Cifrado: Usar HTTPS, SSH o VPNs para proteger datos incluso si el atacante intercepta el tráfico.

- Firewalls y control de acceso: Limitar ejecución de scripts no autorizados y monitorear logs.


