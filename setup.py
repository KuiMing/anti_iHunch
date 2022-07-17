"""
install setup for anti_iHunch
"""
from os import path

from setuptools import find_packages, setup

__version__ = '0.1.1'

PACKAGE_PATH = path.abspath(path.dirname(__file__))

with open(path.join(PACKAGE_PATH, 'requirements.txt'), 'r') as file:
    ALL_REQS = file.read().split('\n')
    ALL_REQS.remove("")
    INSTALL_REQUIRES = [x.strip() for x in ALL_REQS if 'git+' not in x]
    GITHUB_LINKS = [
        file.strip().replace('git+', '') for x in ALL_REQS
        if x.startswith('git+')
    ]
file.close()
setup(name='anti_iHunch',
      packages=find_packages(exclude=['__pycache__', 'build', 'dist']),
      version=__version__,
      description='Avoid Forward Head Posture',
      python_requires='>=3.7',
      long_description=
      "Detect Forward Head Posture with face detection and give alarm",
      author='Kui-Ming Chen',
      author_email='benjamin0901@gmail.com',
      url='https://github.com/KuiMing/anti_iHunch',
      install_requires=INSTALL_REQUIRES,
      dependency_links=GITHUB_LINKS,
      keywords=['future', 'python', 'line'],
      include_package_data=True)
