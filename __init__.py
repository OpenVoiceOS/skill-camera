# Copyright 2021 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ovos_workshop.skills import OVOSSkill
from ovos_workshop.decorators import intent_handler
from ovos_workshop.decorators import skill_api_method
from ovos_utils.process_utils import RuntimeRequirements
from ovos_utils import classproperty


class CameraSkill(OVOSSkill):
    """
    Camera Skill Class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera_mode = None
        self.save_folder = None

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(internet_before_load=False,
                                   network_before_load=False,
                                   gui_before_load=True,
                                   requires_internet=False,
                                   requires_network=False,
                                   requires_gui=True,
                                   no_internet_fallback=True,
                                   no_network_fallback=True,
                                   no_gui_fallback=False)

    def initialize(self):
        """Perform any initial setup."""
        self.save_folder = os.path.expanduser("~/Pictures")
        if not os.path.isdir(self.save_folder):
            os.makedirs(self.save_folder)

        self.add_event("skill-camera.openvoiceos.homepage",
                       self.handle_open_camera)
        # Register Camera GUI Events
        self.gui.register_handler("CameraSkill.ViewPortStatus",
                                  self.handle_camera_status)
        self.gui.register_handler("CameraSkill.EndProcess",
                                  self.handle_camera_completed)

    @intent_handler("CaptureSingleShot.intent")
    def handle_capture_single_shot(self, _):
        """Take a picture."""
        self.speak_dialog("acknowledge")
        self.gui["singleshot_mode"] = False
        self.take_single_photo()

    @intent_handler("OpenCamera.intent")
    def handle_open_camera(self, _):
        """Open the Camera GUI providing a live view of the camera.

        Provides a button to take the photo.
        Back button to immediately return to Homescreen.
        """
        self.speak_dialog("acknowledge")
        self.gui["singleshot_mode"] = False
        self.handle_camera_activity("generic")

    def handle_camera_completed(self, _=None):
        """Close the Camera GUI when finished."""
        self.gui.remove_page("Camera.qml")
        self.gui.release()

    def handle_camera_status(self, message):
        """Handle Camera GUI status changes."""
        current_status = message.data.get("status")
        if current_status == "generic":
            self.gui["singleshot_mode"] = False
        if current_status == "imagetaken":
            self.gui["singleshot_mode"] = False
        if current_status == "singleshot":
            self.gui["singleshot_mode"] = True

    @skill_api_method
    def take_single_photo(self):
        """Take a single photo using the attached camera."""
        self.handle_camera_activity("singleshot")

    @skill_api_method
    def open_camera_app(self):
        """Open the camera live view mode."""
        self.handle_camera_activity("generic")

    def handle_camera_activity(self, activity):
        """Perform camera action.
        
        Arguments:
            activity (str): the type of action to take, one of:
                "generic" - open the camera app
                "singleshot" - take a single photo
        """
        self.gui["save_path"] = self.save_folder
        if activity == "singleshot":
            self.gui["singleshot_mode"] = True
        if activity == "generic":
            self.gui["singleshot_mode"] = False
        self.gui.show_page("Camera.qml", override_idle=60)

    def stop(self):
        """Respond to system stop command."""
        self.handle_camera_completed()
