# OpenFlowSDN
Implementation of a full-mesh three switch topology, using a POX controller.

The project requirements are as follows:

<img src="images/requirements.png" width="80%">


First of all, it is necessary to set up the Mininet virtual machine properly.

# Mininet Setup
In the first place, it is necessary to run dhclient, which sets the IP of all interfaces created on the virtual machine.
```
sudo dhclient
```
We can use different PuTTy sessions to connect to the virtual machine. 
________________________________________________________________________________________

# Mininet Topology
The topology implemented is as the following sketch:

<img src="images/topology.png" width="80%">

## Source code of the topology and its description
In order to execute the topology script and create it on Mininet.
```
sudo python topology.py
```

### 1.Importing libraries
In this section I imported all the **libraries** needed to create the components of the topology above.

```python
from mininet.net import Mininet
from mininet.node import Controller,OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import RemoteController
```
### 2.Creating the Mininet instance
Here I created a Mininet class object and as arguments I passed the type of links and switches, respectively.
```python
net = Mininet( link=TCLink, switch=OVSKernelSwitch )
```
### 3.Creating the hosts, switches and controller
The following lines show the creation of the 15 hosts of our topology, assigning each IP address, MAC address and their default route. Each host is named by the switch associated. 
* Host 1 of switch 1: h1_s1
* Host 4 of switch 3: h4_s3

There are 3 LANs, one for each switch:
* **Switch 1** and its hosts: **10.0.0.0/8**
* **Switch 2** and its hosts: **11.0.0.0/8**
* **Switch 3** and its hosts: **12.0.0.0/8**

There is also a pattern concerning the MAC addresses---> The least significant bit of the last byte is the **host number**, and the most significant bit of the last byte is an **enumeration** from 0 to 2. 

This is helpful to identify in a more simple way the corresponding MAC addresses.

Finally, I added the 3 switches to the net and the controller.

I also assigned a port(6633) and an IP address(127.0.0.1) to the remote controller.
```python
h1_s1 = net.addHost( 'h1_s1', ip='10.0.0.1/8',mac='00:00:00:00:00:01',defaultRoute="via 10.0.0.1")
h2_s1 = net.addHost( 'h2_s1', ip='10.0.0.2/8',mac='00:00:00:00:00:02',defaultRoute="via 10.0.0.1")
h3_s1 = net.addHost( 'h3_s1', ip='10.0.0.3/8',mac='00:00:00:00:00:03',defaultRoute="via 10.0.0.1")
h4_s1 = net.addHost( 'h4_s1', ip='10.0.0.4/8',mac='00:00:00:00:00:04',defaultRoute="via 10.0.0.1")
h5_s1 = net.addHost( 'h5_s1', ip='10.0.0.5/8',mac='00:00:00:00:00:05',defaultRoute="via 10.0.0.1")

h1_s2 = net.addHost( 'h1_s2', ip='11.0.0.1/8',mac='00:00:00:00:00:11',defaultRoute="via 11.0.0.1")
h2_s2 = net.addHost( 'h2_s2', ip='11.0.0.2/8',mac='00:00:00:00:00:12',defaultRoute="via 11.0.0.1")
h3_s2 = net.addHost( 'h3_s2', ip='11.0.0.3/8',mac='00:00:00:00:00:13',defaultRoute="via 11.0.0.1")
h4_s2 = net.addHost( 'h4_s2', ip='11.0.0.4/8',mac='00:00:00:00:00:14',defaultRoute="via 11.0.0.1")
h5_s2 = net.addHost( 'h5_s2', ip='11.0.0.5/8',mac='00:00:00:00:00:15',defaultRoute="via 11.0.0.1")

h1_s3 = net.addHost( 'h1_s3', ip='12.0.0.1/8',mac='00:00:00:00:00:21',defaultRoute="via 12.0.0.1")
h2_s3 = net.addHost( 'h2_s3', ip='12.0.0.2/8',mac='00:00:00:00:00:22',defaultRoute="via 12.0.0.1")
h3_s3 = net.addHost( 'h3_s3', ip='12.0.0.3/8',mac='00:00:00:00:00:23',defaultRoute="via 12.0.0.1")
h4_s3 = net.addHost( 'h4_s3', ip='12.0.0.4/8',mac='00:00:00:00:00:24',defaultRoute="via 12.0.0.1")
h5_s3 = net.addHost( 'h5_s3', ip='12.0.0.5/8',mac='00:00:00:00:00:25',defaultRoute="via 12.0.0.1")

s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
s3 = net.addSwitch('s3')

c1 = net.addController( 'c1', controller=RemoteController, ip='127.0.0.1', port=6633)
```
### 4.Creating links
The function of these instructions is to set the links among hosts and switches, I also passed the connected ports as an argument, this was necessary to clarify the right paths all over the networks.
```python
net.addLink(h1_s1, s1,port1=1,port2=1)
net.addLink(h2_s1, s1,port1=1,port2=2)
net.addLink(h3_s1, s1,port1=1,port2=3)
net.addLink(h4_s1, s1,port1=1,port2=4)
net.addLink(h5_s1, s1,port1=1,port2=5)

net.addLink(h1_s2, s2,port1=1,port2=1)
net.addLink(h2_s2, s2,port1=1,port2=2)
net.addLink(h3_s2, s2,port1=1,port2=3)
net.addLink(h4_s2, s2,port1=1,port2=4)
net.addLink(h5_s2, s2,port1=1,port2=5)

net.addLink(h1_s3, s3,port1=1,port2=1)
net.addLink(h2_s3, s3,port1=1,port2=2)
net.addLink(h3_s3, s3,port1=1,port2=3)
net.addLink(h4_s3, s3,port1=1,port2=4)
net.addLink(h5_s3, s3,port1=1,port2=5)
```
### 5.Starting the Mininet object and the Mininet CLI(Interface)
Once the **exit** command is sent in the CLI, the net.stop() command will be executed, stopping the simulation.
```python
net.build()
net.start()
CLI( net )
net.stop()
```
### 6.Set some parameters to display information.
The **setLogLevel()** command will display more information about the components of the topology, showing all the components in the CLI, then the main topology function is called and executed.
```python
if __name__ == '__main__':
	setLogLevel( 'info' )
	topology()

```

It is important to run the following command to clean up all the simulation environment so we can start another one without having previous components or information not deleted.
```
sudo mn -c
```
________________________________________________________________________________________
# POX Controller
I coded my own POX controller to fulfill the requirements of the project. 
First of all, the controller must be created in the **pox/ext** directory. 
```
cd pox/ext
```
```
geany controller.py
```

## Source code of the controller and its description
In order to execute the controller, we must be in the **pox** directory.
```
cd pox
```
Then we can execute the controller
```
sudo python ./pox.py controller
```
### 1.Importing libraries
In this section I imported the **libraries** needed to use  OpenFlow commands and instructions.

I also imported other libraries which I used to implement some other processes that will explained.

```python
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.openflow.flow_table import *
from pox.lib.util import dpidToStr
import os
```
### Program sequence
#### 1. Switches connection up

