import sys

def main(solnFile, testCode):
    sys.argv = [testCode, 'arg2']
    script_locals = dict()
    exec( open(solnFile).read() , dict() , script_locals)
    return script_locals

