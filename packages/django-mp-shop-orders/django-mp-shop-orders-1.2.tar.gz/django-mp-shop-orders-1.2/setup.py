
from setuptools import setup, find_packages

from orders import __version__


with open('requirements.txt') as f:
    requires = f.read().splitlines()


url = 'https://github.com/pmaigutyak/mp-shop-orders'


setup(
    name='django-mp-shop-orders',
    version=__version__,
    description='Django shop orders apps',
    long_description=open('README.md').read(),
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, __version__),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=requires
)
