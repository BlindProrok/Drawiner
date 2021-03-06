import kivy

kivy.require("1.10.0")
from kivy.app import App
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from Keyboard import Keyboard
from Mouse import Mouse
from Canvas import Game
from Settings import Settings


class DrawinerApp(App):
    bullets = []

    def build(self):
        self.game = Game()
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.settings = Settings()
        # Create loop with 1/60 sec delay
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        return self.game

    def update(self, dt):
        self.game.move()
        self.game.usership.move()
        self.game.usership.cooling(0.1)
        self.game.usership.angle = (Vector(Window.mouse_pos) -
                                Vector(Window.width / 2, Window.height / 2)
                                ).angle(Vector(1, 0))
        for key in (self.keyboard.key_set | self.mouse.key_set):
            if key in self.settings.keys["Move"]["move_up"]:
                self.game.usership.thrust("forward_t")
            elif key in self.settings.keys["Move"]["move_down"]:
                self.game.usership.thrust("backward_t")
            elif key in self.settings.keys["Move"]["move_left"]:
                self.game.usership.thrust("left_t")
            elif key in self.settings.keys["Move"]["move_right"]:
                self.game.usership.thrust("right_t")
            elif key in self.settings.keys["Combat"]["fire"]:
                # latter there will be bullet type
                self.game.usership.fire()
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
            if (bullet.coords - self.game.usership.coords).length() > Window.height * 2:
                self.game.remove_widget(bullet)
                self.bullets.remove(bullet)
                del bullet
        # For triggers:
        if not self.settings.keys["Utils"]["FA"][0] in self.keyboard.key_set:
            self.settings.keys["Utils"]["FA"][1] = False
        # ------------
        if self.settings.FA and len(self.keyboard.key_set) == 0:
            self.game.usership.flight_assist()
        if len(self.keyboard.del_key_set) != 0:
            self.keyboard.key_set -= self.keyboard.del_key_set
            self.keyboard.del_key_set.clear()
        if len(self.mouse.del_key_set) != 0:
            self.mouse.key_set -= self.mouse.del_key_set
            self.mouse.del_key_set.clear()


DrawinerApp().run()
