from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(include_files=["libssl-1_1-x64.dll", "libpq.dll", "libintl-8.dll", "libiconv-2.dll", "libcrypto-1_1-x64.dll"])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, targetName = 'pyOffer')
]

setup(name='pyOffer',
      version = '0.1',
      description = 'Program for creating business proposals for purchase of items',
      options = dict(build_exe = buildOptions),
      executables = executables)
