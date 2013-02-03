# -*- coding: utf-8 *-*
# InfoBox - Generate data for a display screen
# Copyright 2013 by Nikolaj Brandt Jensen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os

from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin

from Utils import Utils
from IInfoBoxPlugin import IInfoBoxPlugin

	

def main():
	# Find all plugin directories (xxx.plugin)
	dirs = [f for f in os.listdir('.') if f.endswith('.plugin')]
	for x in dirs:
		print x
        
	# Load the plugins from the plugin directory.
	manager = PluginManager()
	manager.setPluginPlaces(dirs)
	manager.setCategoriesFilter({"plugin" : IInfoBoxPlugin})
	manager.collectPlugins()

	y = Utils()
	
	# Loop round the plugins and print their names.
	for plugin in manager.getPluginsOfCategory("plugin"):
		plugin.plugin_object.print_name()
		plugin.plugin_object.foo(y)


	
main()
print "Ready"
