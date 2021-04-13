from mininet.net import Mininet
from mininet.node import Controller,OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import RemoteController

def topology():
	
	print("Create a network.")
	net = Mininet( link=TCLink, switch=OVSKernelSwitch )

	print("*** Creating nodes")
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
	
	h1_s3= net.addHost(  'h1_s3', ip='12.0.0.1/8',mac='00:00:00:00:00:21',defaultRoute="via 12.0.0.1")
	h2_s3 = net.addHost( 'h2_s3', ip='12.0.0.2/8',mac='00:00:00:00:00:22',defaultRoute="via 12.0.0.1")
	h3_s3 = net.addHost( 'h3_s3', ip='12.0.0.3/8',mac='00:00:00:00:00:23',defaultRoute="via 12.0.0.1")
	h4_s3 = net.addHost( 'h4_s3', ip='12.0.0.4/8',mac='00:00:00:00:00:24',defaultRoute="via 12.0.0.1")
	h5_s3 = net.addHost( 'h5_s3', ip='12.0.0.5/8',mac='00:00:00:00:00:25',defaultRoute="via 12.0.0.1")
	
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')
	
	c1 = net.addController( 'c1', controller=RemoteController, ip='127.0.0.1', port=6633)
	
	print("*** Associating and Creating links")
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
	
	print( "Adding switch links")
	net.addLink(s1,s2,port1=6,port2=6)
	net.addLink(s2,s3,port1=7,port2=7)	
	net.addLink(s1,s3,port1=7,port2=6)
	
	

	print("*** Starting network")
	net.build()
	net.start()
	   	
	print("*** Running CLI")
	CLI( net )

	print("*** Stopping network")
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	topology()
