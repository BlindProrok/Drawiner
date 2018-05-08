import kivy
kivy.require("1.10.0")
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from Keyboard import Keyboard
from Mouse import Mouse
from Canvas import Game
from Settings import Settings
from Bullet import Bullet

class DrawinerApp(App):
	bullets = []
	cooldown = {
		"bullet": 0,
		}
	def cooling(self, cooldown_list, speed):
		for cooldown_type in cooldown_list:
			if cooldown_list[cooldown_type] > 0:
				cooldown_list[cooldown_type] = round(cooldown_list[cooldown_type] - 0.1, 1)
	def build(self):
		self.game = Game()
		self.keyboard = Keyboard()
		self.mouse = Mouse()
		self.settings = Settings()
		#Create loop with 1/60 sec delay
		Clock.schedule_interval(self.update, 1.0/60.0)
		return self.game
	def update(self, dt):
		self.cooling(self.cooldown, 0.1)
		self.game.move()
		self.game.ship.move()
		self.game.ship.angle = (Vector(Window.mouse_pos) - 
								Vector(Window.width / 2, Window.height / 2)
								).angle(Vector(1,0))
		for key in (self.keyboard.key_set | self.mouse.key_set):
			if (key in self.settings.keys["Move"]["move_up"]):
				self.game.ship.thrust("forward_t")
			elif (key in self.settings.keys["Move"]["move_down"]):
				self.game.ship.thrust("backward_t")
			elif (key in self.settings.keys["Move"]["move_left"]):
				self.game.ship.thrust("left_t")
			elif (key in self.settings.keys["Move"]["move_right"]):
				self.game.ship.thrust("right_t")
			elif (key in self.settings.keys["Combat"]["fire"]):
				#latter there will be bullet type
				print(self.cooldown["bullet"])
				if self.cooldown["bullet"] == 0:
					bullet = Bullet("bullet", self.game.ship)
					self.bullets += [bullet]
					self.game.add_widget(bullet)
					self.cooldown["bullet"] = 1
			elif (key in self.settings.keys["Utils"]["FA"] and
				 	not self.settings.keys["Utils"]["FA"][1]
				 ):
				self.settings.FA = not self.settings.FA
				self.settings.keys["Utils"]["FA"][1] = True
				if self.settings.FA:
					print("Flight assist enabled")
				else: 
					print("Flight assist disabled")
		for bullet in self.bullets:
			bullet.move()
			if (bullet.coords - self.game.ship.coords).length() > Window.height * 2:
				self.game.remove_widget(bullet)
				self.bullets.remove(bullet)
				del bullet
		#For trigers:
		if (not (self.settings.keys["Utils"]["FA"][0] in
				self.keyboard.key_set
				)
			):
			self.settings.keys["Utils"]["FA"][1] = False
		#------------
		if (self.settings.FA and len(self.keyboard.key_set) == 0):
			self.game.ship.flight_assist()
		if (len(self.keyboard.del_key_set) != 0):
			self.keyboard.key_set -= self.keyboard.del_key_set
			self.keyboard.del_key_set.clear()
		if (len(self.mouse.del_key_set) != 0):
			self.mouse.key_set -= self.mouse.del_key_set
			self.mouse.del_key_set.clear()
DrawinerApp().run()