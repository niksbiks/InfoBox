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



class Context:
	screen = 0
	
	

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
		u.initLog(screen, "Init " + plugin.name + "...")
		plugin.plugin_object.init(screen)
	
	
def loop(manager, screen):
	active = 0				# The active plugin that is currently displayed
	
	# Build plugin control data structure
	# Dictionary of all plugins:
	#	key = Yapsy plugin name
	# Each control is a list of:
	#	object instance
	#	when to call update
	control = []
	for plugin in manager.getPluginsOfCategory("plugin"):
		c = []
		c.append(plugin.plugin_object)
		c.append(0)			# Run update immediately
		active = plugin.plugin_object
		
        # Main loop
	while True:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit_game()
			if event.type == pygame.KEYDOWN:
				redraw = True
			if event.type == pygame.USEREVENT:
				print "tick"

		# Render active plugin
		active.render(screen)
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

# Load all plugins
pluginManager = loadPlugins()
u.initLog(screen, "Plugins loaded")

# Load configuration
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Init all plugins
initPlugins(pluginManager, screen)

u.initLog(screen, "READY")
time.sleep(3)

# Run "game" loop forever...
loop(pluginManager, screen)
