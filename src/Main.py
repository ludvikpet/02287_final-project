import Network
import LDSN
import Node
import NetworkSimulations

network = Network.Network("Problems/example3.txt")
network.print_dict(network.network)
network.print_dict(network.agents)

simulation = NetworkSimulations.NetworkSimulations(network)
# simulation.simulate_network(network, network.get_agent_from_name("A"),print_to_graph=True)
simulation.simulate_network(network, network.get_agent_from_name("D"),print_to_graph=True)