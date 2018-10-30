#!/usr/bin/env python2.7
"""Bootstrap OpenStack Environments - addnode """

import argparse
import os
import subprocess
import base64
from jinja2 import Environment, FileSystemLoader

__author__ = "Patrick Blaas <patrick@kite4fun.nl>"
__license__ = "GPL v3"
__version__ = "0.0.1"
__status__ = "Active"

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, '.')),
    trim_blocks=True)

# Testing if environment variables are available.
if "OS_USERNAME" not in os.environ:
    os.environ["OS_USERNAME"] = "Default"
if "OS_PASSWORD" not in os.environ:
    os.environ["OS_PASSWORD"] = "Default"
if "OS_TENANT_NAME" not in os.environ:
    if "OS_PROJECT_NAME" in os.environ:
        os.environ["OS_TENANT_NAME"] = os.environ["OS_PROJECT_NAME"]
    else:
        os.environ["OS_TENANT_NAME"] = "Default"
if "OS_TENANT_ID" not in os.environ:
    os.environ["OS_TENANT_ID"] = "Default"
if "OS_REGION_NAME" not in os.environ:
    os.environ["OS_REGION_NAME"] = "Default"
if "OS_AUTH_URL" not in os.environ:
    os.environ["OS_AUTH_URL"] = "Default"

parser = argparse.ArgumentParser()
parser.add_argument("ipaddress", help="node ip address")
parser.add_argument("--workerimageflavor", help="Worker image flavor ID")
parser.add_argument("--glanceimagename", help="Glance image name ID - (CentOS 7 (LTS))", default="CentOS 7 (LTS)")
parser.add_argument("--username", help="Openstack username - (OS_USERNAME environment variable)", default=os.environ["OS_USERNAME"])
parser.add_argument("--projectname", help="Openstack project Name - (OS_TENANT_NAME environment variable)", default=os.environ["OS_TENANT_NAME"])
args = parser.parse_args()

additional_node_template = TEMPLATE_ENVIRONMENT.get_template('./templates/ostfadditionalnode.tf.tmpl')

try:

    if args.ipaddress != "":
        lanip = str(args.ipaddress)
        with open('cluster.status', 'r') as clusterstat:
            fh = clusterstat.readlines()
            print lanip
            clustername = fh[0].split("\t")[1][:-1]
            subnetcidr = str(fh[1].split("\t")[1])[:-1]
            workers = str(fh[2].split("\t")[1])[:-1]
            if args.workerimageflavor is None:
                workerimageflavor = str(fh[3].split("\t")[1])[:-1]
            else:
                workerimageflavor = args.workerimageflavor
            floatingip = str(fh[4].split("\t")[1])[:-1]
            keypair = str(fh[6].split("\t")[1])[:-1]
            sshkey = str(fh[5].split("\t")[2])[:-1]
            availabilityzone = str(fh[7].split("\t")[2])[:-1]
            defaultsecuritygroupid = str(fh[9].split("\t")[1])[:-1]

            additional_node = (additional_node_template.render(
                clustername=clustername,
                ipaddress=lanip,
                workerimageflavor=workerimageflavor,
                glanceimagename=args.glanceimagename,
                keypair=keypair,
                subnetcidr=subnetcidr,
                octet=lanip.rsplit('.', 1)[1],
                availabilityzone=availabilityzone,
                defaultsecuritygroupid=defaultsecuritygroupid
            ))

            with open("main.tf", 'a') as main:
                main.write(additional_node)

except Exception as e:
    raise
else:
    print("Done")
