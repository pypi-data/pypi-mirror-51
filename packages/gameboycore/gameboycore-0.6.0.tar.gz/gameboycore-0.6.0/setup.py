#!/usr/bin/env python
#
# Setup for GameboyCore Python bindings
#
# @author Natesh Narain <nnaraindev@gmail.com>
# @date Dec 2 2016
#

from __future__ import print_function

import os
import sys
import shlex
import platform
import subprocess

import setuptools
from setuptools import setup
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext


class get_pybind_include(object):
    """Helper to get pybind11 include directory"""
    def __init__(self, user=False):
        self.user = user
    
    def __str__(self):
        try:
            import pybind11
            return pybind11.get_include(self.user)
        except:
            return ''

#== GameboyCore Configuration ==
# get this directory
DIR = os.path.dirname(os.path.realpath(__file__))

GAMEBOYCORE_INCLUDE_DIR = os.path.join('src', 'gameboycore', 'include')

# collect sources
sources = []
for current_dir, dirs, files in os.walk('src'):
    # skip test code
    if 'tests' in dirs:
        dirs.remove('tests')
    if 'example' in dirs:
        dirs.remove('example')

    for f in files:
        ext = os.path.splitext(f)[1]
        if ext == '.cpp':
            filepath = os.path.join(current_dir, f)
            sources.append(os.path.relpath(filepath, DIR))

endianness = '__LITTLEENDIAN__' if sys.byteorder == 'little' else '__BIGENDIAN__'

cxx_flags = []
if platform.system() == 'Linux':
    cxx_flags = ['-Wno-format-security']

print('== GameboyCore Configuration ==')
print('-- INCLUDE_DIR: %s' % GAMEBOYCORE_INCLUDE_DIR)
print('-- ENDIAN:      %s' % endianness)
print('-- CXX_FLAGS:   %s' % cxx_flags)
print('')

#== Setup tools ==

# Extension
gameboycore_module = Extension(
    'gameboycore',
    define_macros = [
        (endianness,''),
        ('GAMEBOYCORE_STATIC', ''),
        ('_CRT_SECURE_NO_WARNINGS', '')
    ],
    include_dirs = [
        get_pybind_include(),
        get_pybind_include(user=True),
        GAMEBOYCORE_INCLUDE_DIR
    ],

    sources = sources,

    extra_compile_args = cxx_flags
)

# From https://github.com/pybind/python_example/blob/master/setup.py

# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.
    The c++14 is prefered over c++11 (when it is available).
    """
    flags = ['-std=c++17', '-std=c++14', '-std=c++11']

    for flag in flags:
        if has_flag(compiler, flag):
            return flag

    raise RuntimeError('Unsupported compiler -- at least C++11 support is needed!')

class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }

    if sys.platform == 'darwin':
        c_opts['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args.extend(opts)
        build_ext.build_extensions(self)

readme_file = os.path.join(DIR, 'README.rst')

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().split('\n')

# Read latest git tag

try:
    latest_tag = subprocess.check_output(shlex.split('git describe --tags --abbrev=0'), cwd=DIR).decode('utf-8').strip()
except Exception:
    print('Failed to get latest git tag')
    exit(1)

setup(
    name="gameboycore",
    version=str(latest_tag),

    ext_modules = [gameboycore_module],
    cmdclass = {'build_ext': BuildExt},

    install_requires=requirements,
    setup_requires=requirements,

    # Authoring Information
    author="Natesh Narain",
    author_email="nnaraindev@gmail.com",
    description="Python bindings for Gameboy Core",
    long_description=open(readme_file).read(),
    license="MIT",
    keywords="gameboy emulator emulation",
    url="https://github.com/nnarain/gameboycore-python"
)
