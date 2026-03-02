from scapy.all import ARP, Ether, srp

# Укажите ваш диапазон сети (например, 192.168.1.0/24)
target_ip = "192.168.1.0/24"
# arp = ARP(pdst=target_ip)
# ether = Ether(dst="ff:ff:ff:ff:ff:ff")
# packet = ether/arp
# result = srp(packet, timeout=3, verbose=0)[0]
result = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=target_ip), timeout=3, verbose=0)[0]

devices = []
for _, received in result:
    devices.append({'ip': received.psrc,'mac': received.hwsrc})

for device in devices:
    print(f"IP: {device['ip']},\tMAC: {device['mac']}")