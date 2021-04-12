from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.openflow.flow_table import *
from pox.lib.util import dpidToStr
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.arp import arp
from pox.lib.packet.icmp import icmp
import pox.lib.packet as pkt
import os

log = core.getLogger()
s1_dpid = 0
s2_dpid = 0
s3_dpid = 0

def _handle_ConnectionUp(event):
	
		global s1_dpid, s2_dpid, s3_dpid
		print("ConnectionUp: ", dpidToStr(event.connection.dpid))
		
		add_queues("s1-eth7")
		add_queues("s1-eth6")
		add_queues("s2-eth7")
		add_queues("s2-eth6")
		add_queues("s3-eth7")
		add_queues("s3-eth6")

		for m in event.connection.features.ports:
			if m.name == "s1-eth1":
				s1_dpid = event.connection.dpid
			elif m.name == "s2-eth1":
				s2_dpid = event.connection.dpid
			elif m.name == "s3-eth1":
				s3_dpid = event.connection.dpid
            
             
def add_flows(ev,ipsrc,ipdst,n):
	inport=0
	if str(ipsrc).rsplit('.',1)[0]=="10.0.0" and str(ipdst).rsplit('.',1)[0]=="11.0.0":
		inport=6
	elif str(ipsrc).rsplit('.',1)[0]=="10.0.0" and str(ipdst).rsplit('.',1)[0]=="12.0.0":
		inport=7
	elif str(ipsrc).rsplit('.',1)[0]=="11.0.0" and str(ipdst).rsplit('.',1)[0]=="10.0.0":
		inport=6
	elif str(ipsrc).rsplit('.',1)[0]=="11.0.0" and str(ipdst).rsplit('.',1)[0]=="12.0.0":
		inport=7
	elif str(ipsrc).rsplit('.',1)[0]=="12.0.0" and str(ipdst).rsplit('.',1)[0]=="10.0.0":
		inport=6
	elif str(ipsrc).rsplit('.',1)[0]=="12.0.0" and str(ipdst).rsplit('.',1)[0]=="11.0.0":
		inport=7
		
	for j in range(1,6):
		msg = of.ofp_flow_mod()
		msg.match.dl_type = 0x0800
		myipdst=ipdst + str(j)
		msg.match.nw_dst = myipdst
		msg.actions.append(of.ofp_action_dl_addr.set_dst(EthAddr("00:00:00:00:00:"+str(n)+str(j))))
		
		if str(myipdst).rsplit('.',1)[1]=="1" or str(myipdst).rsplit('.',1)[1]=="2":
			msg.actions.append(of.ofp_action_enqueue(port = inport,queue_id=1))
		elif str(myipdst).rsplit('.',1)[1]=="3" or str(myipdst).rsplit('.',1)[1]=="4":
			msg.actions.append(of.ofp_action_enqueue(port = inport,queue_id=2))
		elif str(myipdst).rsplit('.',1)[1]=="5":
			msg.actions.append(of.ofp_action_enqueue(port = inport,queue_id=3))
			
		ev.connection.send(msg)
			
def add_sameNetworkFlows(ev,ipdst):
	for i in range(1,6):
			msg = of.ofp_flow_mod()
			msg.priority =1
			msg.idle_timeout = 0
			msg.hard_timeout = 0
			msg.match.dl_type = 0x0800
			myipdst=ipdst+str(i)
			msg.match.nw_dst = myipdst
			msg.actions.append(of.ofp_action_output(port = i))
			ev.connection.send(msg)
			
def add_queues(port):
	command = 'ovs-vsctl set port '+port+' qos=@newqos -- \
--id=@newqos create QoS type=linux-htb  \
 other-config:max-rate=100000000 \
 queues:1=@1\
 queues:2=@2 \
 queues:3=@3 -- \
--id=@1 create queue other-config:min-rate=1000000 other-config:max-rate=1000000 -- \
--id=@2 create queue other-config:min-rate=2000000 other-config:max-rate=2000000 -- \
--id=@3 create queue other-config:min-rate=3000000 other-config:max-rate=3000000 > /dev/null'
	os.system(command)
		
          
def _handle_PacketIn (event):
	packet = event.parsed
	global s1_dpid, s2_dpid, s3_dpid
	
	if event.connection.dpid==s1_dpid:
		msg = of.ofp_flow_mod()
		msg.idle_timeout = 0
		msg.hard_timeout = 0
		msg.match.dl_type = 0x0806
		msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
		event.connection.send(msg)
		
		add_flows(event,"10.0.0.","11.0.0.",1)
		add_flows(event,"10.0.0.","12.0.0.",2)
		
		add_sameNetworkFlows(event,"10.0.0.")
		
		
				
	elif event.connection.dpid==s2_dpid:
		msg = of.ofp_flow_mod()
		msg.idle_timeout = 0
		msg.hard_timeout = 0
		msg.match.dl_type = 0x0806
		msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
		event.connection.send(msg)	
		
		add_sameNetworkFlows(event,"11.0.0.")
		
		add_flows(event,"11.0.0.","10.0.0.",0)
		add_flows(event,"11.0.0.","12.0.0.",2)
		
		
		
	elif event.connection.dpid==s3_dpid:
		msg = of.ofp_flow_mod()
		msg.idle_timeout = 0
		msg.hard_timeout = 0
		msg.match.dl_type = 0x0806
		msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
		event.connection.send(msg)
		
		add_sameNetworkFlows(event,"12.0.0.")
		
		add_flows(event,"12.0.0.","10.0.0.",0)
		add_flows(event,"12.0.0.","11.0.0.",1)
		
		
		
def launch ():
	core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
	core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
