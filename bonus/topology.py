from mininet.net import Mininet
from mininet.node import Controller,OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import RemoteController
import os

def topology():
	
	print("Create a network.")
	net = Mininet( link=TCLink, switch=OVSKernelSwitch )

	print("*** Creating nodes")
	h1_s1 = net.addHost( 'h1_s1', ip='10.0.0.1/8')
	h2_s1 = net.addHost( 'h2_s1', ip='10.0.0.2/8')
	h3_s1 = net.addHost( 'h3_s1', ip='10.0.0.3/8')
	h4_s1 = net.addHost( 'h4_s1', ip='10.0.0.4/8')
	h5_s1 = net.addHost( 'h5_s1', ip='10.0.0.5/8')
	
	h1_s2 = net.addHost( 'h1_s2', ip='10.0.1.1/8')
	h2_s2 = net.addHost( 'h2_s2', ip='10.0.1.2/8')
	h3_s2 = net.addHost( 'h3_s2', ip='10.0.1.3/8')
	h4_s2 = net.addHost( 'h4_s2', ip='10.0.1.4/8')
	h5_s2 = net.addHost( 'h5_s2', ip='10.0.1.5/8')
	
	h1_s3= net.addHost(  'h1_s3', ip='10.0.2.1/8')
	h2_s3 = net.addHost( 'h2_s3', ip='10.0.2.2/8')
	h3_s3 = net.addHost( 'h3_s3', ip='10.0.2.3/8')
	h4_s3 = net.addHost( 'h4_s3', ip='10.0.2.4/8')
	h5_s3 = net.addHost( 'h5_s3', ip='10.0.2.5/8')
	
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')
	
	c1 = net.addController( 'c1', controller=RemoteController, ip='127.0.0.1', port=6633)
	
	print("*** Associating and Creating links")
	net.addLink(h1_s1, s1)
	net.addLink(h2_s1, s1)
	net.addLink(h3_s1, s1)
	net.addLink(h4_s1, s1)
	net.addLink(h5_s1, s1)
	
	net.addLink(h1_s2, s2)
	net.addLink(h2_s2, s2)
	net.addLink(h3_s2, s2)
	net.addLink(h4_s2, s2)
	net.addLink(h5_s2, s2)
	
	net.addLink(h1_s3, s3)
	net.addLink(h2_s3, s3)
	net.addLink(h3_s3, s3)
	net.addLink(h4_s3, s3)
	net.addLink(h5_s3, s3)
	
	print( "Adding switch links")
	net.addLink(s1,s2)
	net.addLink(s1,s3)
	net.addLink(s2,s3)	
	

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
