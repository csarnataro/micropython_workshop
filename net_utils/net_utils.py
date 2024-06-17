import json
import network
import time
import binascii

'''
1000 STAT_IDLE – no connection and no activity,
1001 STAT_CONNECTING – connecting in progress,
 202 STAT_WRONG_PASSWORD – failed due to incorrect password,
 201 STAT_NO_AP_FOUND – failed because no access point replied,
 203 STAT_ASSOC_FAIL/STAT_CONNECT_FAIL – failed due to other problems,
1010 STAT_GOT_IP – connection successful.
'''
NETWORK_CACHE_LIFE = 10
NETWORK_CONFIG_FILE = 'network_config.json'
ssid = b'insert_wifi_ssid_here'
key = b'insert_wifi_password_here'

net_if = None

net_config = {
  "ap":{},
  "known_networks":[]
}

net_entry = {
  "name":b'',
  "mac": b'',
  "key": b''
}

local_networks_cache = {
  'last_scan': 0,
  'networks': []
}

def init_if(network_interface = None):
  global net_if
  interface = None
  if network_interface == None:
    interface = network.WLAN(network.STA_IF)
  else:
    interface = network_interface

  interface.active(False)
  interface.active(True)
  net_if = interface
  return interface

def set_ap_config(ssid, key):
  pass

def init_ap(ssid, key):
  global net_if, net_config
  if net_if != None:
    net_if.active(False)
  net_if = network.WLAN(network.AP_IF)
  
  net_if.active(True)
  net_if.config(ssid=ssid, security=network.AUTH_WPA2_PSK, key=key)
  net_config['ap'] = {'ssid': ssid, 'key': key}

def get_network_index(network_name):
  if type(network_name) == str:
    network_name = str.encode(network_name)
  networks_list = local_networks_cache['networks']
  result = list(filter(lambda m:networks_list[m][0] == network_name, range(len(networks_list))))
  if len(result) > 0:
    return result[0]
  else:
    return None

def get_ap_settings():
  try:
    ssid = net_config['ap']['ssid']
    key = net_config['ap']['key']
    return ssid, key
  except KeyError:
    return None
  # return net_config['ap']['ssid'], net_config['ap']['key']

def auto_connect():
  init_if()
  load_network_config()
  local_list = scan()
  known_list = net_config['known_networks']
  print(local_list)
  print(known_list)

def scan(force_scan = False):
  if net_if == None:
    init_if()
  now = time.mktime(time.localtime())
  if now - local_networks_cache['last_scan'] < NETWORK_CACHE_LIFE and force_scan == False:
    return local_networks_cache['networks']
  networks_list = net_if.scan()
  networks_list.sort(key=lambda tup:tup[0])
  
  # global local_networks_cache
  local_networks_cache['networks'] = networks_list
  local_networks_cache['last_scan'] = time.mktime(time.localtime())
  return networks_list


def list_networks(rescan = False):
  scan(rescan)
  list_scan_results()

def list_scan_results():
  for i, n in enumerate(local_networks_cache['networks']):
    mac = binascii.hexlify(n[1], ':')
    print(f'{i:>2}: {(n[0]).decode('utf-8'):<20} [{mac}]')

def connect_to_scan_result(id):
  networks_list = local_networks_cache['networks']
  ssid = networks_list[id][0]
  print(f'Connect to {ssid.decode('utf-8')}')
  key = input('Password:')
  print(key)
  conn = connect(ssid, key, display_progress = True)
  print(f'connection: {conn}')
  if conn == network.STAT_GOT_IP:
    store_net_entry(id, key)


def connect(ssid = ssid, key = key, interface = None, timeout = 10, display_progress = False):
  '''
  if no ssid/key are provided
  load saved configuration
  load_network_config()
  then scan network
  and check if any of the saved networks matches
  match b'MAC' first, b'NAME' after, since name might have changed
  
  '''
  time.sleep_ms(500)
  global net_if
  if interface == None:
    net_if = init_if()
  else:
    net_if = interface

  net_if.active(False)
  time.sleep_ms(100)
  net_if.active(True)
  time.sleep_ms(100)
  
  net_if.connect(ssid, key)
  connection_attempt_start_time = time.time()
  if display_progress:
    print()
    print(f"Connecting to {ssid}")
  max_dot_cols = 20
  dot_col = 0

  # originally `not_used()` function was here
  
  if display_progress:
    print() 
    print(f'{"C" if net_if.isconnected() else "NOT c"}onnected to network')
    if net_if.isconnected():
      print(f'Connected to {ssid}')
      print_network_details(net_if)
    else:
      net_if.active(False)
      print(f'Connection to {ssid} failed [code {connection_status}]')
  return connection_status


def not_used():  
  pass ## on my home router this doesn't seem to work, so i'm just returning here hoping the connection is fine
  while net_if.status() == 'network.STAT_IDLE':
    pass
  connection_status = network.STAT_CONNECTING
  while connection_status == network.STAT_CONNECTING:
    # Network Connection Progress
    connection_status = net_if.status()
    if display_progress:
      if(dot_col % max_dot_cols == 0):
          print()
      print('.', end = '')
      dot_col +=1
      if time.time() - connection_attempt_start_time > timeout:
        break
      time.sleep_ms(300)

  if display_progress:
    print() 
    print(f'{"C" if net_if.isconnected() else "NOT c"}onnected to network')
    if net_if.isconnected():
      print(f'Connected to {ssid}')
      print_network_details(net_if)
    else:
      net_if.active(False)
      print(f'Connection to {ssid} failed [code {connection_status}]')
  return connection_status

def print_network_details(interface):
  network_details = interface.ifconfig()
  mac_address = binascii.hexlify(interface.config('mac'), ':')
  print(f'MAC: {mac_address}')
  print(f'IP: {network_details[0]}')
  print(f'Subnet: {network_details[1]}')
  print(f'Gateway: {network_details[2]}')
  print(f'DNS: {network_details[3]}')


def store_net_entry(id, key):
  # TODO: checks against MAC and updates name/pwd if necessary
  networks_list = local_networks_cache['networks']
  net_info = networks_list[id]
  nec = net_entry.copy()
  nec['name'] = net_info[0].decode('utf-8')
  nec['mac'] = binascii.hexlify(net_info[1])
  nec['key'] = key
  net_config['known_networks'].append(nec)
  save_network_config()
  return nec

def save_network_config():
  # fails when field is b''
  try:
    with open(NETWORK_CONFIG_FILE, 'w', encoding = 'utf-8') as f:
      return json.dump(net_config, f, separators=(',', ':'))
  except OSError as e:
    return None

def load_network_config():
  global net_config
  try:
    with open(NETWORK_CONFIG_FILE, 'r') as f:
      net_config = json.load(f)  
  except OSError as e:
    pass
  return net_config

# TODO
# encrypt passwords for stored network credentials
# use encryption function with a 4-6 numeric PIN to decrypt

