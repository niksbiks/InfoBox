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
	context = None
	text_colour = (255, 255, 255)
	text_colour_warning = (250, 25, 25)
	line_colour = (128, 128, 128)
	background_colour = (0, 0, 0)
	fontName = "arial"
        
	initLogMessages = []

        # Only call this from the init() function!
	def initLog(self, message):
		initLogFontSize = 12
		initLogLineCount = self.context.screen_height / 12
	
		Utils.initLogMessages.append(message)
		if len(Utils.initLogMessages) > initLogLineCount:
			Utils.initLogMessages.pop(0)
			
		# Background
		self.context.screen.fill(Utils.background_colour)

		# Draw text lines
		font = pygame.font.SysFont('arial', initLogFontSize)
		height = 0
		for text in Utils.initLogMessages:
			message = font.render(text, True, Utils.text_colour)
			r = message.get_rect()
			r.topleft = (0, height)
			self.context.screen.blit(message, r)
			height += initLogFontSize

		pygame.display.flip()



	# Draw a horizontal line at height 'y'
	def draw_h_divider(self, y):
		pygame.draw.line(self.context.screen, Utils.line_colour, (0, y), (screen_width, y))



	# Draw a line in the middle of the screen from y to bottom of screen
	def draw_v_divider(self, y):
		pygame.draw.line(self.context.screen, Utils.line_colour, (screen_width / 2, y), (screen_width / 2 , screen_height))



	# Draw top status bar without doing flip()
	def drawTopStatusBar(self):
		draw_h_divider(40)
