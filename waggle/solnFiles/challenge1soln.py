import os
import subprocess

def writeTestFile(string):
    test_file = open("test.py","w")
    test_file.write(string)
    test_file.close()

def main(client_code):
    writeTestFile(client_code)
    base_dir = "/Users/smeo/django_waggle/waggle/solnFiles/"
    try:
        p = subprocess.Popen('python '+ base_dir +'test.py', stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE, shell=True)
        return p.communicate()  # this gets you pipe values
    except Exception as e:
        return 'error'+e
    else:
        return "else"


if __name__ == '__main__':
    main()
