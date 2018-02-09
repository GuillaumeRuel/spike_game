class player:

    x = 0
    y = 0
    color = (255, 255, 255)
    vely = 0
    velx = 0
    name = ""
    
    jump = False
    is_press = False
        
    def __init__(self, start_pos, velx, color, name):

        self.x = start_pos[0]
        self.y = start_pos[1]
        self.velx = velx
        self.color = color
        self.name = name