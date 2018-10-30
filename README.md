## what is bo

bo is a python script to automate the creation of a basic infrastructure on OpenStack.

This includes: 
* network
* private subnet
* router and router interface
* security group
* X instances
* floating IP

## Usage

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


