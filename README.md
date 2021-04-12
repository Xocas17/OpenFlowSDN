# OpenFlowSDN
Implementation of a full-mesh three switch topology, using a POX controller

The project requirements are as follows:

![Screenshot](images/requirements.png)

# Mininet VM Setup
First of all, it is necessary to set up the Mininet virtual machine properly.

In the first place, it is necessary to run dhclient, which sets the IP of all interfaces created on the virtual machine.
```
sudo dhclient
```
