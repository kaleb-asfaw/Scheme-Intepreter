import sys 
import traceback
import built_ins as b
import errors as Scheme

sys.setrecursionlimit(100000)

def interpreter(verbose=False):
    """
    Run file to load interpreter.
    """
    _, frame = b.result_and_frame(['+'])  # make a global frame
    
    for arg in sys.argv[1:]:
        b.evaluate_file(arg, frame)
    print("  ")
    print("Welcome to my Scheme interpreter!")
    print("Visit the 'Python -> Scheme' folder to if you are not familiar with the language") 
    print("If you would like to exit, type 'QUIT'. Begin typing below.")
    print("  ")
        
    while True:
        input_str = input("in> ")
        if input_str == "QUIT":
            print("  ")
            print("Thanks for using. For more cool projects, visit github.com/kaleb-asfaw")
            print("  ")
            return
        try:
            token_list = b.tokenize(input_str)
            if verbose:
                print("tokens>", token_list)
            expression = b.parse(token_list)
            if verbose:
                print("expression>", expression)
            output, frame = b.result_and_frame(expression, frame)
            print("  out>", output)
        except Scheme.Error as e:
            if verbose:
                traceback.print_tb(e.__traceback__)
            print("Error>", repr(e))

if __name__ == "__main__":
    interpreter(True)
    
