import Network
import LDSN
import Node
import NetworkSimulations

network = Network.Network("Problems/Polarization/polarize.txt")
network.print_dict(network.network)
network.print_dict(network.agents)

simulation = NetworkSimulations.NetworkSimulations(network)
cascade_literal = [LDSN.Literal("V_CS(guilty)"), LDSN.Literal("V_CS(innocent)")]
initial_node = [network.get_agent_from_name("A"),
                network.get_agent_from_name("R")]
# initial_node = [network.get_agent_from_name("D")]
# simulation.simulate_network(network, network.get_agent_from_name("A"),print_to_graph=True)
simulation.simulate_network(network, initial_node, cascade_literal, print_to_graph=True)