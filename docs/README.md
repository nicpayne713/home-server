Home Server Note
---

Welcome to the PaynePride home server notes page!
Here is where I keep track of set-up notes, known technical challenges, reset notes, etc.

| Static Ip Address | | |
| --- | --- | --- |
| **Service** | **IP** | **Port** | 
| FreeNAS | [192.168.1.24](http://192.168.1.24) | | 
| Jellyfin | [192.168.1.235](http://192.168.1.235) | 8096 |
| Pi-hole | [192.168.1.123](http://162.168.1.123) | |
| Piwigo | [192.168.1.124](http://192.168.1.124) | |
| Nginx | [192.168.1.169](http://192.168.1.169) | |
| Ubuntu VM | [192.168.1.212](http://192.168.1.212) | |

| Public Service Access | | 
| --- | --- |
| **Service** | **URL** 
| Jellyfin | [movienight.paynepride.com](http://movienight.paynepride.com) | 
| Piwigo | [www.paynepride.com](http://www.paynepride.com) | 
| VPN | [omitted]() | 

>Note that the VPN service only has a CNAME so that wireguard doesn't have to have the public IP of the router changed all the time - it can just resolve it through the CNAME since Cloudflare always has the up-to-date public IP of our router via a Python script running in the Nginx container.

### Services
- Nextcloud
- Jellyfin
- Pi-hole
- Piwigo (image gallery)
- Nginx
- General Ubuntu VM
- VPN (wireguard)

### FreeNAS
The FreeNAS box runs the open source FreeNAS software and is the host for our cloud. Currently it is a simple ZFS mirror for our main data. There is another pool for the Piwigo gallery that uses its own HDD.
User accounts can be accessed with the root login under System/Users.

To hose our services publicly our router is set up with port-forwarding for port 80 and 443 to the Nginx IP where it handles all the reverse proxy stuff.

### Network on the FreeNAS
I set up all virtual machines ver similarly with the network configuration so that public facing services like Jellyfin and the Piwigo gallery can sit behind the Nginx reverse proxy. The iamge I've used for installin the Ubuntu 18.04 Server OS seems to have an issue with with network setup on installation but the steps to fix are pretty easy.

1. After a successful install be sure to remove the CD-ROM device with the FreeNAS devices GUI for the VM management.
2. Edit the `/etc/netplan/*.yaml` file so that it looks like this
    ```yaml
    network:
      version: 2
      ethernets:
        enp0s4:
          addresses: [192.168.1.{Static IP}/24]
          gateway4: 192.168.1.1
          nameservers:
            addresses: [8.8.4.4, 8.8.8.8]
    ```
   Then run `sudo netplan apply` and all should be right with the world

3. To set up a service to be accessible with `<service>.paynepride.com` then Nginx needs to be configured, and this is also pretty easy following the tutorials [here](https://linuxhint.com/nginx_reverse_proxy-2/)
    
    a. Add the CNAME service to Cloudflare
    >Note some services need to not use the Cloudflare proxy and only use DNS to be accessed properly. Jellyfin is set up at [movienight.paynepride.com](http://movienight.paynepride.com) and the VPN is setup at [nightshade.paynepride.com](http://nightshade.paynepride.com). Neither of these use the Cloudflare proxy because the home router public IP needs to be found by the services. For Piwigo and Nextcloud the cloudflare proxy does not get in the way though
    
    b. Create a <service>.conf file in `/etc/conf.d/`
    
    c. The file should look like this:
    
        ```
        <VirtualHost *:80>
         ServerAdmin nicpayne713@gmail.com
         DocumentRoot /var/www/html/{service}
         ServerName {service_name}.paynepride.com
         <Directory /var/www/html/{service}/>
            Options +FollowSymlinks
            AllowOverride All
            Require all granted
         </Directory>
    
         ErrorLog ${APACHE_LOG_DIR}/error.log
         CustomLog ${APACHE_LOG_DIR}/access.log combined
    
        </VirtualHost>
        ```
    
    d. Follow the tutorial on updating Certbox

### Jellyfin
Jellyfin is our home media server. It runs in an Ubuntu 18.04-Server VM running on the FreeNAS box. The movies are at `/mnt/movies` and the music is at `/mnt/music`. 
> Note that in the event of a power outage or anytime the FreeNAS box loses power for whatever reason, the volume mounts are lost. The data is not copied into the ZVOL, instead an NFS mount is used to the FreeNAS storage itself. If this connection is lost simply SSH in to the Jellyfin server, go to `/mnt` and run the two mount scripts with `. mount_movies.sh` and `. mount_music.sh`. Admin password is in the password manager.

### Pi-hole
Network wide ad blocking. [Pi-hole](https://pi-hole.net/).
This is running on my pi-zero W plugged in next the our router

### Nginx
Followed [this tutorial](https://linuxhint.com/nginx_reverse_proxy/)

### VPN
Codename `nightshade`. In order for wireguard to properly resolve the IP address of our router for the VPN the CNAME can't use the cloudflare proxy, so cloudflare only has the DNS service setup (grey cloud, not the orange cloud)