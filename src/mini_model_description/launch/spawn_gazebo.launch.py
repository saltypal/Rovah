import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, EnvironmentVariable, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import (
    PackageNotFoundError,
    get_package_prefix,
    get_package_share_directory,
)


def _odom_publisher_node(enabled):
    return Node(
        package='mini_model_description',
        executable='odom_publisher',
        name='odom_publisher',
        output='screen',
        condition=IfCondition(enabled),
    )


def _tf_broadcaster_node(enabled):
    return Node(
        package='mini_model_description',
        executable='tf_broadcaster',
        name='tf_broadcaster',
        output='screen',
        condition=IfCondition(enabled),
    )


def generate_launch_description():
    pkg_share = get_package_share_directory('mini_model_description')
    pkg_prefix = get_package_prefix('mini_model_description')
    share_root = os.path.join(pkg_prefix, 'share')

    model_arg = DeclareLaunchArgument(
        'model',
        default_value=os.path.join(pkg_share, 'urdf', 'mini_model_ignition.xacro'),
        description='Path to robot model xacro/urdf for Gazebo Fortress',
    )
    entity_name_arg = DeclareLaunchArgument(
        'entity_name',
        default_value='mini_model_ignition',
        description='Name of spawned model in Gazebo',
    )
    start_gz_arg = DeclareLaunchArgument(
        'start_gz',
        default_value='true',
        description='Start Gazebo (ros_gz_sim) from this launch',
    )
    gz_args_arg = DeclareLaunchArgument(
        'gz_args',
        default_value='-r empty.sdf',
        description='Arguments forwarded to ros_gz_sim gz_sim.launch.py',
    )
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation clock',
    )
    publish_odom_arg = DeclareLaunchArgument(
        'publish_odom',
        default_value='true',
        description='Run odom publisher node',
    )
    publish_tf_arg = DeclareLaunchArgument(
        'publish_tf',
        default_value='true',
        description='Run TF broadcaster node',
    )
    spawn_x_arg = DeclareLaunchArgument(
        'spawn_x',
        default_value='0.0',
        description='Initial spawn X position (meters)',
    )
    spawn_y_arg = DeclareLaunchArgument(
        'spawn_y',
        default_value='0.0',
        description='Initial spawn Y position (meters)',
    )
    spawn_z_arg = DeclareLaunchArgument(
        'spawn_z',
        default_value='0.32',
        description='Initial spawn Z position (meters)',
    )
    spawn_roll_arg = DeclareLaunchArgument(
        'spawn_roll',
        default_value='1.57079632679',
        description='Initial spawn roll in radians (+90 deg to align CAD up-axis with Gazebo Z-up)',
    )
    spawn_pitch_arg = DeclareLaunchArgument(
        'spawn_pitch',
        default_value='0.0',
        description='Initial spawn pitch in radians',
    )
    spawn_yaw_arg = DeclareLaunchArgument(
        'spawn_yaw',
        default_value='-1.57079632679',
        description='Initial spawn yaw in radians (-90 deg = clockwise)',
    )

    model = LaunchConfiguration('model')
    entity_name = LaunchConfiguration('entity_name')
    start_gz = LaunchConfiguration('start_gz')
    gz_args = LaunchConfiguration('gz_args')
    use_sim_time = LaunchConfiguration('use_sim_time')
    publish_odom = LaunchConfiguration('publish_odom')
    publish_tf = LaunchConfiguration('publish_tf')
    spawn_x = LaunchConfiguration('spawn_x')
    spawn_y = LaunchConfiguration('spawn_y')
    spawn_z = LaunchConfiguration('spawn_z')
    spawn_roll = LaunchConfiguration('spawn_roll')
    spawn_pitch = LaunchConfiguration('spawn_pitch')
    spawn_yaw = LaunchConfiguration('spawn_yaw')

    # Ensure Gazebo Fortress can resolve model://mini_model_description/... URIs.
    resource_path_value = [
        share_root,
        os.pathsep,
        pkg_share,
        os.pathsep,
        os.path.join(pkg_share, 'meshes'),
        os.pathsep,
        os.path.join(pkg_share, 'urdf'),
    ]

    gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=resource_path_value + [
            os.pathsep,
            EnvironmentVariable('GZ_SIM_RESOURCE_PATH', default_value=''),
        ],
    )
    ign_resource_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=resource_path_value + [
            os.pathsep,
            EnvironmentVariable('IGN_GAZEBO_RESOURCE_PATH', default_value=''),
        ],
    )

    robot_description = ParameterValue(Command(['xacro', ' ', model]), value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': use_sim_time,
        }],
        output='screen',
    )

    try:
        get_package_share_directory('ros_gz_bridge')
        clock_bridge_node = Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
            output='screen',
        )
    except PackageNotFoundError:
        clock_bridge_node = LogInfo(
            msg='Package ros_gz_bridge not found. /clock bridge will not run.'
        )

    try:
        ros_gz_sim_share = get_package_share_directory('ros_gz_sim')
        gz_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
            ),
            condition=IfCondition(start_gz),
            launch_arguments={'gz_args': gz_args}.items(),
        )

        spawn_entity = Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', entity_name,
                '-topic', '/robot_description',
                '-x', spawn_x,
                '-y', spawn_y,
                '-z', spawn_z,
                '-R', spawn_roll,
                '-P', spawn_pitch,
                '-Y', spawn_yaw,
            ],
            output='screen',
        )
    except PackageNotFoundError:
        gz_launch = LogInfo(
            msg='Package ros_gz_sim not found. Install ros-humble-ros-gz-sim.'
        )
        spawn_entity = LogInfo(
            msg='Skipping robot spawn because ros_gz_sim is unavailable.'
        )

    return LaunchDescription([
        model_arg,
        entity_name_arg,
        start_gz_arg,
        gz_args_arg,
        use_sim_time_arg,
        publish_odom_arg,
        publish_tf_arg,
        spawn_x_arg,
        spawn_y_arg,
        spawn_z_arg,
        spawn_roll_arg,
        spawn_pitch_arg,
        spawn_yaw_arg,
        gz_resource_path,
        ign_resource_path,
        gz_launch,
        robot_state_publisher_node,
        clock_bridge_node,
        spawn_entity,
        _odom_publisher_node(publish_odom),
        _tf_broadcaster_node(publish_tf),
    ])
