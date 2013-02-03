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

import os, sys, time
import pygame

from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin

from Utils import Utils
from IInfoBoxPlugin import IInfoBoxPlugin



# Globals
screen_height = 400
screen_width = 800
screen_padding = 10
screen_wide = screen_width > screen_height


	

def loadPlugins():
	# Find all plugin directories (xxx.plugin)
	dirs = [f for f in os.listdir('.') if f.endswith('.plugin')]
#	for x in dirs:
#		print x
        
	# Load the plugins from the plugin directory.
	manager = PluginManager()
	manager.setPluginPlaces(dirs)
	manager.setCategoriesFilter({"plugin" : IInfoBoxPlugin})
	manager.collectPlugins()

	return manager



def initPlugins(manager, screen):
	u = Utils()
	
	# Loop round the plugins and init them
	for plugin in manager.getPluginsOfCategory("plugin"):
		u.initLog(screen, plugin.name)
#		plugin.plugin_object.print_name()
#		plugin.plugin_object.foo(u)
	
	
def loop(screen):
        # Main loop
	while True:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit_game()
			if event.type == pygame.KEYDOWN:

				redraw = True
			if event.type == pygame.USEREVENT:
				print "tick"
				text = "test"
				u = Utils()
				u.initLog(screen, "tick")

				height = screen_height / 10

				font = pygame.font.SysFont('arial', height)
				message = font.render(text, True, Utils.text_colour)
				r = message.get_rect()
				r.topright = (screen_width - screen_padding, 0)
		
				screen.blit(message, r)

#		draw_screen()
		pygame.display.flip()

		time.sleep(0.1)



def exit_game():
	pygame.quit()
	sys.exit()


# Start Pygame	
pygame.init()

flags = 0 #pygame.FULLSCREEN + pygame.DOUBLEBUF + pygame.HWSURFACE
screen = pygame.display.set_mode((screen_width, screen_height), flags)

pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1 second timer

u = Utils()

pluginManager = loadPlugins()
u.initLog(screen, "Plugins loaded")

initPlugins(pluginManager, screen)

loop(screen)
