from diagrams import Diagram
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Apache, Nginx
from diagrams.onprem.client import Client
from diagrams.generic.blank import Blank
from diagrams.generic.network import Router
from diagrams.aws.storage import S3

import os
os.environ['PATH'] += os.pathsep + r'C:\Program Files\Graphviz\bin'


with Diagram('payne-pride', show=False, direction='LR'):
    Client('Internet') >> Router('www.paynepride.com') >> Nginx('Reverse Proxy') >> Apache('www.paynepride.com')

with Diagram('duplicati backups', show=False, direction='BT'):
    Client('FreeNAS Home Server / datasets') >> Server('duplicati') >> S3('paynepride-backup')
