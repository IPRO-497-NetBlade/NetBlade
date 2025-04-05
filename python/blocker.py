import sys, requests, subprocess
from win10toast import ToastNotifier

# constants
hosts_file = "C:\\Windows\\System32\\drivers\\etc\\hosts"
start = "# Added by NetBlade"
end = "# End of NetBlade section"


# functions

def add_rules(ip_list):

    for ip in ip_list:
        if(ip) != ("dist_ip"):
            rule = f"netsh advfirewall firewall add rule name='BadIP, added by NetBlade' Dir=Out Action=Block RemoteIP={ip}"
            subprocess.run(["Powershell", "-Command", rule])


def delete_rules():
  rule = "netsh advfirewall firewall delete rule name='BadIP, added by NetBlade'"
  subprocess.run(["Powershell", "-Command", rule])


def hostsWrite(hosts, hosts_path):

    with open(hosts_path, 'a') as file:
        file.write(start + "\n")

        for domain in hosts:
            file.write(domain + "\n") 
        file.write(end + "\n")

    print("Finished writing", flush=True)
  

def hostsRemove(hosts_path):

  with open(hosts_path, 'r') as f:
    lines = f.readlines()

  new_lines = []
  skip = False

  for line in lines:
    if line.strip() == "# Added by NetBlade":
      skip = True
      continue
    if skip:
      if line.strip() == "# End of NetBlade section":
        skip = False
      continue
    new_lines.append(line)
  
  with open(hosts_path, 'w') as f:
    f.writelines(new_lines)


def my_print(str):
    print('Python    : "' + str + '"', flush=True)  # Add flush=True here


# code

toast = ToastNotifier()

toast.show_toast(
   "Starting",
   "NetBlade is blocking domains and IPs",
   duration=2,
   icon_path= "netBlade-logo.ico",
   threaded=True
)

hosts_response = requests.get("https://raw.githubusercontent.com/Ultimate-Hosts-Blacklist/Ultimate.Hosts.Blacklist/refs/heads/master/hosts.windows/hosts0.windows")
ip_response = requests.get("https://raw.githubusercontent.com/Ultimate-Hosts-Blacklist/Ultimate.Hosts.Blacklist/refs/heads/master/ips/ips0.list")

hosts_lines = [line.strip() for line in hosts_response.text.splitlines() if line.strip() and not line.strip().startswith(('#', '127.0.0.1 localhost', '255.255.255.255 broadcasthost', '::1 localhost'))]
ip_lines = ip_response.text.splitlines()

domains_blacklist = hosts_lines[:10]
ip_blacklist = ip_lines[:10]

my_print('Spawned from within electron (js)')
add_rules(ip_blacklist)
hostsWrite(domains_blacklist, hosts_file)

toast.show_toast(
   "Done",
   "NetBlade finished blocking domains and IPs",
   duration=10,
   icon_path="netBlade-logo.ico",
   threaded=True
)


while True:
    line = sys.stdin.readline().strip()

    if line == "terminate":
        my_print('I got a terminate request from electron (js)...terminating')
        toast.show_toast(
           "Terminating",
           "NetBlade has been stopped",
           duration=5,
           icon_path="netBlade-logo.ico",
           threaded=True
        )
        exit(0)
    elif line == "":
        my_print('Terminating as there is no data given...terminated')
        exit(0)
    else:
        my_print('I got string: "' + line + '", from electron (js)')
