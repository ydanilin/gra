from distutils.core import setup, Extension
# C:\Miniconda2\Lib\distutils\msvc9compiler.py
# C:\Users\Yuretzz\AppData\Local\Programs\Common\Microsoft\Visual C++ for Python\9.0\vcvarsall.bat
# build_ext --inplace

setup(
    name='gvzpassage',
    ext_modules=[Extension("gvzpassage",
                           ["gvzpassage.cpp"],
                           # define_macros=[('GVDLL', None)],
# http://stackoverflow.com/questions/2885750/difficulties-getting-graphviz-working-as-a-library-in-c
                           include_dirs=['C://Program Files (x86)//Graphviz2.38//include'],
                           library_dirs=['C://Program Files (x86)//Graphviz2.38//lib//release//lib'],
                           libraries=["cdt", "cgraph", "gvc"],
                           )
                 ]
)
