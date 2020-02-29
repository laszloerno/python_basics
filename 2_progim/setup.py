# THIS SCRIPT SHOULD BE CALLED SETUP.PY
import cx_Freeze
import os

executables = [
        #                   name of your game script
        cx_Freeze.Executable("kocka.py")
        ]
os.environ['TCL_LIBRARY'] = r'C:\Users\laszl\AppData\Local\Programs\Python\Python37-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\laszl\AppData\Local\Programs\Python\Python37-32\tcl\tk8.6'
cx_Freeze.setup(
        name = "Kocka",
        options = {"build_exe": {"packages":["pygame"]}},
        description = "",
        executables = executables)


#python setup.py build
#python setup.py bdist_msi