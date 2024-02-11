# arpoison
ARP cache poisoning


### Usage
```
usage: arpoison [-h] -t TARGET -g GATEWAY [-gmac GMAC] [-tmac TMAC]
								[-i IFACE]

ARP cache poisoning between target and gateway. Quit with Ctrl+C

options:
	-h, --help  show this help message and exit
	-t TARGET   target IP address
	-g GATEWAY  gateway IP address
	-gmac GMAC  gateway MAC address
	-tmac TMAC  target MAC address
	-i IFACE    specify network interface
```


### Packet forwarding
On linux
```
$ echo 1 > /proc/sys/net/ipv4/ip_forward
```
