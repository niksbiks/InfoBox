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

import time

import pygame
from yapsy.IPlugin import IPlugin
import requests
import json
from datetime import datetime

from IInfoBoxPlugin import IInfoBoxPlugin
from Utils import Utils



class Weather(IInfoBoxPlugin):
	city = None
	today = None


        
	def init(self, context):
		self.city = context.config.get("Weather", "City")

		

	def render(self, context):		
		weather = []
		for w in self.today['weather']:
			weather.append(w['id'])

		pressure = self.today['main']['pressure']
		humidity = self.today['main']['humidity']
		temp = round(self.today['main']['temp'] - 273.15, 1)
		windDirection = self.today['wind']['deg']
		windSpeed = round(self.today['wind']['speed'], 1)

		weatherIcon = self.getWeatherIconFromCodes(weather)

		warnings = self.getWeatherWarningsFromCodes(weather)
	
		# Background
		context.screen.fill(Utils.background_colour)

		# Top status
		context.u.drawTopStatusBar(self.today['name'])
			
		picture = pygame.image.load(weatherIcon)
		context.screen.blit(picture, (10, 10))

		height = context.screen_height / 10
		font = pygame.font.SysFont(Utils.fontName, height)
		message = font.render(str(temp) + u' °C', True, Utils.text_colour)
		r = message.get_rect()
		r.topleft = (400, height)
		context.screen.blit(message, r)

		height = height + context.screen_height / 10

		message = font.render(str(windSpeed) + " m/s " + self.getWindDirectionAbbreviation(windDirection), True, Utils.text_colour)
		r = message.get_rect()
		r.topleft = (400, height)
		context.screen.blit(message, r)

		height = height + context.screen_height / 10

		message = font.render(str(pressure) + "MPa, " + str(humidity) + "%", True, Utils.text_colour)
		r = message.get_rect()
		r.topleft = (400, height)
		context.screen.blit(message, r)

		height = height + context.screen_height / 10

		message = font.render(warnings, True, Utils.text_colour_warning)
		r = message.get_rect()
		r.topleft = (400, height)
		context.screen.blit(message, r)



	def update(self, context):
# TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		url = "http://openweathermap.org/data/2.1/weather/city/" + self.city
		r = requests.get(url)

		self.today = json.loads(r.content)

		context.u.debug(datetime.now())
		context.u.debug(self.today['weather'])
		context.u.debug(self.today['main'])
		pressure = self.today['main']['pressure']
		context.u.debug(pressure)
		humidity = self.today['main']['humidity']
		context.u.debug(humidity)
		temp = round(self.today['main']['temp'] - 273.15, 1)
		context.u.debug(temp)
		context.u.debug(self.today['wind'])
		windDirection = self.today['wind']['deg']
		windSpeed = round(self.today['wind']['speed'], 1)
		if 'rain' in self.today:
			context.u.debug(self.today['rain'])
	
		return 55 * 60



	def getWeatherIconFromCodes(self, weather):
		filename = "Weather.plugin/Status-weather-"
		style = "blank"
		day_night = False
	
		# Missing 700 mist/haze...

		# Clouds
		if (800 in weather):
			style = "clear"
			day_night = True
		elif (801 in weather):
			style = "few-clouds"
			day_night = True
		elif (802 in weather or 803 in weather):
			style = "clouds"
			day_night = True
		elif (804 in weather):
			style = "many-clouds"

		# Drizzel + Rain
		elif (300 in weather or 310 in weather or 500 in weather or 520 in weather):
			style = "showers-scattered"
			day_night = True
		elif (301 in weather or 302 in weather or 311 in weather or 312 in weather or 321 in weather):
			style = "showers"
			day_night = True
		elif (501 in weather or 502 in weather or 503 in weather or 504 in weather or 521 in weather or 522 in weather):
			style = "showers"
		elif (511 in weather):
			style = "hail"

		# Snow
		elif (600 in weather):
			style = "snow-scattered"
			day_night = True
		elif (601 in weather):
			style = "snow-scattered"
		elif (602 in weather):
			style = "snow"
		elif (611 in weather or 621 in weather):
			style = "snow-rain"

		# Thunderstorm
		elif (200 in weather or 230 in weather or 231 in weather):
			style = "storm"
			day_night = True
		elif (201 in weather or 202 in weather or 210 in weather or 211 in weather or 212 in weather or 221 in weather or 232 in weather):
			style = "storm"
		
		filename += style
# TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		if (day_night):
			if (random.randint(0, 1) == 1):
				filename += "-day"
			else:
				filename += "-night"
		filename += "-icon.png"

		return filename



	def getWeatherWarningsFromCodes(self, weather):
		warnings = ""

		if (900 in weather):
			warnings = "Tornado"
		elif (901 in weather):
			warnings = "Tropisk storm"
		elif (902 in weather):
			warnings = "Storm"
		elif (903 in weather):
			warnings = "Kulde"
		elif (904 in weather):
			warnings = "Varme"
		elif (905 in weather):
			warnings = "Vindhastighed"
		elif (906 in weather):
			warnings = "Hagl"

		return warnings



	def getWindDirectionAbbreviation(self, degree):
		result = str(degree)

		if degree >= 337 or degree < 22:
			result = u'N'
		elif degree < 67:
			result = u'NØ'
		elif degree < 112:
			result = u'Ø'
		elif degree < 157:
			result = u'SØ'
		elif degree < 202:
			result = u'S'
		elif degree < 247:
			result = u'SV'
		elif degree < 292:
			result = u'V'
		elif degree < 337:
			result = u'NV'
		
		return result
