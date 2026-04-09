import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Get package directory
    pkg_share = get_package_share_directory('mini_model_description')
    
    # Declare launch arguments
    model_arg = DeclareLaunchArgument(
        'model',
        default_value=os.path.join(pkg_share, 'urdf', 'mini_model.urdf'),
        description='Path to robot URDF file'
    )
    gui_arg = DeclareLaunchArgument(
        'gui',
        default_value='true',
        description='Flag to enable joint_state_publisher_gui'
    )
    rvizconfig_arg = DeclareLaunchArgument(
        'rvizconfig',
        default_value=os.path.join(pkg_share, 'rviz', 'mini_model.rviz'),
        description='Path to RViz config file'
    )
    
    # Get arguments
    model = LaunchConfiguration('model')
    gui = LaunchConfiguration('gui')
    rvizconfig = LaunchConfiguration('rvizconfig')
    
    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': ParameterValue(Command(['cat ', model]), value_type=str)
        }]
    )
    
    # Joint State Publisher GUI (for manual control)
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        condition=IfCondition(gui)
    )
    
    # RViz
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rvizconfig],
    )
    
    return LaunchDescription([
        model_arg,
        gui_arg,
        rvizconfig_arg,
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
    ])
