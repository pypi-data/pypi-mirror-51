from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError

from setuptools import Extension, find_packages, setup

try:
    from Cython.Build import cythonize

    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False

ext = '.pyx' if USE_CYTHON else '.c'

extensions = [Extension("aiochclient._types", ["aiochclient/_types" + ext])]

if USE_CYTHON:
    extensions = cythonize(extensions, compiler_directives={'language_level': 3})


class BuildFailed(Exception):
    pass


# This class was copy/paced from
# https://github.com/aio-libs/aiohttp/blob/master/setup.py
class ve_build_ext(build_ext):
    # This class allows C extension building to fail.

    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError, DistutilsPlatformError, ValueError):
            raise BuildFailed()


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup_opts = dict(
    name='aiochclient',
    version='1.1.4',
    description='Async http clickhouse client for python 3.6+',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='Danilchenko Maksim',
    author_email='dmax.dev@gmail.com',
    packages=find_packages(exclude=('test*',)),
    package_dir={'aiochclient': 'aiochclient'},
    include_package_data=True,
    install_requires=['aiohttp>=3.0.1'],
    license='MIT',
    url='https://github.com/maximdanilchenko/aiochclient',
    zip_safe=False,
    keywords='clickhouse async python aiohttp',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    ext_modules=extensions,
    extras_require={'speedups': ['aiodns', 'cchardet', 'ciso8601>=2.1.1']},
    cmdclass=dict(build_ext=ve_build_ext),
)

try:
    setup(**setup_opts)
except BuildFailed:
    print("************************************************************")
    print("Cannot compile C accelerator module, use pure python version")
    print("************************************************************")
    del setup_opts['ext_modules']
    del setup_opts['cmdclass']
    setup(**setup_opts)
