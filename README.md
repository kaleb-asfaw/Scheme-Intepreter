Scheme is a dialect of the Lisp family of programming languages. It was created during the 1970s at the MIT Computer Science and Artificial Intelligence Laboratory (MIT CSAIL). This repository is a Python implementation of a Scheme Interpreter, which is Turing-complete, and supports basic programming fundamentals, including arithmetic operations, variables, if-else statements, lambda expressions, functions (w/ lexical scoping), recursion, iteration, file imports, and so much more. Below is a guide on basic Scheme syntax so that anyone can use the interpreter:


                                                    |          Python         |        Scheme
                                                    |                         |
             Arithmetic (applies to any operation)  |           2 + 3         |         (+ 2 3)
                                                    |                         |
                      Variable Assignment           |           x = 5         |      (define x 5)
                                                    |                         |
                       Defining Function            | def craft(stick, wood): |   (define (craft stick wood)
                                                    |   function body...      |      function body...  
                                                                                                     )
This is how inputs/outputs will appear within the interpreter (specifically in the terminal or console log):

                      in>  (define x 7)            in> (+ x 10)              in> x
                          out> 7                       out> 17                 out> 7          

Similarly, functions must be defined, and then called just like this:

                            in> (define (square x) (* x x))        in> (square 2)
                                out> FUNCTION OBJECT                   out> 4


How it works:
To begin, run the 'run_interpreter.py' file, which will prompt the interpreter to start up in the console log/terminal. Text entered into the terminal is parsed through, (lines 30-119 under the functions 'tokenize' and 'parse'). Parsed text is then evaluated (via the 'evaluate' function on lines 528-640). This function is responsible for processing the many built-in and user-defined functions that make up the bulk of 'built_ins.py'. If the parsed text cannot be evaluated, a particular SchemeError message will pop up detailing why your code is not running. The general errors are concentrated in the 'errors.py'

# Happy coding!
                                                                                                
        
