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

from jpype import javax, JObject

__JMenuBar = javax.swing.JMenuBar
__JMenu = javax.swing.JMenu


def buildMenuBar(menuDef):
    mb = __JMenuBar()
    for i in menuDef:
        jm = buildMenu(i[0], i[1])
        mb.add(JObject(jm, __JMenu))
    return mb


def buildMenu(name, menuDef):
    jm = __JMenu(name)
    for i in menuDef:
        if i is None:
            jm.addSeparator()
        elif isinstance(i, list) or isinstance(i, tuple):
            jm2 = buildMenu(i[0], i[1])
            jm.add(jm2)
        else:
            jm.add(i.proxy)

    return jm
