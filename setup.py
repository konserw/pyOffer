import sys
from pathlib import Path

import PySide2
from cx_Freeze import setup, Executable

plugins_path = Path(PySide2.__path__[0]) / "plugins"

build_options = {
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

executables = [
    Executable(
        'main.py',
        base='Win32GUI' if sys.platform == 'win32' else None,
        target_name='pyOffer'
    )
]

setup(
    name='pyOffer',
    description='Program for creating business proposals for purchase of items',
    use_scm_version={
        'write_to': 'src/version.py'
    },
    options=dict(build_exe=build_options),
    executables=executables
)
