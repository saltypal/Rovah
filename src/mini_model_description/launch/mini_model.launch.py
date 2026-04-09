# import os
# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument
# from launch.substitutions import LaunchConfiguration, Command
# from launch_ros.actions import Node
# from launch_ros.parameter_descriptions import ParameterValue
# from ament_index_python.packages import get_package_share_directory


# def generate_launch_description():
#     # Get package directory
#     pkg_share = get_package_share_directory('mini_model_description')
    
#     # Path to URDF file
#     urdf_file = os.path.join(pkg_share, 'urdf', 'mini_model.xacro')
    
#     # Declare launch arguments
#     use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    
#     # Robot state publisher node
#     robot_state_publisher_node = Node(
#         package='robot_state_publisher',
#         executable='robot_state_publisher',
#         parameters=[
#             {
#                 'robot_description': ParameterValue(Command(['xacro', ' ', urdf_file]), value_type=str),
#                 'use_sim_time': use_sim_time,
#             }
#         ],
#     )

#     return LaunchDescription([
#         DeclareLaunchArgument('use_sim_time', default_value='false'),
#         robot_state_publisher_node,
#     ])
