
# Define an Agent that acts within the scope of the main article:
class Agent:

    def __init__(self, FP, name):
        self.FP = FP # The set of feature propositions
        self.name = name
        self.friends = []
    
    # Set the agent's friends: 
    def set_friends(self, friends):
        self.friends = friends

    def add_edges(self, new_friends):
        for x in new_friends:
            self.network.append(x)

    def has_fp(self, fp):
        return any(fp == feature for feature in self.FP)
    
    def add_assignment(self, assignment):
        self.FP.append(assignment)

    # F operator evaluation
    def check_friends(self, n, expr):
        ## Evaluate the arg for all friends and count if it is above n
        # print ("friends: " + str([friend.name for friend in self.friends]))
        # print("Evaluating friend expression: " + str(expr))
        if len([friend for friend in self.friends if expr.evaluate(friend)]) >= n:
            return True
        return False

    def get_assignments(self):
        return self.FP

    def __str__(self):
        return f"Agent(name={self.name}, assignments={self.FP})"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Agent):
            return self.name == o.name
        return False

# Define a version of Agent including probabilistic uncertainties:
class ProbabilisticAgent:

    def __init__(self, init_val, friends):

        self.prior = init_val
        self.network = friends

