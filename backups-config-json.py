import json 
import time 
from datetime import datetime
from netmiko import ConnectHandler
import concurrnet.futures
"""
this app will iterate over the devices.json file 
and try to backup the running configuration 
to a text file in a relative path to this script
"""
# Abrir archivo y cargar el archivo JSON al diccionario
with open ('devices.json') as f:
    read_data = f.read()
    devices = json.loads(read_data)
    

def worker (device):
    """fucnion del proceso worker"""
    try:
        #try to get and write the running configuration to a file
        host_name = device['ip']
        current_timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        file_name = 'host_{}_{}'.format(host_name, current_timestamp)
        
        # connect to devices using netmiko and sen IOS commands
        print('*** conectando a {} ***'.format(host_name))
        net_connect = ConnectHandler(**device)
        output = net_connect.send_command('terminal length 0')
        output = net_connect.send_command('show running-config')
        
        # open a text file and write the output to it
        with open('{}.txt'.format(file_name), 'a') as the_file:
            the_file.writelines(output)
        print('*** host {} *** saved as {}'.format(host_name, file_name))
      except Exception as e:
        # catch the errors and append them to file Backup_filed.txt
        print('*** {} ***'.format(e))
        with open('Backup_filed.txt', 'a') as the_file:
            the_file.writelines('{} - {}\n'.format(current_timestamp, str(e)))
            
            
# loop over the 'devices.json' file with ProcessPoolExecutor
start = time.time()
if _name_ == '_main_':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        [executor.submit(worker, device) for device in devices]
end = time.time()
print('#'*80)
print('*** it took {} seconds to complete the task***'.format(end - start))
            