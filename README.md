## What is bo

`bo` is a python script to automate the creation of a basic infrastructure on OpenStack.

This includes: 
* network
* private subnet
* router and router interface
* security group
* X instances
* floating IP

### Usage

```
usage: bo.py [-h] [--username USERNAME] [--projectname PROJECTNAME]
             [--clustername CLUSTERNAME] [--subnetcidr SUBNETCIDR]
             [--workers WORKERS] [--workerimageflavor WORKERIMAGEFLAVOR]
             [--glanceimagename GLANCEIMAGENAME]
             [--availabilityzone AVAILABILITYZONE]
             [--externalnetid EXTERNALNETID]
             keypair floatingip

positional arguments:
  keypair               Keypair ID
  floatingip            Floatingip for public access to cluster

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME   Openstack username - (OS_USERNAME environment
                        variable)
  --projectname PROJECTNAME
                        Openstack project Name - (OS_TENANT_NAME environment
                        variable)
  --clustername CLUSTERNAME
                        Clustername - (cluster)
  --subnetcidr SUBNETCIDR
                        Private subnet CIDR - (192.168.3.0/24)
  --workers WORKERS     Number of workers - (3)
  --workerimageflavor WORKERIMAGEFLAVOR
                        Worker image flavor ID - (2008)
  --glanceimagename GLANCEIMAGENAME
                        Glance image name ID - (CentOS 7 (LTS))
  --availabilityzone AVAILABILITYZONE
                        Availability zone - (AMS-EQ1)
  --externalnetid EXTERNALNETID
                        External network id - (f9c73cd5-9e7b-4bfd-89eb-
                        c2f4f584c326)
```

### Example infrastructure bootstrap
```
./bo.py PB_ITE_1 xxx.xxx.xxx.xxx --workers 10
terraform init
terraform apply
```

### Extending the cluster
If you would like to extend the initial cluster you can easily add nodes by using the `addnode.py` script. Currently you will need to provide a free available IP in the subnet range you provided earlier; or in the 192.168.3.0/24 range by default.
```
./addnode 192.168.3.13
terraform apply
```

### SecurityGroup defaults
The script will create a new security group which is applied to all the nodes with the following rules. 
* allow any to any on all protocols within the LAN
* allow TCP 22 from outside
* allow TCP 80 from outside 
* allow TCP 443 from outside
* allow TCP 8081 from outside


The outside rules will only make sense if there is a floating IP attached to the node.