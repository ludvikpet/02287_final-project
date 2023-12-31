
class LDSN:
    # Evaluate if the given expression holds for the agent
    def evaluate(self, agent):
        raise NotImplementedError()

    # Parse string like: OR(AND(indifferent,centre,F(5,flat)), (F(1,(AND(isExpert,flat))))) and set to expression:
    def parse_expression(self, values):
        values = values.replace(" ", "")

        ## if just a word, return literal
        # if values.find('(') == -1:
        if values.count('(') + values.count(')') == 2:
            return Literal(values)
        
        # First remove and retrieve the letter or word at the front, and the outermost brackets:
        # content = values[values.find('(')+1:values.rfind(')')]
        opr = values[:values.find('(')]
        content = values[values.find('(')+1:values.rfind(')')]

        # Separate into arguments by comma, but only if not inside brackets:
        args = []
        arg = ""
        bracket_count = 0
        for c in content:
            if c == '(':
                bracket_count += 1
            elif c == ')':
                bracket_count -= 1
            elif c == ',' and bracket_count == 0:
                args.append(arg)
                arg = ""
                continue
            arg += c
        args.append(arg)

        print("Reading opr: " + str(opr) + " with args: " + str(args))
        
        if opr == 'AND':
            return AndExpression(*[self.parse_expression(arg) for arg in args])
        elif opr == 'OR':
            return OrExpression(*[self.parse_expression(arg) for arg in args])
        elif opr == 'NOT':
            return NotExpression(self.parse_expression(args[0]))
        elif opr[0] == 'F':
            expr = args[1][args[1].find('(')+1:values.rfind(')')]
            # return FriendExpression(int(args[0]), self.parse_expression(expr))
            return FriendExpression(int(args[0]), self.parse_expression(args[1]))
        else:
            return Literal(opr)
        
class AndExpression(LDSN):
    def __init__(self, *args):
        self.args = args

    def evaluate(self, agent):
        res = all(arg.evaluate(agent) for arg in self.args)
        return res
    
    def __str__(self):
        return f"AND({','.join([str(arg) for arg in self.args])})"

class OrExpression(LDSN):
    def __init__(self, *args):
        self.args = args

    def evaluate(self, agent):
        res = any(arg.evaluate(agent) for arg in self.args)
        return res
    
    def __str__(self):
        return f"OR({','.join([str(arg) for arg in self.args])})"

class NotExpression(LDSN):
    def __init__(self, arg):
        self.arg = arg

    def evaluate(self, agent):
        res = not self.arg.evaluate(agent)
        return res
    
    def __str__(self):
        return f"NOT({str(self.arg)})"

class FriendExpression(LDSN):
    def __init__(self, n, expr):
        self.n = n
        self.expr = expr

    def evaluate(self, agent):
        res = agent.check_friends(self.n, self.expr)
        return res

    def __str__(self):
        return f"F({self.n},{self.expr})"

class Literal(LDSN):
    def __init__(self, value):
        # self.var = value[:value.find('(')] # Feature proposition
        # self.value = value[value.find('(')+1:value.rfind(')')] # Expr
        # self.value = value.strip('()')
        self.value = value


    def evaluate(self, agent):
        res = any(self.value == value for value in agent.FP)
        return any(self.value == value for value in agent.FP)
    
    def __str__(self):
        return self.value

class Rule:
    def __init__(self, properties_in_order, property, antecedent, consequent):
        self.properties = properties_in_order
        self.property = property
        self.antecedent = antecedent
        self.consequent = consequent

    def get_antecedent(self):
        return self.antecedent
    
    def get_consequent(self):
        return self.consequent
    
    ## Evalues the rule, and applies the consequent if the antecedent is true
    # Returns true only if consequent changed the belief of the agent (pre condition -> post condition)
    def evaluate(self, agent):
        index = self.properties.index(self.property)
        if self.antecedent.evaluate(agent):
            before = agent.FP[index]
            agent.FP[index] = self.consequent
            return before != agent.FP[index]
        return False

    def __str__(self):
        return f"{self.antecedent} -> {self.consequent}"