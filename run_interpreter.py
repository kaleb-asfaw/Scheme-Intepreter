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
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()
    interpreter(True)
    # source = "(define circle-area (lambda (r) (* 3.14 (* r r))))"
    # source2 = '(w3!|]\\d5y8[]1$)'
    # source3 = '(multi\nline\nstatement)'
    # source4 = '(multiline ; with comments\n statement) ; with comments'
    # source5 = "(cat (dog (tomato)))"
    # tokens = tokenize(source)
    # print(tokens)
    # print(parse(tokenize(source)))
    # print(evaluate(['+', 3, ['-', 7, 5]]))
    # print(result_and_frame([['lambda', ['x', 'y', 'z'], ['+', ['*', 'x', 'x'], ['*', 'y', 'y'], ['*', 'z', 'z']]], 7, 8, 9]))
    # print(evaluate(['and', ['>', 3, 2], ['not', ['equal?', 3, 4]] ,['<', 7, 8, 9], '#t', ["equal?", 1, 0, 0, 0]]))
    # blud = 5
    # x = ["cons", 1, ["cons", 2, ["cons", 3, ["cons", blud, "nil"]]]]
    # x = ["cons", 1, 2]
    # l = 'nil'
    # L = evaluate(l)
    # # print(list_len('nil'))
    # hi = evaluate(x)
    # print(hi)
    # print(check_list(x))
    # # print(list_len(hi))
    # # print(get_val_at_i(hi, 2))
    # # print(listt([1,2,3,4,3]))
    # l1 = listt([1,2, 3, 4, 5])
    # l2 = listt([6, 7, 8, 9])
    # print(check_list(l1))
    # print(check_list(hi))
    # print(get_val_at_i(hi, 0))