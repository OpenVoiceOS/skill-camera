#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'mycroft-camera.mycroftai=ovos_skill_camera:WifiConnectSkill'
# in this case the skill_id is defined to purposefully replace the mycroft version of the skill,
# or rather to be replaced by it in case it is present. all skill directories take precedence over plugin skills


setup(
    # this is the package name that goes on pip
    name='ovos-skill-camera',
    version='0.0.1',
    description='OVOS camera skill plugin',
    url='https://github.com/OpenVoiceOS/skill-camera',
    author='AIIX',
    author_email='',
    license='Apache-2.0',
    package_dir={"ovos_skill_camera": ""},
    package_data={'ovos_skill_camera': ['locale/*', "ui/*", "res/*"]},
    packages=['ovos_skill_camera'],
    include_package_data=True,
    install_requires=["ovos-plugin-manager>=0.0.2"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
