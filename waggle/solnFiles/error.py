import sys, traceback

try:
    with open("testerror.py") as f:
            code = compile(f.read(), "testerror.py", 'exec')
            exec(code)
except Exception as e:
    print(e)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    #assuming traceback the 3rd item so using [2]
    print( "*** print_tb:")
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    #traceback.print_tb(exc_traceback, limit=1, file=sys.stdout) #syntax probably wrong
