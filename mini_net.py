from mininet.topo import Topo
class Mesh(Topo):
	def build(self,n=4):
		switches = []
		hosts = []
		for i in range(n):
			switch = self.addSwitch('s{}'.format(i+1))
			switches.append(switch)
		for i in range(n):
			host = self.addHost('h{}'.format(i+1))
			hosts.append(host)
			self.addLink(host,switches[i])
		for i in range(n):
			for j in range(i+1,n):
				self.addLink(switches[i],switches[j])
		for i in range(n):
			for j in range(i+1,n):
				self.addLink(hosts[i],hosts[j])
topos = {'mesh':Mesh}

#sudo mn --custom mini_net.py --top mesh --controller none
