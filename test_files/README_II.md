The interpreter also supports file imports. To utilize this functionality, we need to enter the file name as a command line argument:

  
Instead of running the file with
                                            
                                             $ python3 run_interpreter.py


We can do:
                                                      
                                        $ python3 run_interpreter.py path/file
                                        
For example, if we wanted to use the functions and variable definitions already declared within the definitions.scm, I would simply enter this into the command line:

                                   $ python3 run_interpreter.py test_files/definitions.scm
                                        
There are plenty of files to try this out on, you can feel free to type up your own functions on a separate file before importing them into the interpreter. My favorite is ndmines.scm (n-dimensional mines), a lab that I completed in Python during my freshman year spring for my data structures class, which is fully solvable when translated to Scheme using this interpreter.
