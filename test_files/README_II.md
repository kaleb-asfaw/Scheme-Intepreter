The interpreter also supports file imports. To utilize this functionality, we need to enter the file name as a command line argument:

  
Instead of running the file with
                                            
                                              $ python3 run_interpreter.py


We can do:
                                                      
                                        $ python3 run_interpreter.py 'path/file/'
                                        
For example, if we wanted to use the functions and variable definitions already declared within the definitions.scm, I would simply enter this into the command line:

                                        $ python3 run_interpreter.py test_files/definitions.scm
                                        
