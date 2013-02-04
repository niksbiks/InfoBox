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

from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin



class IInfoBoxPlugin(IPlugin):
        # Do whatever initialisation is necessary
        # Do not call update() from the init() function
	def init(self):
		print 'init() not implemented'

        # Render a frame to the display
        def render(self, screen):
		print ''

        # Update the data needed for rendering frames
        # Must return the number of seconds until next requested update
        # Note that updates are "best effort", and not guaranteed to run at the exact specified delay
	def update(self):
		return 60*60

	def keyInput(self, key):
		print''

	def mouseInput(self, action):
		print ''

	def touchInput(self, action):
		print ''

