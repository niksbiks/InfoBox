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
import requests
from lxml import etree

from IInfoBoxPlugin import IInfoBoxPlugin
from Utils import Utils



class Stog(IInfoBoxPlugin):
	trainsNorth = None
	trainsSouth = None
	activeStation = None
	

	def init(self, context):
		self.activeStation = context.config.get("Stog", "Station")
		# station list



	def render(self, context):		
		# Background
		context.screen.fill(Utils.background_colour)
		

		# Lines
		if context.isScreenWide():
			context.u.drawVDivider(context.screen_height / 10)
		# Station
#		stationDef = stationDict[station]
#		name = stationDef[1]
		context.u.drawTopStatusBar("S-tog")

	
		# First column		
		y = (context.screen_height / 10) * 1.5
		x = 0
	
		# Trains going north
		for (line, destination, direction, departure, train, cancelled) in self.trainsNorth:
			self.drawTrain(context, x, y, line, destination, departure)
			y += context.screen_height / 10

		# Second column		
		y = (context.screen_height / 10) * 1.5
		x = context.screen_width / 2
	
		# Trains going south
		for (line, destination, direction, departure, train, cancelled) in self.trainsSouth:
			self.drawTrain(context, x, y, line, destination, departure)
			y += context.screen_height / 10



	def drawTrain(self, context, x, y, line, destination, departure):
		top = y + Utils.screen_padding
		size = context.screen_height / 10 - Utils.screen_padding - Utils.screen_padding
		self.drawLine(context, x, top, size, line)
		self.drawDestination(context, x, top, size, destination)
		self.drawDeparture(context, x, top, size, departure)
		self.drawMinutes(context, x, top, size)



	def drawLine(self, context, x, top, size, line):
		rect_colour = self.getLineColour(line)
		r = (x + size / 2, top, size, size)
		pygame.draw.rect(context.screen, rect_colour, r)

		font = pygame.font.SysFont(Utils.fontName, size / 2)
		message = font.render(line, True, Utils.text_colour)
		r = message.get_rect()
		r.center = (x + size, top + size / 2)
		context.screen.blit(message, r)



	def drawDestination(self, context, x, top, size, destination):
		font = pygame.font.SysFont(Utils.fontName, size / 2)
		message = font.render(destination, True, Utils.text_colour)
		r = message.get_rect()
		r.midleft = (x + size * 2, top + size / 2)
		context.screen.blit(message, r)



	def drawDeparture(self, context, x, top, size, departure):
		font = pygame.font.SysFont(Utils.fontName, size / 2)
		message = font.render(departure, True, Utils.text_colour)
		r = message.get_rect()
		r.midleft = (x + (context.screen_width / 2) - size * 3, top + size / 2)
		context.screen.blit(message, r)



	def drawMinutes(self, context, x, top, size):
		font = pygame.font.SysFont(Utils.fontName, size / 2)
		message = font.render("min", True, Utils.text_colour)
		r = message.get_rect()
		r.midleft = (x + (context.screen_width / 2) - size * 2, top + size / 2)
		context.screen.blit(message, r)



	def getLineColour(self, line):
		if line == "A":
			return (0, 167, 227)
		if line == "B":
			return (84, 171, 38)
		if line == "Bx":
			return (174, 205, 106)
		if line == "C":
			return (242, 148, 0)
		if line == "E":
			return (122, 111, 172)
		if line == "F":
			return (251, 186, 0)
		if line == "H":
			return (230, 68, 23)
		return (0, 0, 0)



	def update(self, context):
		url = "http://traindata.dsb.dk/stationdeparture/opendataprotocol.svc/Queue()?$filter=StationUic eq '" + self.activeStation + "'"
		context.u.debug(url)
		r = requests.get(url)
	
		root = etree.fromstring(r.content)

		entries = root.xpath("//m:properties", namespaces={"a": "http://www.w3.org/2005/Atom", "d": "http://schemas.microsoft.com/ado/2007/08/dataservices", "m": 
"http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"})

		self.trainsNorth = []
		self.trainsSouth = []
	
		for entry in entries:
			line = entry.xpath("d:Line/text()", namespaces={"a": "http://www.w3.org/2005/Atom", "d": "http://schemas.microsoft.com/ado/2007/08/dataservices", "m": 
"http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"})[0]
			destination = entry.xpath("d:DestinationName/text()", namespaces={"a": "http://www.w3.org/2005/Atom", "d": 
"http://schemas.microsoft.com/ado/2007/08/dataservices", "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"})[0]
			direction = entry.xpath("d:Direction/text()", namespaces={"a": "http://www.w3.org/2005/Atom", "d": "http://schemas.microsoft.com/ado/2007/08/dataservices", 
"m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"})[0]
			departure = entry.xpath("d:MinutesToDeparture/text()", namespaces={"a": "http://www.w3.org/2005/Atom", "d": 
"http://schemas.microsoft.com/ado/2007/08/dataservices", "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"})[0]
			train = entry.xpath("d:TrainType/text()", namespaces={"a": "http://www.w3.org/2005/Atom", "d": "http://schemas.microsoft.com/ado/2007/08/dataservices", "m": 
"http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"})[0]
			cancelled = entry.xpath("d:Cancelled/text()", namespaces={"a": "http://www.w3.org/2005/Atom", "d": "http://schemas.microsoft.com/ado/2007/08/dataservices", 
"m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"})[0]

			if direction == "Nord":
				self.trainsNorth.append((line, destination, direction, departure, train, cancelled))
			else:
				self.trainsSouth.append((line, destination, direction, departure, train, cancelled))

			context.u.debug(line + " " + destination + " " + direction + " " + departure + " " + train + " " + cancelled)

		return 45
