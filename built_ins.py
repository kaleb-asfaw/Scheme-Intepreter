import sys
import errors as Scheme

sys.setrecursionlimit(100000)

############################
# Tokenization and Parsing #
############################


def number_or_symbol(value):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8') should return 8
    >>> number_or_symbol('-5.32') should return -5.32
    >>> number_or_symbol('1.2.3.4') should return '1.2.3.4'
    >>> number_or_symbol('x') should return 'x'
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    """
    token = []
    comment = False
    parentheses = "()"
    running_str = ""
    for _, char in enumerate(source):
        # if the character is a semi-colon, then a comment begins
        if char == ";":
            comment = True

        else:
            # if we run into parentheses
            if char in parentheses and not comment:
                if running_str:
                    token.append(running_str)
                    running_str = ""
                token.append(char)

            # if end of line
            elif char == "\n":
                if running_str:
                    token.append(running_str)
                    running_str = ""
                comment = False

            # if there is a space
            elif char == " " and not comment:
                if running_str:
                    token.append(running_str)
                    running_str = ""

            # any other character
            elif char != " " and not comment:
                running_str += char

    if running_str:
        token.append(running_str)

    return token


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    # will raise an error if there aren't equal left and right parent.
    if tokens.count("(") != tokens.count(")"):
        raise Scheme.SyntaxError

    # raise assertion error if expression doesn't start/end with parent.
    if len(tokens) > 1:
        if tokens[0] != "(" or tokens[-1] != ")":
            raise Scheme.SyntaxError

    def parse_helper(i):
        tree = []
        paren = "()"
        while i < len(tokens):
            # base case 1: right paren means return the list
            if number_or_symbol(tokens[i]) == ")":
                return tree, i + 1
            # base case 2: left paren means recurse on rest of list
            elif number_or_symbol(tokens[i]) == "(":
                next_ex, i = parse_helper(i + 1)
                tree.append(next_ex)
            else:
                tree.append(number_or_symbol(tokens[i]))
                i += 1

        return tree, i

    r_expression, last_index = parse_helper(0)
    if r_expression:
        return r_expression[0]
    else:
        return []


class Pair:
    #Basic linked list implementation, where car is an element and cdr is a pointer 
    #to next "Pair" object
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def set_cdr(self, nu_cdr):
        self.cdr = nu_cdr

    def __str__(self):
        return f"Pair({self.car}, {self.cdr})"


######################
# Built-in Functions #
######################
def mul(args):
    ret_value = 1
    for val in args:
        ret_value *= val

    return ret_value


def div(args):
    return args[0] / mul(args[1:])


######################
#   Boolean returns  #
######################
def equal(args):
    for i in args[1:]:
        if args[0] != i:
            return "#f"
    return "#t"


def greaterthan(args):
    for i in range(len(args) - 1):
        if not args[i] > args[i + 1]:
            return "#f"
    return "#t"


def geq(args):
    for i in range(len(args) - 1):
        if not args[i] >= args[i + 1]:
            return "#f"
    return "#t"


def lessthan(args):
    for i in range(len(args) - 1):
        if not args[i] < args[i + 1]:
            return "#f"
    return "#t"


def leq(args):
    for i in range(len(args) - 1):
        if not args[i] <= args[i + 1]:
            return "#f"
    return "#t"


def naught(arg):
    if isinstance(arg, list):
        if len(arg) != 1:
            raise Scheme.EvaluationError

        arg = arg[0]

    if arg == "#t":
        return "#f"
    else:
        return "#t"


def cons(args):
    if len(args) != 2:
        raise Scheme.EvaluationError("Incorrect number of arguments for cons")

    return Pair(args[0], args[1])


def car(pair_obj):
    if not isinstance(pair_obj, list):
        pair_obj = [pair_obj]

    if len(pair_obj) != 1:
        raise Scheme.EvaluationError("empty list or too many")

    if not isinstance(pair_obj[0], Pair):
        raise Scheme.EvaluationError("not a list")

    return pair_obj[0].car


def cdr(pair_obj):
    if not isinstance(pair_obj, list):
        pair_obj = [pair_obj]
    if len(pair_obj) != 1:
        raise Scheme.EvaluationError("empty list or too many")

    if not isinstance(pair_obj[0], Pair):
        raise Scheme.EvaluationError("not a list")

    return pair_obj[0].cdr


def listt(args):
    if len(args) == 0:
        return "nil"

    elif len(args) == 1:
        return Pair(args[0], "nil")
    else:
        list_obj = Pair(args[0], listt(args[1:]))

    return list_obj


def check_list(object):
    if isinstance(object, list):
        object = object[0]

    while isinstance(object, Pair):
        object = cdr(object)

    # if isinstance(object, Pair):
    #     return check_list([cdr(object)])

    if object == "nil":
        return "#t"

    else:
        return "#f"


def list_len(pair_obj, sofar=0):
    """
    Given a pair object, return the length. Raise eval
    error if not given a pair object.
    """
    if isinstance(pair_obj, list):
        pair_obj = pair_obj[0]

    if pair_obj == "nil":
        return sofar

    if check_list(pair_obj) == "#f":
        raise Scheme.EvaluationError("Not a pair object")

    
    while pair_obj != "nil":
        left = car(pair_obj)
        right = cdr(pair_obj)
        if left != "nil":
            sofar += 1
        pair_obj = right

    return sofar
        
def get_val_at_i(pair_obj, index, sofar=0):
    #### CHECKS @ BEGINNING  ####
    
    if isinstance(pair_obj, list):
        pair_obj = pair_obj[0]

    if check_list(pair_obj) == "#f":
        if index != 0:
            raise Scheme.EvaluationError("not able to index cons object")
        else:
            return car(pair_obj)

    if index < 0:
        raise Scheme.EvaluationError("index must be a positive int")
        

    #### FUNCTION CODE ####
    
    while pair_obj != "nil":
        left = car(pair_obj)
        if index == sofar:
            return left

        sofar += 1

        pair_obj = cdr(pair_obj)
        
    
    raise Scheme.EvaluationError("index out of range")
    
    
def append_lists(args):
    if len(args) == 0:
        return "nil"

    elif check_list(args[0]) == "#f":
        raise Scheme.EvaluationError("You tried appending a non-list object")

    elif args[0] == "nil":
        return append_lists(args[1:])

    else:
        rest = [cdr(args[0])] + args[1:]
        # print(rest)
        return Pair(car(args[0]), append_lists(rest))


def map_list(func, list):
    """
    Given a list and function, return a new list that applied the function
    to each of the list's elements.
    """
    if check_list(list) == "#f":
        raise Scheme.EvaluationError("argument passed in is not a list")

    if list_len(list) == 0:
        return "nil"

    else:
        return Pair(func([car(list)]), map_list(func, cdr(list)))

def filter(func, list):
    """
    Given a list and function, return a new list for which each element
    satisfies the parameter 'func'.
    """
    if check_list(list) == "#f":
        raise Scheme.EvaluationError("argument passed in is not a list")

    if list_len(list) == 0:
        return "nil"

    else:
        if func([car(list)]) == "#t":
            return Pair(car(list), filter(func, cdr(list)))
        else:
            return filter(func, cdr(list))

def reduce(func, list, init):
    """
    Applied the function to the init value with every value in the list.
    Returns a value which applies every element of the list to the init.
    """
    if check_list(list) == "#f":
        raise Scheme.EvaluationError("argument passed in is not a list")

    if list_len(list) == 0:
        return init

    else:
        val = func([init, car(list)])
        return reduce(func, cdr(list), val)
    
def begin(expression):
    """
    Given an arbitrary number of arguments and an expression to evaluate,
    return the expression after it's evaluated by args.
    """
    return expression

def evaluate_file(file, frame):
    with open(file, "r") as f:
        text = f.read()
        tokenized = tokenize(text)
        parsed = parse(tokenized)
        return evaluate(parsed, frame)


scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": mul,
    "/": div,
    "equal?": equal,
    ">": greaterthan,
    ">=": geq,
    "<": lessthan,
    "<=": leq,
    "not": naught,
    "cons": cons,
    "car": car,
    "cdr": cdr,
    "list": listt,
    "list?": check_list,
    "length": list_len,
    "list-ref": lambda args: get_val_at_i(args[0], args[1]),
    "append": append_lists,
    "map": lambda args: map_list(args[0], args[1]),
    "filter": lambda args: filter(args[0], args[1]),
    "reduce": lambda args: reduce(args[0], args[1], args[2]),
    "begin": lambda args: begin(args[-1]),
    "evaluate_file": evaluate_file,

}


##############
# Evaluation #
##############
class Frame:
    """
    When a variable is initializes (via 'define' key word), we must
    assign it a value, and a frame.
    """

    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def __contains__(self, var):
        """
        This dunder checks whether a variable has been defined 
        in the current frame or any parent frames.
        """
        if var in self.variables:
            return True

        elif self.parent is None:
            return False

        else:
            return var in self.parent

    def delete(self, var):
        """
        Given a frame and a value, will delete the value associated with
        var from the frame. If the value does not exist, will raise a 
        SchemeEvaluationError.
        """
        if var not in self.variables:
            raise Scheme.NameError("variable doesn't exist in current frame")
        
        else:
            val = self.variables[var]
            del self.variables[var]
            return val
    
    def get_frame(self, var):
        """
        Given a frame and a desired variable, return the frame object in 
        which the variable is defined. If the variable isn't defined, 
        raises a SchemeNameError.
        """
        if var not in self:
            raise Scheme.NameError("variable doesn't exist in any frame")
        
        if var in self.variables:
            return self
        
        else:
            return self.parent.get_frame(var)
            
        
    def set_var(self, var, val):
        self.variables[var] = val

    def get_val(self, var):
        if var in self.variables:
            return self.variables[var]

        elif self.parent is None:
            raise Scheme.NameError("No variable found in any frame")

        else:
            return self.parent.get_val(var)


#creates a built in frame, which has no parents (the ancestor
# of all frames)
built_in_frame = Frame()
built_in_frame.variables = scheme_builtins


class Functions:
    """
    User-defined functions are initialized with a frame, parameters,
    and body of code
    """

    def __init__(self, parameters, body, frame):
        self.parameters = parameters
        self.body = body
        self.enclosing_frame = frame

    # treated like function (takes parameters through the object)
    def __call__(self, vals):
        nu_frame = Frame(self.enclosing_frame)

        if len(vals) != len(self.parameters):
            raise Scheme.EvaluationError("incorrent number of arguments in func")

        for par, val in zip(self.parameters, vals):
            # mapping each variable to the value it was called (in nu_frame)
            nu_frame.set_var(par, val)

        return evaluate(self.body, nu_frame)

    def __str__(self):
        return f"arg: {str(self.parameters)} & body: {str(self.body)}"


def evaluate(tree, frame=None):
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    if frame is None:
        # create a frame where the parent is the built-in frame
        frame = Frame(built_in_frame)

    if isinstance(tree, (int, float)):
        return tree

    if isinstance(tree, str):
        if tree == "#t":
            return "#t"
        elif tree == "#f":
            return "#f"

        elif tree == "nil":
            return "nil"

        return frame.get_val(tree)

    if isinstance(tree, list):
        #####CHECK EVERY SPECIAL WORD HERE
        if len(tree) == 0:
            raise Scheme.EvaluationError

        if tree[0] == "define":
            if isinstance(tree[1], list):
                exp = ["define", tree[1][0], ["lambda", tree[1][1:], tree[2]]]
                return evaluate(exp, frame)

            # setting the value in the given frame
            var = tree[1]
            val = evaluate(tree[2], frame)
            frame.set_var(var, val)
            return val

        elif tree[0] == "lambda":
            parameters = tree[1]
            expression = tree[2]
            return Functions(parameters, expression, frame)

        elif tree[0] == "or":
            for exp in tree[1:]:
                if evaluate(exp, frame) == "#t":
                    return "#t"

            return "#f"

        elif tree[0] == "and":
            # will loop through the individual expressions and evaluate their truth
            for exp in tree[1:]:
                if evaluate(exp, frame) == "#f":
                    return "#f"
            return "#t"

        elif tree[0] == "if":
            boolean = evaluate(tree[1], frame)
            if boolean == "#t":
                return evaluate(tree[2], frame)
            else:
                return evaluate(tree[3], frame)

        elif tree[0] == "del":
            return frame.delete(tree[1])
        
        elif tree[0] == "let":
            args = tree[1]
            exp = tree[2]
            #create temporary frame for args (from let)
            nu_frame = Frame(frame)
            #map the variables in the temporary frame
            for var, val in args:
                nu_frame.set_var(var, evaluate(val, nu_frame))
            
            return evaluate(exp, nu_frame)

        elif tree[0] == "set!":
            var = tree[1]
            val = evaluate(tree[2], frame)
            enc_frame = frame.get_frame(var)
            enc_frame.set_var(var, val)
            return val

        # IN-PLACE LAMBDA EVAL                    OLDD
        elif isinstance(tree[0], list):
            if tree[0][0] == "lambda":
                f = evaluate(tree[0], frame)
                # evaluate each parameter, and then evaluate
                return f([evaluate(par, frame) for par in tree[1:]])

            head = evaluate(tree[0], frame)
            rest = [evaluate(i, frame) for i in tree[1:]]
            return head(rest)

        ####### BUILT-INS ARE HANDLED HERE #########
        elif tree[0] in frame:
            func = evaluate(tree[0], frame)
            # func = frame.get_val(tree[0]) OLD
            eval = func([evaluate(element, frame) for element in tree[1:]])
            return eval

        elif tree[0] not in frame and isinstance(tree[0], str):
            raise Scheme.NameError("function does not exist in the frame")
        # if the string is not 'define' or an operation, raise error
        else:
            raise Scheme.EvaluationError("operation", tree[0], "was invalid")


def result_and_frame(tree, frame=None):
    if frame is None:
        frame = Frame(built_in_frame)
    x = evaluate(tree, frame)
    return (x, frame)
