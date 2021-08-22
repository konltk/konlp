# *****************************************************************************
#   Copyright 2004-2008 Steve Menard
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

import warnings

from ._jpackage import *
from ._jclass import *
from ._jarray import *
from ._jwrapper import *
from ._jproxy import *
from ._jexception import *
from ._core import *
from ._gui import *

# Module version (same as in the setup file)
__version_info__ = (0, 5, 5, 4)
__version__ = ".".join(str(x) for x in __version_info__)

java = JPackage("java")
javax = JPackage("javax")

# Deprecation warning
warnings.warn(
    "This version of JPype is now deprecated. Please use this version "
    "instead: https://github.com/jpype-project/jpype",
    DeprecationWarning, stacklevel=2
)
