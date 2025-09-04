import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'graduation_project'  # اسم الباكدج بتاعك

    # 1) robot_state_publisher (علشان يpublish الـ URDF)
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
            )
        ]),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # 2) Gazebo server + client (مع plugin factory)
    gzserver = ExecuteProcess(
        cmd=['gzserver', '--verbose', '-s', 'libgazebo_ros_factory.so'],
        output='screen'
    )

    gzclient = ExecuteProcess(
        cmd=['gzclient'],
        output='screen'
    )

    # 3) Spawn الروبوت من الـ robot_description (مع تأخير 5 ثواني)
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'my_bot',
            '-x', '0.0', '-y', '0.0', '-z', '0.3'   # فوق الأرض شوية
        ],
        output='screen'
    )

    gzserver = ExecuteProcess(
    cmd=[
        'gzserver',
        '--verbose',
        '-s', 'libgazebo_ros_factory.so',
        os.path.join(
            get_package_share_directory(package_name),
            'worlds',
            'obstacles.world'
        )
    ],
    output='screen'
)


    delayed_spawn = TimerAction(period=5.0, actions=[spawn_entity])

    return LaunchDescription([
        rsp,
        gzserver,
        gzclient,
        delayed_spawn,
    ])
