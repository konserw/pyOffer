import sys
from pathlib import Path

import PySide2
from cx_Freeze import setup, Executable

from main import VERSION

plugins_path = Path(PySide2.__path__[0]) / "plugins"

buildOptions = {
    "include_files": [
        "libssl-1_1-x64.dll",
        "libpq.dll",
        "libintl-8.dll",
        "libiconv-2.dll",
        "libcrypto-1_1-x64.dll",
        plugins_path / "sqldrivers",
        plugins_path / "platforms",
        plugins_path / "printsupport",
        plugins_path / "styles",
        plugins_path / "imageformats",
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
      version=str(VERSION),
      description='Program for creating business proposals for purchase of items',
      options=dict(build_exe=buildOptions),
      executables=executables)
