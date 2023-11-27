from Node import Agent
import LDSN
from LDSN import Rule
import graphviz

class Network:
    def __init__(self, src):
        self.read_input(src, {})

    # Read input file and create network connections:
    def read_input(self, src, network):
        self.filename = src.split('/')[-1].split('.')[0] 
        with open(src) as f:
            lines = f.readlines() # Read all lines
            skip_line = {'##Feature_propositions:', '##Edge_relations:', '##Agent_assignments:', '##pre_and_post_conditions:'}
            
            # Create all agents (empty):
            agt_tuples = [(name, Agent([], name)) for name in lines[1].strip('\n').split(', ')]
            
            # Create dictionary of agent name to the agent object
            name_to_agent = {name: agent for name, agent in agt_tuples}
            FP_in_order = []
            FP = {}
            FP_list = []
            rules = []
            ldsn = LDSN.LDSN()

            scope = 0
            for elem in lines[3:]:
                
                elem = elem.strip('\n')
                
                # Skip line if necessary:
                if elem in skip_line:
                    scope += 1
                    continue

                line_split = elem.split(': ')
                if scope == 0: # Read feature propositions and its values
                    V, Rs = line_split[0], line_split[1].split(', ')
                    # V, Rs = line_split[0], line_split[1].split('##')[0].strip().split(', ')
                    # print(f"V:{V},\nRs: {Rs}")
                    FP[V] = Rs
                    FP_in_order.append(V)
                    FP_list.append(V)

                elif scope == 1: # Read network (edges between agents)
                    # If agents has friends, add them to agent connections:
                    if len(line_split) > 1:
                        # name, friends = agt_split[0], [agents[friend] for friend in agt_split[1].split(', ')]
                        name, friend_names = line_split[0], line_split[1].split(', ')
                        
                        # Add agent and its connections to network:
                        network[name] = friend_names
                        friends = []
                        for friend in friend_names:
                            friends.append(name_to_agent[friend])
                        name_to_agent[name].set_friends(friends)

                elif scope == 2: # Read agent assignments
                    agent, assignments = name_to_agent[line_split[0]], line_split[1].split(', ')
                    for assignment in assignments:
                        agent.add_assignment(assignment)

                elif scope == 3: # Read pre and post conditions
                    antecedent = line_split[1].split('->')[0]
                    antecedent = ldsn.parse_expression(antecedent)
                    consequent = line_split[1].split('->')[1].replace(' ', '')
                    rules.append(Rule(FP_in_order, line_split[0], antecedent, consequent))

        # Add variables to class:
        self.network = network # Str -> Str[]
        self.agents = name_to_agent # Str -> Agent
        self.rules = rules
    
    def get_agent_from_name(self, name):
        return self.agents[name]

    def create_preconditions(conditions):
        and_split = conditions.split(' AND ')
    pass

    def to_graph(self, filename):
        dot_string = "digraph SocialNetwork {\n"
        for agent_name in self.network:
            for friend_name in self.network[agent_name]:
                dot_string += f' "{agent_name}" -> "{friend_name}" \n'
        dot_string += "}"
        return dot_string

    def render_graph(self, dot_string, filename):
        format = 'png'
        dot = graphviz.Source(dot_string)
        dot.render(filename, format=format, cleanup=True)
    
    def print_dict(self, dict):
        for key, value in dict.items():
            print(f"{key}: {value}")