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

import os, sys, time, pprint
from ConfigParser import SafeConfigParser
import codecs
import pygame
from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin

from Utils import Utils
from IInfoBoxPlugin import IInfoBoxPlugin



class Context:
	screen = None
	u = None
	config = None
	screen_height = 400
	screen_width = 800
	
	def isScreenWide(self):
		if self.screen_width > self.screen_height:
			return True
		else:
			return False
		
	

def loadConfig():
	parser = SafeConfigParser()
	f = codecs.open('configuration.ini', 'r', encoding='utf-8')
	parser.readfp(f)

	return parser



def loadPlugins():
	# Find all plugin directories (xxx.plugin)
	dirs = [f for f in os.listdir('.') if f.endswith('.plugin')]
        
	# Load the plugins from the plugin directory.
	manager = PluginManager()
	manager.setPluginPlaces(dirs)
	manager.setCategoriesFilter({"plugin" : IInfoBoxPlugin})
	manager.collectPlugins()

	return manager



def initPlugins(manager, context):
	# Loop round the plugins and init them
	for plugin in manager.getPluginsOfCategory("plugin"):
		context.u.initLog("Init " + plugin.name + "...")
		plugin.plugin_object.init(context)
	
	
def loop(manager, context):
	active = None	# The active plugin that is currently displayed
	nextActiveChange = 0
	
	# Build plugin control data structure
	# Dictionary of all plugins:
	#	key = Yapsy plugin name
	# Each control is a list of:
	#	plugin name
	#	object instance
	#	when to call update
	control = {}
	
	for plugin in manager.getPluginsOfCategory("plugin"):
		c = []
		c.append(plugin.name) # 1: Name
		c.append(plugin.plugin_object) # 2: Instance
		nextUpdate = plugin.plugin_object.update(context) + time.time()	# Run update immediately
		c.append(nextUpdate) # 3: Update time
		control[plugin.name] = c
		
        # Main loop
	while True:
		
		# Switch display?
		if time.time() > nextActiveChange:
			active = nextActive(control, active)
			nextActiveChange = time.time() + 15 # !!!!!!!!!!!!!! .displayTime in %
			context.u.debug("New display: " + str(active))

		# Look for events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit_game()
			if event.type == pygame.KEYDOWN:
				# Exit (Esc)
				# Next display (arrow right)
				# Debug (Space)
				print "Now: " + str(time.time())
				pprint.pprint(control)
				print "Active: "
				pprint.pprint(active)
			if event.type == pygame.USEREVENT:
				context.u.debug("tick")

		# Check for necessary updates
		for key in control:
			if control[key][2] < time.time():			# Is requested update time reached?
				control[key][2] = control[key][1].update(context) + time.time()	# Call update and store new requested update time

		# Render active plugin
		active.render(context)
		pygame.display.flip()

		time.sleep(0.1)



# Find next display, round-robin style, based on plugin load order
def nextActive(control, active):
	newActive = control[control.keys()[0]][1]	# Default to first one loaded

	nextIsNewActive = False
	for key in control.keys():	# Find next after active, if any
		if nextIsNewActive:
			newActive = control[key][1]
			nextIsNewActive = False
		if control[key][1] == active:
			nextIsNewActive = True
	return newActive


	
def exit_game():
	pygame.quit()
	sys.exit()



# Start Pygame	
pygame.init()

#Setup global context (ugly style)
c = Context()
c.u = Utils()
c.u.context = c

flags = 0 #pygame.FULLSCREEN + pygame.DOUBLEBUF + pygame.HWSURFACE
screen = pygame.display.set_mode((c.screen_width, c.screen_height), flags)

c.screen = screen

# Load all plugins
pluginManager = loadPlugins()
c.u.initLog("Plugins loaded")

# Load configuration
c.u.initLog("Configuration:")
c.config = loadConfig()
for section_name in c.config.sections():
	c.u.initLog(section_name)
	for name, value in c.config.items(section_name):
		c.u.initLog("   " + name + ": " + value)

# Init all plugins
initPlugins(pluginManager, c)

c.u.initLog("READY")
time.sleep(4)

# Start 1 second timer
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Run "game" loop forever...
loop(pluginManager, c)
