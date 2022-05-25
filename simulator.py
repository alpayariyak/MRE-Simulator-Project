import math
import random

#
game_length = 180
s_to_ms = 1000
timestep = 0.1
create_interval = 0.5 * s_to_ms  # 5 seconds
#

# page height, easier to reference js code

cnvheight = 1230  # or 800
cnvwidth = 3024

#
totalObjects = -11
totalRejects = 0
trash_id = 0
#

aluminumCan = [f'aluminumCan/can{i}.png' for i in range(10)]
cardboard = [f'cardboard/cardboard{i}.png' for i in range(10)]
carton = [f'carton/carton{i}.png' for i in range(10)]
glassBottle = [f'glassBottle/glassBottle{i}.png' for i in range(9)]
paper = [f'paper/paper{i}.png' for i in range(21)]
paperBag = [f'paperBag/paperBag{i}.png' for i in range(15)]
plasticBag = [f'plasticBag/plasticBag{i}.png' for i in range(23)]
plasticBottle = [f'plasticBottle/plasticBottle{i}.png' for i in range(12)]
reject = [f'reject/reject{i}.png' for i in range(20)]

trash_classes = aluminumCan \
                + cardboard \
                + carton \
                + glassBottle \
                + paper \
                + paperBag \
                + plasticBag \
                + plasticBottle \
                + reject


class Simulator_Object:

    def __init__(self, obj, x, y, speedx=0, speedy=0, rot=0, width=100, height=100):
        global s_to_ms, timestep
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

        global totalObjects
        global totalRejects
        totalObjects += 1

    def get_state(self):
        return [self.x, self.y, self.speedx, self.speedy]

    def __contains__(self, item):

        xcenter_self, ycenter_self, radius = self.hitbox["x"], self.hitbox["y"], self.hitbox["radius"]

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

    def setSpeed(self, speed_X, speedy_y=0):
        self.speedx = speed_X
        self.speedy_y = speedy_y


class Belt(Simulator_Object):
    def __init__(self, belt_number,
                 x=-50,
                 speedx=0,
                 speedy=0,
                 rot=0,
                 width=cnvwidth + 150,
                 height=160,
                 obj='ConvBeltNew'):

        global s_to_ms, timestep

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


# might not need these
# endboxes
end1 = Simulator_Object('undergroundConvBelt',
                        cnvwidth - 80,  # x
                        150,  # y
                        width=100,  # width
                        height=200)  # height

end2 = Simulator_Object('undergroundConvBelt',
                        cnvwidth - 80,  # x
                        350,  # y
                        width=100,  # width
                        height=200)  # height

end3 = Simulator_Object('undergroundConvBelt',
                        cnvwidth - 80,  # x
                        550,  # y
                        width=100,  # width
                        height=200)  # height

# belts

belt1 = Belt(1)

belt2 = Belt(2)

belt3 = Belt(3)

trash_bin = Simulator_Object('trashbin',
                             cnvwidth / 2 - 75,
                             15,
                             width=150,
                             height=150)

belts = [belt1, belt2, belt3]
endboxes = [end1, end2, end3]

trash_objects = {}  # id:object


class Trash_Object(Simulator_Object):
    def __init__(self, obj, x, y, speedx=0, speedy=0, rot=0, width=100, height=100):
        global trash_id

        trash_id = trash_id + 1
        super().__init__(obj, x, y, speedx, speedy, rot, width, height)

        self.deleted = False

        global totalRejects
        if self.obj_class == 'reject':
            totalRejects += 1

    def update_position(self):
        self.x = self.x + self.speedx
        self.y = self.y + self.speedy
        self.hitbox["x"] += self.speedx
        self.hitbox["y"] += self.speedy

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


def makeRandomTrash(beltNumber):
    if beltNumber == 1:
        globals()[f'trash_object_{trash_id}'] = Trash_Object(
            random.choice(trash_classes),
            -100 - random.randint(0, 150),
            200,
            speedx=belt1.belt_speed,
            speedy=0,
            rot=random.randint(-90, 90)
        )
        trash_objects[trash_id] = globals()[f'trash_object_{trash_id}']
    elif beltNumber == 2:
        globals()[f'trash_object_{trash_id}'] = Trash_Object(
            random.choice(trash_classes),
            -100 - random.randint(0, 150),
            400,
            speedx=belt2.belt_speed,
            speedy=0,
            rot=random.randint(-90, 90)
        )
        trash_objects[trash_id] = globals()[f'trash_object_{trash_id}']
    else:
        globals()[f'trash_object_{trash_id}'] = Trash_Object(
            random.choice(trash_classes),
            -100 - random.randint(0, 150),
            600,
            speedx=belt3.belt_speed,
            speedy=0,
            rot=random.randint(-90, 90)
        )
        trash_objects[trash_id] = globals()[f'trash_object_{trash_id}']


# makeRandomTrash(1)
# makeRandomTrash(2)
# makeRandomTrash(3)
#
#
# for i in range(5):
#     for id, trash in trash_objects.items():
#         trash.update_position()
#         if i % 1 == 0:
#             print(f"TrashID: {id}  State: {trash.get_state()}")
#         if id == 3 and i % 1 == 0:
#             print("\n")


randomtr = Trash_Object(
    'aluminumCan',
    1512,
    90,
    speedx=0,
    speedy=0,
    rot=random.randint(-90, 90)
)

print(randomtr in trash_bin)
print(trash_bin.checkCoordinateIntersection(1512, 90))

score = 100


class Mouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speedx = x
        self.speedy = y


j = 0
k = 0
m = 0
reward = 100

f = open('MRE-Simulator-Project/rollout.txt', 'w')
for i in range(180000):  # 180000 ms in 3 minutes

    if i % create_interval == 0:
        makeRandomTrash(1)
        makeRandomTrash(2)
        makeRandomTrash(3)
        j += 1

    if i % (timestep * s_to_ms) == 0:
        k += 1
        deletecalled = False
        for trash_obj_id, trash_obj in trash_objects.items():


            if trash_obj.x > cnvwidth:

                if trash_obj.obj_class == 'reject' and not trash_obj.deleted:
                    reward -= 1
                    score -= 1
                    # print(f'Trash ID {trash_obj_id} reject, total: {totalRejects}')
                trash_obj.deleted = True

            if not trash_obj.deleted:

                # policy - always drag
                # if cnvwidth/2 + 200 > trash_obj.hitbox["x"] > cnvwidth/2 - 200:
                #     trash_obj.dragToTrash()
                #     print("trash in the middle")

                if trash_obj.checkCoordinateIntersection(cnvwidth / 2, 250) and trash_obj.obj_class == 'reject':
                    trash_obj.dragToTrash()
                    deletecalled = True
                    reward -= 0.1
                    m += 1

                if trash_obj in trash_bin and trash_obj.obj_class != 'reject':
                    score -= 1
                    reward -= 1
                    print(f'Trash ID {trash_obj_id} deleted')
                    trash_obj.deleted = True

                elif trash_obj in trash_bin and trash_obj.obj_class == 'reject':
                    trash_obj.deleted = True

                else:
                    if 300 > trash_obj.hitbox['y'] > 200:
                        trash_obj.setSpeed(belt1.belt_speed)
                    elif 500 > trash_obj.hitbox['y'] > 400:
                        trash_obj.setSpeed(belt2.belt_speed)
                    elif 700 > trash_obj.hitbox['y'] > 600:
                        trash_obj.setSpeed(belt3.belt_speed)
                    else:
                        trash_obj.setSpeed(0)

                    trash_obj.update_position()
                    print(f"TrashID: {trash_obj_id}  State: {trash_obj.get_state()}")
                    f.write(f"\nTrashID: {trash_obj_id}  State: {trash_obj.get_state()}")

        print(f"Score: {score}\nTotal Rejects: {totalRejects}"
              f"\nTimestep: {k}"
              f"\nReward: {reward}\n")
        f.write('\n------------------------------------------')
        f.write(f"\nTimestep: {k}"
                f"\nScore: {score}"
                f"\nReward: {reward}"
                f"\nAction Taken:")
        if deletecalled:
            f.write(" Dispose non-recyclable from middle\n\n")
        else:
            f.write(" none\n\n")

print(f"Score: {score}\nTotal Rejects: {totalRejects}"
      f"\nTimes Objects Were Created: {j}"
      f"\nTimestep total: {k}"
      f"\nTimes Policy Called: {m}"
      f"\nReward: {reward}")
