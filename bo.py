#!/usr/bin/env python2.7
"""Bootstrap OpenStack Environments"""

import argparse
import os
import subprocess
import base64
import crypt
import string
import random
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

def ValidateDNS(v):
    import re  # Unless you've already imported re previously
    try:
        return re.match("^[a-z0-9]*$", v).group(0)
    except:
        raise argparse.ArgumentTypeError("String '%s' does not match required format" % (v,))


def ValidateCIDR(v):
    import re  # Unless you've already imported re previously
    try:
        return re.match("^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$", v).group(0)
    except:
        raise argparse.ArgumentTypeError("String '%s' does not match required format" % (v,))


parser = argparse.ArgumentParser()
parser.add_argument("keypair", help="Keypair ID")
parser.add_argument("floatingip", help="Floatingip for public access to cluster")
parser.add_argument("--username", help="Openstack username - (OS_USERNAME environment variable)", default=os.environ["OS_USERNAME"])
parser.add_argument("--projectname", help="Openstack project Name - (OS_TENANT_NAME environment variable)", default=os.environ["OS_TENANT_NAME"])
parser.add_argument("--clustername", help="Clustername - (cluster)", type=ValidateDNS, default="cluster")
parser.add_argument("--subnetcidr", help="Private subnet CIDR - (192.168.3.0/24)", type=ValidateCIDR, default="192.168.3.0/24")
parser.add_argument("--workers", help="Number of workers - (3)", type=int, default=3)
parser.add_argument("--workerimageflavor", help="Worker image flavor ID - (2008)", type=int, default=2008)
parser.add_argument("--glanceimagename", help="Glance image name ID - (CentOS 7 (LTS))", default="CentOS 7 (LTS)")
parser.add_argument("--availabilityzone", help="Availability zone - (AMS-EQ1)", default="AMS-EQ1")
parser.add_argument("--externalnetid", help="External network id - (f9c73cd5-9e7b-4bfd-89eb-c2f4f584c326)", default="f9c73cd5-9e7b-4bfd-89eb-c2f4f584c326")
args = parser.parse_args()

ostf_template = TEMPLATE_ENVIRONMENT.get_template('./templates/ostftemplate.tf.tmpl')
boe_stat_template = TEMPLATE_ENVIRONMENT.get_template('./templates/boestattemplate.tmpl')


try:

    def returnPublicKey():
        """Retrieve rsa-ssh public key from OpenStack."""
        global rsakey
        rsakey = subprocess.check_output(["openstack", "keypair", "show", "--public-key", args.keypair]).strip()
        return rsakey


    def returnDefaultSecurityGroupId():
        """Retrieve default security group id from OpenStack."""
        global defaultsecuritygroupid
        defaultsecuritygroupid = subprocess.Popen("openstack security group list -f value -c ID -c Name | grep default", shell=True, stdout=subprocess.PIPE).stdout.read().split(" ")[0]
        return defaultsecuritygroupid

    def printClusterInfo():
        """Print cluster info."""
        print("-" * 40 + "\n\nCluster Info:")
        print("Keypair:\t" + str(rsakey))
        print("Clustername:\t" + str(args.clustername))
        print("Cluster cidr:\t" + str(args.subnetcidr))
        print("Workers:\t" + str(args.workers))
        print("Worker flavor:\t" + str(args.workerimageflavor))
        print("Glance imgname:\t" + str(args.glanceimagename))
        print("VIP:\t\t" + str(args.floatingip))
        print("defaultsecgrp:\t" + str(defaultsecuritygroupid))
        print("-" * 40 + "\n")
        print("To start building the cluster: \tterraform init && terraform plan && terraform apply")
        print("To interact with the cluster: \tsh kubeconfig.sh")

    returnPublicKey()
    returnDefaultSecurityGroupId()

    boe_stat_tmp = (boe_stat_template.render(
        clustername=args.clustername,
        subnetcidr=args.subnetcidr,
        workers=args.workers,
        workerimageflavor=args.workerimageflavor,
        glanceimagename=args.glanceimagename,
        floatingip=args.floatingip,
        keypair=args.keypair,
        rsakey=rsakey,
        availabilityzone=args.availabilityzone,
        externalnetid=args.externalnetid,
        defaultsecuritygroupid=defaultsecuritygroupid,
    ))

    with open('cluster.status', 'w') as boe_stat:
        boe_stat.write(boe_stat_tmp)

    main_template = (ostf_template.render(
        username=args.username,
        projectname=args.projectname,
        clustername=args.clustername,
        workers=args.workers,
        subnetcidr=args.subnetcidr,
        keypair=args.keypair,
        workerimageflavor=args.workerimageflavor,
        glanceimagename=args.glanceimagename,
        floatingip=args.floatingip,
        availabilityzone=args.availabilityzone,
        externalnetid=args.externalnetid,
        defaultsecuritygroupid=defaultsecuritygroupid
    ))

    with open('main.tf', 'w') as main:
        main.write(main_template)


except Exception as e:
    raise
else:
    printClusterInfo()
