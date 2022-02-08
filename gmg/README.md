# Green Mountain Grill

## Reverse Engineering

Tried to use other repos to figure it out, but not sure how they're connecting. Going to see if I can use a RasPi as an AP and just sniff all traffic.


```
sudo apt-get install -y dnsmasq hostapd
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
```

`/etc/dhcpd.conf`
```
interface wlan0
    static ip_address=192.168.142.1/24
    nohook wpa_supplicant
```

`/etc/dnsmasq.conf`
```
interface=wlan0
dhcp-range=192.168.142.100,192.168.142.120,255.255.255.0,24h
```
