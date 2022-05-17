import math

# page height, easier to reference js code
import random

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

    def __init__(self, object, x, y, speedx=0, speedy=0, rot=0, width=100, height=100):
        self.obj_class = object.split('/')[0]
        self.object = object
        self.rot = (rot * math.pi) / 180
        self.height = height
        self.width = width
        self.speedx = speedx
        self.speedy = speedy
        self.x = x
        self.y = y


        global totalObjects
        global totalRejects
        totalObjects += 1
    def get_state(self):
        return [self.x, self.y, self.speedx, self.speedy]

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

belt1 = Simulator_Object('ConvBeltNew',
                         -50,  # x
                         185,  # y
                         width=cnvwidth + 150,  # width
                         height=160)  # height

belt2 = Simulator_Object('ConvBeltNew',
                         -50,  # x
                         385,  # y
                         width=cnvwidth + 150,  # width
                         height=160)  # height

belt3 = Simulator_Object('ConvBeltNew',
                         -50,  # x
                         585,  # y
                         width=cnvwidth + 150,  # width
                         height=160)  # height

trash_bin = Simulator_Object('trashbin',
                             cnvwidth / 2 - 75,
                             15,
                             width=150,
                             height=150)

belts = [belt1, belt2, belt3]
endboxes = [end1, end2, end3]

trash_objects = {} #id:object


class Trash_Object(Simulator_Object):
    def __init__(self, object, x, y, speedx=0, speedy=0, rot=0, width=100, height=100):
        global trash_id
        trash_id = trash_id+1
        super().__init__(object, x, y, speedx, speedy, rot, width, height)


        global totalRejects
        if self.obj_class == 'reject':
            totalRejects += 1
    def update_position(self):
        self.x = self.x + self.speedx
        self.y = self.y + self.speedy

    def set_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y


print(len(trash_classes))


def makeRandomTrash(beltNumber):
    if beltNumber == 1:
        globals()[f'trash_object_{trash_id}'] = Trash_Object(
            random.choice(trash_classes),
            -100 - random.randint(0, 150),
            200,
            speedx=3,
            speedy=0,
            rot=random.randint(-90, 90)
        )
        trash_objects[trash_id] = globals()[f'trash_object_{trash_id}']
    elif beltNumber == 2:
        globals()[f'trash_object_{trash_id}'] = Trash_Object(
            random.choice(trash_classes),
            -100 - random.randint(0, 150),
            400,
            speedx=2,
            speedy=0,
            rot=random.randint(-90, 90)
        )
    else:
        globals()[f'trash_object_{trash_id}'] = Trash_Object(
            random.choice(trash_classes),
            -100 - random.randint(0, 150),
            600,
            speedx=4,
            speedy=0,
            rot=random.randint(-90, 90)
        )

makeRandomTrash(1)
makeRandomTrash(1)
makeRandomTrash(1)
makeRandomTrash(1)
makeRandomTrash(1)
makeRandomTrash(1)

print(trash_objects[1].get_state())
for i in range(300):
    trash_objects[1].update_position()
print(trash_objects[1].get_state())

print(len(trash_objects))