from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def run(self):
        _install.run(self)

setup(
    cmdclass = { 'install' : install },
    name = 'tython',
    version = '0.1',
    author = 'tatsy',
    author_email = 'tatsy.mail@gmail.com',
    url = 'https://github.com/tatsy/hydra.git',
    description = 'Python HDR image processing library.',
    license = 'MIT',
    classfieers = [
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    packages = [
        'hydra',
        'hydra.core',
        'hydra.gen',
        'hydra.io',
        'hydra.tonemap'
    ]
)
