from setuptools import find_packages, setup
from glob import glob
from os.path import join

package_name = 'mini_model_control'

# Automatically find all config files
config_files = glob(join('config', '*.yaml'))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config', config_files),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='satya',
    maintainer_email='satya@todo.todo',
    description='Control package for mini_model rover',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
