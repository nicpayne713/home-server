from diagrams import Diagram
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Apache, Nginx
from diagrams.onprem.client import Client
from diagrams.generic.blank import Blank
from diagrams.generic.network import Router
from diagrams.aws.storage import S3
from diagrams import Cluster
from diagrams.onprem.container import Docker
from diagrams.generic.network import VPN
from diagrams.generic.place import Datacenter
import os
os.environ['PATH'] += os.pathsep + r'C:\Program Files\Graphviz\bin'


with Diagram('payne-pride', show=False, direction='LR'):
    internet = Client('Internet')
    with Cluster('Home'):
        nginx = Nginx('Reverse Proxy')
        images = Apache('www/photos')
        vpn = VPN('nightshade')
        nextcloud = Datacenter('nextcloud')
        jellyfin = Blank('jellyfin')
    internet >> Router('<service>.paynepride.com') >> nginx
    nginx >> images
    nginx >> vpn
    nginx >> nextcloud
    nginx >> jellyfin

with Diagram('duplicati backups', show=False, direction='BT'):
    with Cluster('FreeNAS'):
        freenas = Client('FreeNAS Home Server / datasets')
        duplicati = Server('duplicati')
    s3 = S3('paynepride-backup')
    with Cluster('RyzenRender'):
        fdrive = Server('F drive on RyzenRender')
        docker_duplicati = Docker('duplicati')
    freenas >> duplicati >> s3
    s3 >> docker_duplicati >> fdrive
