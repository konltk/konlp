# *****************************************************************************
# Copyright 2004-2008 Steve Menard
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# *****************************************************************************

import os

from . import _jvmfinder
import winreg


class WindowsJVMFinder(_jvmfinder.JVMFinder):
    """
    Windows JVM library finder class
    """
    def __init__(self):
        """
        Sets up members
        """
        # Call the parent constructor
        _jvmfinder.JVMFinder.__init__(self)

        # Library file name
        self._libfile = "jvm.dll"

        # Predefined locations
        self._locations = set()
        for key in (
                # 64 bits (or 32 bits on 32 bits OS) JDK
                'ProgramFiles'
                # 32 bits JDK on 32 bits OS
                'ProgramFiles(x86)'):
            try:
                env_folder = os.environ[key]
                self._locations.add(os.path.join(env_folder, "Java"), )

            except KeyError:
                # Environment variable is missing (ignore)
                pass

        # Search methods
        self._methods = (self._get_from_java_home,
                         self._get_from_registry,
                         self._get_from_known_locations)

    def _get_from_registry(self):
        """
        Retrieves the path to the default Java installation stored in the
        Windows registry

        :return: The path found in the registry, or None
        """
        try:
            jreKey = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\JavaSoft\Java Runtime Environment")
            cv = winreg.QueryValueEx(jreKey, "CurrentVersion")
            versionKey = winreg.OpenKey(jreKey, cv[0])
            winreg.CloseKey(jreKey)

            cv = winreg.QueryValueEx(versionKey, "RuntimeLib")
            winreg.CloseKey(versionKey)
            return cv[0]
        except WindowsError:
            pass

        return None
