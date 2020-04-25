import os
import sys

import PySide2
from cx_Freeze import setup, Executable

plugins_path = os.path.join(PySide2.__path__[0], "plugins")

buildOptions = {
    "include_files": ["libssl-1_1-x64.dll", "libpq.dll", "libintl-8.dll", "libiconv-2.dll", "libcrypto-1_1-x64.dll",
                      os.path.join(plugins_path, "sqldrivers"),
                      os.path.join(plugins_path, "platforms"),
                      os.path.join(plugins_path, "printsupport"),
                      "translations",
                      ],
    "excludes": ["tkinter", "unittest", "email", "http", "xml", "pydoc", "pdb"],
    "zip_include_packages": ["PySide2", "shiboken2", "encodings"],
    "optimize": 2
}

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base, targetName='pyOffer')
]

setup(name='pyOffer',
      version='0.1',
      description='Program for creating business proposals for purchase of items',
      options=dict(build_exe=buildOptions),
      executables=executables)
