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

`/etc/hostapd/hostapd.conf`
```
country_code=US
interface=wlan0
ssid=HoneyPot
hw_mode=g
channel=7
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=xijinping
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```


Climate

Pizza mode on?
0000   55 43 05 2a 14 32 19 19 19 19 21                  UC.*.2....!

Reply
0000   55 52 da 00 14 01 e1 00 05 2a 14 32 19 19 19 19   UR.......*.2....
0010   0b 01 00 00 ff ff ff ff 00 00 00 00 00 00 01 00   ................
0020   03 64 00 03                                       .d..


Pizza mode off?
0000   55 43 05 0a 14 32 19 19 19 19 21                  UC...2....!
             ^^^^^^^^^^^^^^^^^^^^^^^
                bytes 2-9 repeated in reply

Reply
0000   55 52 da 00 16 01 e1 00 05 0a 14 32 19 19 19 19   UR.........2....
                               ^^^^^^^^^^^^^^^^^^^^^^^
                                ...as bytes 8-15
0010   0b 01 00 00 ff ff ff ff 00 00 00 00 00 00 01 00   ................
0020   03 64 00 03                                       .d..
