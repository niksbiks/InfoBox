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
import pygame



class Utils:
	text_colour = (255, 255, 255)
	text_colour_warning = (250, 25, 25)
	line_colour = (128, 128, 128)
	background_colour = (0, 0, 0)

	initLogMessages = []

	def initLog(self, screen, message):
		initLogFontSize = 12
		initLogLineCount = screen.get_height() / 12
	
		Utils.initLogMessages.append(message)
		if len(Utils.initLogMessages) > initLogLineCount:
			Utils.initLogMessages.pop(0)
			
		# Background
		screen.fill(Utils.background_colour)

		# Draw text lines
		font = pygame.font.SysFont('arial', initLogFontSize)
		height = 0
		for text in Utils.initLogMessages:
			message = font.render(text, True, Utils.text_colour)
			r = message.get_rect()
			r.topleft = (0, height)
			screen.blit(message, r)
			height += initLogFontSize

		pygame.display.flip()



	def b(self):
		print "Utils is helping"
