from Nodes import Agent, ProbabilisticAgent

def modify_agents(agents, modify_list):
    for agt, features in modify_list:

        #Get Agent:
        agent = agents[key]
        
        # Modify mapped features for agent:
        for key, value in features:
            agent.FP[key] = value
    return agents

def print_network(agents):
    output = ""
    for agt in agents:
        output += "Name: " + agt.ID + "\n network: " + agt.network + "\n FP: " + agt.FP + "\n\n"
    print(output)

def simple_model(num_agents, FP, modify_list, friends_list, transformations):

    # Initialize agents:
    agents = [Agent(i, FP) for i in range(num_agents)]
    
    # Modify agents accordingly:
    agents = modify_agents(agents, modify_list)

    # Update friends list for every agent:
    for idx, agt_relations in enumerate(friends_list):
        agents[idx].add_edge(agt_relations)

    print_network(agents)







    

    