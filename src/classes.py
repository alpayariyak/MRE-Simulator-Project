import math
from sim_v3 import cnvwidth, s_to_ms, timestep

y_cells = {250:0, 450:1, 650:2}
class Simulator_Object:

    def __init__(self, obj, x, y, speedx=0, speedy=0, rot=0, width=100, height=100):
        self.obj_class = obj.split('/')[0]
        self.object = obj
        self.rot = (rot * math.pi) / 180
        self.height = height
        self.width = width
        self.speedx = speedx
        self.speedy = speedy
        self.x = x
        self.y = int(y)
        self.hitbox = {"x": int(x + width / 2), "y": int(y + height / 2), "radius": 50}

    def get_state(self):
        return [self.x, self.y, self.speedx, self.speedy]

    def __contains__(self, item):

        if type(item) is Simulator_Object or Trash_Object:
            xcenter_item, ycenter_item = item.hitbox["x"], item.hitbox["y"]

            if self.x + self.width > xcenter_item > self.x and self.y + self.height > ycenter_item > self.y:
                return True
            else:
                return False

    def checkCoordinateIntersection(self, x, y):
        xcenter_self, ycenter_self, radius = self.hitbox["x"], self.hitbox["y"], self.hitbox["radius"]

        dist = math.sqrt(
            math.pow(abs(xcenter_self - x), 2) + math.pow(abs(ycenter_self - y), 2)
        )

        if dist < radius:
            return True
        else:
            return False

    def setSpeed(self, speed_X, speed_y=0):
        self.speedx = speed_X
        self.speedy = speed_y


class Belt(Simulator_Object):
    def __init__(self, belt_number,
                 x=-50,
                 speedx=0,
                 speedy=0,
                 rot=0,
                 width=cnvwidth + 150,
                 height=160,
                 obj='ConvBeltNew'):

        belt_speeds = [300, 200, 400]
        belt_speeds = [speed * timestep for speed in belt_speeds]
        if belt_number == 1:
            self.y = 185
            self.belt_speed = belt_speeds[0]
        elif belt_number == 2:
            self.y = 385
            self.belt_speed = belt_speeds[1]
        elif belt_number == 3:
            self.y = 585
            self.belt_speed = belt_speeds[2]

        super().__init__(obj, x, self.y, speedx, speedy, rot, width, height)


from assets import trash_visibility, trash_classes


class Trash_Object(Simulator_Object):
    def __init__(self, obj, x, y, speedx=0, speedy=0, rot=0, width=100, height=100):
        import global_

        global_.trash_id += 1
        super().__init__(obj, x, y, speedx, speedy, rot, width, height)

        self.deleted = False
        self.visibility = trash_visibility[trash_classes.index(obj)]
        self.row = -999
        self.column = -999
        if self.obj_class == 'reject':
            global_.total_rejects += 1

    def getCell(self):
        return y_cells[self.hitbox['y']], math.floor((self.hitbox['x']+250)/100)  #row, col

    def update_position(self, state):
        self.x = self.x + self.speedx
        self.y = self.y + self.speedy
        self.hitbox["x"] += self.speedx
        self.hitbox["y"] += self.speedy
        self.row, self.column = self.getCell()
        if self.column > 32:
            self.column = 32
        state['grid']['Full Grid'][self.row][self.column][int(self.obj_class != 'reject')] += 1
        state['grid']['Element Grid'][self.row][self.column].append(self)

    def set_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.hitbox = {"x": int(new_x + self.width / 2), "y": int(new_y + self.height / 2), "radius": 50}

    def dragToTrash(self):
        self.x = 1512
        self.y = 90
        self.hitbox = {"x": int(self.x + self.width / 2), "y": int(self.y + self.height / 2), "radius": 50}
        self.speedx = 0
        self.speedy = 0
