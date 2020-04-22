from controllers import *
from rotating_rectangle import RotatingRect
from colors import *

class Player():

    def __init__(self, name, pos, surf_size):
        self.times = 2
        self.__paddle = None
        self.__name = name
        self.__controller = Controller() # default controller. Does nothing when polled

        self.__position = pos

        self.__move_rate = self.times * 5
        self.__rotate_rate = 10
        self.__rotate_max = 360
        self.__rotate_min = -360

        self.__scoring_font = pygame.font.Font("PROMETHEUS.ttf", 64)

        self.__score = 0
        self.color = Color
        self.surface_height = 0
        self.surface_width = 0


        # set dimensions
        self.set_surf_size(surf_size)

        # init
        self.set_initial_pos(self.__position)

    def reset(self):
        self.set_initial_pos(self.__position)

    def set_surf_size(self, surf_size):
        if isinstance(surf_size, tuple):
            self.surface_height = surf_size[1]
            self.surface_width = surf_size[0]
        else:
            raise ValueError

    def set_initial_pos(self, pos):

        paddle_height = 80
        paddle_width = 10
        paddle_margin = 80
        paddle_center = (self.surface_height / 2) - (paddle_height / 2)

        if pos == 'l':
            # position rectangle on left side
            self.__paddle = RotatingRect(paddle_margin, paddle_center, paddle_width, paddle_height)
        elif pos == 'r':
            xpos = self.surface_width - paddle_margin
            self.__paddle = RotatingRect(xpos, paddle_center, paddle_width, paddle_height)

        #Left Top Wall
        elif pos == 'q':
            #Wall Calcs
            paddle_height = 260
            paddle_width = 10
            paddle_margin = 5   #x position
            paddle_center = ((self.surface_height - 120) / 4)
            self.__paddle = RotatingRect(paddle_margin, paddle_center, paddle_width, paddle_height)

        #Left Bottom Wall
        elif pos == 'w':
            #Wall Calcs
            paddle_height = 260
            paddle_width = 10
            paddle_margin = 5   #x position
            paddle_center = ((self.surface_height + 40) / 4) * 3
            self.__paddle = RotatingRect(paddle_margin, paddle_center, paddle_width, paddle_height)
        #Right Top Wall
        elif pos == 'e':
            #Wall Calcs
            paddle_height = 260
            paddle_width = 10
            paddle_margin = 5   #x position
            paddle_center = ((self.surface_height - 120) / 4)
            xpos = self.surface_width - paddle_margin
            self.__paddle = RotatingRect(xpos, paddle_center, paddle_width, paddle_height)
        #Right Bottom Wall
        elif pos == 't':
            #Wall Calcs
            paddle_height = 260
            paddle_width = 10
            paddle_margin = 5   #x position
            paddle_center = ((self.surface_height + 40) / 4) * 3
            xpos = self.surface_width - paddle_margin
            self.__paddle = RotatingRect(xpos, paddle_center, paddle_width, paddle_height)
        else:
            raise ValueError

    def get_paddle(self):
        return self.__paddle

    def get_rotation(self):
        return self.__paddle.get_rotation()

    def get_name(self):
        return self.__name

    def set_controller(self, con):
        self.__controller = con

    def get_score(self):
        return self.__score

    def draw_score(self, surface):

        x_margin = 25
        y_margin = 50

        if self.__position == "l":
            horiz_pos = self.__paddle.getX() + x_margin
        elif self.__position == "r":
            horiz_pos = self.surface_width - 64 - x_margin
        else:
            horiz_pos = self.surface_width / 2

        scoreBlit = self.__scoring_font.render(str(self.__score), 1, (0, 0, 0))
        surface.blit(scoreBlit, (horiz_pos, y_margin))

    def score(self):
        self.__score = self.__score + 1


    def update_movement(self):
        e = self.__controller.poll()

        # eval up/down
        if e[self.__controller.CONTROL_UP]:
            self.__move('u')
        elif e[self.__controller.CONTROL_DOWN]:
            self.__move('d')

        # eval rotation forward/backward

        if e[self.__controller.CONTROL_ROT_FORWARD]:
            self.__rotate('f')
        elif e[self.__controller.CONTROL_ROT_BACKWARD]:
            self.__rotate('b')

    def __move(self, flag):

        if flag == 'u':
            top = self.get_paddle().getY() - (self.__paddle.get_height() / 2)
            if top > 0:
                self.__paddle.setY(self.__paddle.getY() - self.__move_rate) # UP
        elif flag == 'd':
            bottom = self.get_paddle().getY() + (self.__paddle.get_height() / 2)
            if bottom < self.surface_height:
                self.__paddle.setY(self.__paddle.getY() + self.__move_rate) # DOWN

    def move(self, flag):
        self.__move(flag)

    def __rotate(self, flag):

        if flag == 'f':
            #if self.__paddle.get_rotation() < self.__rotate_max:
            if True:
                self.__paddle.set_rotation(self.__paddle.get_rotation() + self.__rotate_rate)

        elif flag == 'b':
            #if self.__paddle.get_rotation() > self.__rotate_min:
            if True:
                self.__paddle.set_rotation(self.__paddle.get_rotation() - self.__rotate_rate)

    #TODO: FIX Rotated Hitbox
    def did_collide(self, ball):

        #For now simple bounding box collision will work but will not look right
        paddle_rect = self.__paddle.get_rect()
        bX = ball.getX()
        bY = ball.getY()

        return paddle_rect.collidepoint(bX, bY)

    def draw(self, surface):
        self.__paddle.draw(surface)
        if self.__position == 'l' or self.__position == 'r': 
            self.draw_score(surface)

    def getXPos(self):
        return self.get_paddle().getX()

    def getYPos(self):
        return self.get_paddle().getY()

class Ball():

    def __init__(self, surf_size):
        self.__rect = None

        self.set_surf_size(surf_size)
        self.__set_initial_values()

    def set_surf_size(self, surf_size):
        if isinstance(surf_size, tuple):
            self.surface_height = surf_size[1]
            self.surface_width = surf_size[0]
        else:
            raise ValueError

    def set_color(self, color):
        self.__color = color

    def reset(self):
        self.__set_initial_values()

    def __set_initial_values(self):
        self.times = 2
        self.__move_rate = self.times * 6
        self.__x = self.surface_width / 2
        self.__y = self.surface_height / 2
        self.__radius = 14
        self.__x_flip = -1
        self.__y_flip = 1
        self.__ball_charge = ""
        self.__color = COLOR_RED

    def get_rect(self):
        return self.__rect

    def set_speed(self, val):
        val = int(val)
        self.__move_rate = val

    def get_speed(self):
        return self.__move_rate

    def update_movement(self):
        self.__x = self.__x + (self.__move_rate * self.__x_flip)
        self.__y = self.__y - (self.__move_rate * self.__y_flip)

    def draw(self, surface):
        self.__rect = pygame.draw.circle(surface, self.__color, (int(self.__x), int(self.__y)), self.__radius)

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getX_flip(self):
        return self.__x_flip

    def getY_flip(self):
        return self.__y_flip

    def flipX(self):
        self.__x_flip = self.__x_flip * -1

    def flipY(self):
        self.__y_flip = self.__y_flip * -1
