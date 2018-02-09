class player:

    x = 0
    y = 0
    color = (255, 255, 255)
    vely = 0
    velx = 0
    name = ""
    width = 60
    height = 60
    jump_speed = -2000
    gravity = 9800
    is_alive = True
        
    def __init__(self, start_pos, velx, color, name):

        self.x = start_pos[0]
        self.y = start_pos[1]
        self.velx = velx
        self.color = color
        self.name = name
    
    def get_polygon(self):
        return [(self.x, self.y),(self.x, self.y + self.width),(self.x + self.height, self.y + self.height),(self.x + self.width, self.y)]
    
    def jump(self):
        self.vely = self.jump_speed

    def update_y_velocity(self, t):
        self.vely = self.vely + self.gravity * t
    
    def update_y_position(self, t):
        self.y = self.y + self.vely * t
    
    def update_x_position(self, max_width):
        if self.x < 0 or self.x > max_width - self.width:
            self.velx *= -1

        self.x += self.velx
