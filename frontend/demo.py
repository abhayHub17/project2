import os
def func1():
    stringval = open('media/file.txt').read()
    if os.path.exists("./media/"+stringval):
        os.remove("./media/"+stringval)
    else:
        pass

if __name__ == '__main__':
    # Script2.py executed as script
    # do something
    func1()