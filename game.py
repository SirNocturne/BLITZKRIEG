# Program: Superpong !
# Date: 12-10-2015
# Edited by: Cody Huzarski

import pygame, sys, math, time, random
from colors import *
from pygame.locals import *
from entities import *
from controllers import *
from util import LifeCycle

class Game(LifeCycle):
    def __init__(self, surface):
        LifeCycle.__init__(self, surface)

        #Players
        self.player_1 = None
        self.player_2 = None

        #Walls
        self.left_top_wall = None
        self.left_bottom_wall = None
        self.right_top_wall = None
        self.right_bottom_wall = None

        #Ball
        self.ball = Ball(self.surface_size)
        self.vel_x = 0
        self.old_x = self.ball.getX()
        self.old_y = self.ball.getY()

        self.last_collision = time.time()
        self.total_ball_hits = 0

        self.bg_color = COLOR_BLACK
        self.initial_setup()

    def initial_setup(self):
        #Create Players
        self.player_1 = Player("Player 1", 'l', self.surface_size)
        self.player_2 = Player("Player 2", 'r', self.surface_size)

        #Add Controllers to players
        self.player_1.set_controller(KeyboardController(K_w, K_s, K_a, K_d))    
        self.player_2.set_controller(KeyboardController(K_UP, K_DOWN, K_RIGHT, K_LEFT))

        #Create Walls
        self.left_top_wall = Player("Left Top Wall", 'q', self.surface_size)
        self.left_bottom_wall = Player("Left Bottom Wall", 'w', self.surface_size)
        self.right_top_wall = Player("Right Top Wall", 'e', self.surface_size)
        self.right_bottom_wall = Player("Right Bottom Wall", 't', self.surface_size)

    def handle_paddle_collision(self, p, ball):

        #Vertical Paddle
        if p.get_rotation() == 0:
            ball.flipX()

        elif p.get_rotation() < 0 and ball.getY_flip() == 1:
            # Paddle is rotated FORWARD and ball is headed UP
            ball.flipX()
            ball.flipY()
        elif p.get_rotation() > 0 and ball.getY_flip() == 1:
            # Paddle is rotated BACKWARD and ball is headed
            ball.flipX()
        elif p.get_rotation() < 0 and ball.getY_flip() == -1:
            # Paddle is rotated BACKWARD and ball is headed DOWN
            ball.flipX()
            ball.flipY()
        elif p.get_rotation() > 0 and ball.getY_flip() == -1:
            ball.flipX()

    def reset_all(self):
        self.ball.reset()
        self.player_1.reset()
        self.player_2.reset()
        self.left_top_wall.reset()
        self.left_bottom_wall.reset()
        self.right_top_wall.reset()
        self.right_bottom_wall.reset()

        self.total_ball_hits = 0

        self.bg_color = COLOR_BLACK

    def player_collision_event(self, player):
        player = int(player)

        if player is 1:
            self.handle_paddle_collision(self.player_1, self.ball)

        elif player is 2:
            self.handle_paddle_collision(self.player_2, self.ball)

        #LTW
        elif player is 3:
            self.handle_paddle_collision(self.left_top_wall, self.ball)

        #LBW
        elif player is 4:
            self.handle_paddle_collision(self.left_bottom_wall, self.ball)

        #RTW
        elif player is 5:
            self.handle_paddle_collision(self.right_top_wall, self.ball)

        #RBW
        elif player is 6:
            self.handle_paddle_collision(self.right_bottom_wall, self.ball)

        else:
            return False

        self.last_collision = time.time()
        self.total_ball_hits = self.total_ball_hits + 1

    def cycle(self):

        # take input, update movement
        self.player_1.update_movement()
        self.player_2.update_movement()
        self.ball.update_movement()
        # draw
        self.surface.fill(self.bg_color)

        self.player_1.draw(self.surface)
        self.player_2.draw(self.surface)
        self.left_top_wall.draw(self.surface)
        self.left_bottom_wall.draw(self.surface)
        self.right_top_wall.draw(self.surface)
        self.right_bottom_wall.draw(self.surface)

        self.ball.draw(self.surface)

        if (time.time() - self.last_collision) > .05: # Fixes a glitch that causes the ball to collide with paddles infinitely
            # Test collisions
            if self.player_1.did_collide(self.ball):
                self.player_collision_event(1)
            if self.player_2.did_collide(self.ball):
                self.player_collision_event(2)
            if self.left_top_wall.did_collide(self.ball):
                self.player_collision_event(3)
            if self.left_bottom_wall.did_collide(self.ball):
                self.player_collision_event(4)
            if self.right_top_wall.did_collide(self.ball):
                self.player_collision_event(5)
            if self.right_bottom_wall.did_collide(self.ball):
                self.player_collision_event(6)


        # test wall collisions
        if self.ball.getY() <= 0 or self.ball.getY() >= self.surface_size[1]:
            self.ball.flipY()

        if self.ball.getX() <= 0:
            self.player_2.score()
            self.reset_all()

        if self.ball.getX() >= self.surface_size[0]:
            self.player_1.score()
            self.reset_all()

        if self.player_1.get_score() == 10:
            return 1
        if self.player_2.get_score() == 10:
            return 2

        #Calc Velocity
        self.vel_x = self.ball.getX() - self.old_x
        self.vel_y = self.ball.getY() - self.old_y

        #If ball is moving left
        if self.vel_x < 0:
            #Calc final Ball position
            pred_steps = round(abs((self.ball.getX() - 80) / self.vel_x))
            pred_y = round(self.ball.getY() + self.vel_y * pred_steps)
            while (pred_y > 600) or (pred_y < 0):
                if pred_y > 600:
                    temp = pred_y - 600
                    pred_y = 600 - temp
                elif pred_y < 0:
                    pred_y = abs(pred_y)

            if self.player_1.getYPos() < pred_y:
                self.player_1.move('d')
            elif self.player_1.getYPos() > pred_y:
                self.player_1.move('u')

        #If ball is moving right
        if self.vel_x > 0:
            #Calc final Ball position
            pred_steps = round(abs((1000 - self.ball.getX() - 80) / self.vel_x))
            pred_y = round((self.ball.getY()) + self.vel_y * pred_steps)
            while (pred_y > 600) or (pred_y < 0):
                if pred_y > 600:
                    temp = pred_y - 600
                    pred_y = 600 - temp
                elif pred_y < 0:
                    pred_y = abs(pred_y)
            if self.player_2.getYPos() < pred_y:
                self.player_2.move('d')
            elif self.player_2.getYPos() > pred_y:
                self.player_2.move('u')

        #Update Old Coordinates
        self.old_x = self.ball.getX()
        self.old_y = self.ball.getY()

        return "None"

