# Devices

Questa è una lista non esaustiva dei dispositivi smart che utilizzo quotidianamente. Sono stati tutti integrati all'interno di Home Assistant, mediante le configurazioni che trovate in questa _repository_.

> Tutti i link inseriti sono sponsorizzati [Saggiamente](https://www.saggiamente.com/categoria/smarthome/).

## Luci

* [**Philips Hue**](https://saggiolink.it/2Rd17Pz)
* [**Koogeek Smart Socket**](https://saggiolink.it/2Re0Lbl)
* [**Koogeek Smart Light**](https://saggiolink.it/2RamMrJ)
* [**Plafoniera Yeelight YLXD01YL**](https://saggiolink.it/2R3wJqG)

## Gateways

* [**Gateway**](https://saggiolink.it/2RdWBAk)
* [**ConBee di Dresden Elektronik**](https://saggiolink.it/2RjrOC4)

### _Ecosistema_ Xiaomi

* [**Sensori temperatura e umidità**](https://saggiolink.it/2RiIOs4)
* [**Sensori movimento e vibrazione**](https://saggiolink.it/2RanRzN)
* [**Sensori porta-finestra Aqara**](https://saggiolink.it/2GEsHBb)
* [**Sensori di movimento**](https://saggiolink.it/2Re2hKz)
* [**Sensore di presenza acqua Aqara**](https://saggiolink.it/2GzztIf)
* [**Rilevatore fumo Xiaomi Honeywell**](https://saggiolink.it/2RdXM2I)
* [**Smart Buttons Xiaomi**](https://saggiolink.it/2RaW1U0)
* [**Smart Plug Xiaomi**](https://saggiolink.it/2Rhsbgz)

## Switches

* [**Smart Plug TP-Link HS110**](https://saggiolink.it/2ReLuHb)
* [**ITEAD Sonoff Basic**](https://saggiolink.it/2RiijDe)

## Altro

* [**NodeMCU ESP8266 Development Board**](https://saggiolink.it/2RapptB)
* [**Scheda di Sviluppo ESP32 ESP-WROOM-32**](https://saggiolink.it/2RmcqoR)
* [**Programmatore Seriale USB DSD Tech**](https://saggiolink.it/2Re9PwP)
* [**KIT Sensori per Arduino ed ESP**](https://saggiolink.it/2RggfvB)
* [**Aspirapolvere Neato D3 Connected**](https://saggiolink.it/2RejWSl)
* [**Ip Camera Foscam C2**](https://saggiolink.it/2RkDuVu)

Come server domestico utilizzo un [Intel NUC6i3SYH](https://nucblog.net/2016/01/skylake-nuc-review-nuc6i3syh-core-i3/) con 16 GB di RAM, 120 GB di SSD M2 ed una scheda di rete USB 3 aggiuntiva. [Proxmox](https://www.proxmox.com/en/) come sistema operativo mi permette di gestire alcune VM, tra cui:

* [pfSense](https://www.pfsense.org) che utilizzo come Firewall e router
* un sistema Linux [Debian](https://www.debian.org) con [Docker](https://www.docker.com), su cui tra gli altri gira il container ufficiale di [Home Assistant per amd64](https://diyfuturism.com/index.php/2018/03/20/pi-to-nuc-part-1-migrating-hass-io-to-a-virtual-machine-proxmox-docker/)
* una minuscola VM sempre a base Debian, creata con lo scopo di far girare degnamente [Pi-hole](https://pi-hole.net).

Chiudono la fila un Access Point [Ubiquiti UAP-AC-LITE](https://saggiolink.it/2ReaVZt), un modem [D-Link DSL-320B](https://saggiolink.it/2RaqlhB) e uno switch _managed_ [Netgear GS108E-300PES](https://saggiolink.it/2RebUsR) che utilizzo per creare una VLAN IoT separata.