from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'mini_model_description'

# Automatically find all mesh, urdf, launch, and rviz files (must be relative paths)
mesh_files = glob(os.path.join('meshes', '*.stl'))
urdf_files = glob(os.path.join('urdf', '*.xacro')) + glob(os.path.join('urdf', '*.gazebo')) + glob(os.path.join('urdf', '*.trans')) + glob(os.path.join('urdf', '*.urdf'))
launch_files = glob(os.path.join('launch', '*.py'))
rviz_files = glob(os.path.join('rviz', '*.rviz'))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/meshes', mesh_files),
        ('share/' + package_name + '/urdf', urdf_files),
        ('share/' + package_name + '/launch', launch_files),
        ('share/' + package_name + '/rviz', rviz_files),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='satya',
    maintainer_email='satya@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'odom_publisher = mini_model_description.odom_publisher:main',
            'tf_broadcaster = mini_model_description.tf_broadcaster:main',
        ],
    },
)
