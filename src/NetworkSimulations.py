import os
import graphviz

class NetworkSimulations:

    def __init__(self, network):
        self.simulations = []
        self.simulation = None
        self.network = network

    def simulate_network(self, network, initial_node, cascade_literal, print_to_graph=False):

        print("Running simulation on network: " + str(network.filename))

        # Print initial graph of network:
        if print_to_graph:
            self.create_graph(network, None, cascade_literal, 0, 0)

        # Initialize queue with root node:
        queue = [initial_node]
        rules = network.rules

        iterations = 0
        num_changes = 1
        graphs = 1

        state_changed = True

        # While queue is not empty:
        while queue:
            print("Running iteration " + str(iterations))

            # Pop first node from queue:
            current_node = queue.pop(0)
            agent_lst = []
            for current_agent in current_node:

                print("Proceeding with current agent: " + str(current_agent.name))

                # Print graph of network:
                # if print_to_graph and graphs < 12:
                if print_to_graph:
                    graphs += 1
                    self.create_graph(network, current_agent, cascade_literal, num_changes, graphs)
                
                for friend in current_agent.friends:
                    # If rule evaluates to true, add friend to queue:
                    if any(rule.evaluate(friend) for rule in rules):
                        print("Agent " + str(friend.name) + " changed belief to: " + str(friend.FP))
                        agent_lst.append(friend)
                        # queue.append(friend)
                
                num_changes += 1
                
            # If graph has stabilized, break:
            if len(agent_lst) == 0:
                print("GRAPH HAS STABILIZED!")
                break
            queue.append(agent_lst)
            iterations += 1
        
        # Print final graph of network:
        if print_to_graph:
            graphs += 1
            self.create_graph(network, None, cascade_literal, num_changes, graphs)

    def create_graph(self, network, current_agent, cascade_literal, num_changes, graphs):
        print("Printing graph of network...")
        dir = "Graphs/" + str(network.filename) + "/"
        path_to_graph = dir + str(network.filename) + "-" + str(num_changes)
        path_to_dot = dir + "/dot_representation/" + network.filename + "-" + str(num_changes) + ".dot"
        dot_string = self.network_to_dot(network, current_agent, cascade_literal)
        self.dot_to_file(dot_string, path_to_dot)
        self.dot_to_graph(dot_string, path_to_graph)

    def network_to_dot(self, network, current_agent, cascade_literal):
        dot_string = "graph {\n rankdir=TB;\n"
        added_edges = set()

        # Define nodes and colors
        # If node's earth shape is "flat" then filled red
        for agent_name in network.agents:
            agent = network.get_agent_from_name(agent_name)
            if agent == current_agent:
                color = "green"
            elif agent.FP[0] == str(cascade_literal[0]):
                color = "red"
            elif agent.FP[0] == str(cascade_literal[1]):
                color = "yellow"
            else:
                color = "lightblue"
            label_param = "label=<" + agent_name + "<BR /><FONT POINT-SIZE=\"10\">" + str(agent.FP[2]) + ", " + str(agent.FP[1]) + "</FONT>>"
            params = "[" + label_param + "," + "style=filled, color=" + color + "];\n"
            dot_string += str(agent_name) + params
            

        # Define edges
        for agent_name in network.agents:
            dot_string += str(agent_name) + " -- " + "{{"
            agent = network.get_agent_from_name(agent_name)

            for friend in agent.friends:
                edge = tuple(sorted([agent.name, friend.name]))

                if edge not in added_edges:
                    dot_string += str(friend.name) + " "
                    added_edges.add(edge)
            dot_string += "}}\n"

        dot_string += "}"
        return dot_string

    def dot_to_file(self, dot_string, filename):
        # if directory doesn't exist, create it
        dir = filename.rsplit('/', 1)[0]
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(filename, "w") as file:
            file.write(dot_string)

    def dot_to_graph(self, dot_string, filename):
        # if directory doesn't exist, create it
        dir = filename.rsplit('/', 1)[0]
        if not os.path.exists(dir):
            os.makedirs(dir)
        format = 'png'
        dot = graphviz.Source(dot_string)
        dot.render(filename, format=format, cleanup=True)