Home Server TODOs
---
- [ ] Services
  - [ ] Ansible (From Ansible-NAS)
    - [ ] Docker
      - [x] Nextcloud
      - [x] Jellyfin
      - [ ] Calibre Web
      - [x] Reverse proxy (Traefik)
      - [ ] Torrent Downloader
      - [x] Watchtower
      - [x] Portainer
      - [x] Netdata
      - [x] Heimdall
      - [ ] Jackett
      - [x] Guacamole
      - [x] Cloudflare DDNS
      - [x] Duplicati
      - [ ] Home Assistant
      - [ ] Pi-hole
  - [ ] VMs:
    - [x] TrueNAS
    - [ ] PfSense
    - [ ] Security
    - [ ] Linux Server 
      - [ ] Pivpn with Wireguard
      - [ ] All the Ansible-NAS stuff
      - [ ] Docker(-Compose):
        - [ ] Jitsi
        - [ ] Calibre
        - [ ] Piwigo/Image Server
        - [ ] Document Management (Mayan or Teedy)
- [ ] Servers
  - [ ] Rack system
    - [ ] Proxmox
    - [x] Name it
    - [x] Buy 2 1TB SAS drives
    - [ ] Dual gigabit network card
    - [ ] PCIe -> SATA card
  - [ ] Precision tower
    - [x] Name it
    - [ ] Proxmox
      - [x] TrueNAS (VM)
      - [ ] Proxmox Backup Server (VM)
    - [x] 2 4TB HDDs for TrueNAS
- [ ] Roadmap
  - [x] Set up services on TGP
  - [ ] Move services to Hogwarts
  - [ ] Torrenting stuff 


Welcome to the PaynePride home server notes page!
Here is where I keep track of set-up notes, known technical challenges, reset notes, etc.

**Services accessible via the Heimdall dashboard**

## Services
- Nextcloud
- Portainer
- Jellyfin
- Pi-hole
- Piwigo (image gallery)
- VPN (wireguard)
- Duplicati
- Heimdall
- Watchtower
- Guacamole
- Cloudflare DDNS

- Home Assistant
- Netdata
- Jackett

### TrueNAS
Hogwarts runs our main TrueNAS instance with regular replication tasks to a backup on Twelve Grimmauld Place. The main instance consists of 5 1TB SAS drives in a Raid-Z2 configuration. The backup consists of 2 4TB drives in a ZFS mirror.

TrueNAS also takes nightly snapshots of all the ZFS datasets. We have datasets set up so that backups are somewhat organized.

### Jellyfin
Jellyfin is our home media server. Brought up in Docker

### Pi-hole
Network wide ad blocking. [Pi-hole](https://pi-hole.net/).
Pi Hole is running in a VM on the FreeNAS box (see ip in table). It is also set up as a recursive DNS server using unbound.

### VPN
Codename `nightshade`. 
VPN was setup with [pivpn](https://docs.pivpn.io/)

```bash
Backup created in /home/nic/pivpnbackup/20210416-160700-pivpnwgbackup.tgz
To restore the backup, follow instructions at:
https://github.com/pivpn/pivpn/wiki/WireGuard#how-can-i-migrate-my-configs-to-another-pivpn-instance
```

| Ip Address | | 
| --- | --- | 
| **Device** | **IP** |
| HP Laptop | 10.6.0.5 | 
| Dad's Raspberry Pi (Jellyfin) | 10.6.0.7 |
| Nic's Phone | 10.6.0.4 | 
| RyzenRender | 10.6.0.3 | 
| Lenovo Miix | 10.6.0.2 | 

### Cloudflare
~~The Dynamic DNS service is actually solved by using [this repo](https://github.com/adrienbrignon/cloudflare-ddns.git) where the Python script runs on the Nginx container.~~
Cloudflare DDNS Docker service runs on Dumbledore's Army

### Jitsi
**Will be** hosted in Ubuntu VM in docker-compose.

### Dad's Jellyfin Server
Run on Raspberry Pi 3
Users: `pi`, `jellyfin`
Passwords: dad's new password with Julie
Accessed via Wireguard
  - SSH into Wireguard server at 192.168.1.111
  - Jump to pi at 10.6.0.7 with `ssh pi@10.6.0.7` 
The Wifi is setup in `/etc/wpa_supplicant` and static ip in `/etc/dhpcdp.conf`

## Proxmox
1. `apt-get` by default wil go to the pve.enterprise repos so we need to point it to the non-enterprise ones.
```
rm /etc/apt/sources.list.d/pve-enterprise.list
vim /etc/apt/sources.list.d/pve-no-subscription.list
# add deb http://download.proxmox.com/debian/pve buster pve-no-subscription
```
2. new storage are added disabled - so you have to enable each new storage when added
3. Need to grab a few utilities on a new install
  - cifs-utils
  - 

TODOs
0a. Add mounts to fstab or something
2a. restructure libraries
4. migrate pihole
5. migrate pivpn
  ** add wireguard to kassia's phone for local nextcloud connection when traveling

NOTES
1. VM needs cifs utils and other things set up before ansible can deploy services
2. for ansible to deploy docker services into VM then the VM user needs to mount the TrueNAS shares like this
3. Make sure `ansible_nas_user` has a home directory with `nas` as a sub directory that the user can mount all the TrueNAS shares to
```
 sudo mount -t cifs -o username=${USER},password=PASSWORD,uid=$(id -u),gid=$(id -g) //192.168.1.24/nas /home/${USER}/nas
```

note - precision upgarde to 225GB
0. install proxmox onto new ssd - done
1. install truenas - don't start it - done
2. hopefully pass through non-formatted discs and import them directly to new install - done
2a. if fails then format disks, pass through by id, and replicate back from freenas
2b. setup truenas backup - use cloud sync task and figure s3 out
3. stand up dumbledore's army with everything except transmission and jackett - done
4. configure nextcloud - doneish
5. configure jellyfin? - doneish
7. create template vm
8. stand up quidditch pitch - done
9. get torrent/jackett stuff working with toy dataset in truenas (new temp smb share)
10. clean up lan entries in keepass (consider moving this to nextcloud with the Keepweb app)
quidditch-pitch 192.168.1.50
oliver wood
wood@quidditch-pitch.local


notes on setting up DA for ansible-nas deployment
1. make admin account dumbledore
2. make user accounts - I chose potter and the ansible_nas_user who is neville
- set ansible nas user's UID and GID to be the same on trueNAS and DA
3. make sure ssh works for all users
4. for neville mount the smb shares to ~/nas
```
 sudo mount -t cifs -o username=${USER},password=PASSWORD,uid=$(id -u),gid=$(id -g),forceuid,forcegid,noperm //192.168.1.24/nas /home/${USER}/nas
```
> I took away the $() stuff and just wrote neville and 1005

neville only needs modify permissions on nas/sandbox to mount
