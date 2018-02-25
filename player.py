from pygame import transform

class player:

    x = 0
    y = 0
    vely = 0
    velx = 0
    name = ""
    width = 105
    height = 70
    jump_speed = -2000
    gravity = 9800
    is_alive = True

    def __init__(self, start_pos, velx, image, name):

        self.x = start_pos[0]
        self.y = start_pos[1]
        self.velx = velx
        self.image = image
        self.name = name

    def get_position(self):
        return self.x, self.y

    #calculating the hitbox with some pixel perfect adjustement
    def get_polygon(self):
        if self.velx > 0:
            return [(self.x + 5, self.y - 5), (self.x + self.width + 5, self.y + (self.height/2)-5), (self.x + 5, self.y + self.height)]
        else:
            return [(self.x + self.width - 10, self.y - 5), (self.x - 15, self.y + (self.height/2)-5), (self.x + self.width - 10, self.y + self.height)]

    def jump(self):
        self.vely = self.jump_speed

    def update_y_velocity(self, t):
        self.vely = self.vely + self.gravity * t

    def update_y_position(self, t):
        self.y = self.y + self.vely * t

    def update_x_position(self, max_width):
        if self.x < 0 or self.x > max_width - self.width:
            self.velx *= -1
            self.image = transform.flip(self.image, True, False)

        self.x += self.velx
