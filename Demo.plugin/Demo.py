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

import pygame
from yapsy.IPlugin import IPlugin

from IInfoBoxPlugin import IInfoBoxPlugin
from Utils import Utils



class Demo(IInfoBoxPlugin):
	active = 22
	

	def init(self, context):
		context.u.initLog("Active is=" + str(Demo.active))



	def render(self, context):		
		# Background
		context.screen.fill(Utils.background_colour)

		# Draw top bar
		context.u.drawTopStatusBar("Demo")
		

		height = 30
		font = pygame.font.SysFont(Utils.fontName, height)
		message = font.render("Demo", True, Utils.text_colour)
		r = message.get_rect()
		r.topright = (100, 100)
		context.screen.blit(message, r)



	def update(self, context):
		Demo.active = (Demo.active + 7) % 100
		return 3
