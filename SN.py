#Respaldos Masivos para GW Cisco
from netmiko import ConnectHandler

with open('gws.txt') as routers:
    for IP in routers:
        Router = {
            'device_type': 'cisco_ios',
            'ip': IP,
            'username': 'redefonia',
            'password': 'R3d3fonia'
        }

        net_connect = ConnectHandler(**Router)

        hostname = net_connect.send_command('show run | i host') # Imprimir el hostname 
        hostname.split(" ")
        hostname,device = hostname.split(" ")
        print ("Sacando inventario(S/N) de: " + device)

        filename = '/Users/Saul Esparsa/Desktop/Respaldos-GW/' + device + '.txt' # Ruta donde se guardan los respaldos + nombre de carpeta .txt
        # para guardar la copia de seguridad en la misma carpeta que el script, use la línea de abajo y comente la línea de arriba 
        # filename = device + '.txt' 

        showrun = net_connect.send_command('show run | i host')
        showver = net_connect.send_command('show ver | include Processor')#Envio de comandos con configuracion respaldada 
        log_file = open('respaldos.txt', 'a')   # Adjuntar todos los rachivos 
        log_file.write(showrun)
        log_file.write("\n")
        log_file.write(showver)
        log_file.write("\n")

# Termina la conexion 
net_connect.disconnect() 