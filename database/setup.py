import os

from pkg_resources import parse_requirements
from setuptools import setup, find_packages


__version__ = '0.0.1'


def load_requirements(file_name: str) -> list:
    requirements = []

    with open(file_name, 'r') as fp:
        for req in parse_requirements(fp.read()):
            extras = '[{}]'.format(','.join(req.extras) if req.extras else '')
            requirements.append(
                '{}{}{}'.format(req.name, extras, req.specifier)
            )

    return requirements


PKG_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(PKG_DIR)).strip('/')
SETUP_KWARGS = dict(
    name='database',
    version=__version__,
    author='Egor Danilov',
    author_email='danilov6083@outlook.com',
    license='Apache 2.0',
    python_requires='>=3.8',
    packages=find_packages(exclude=['test*', 'repositories']),
    include_package_data=True,
    install_requires=load_requirements('requirements.txt')
)


if __name__ == '__main__':
    setup(**SETUP_KWARGS)
