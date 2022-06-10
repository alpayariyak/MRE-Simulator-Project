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
aluminumCan_visibility =  [2, 3, 3, 2, 3, 3, 3, 2, 3, 3]
cardboard = [f'cardboard/cardboard{i}.png' for i in range(10)]
cardboard_visibility = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
carton = [f'carton/carton{i}.png' for i in range(10)]
carton_visibility = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
glassBottle = [f'glassBottle/glassBottle{i}.png' for i in range(9)]
glassBottle_visibility = [3, 3, 2, 3, 3, 3, 2, 2, 3]
paper = [f'paper/paper{i}.png' for i in range(21)]
paper_visibility = [3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
paperBag = [f'paperBag/paperBag{i}.png' for i in range(15)]
paperBag_visibility = [3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3]
plasticBag = [f'plasticBag/plasticBag{i}.png' for i in range(23)]
plasticBag_visibility = [3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3]
# plasticBottle = [f'plasticBottle/plasticBottle{i}.png' for i in range(12)]
reject = [f'reject/reject{i}.png' for i in range(20)]
reject_visibility = [1, 2, 3, 3, 3, 1, 2, 3, 3, 1, 2, 1, 3, 1, 2, 3, 2, 2, 1, 2]

trash_classes = aluminumCan \
                + cardboard \
                + carton \
                + glassBottle \
                + paper \
                + paperBag \
                + plasticBag \
                + reject
trash_visibility = aluminumCan_visibility + cardboard_visibility+carton_visibility+glassBottle_visibility+paper_visibility+paperBag_visibility+plasticBag_visibility+reject_visibility

class Simulator_Object:

    def __init__(self, obj, x, y, speedx=0, speedy=0, rot=0, width=100, height=100):
        global s_to_ms, timestep
        self.obj_class = obj.split('/')[0]
        self.object = obj
        self.visibility = trash_visibility[trash_classes.index(obj)]
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


<<<<<<< Updated upstream
j = 0
k = 0
m = 0
reward = 100

f = open('rollout.txt', 'w')
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
=======
def policy(policy_n):
    j = 0
    k = 0
    m = 0
    total_reward = 100
    reward = 0
    score = 100
    fatigue = 0
    timeout = 0
    i = 0
    state = {'trash':trash_objects, 'score':score, 'total_reward':total_reward, 'fatigue':fatigue, 'timeout':timeout, 'reward_t':reward, 'timestep':i}
    # f = open('MRE-Simulator-Project/rollout.txt', 'w')
    for i in range(180000):  # 180000 ms in 3 minutes
        state['timestep'] = i
        if i % create_interval == 0:
            makeRandomTrash(1)
            makeRandomTrash(2)
            makeRandomTrash(3)
            j += 1

        if i % (timestep * s_to_ms) == 0:
            reward = 0
            k += 1
            deletecalled = False
            for trash_obj_id, trash_obj in trash_objects.items():

                if trash_obj.x > cnvwidth:

                    if trash_obj.obj_class == 'reject' and not trash_obj.deleted:
                        reward -= 1
                        score -= 1
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
print(f"Score: {score}\nTotal Rejects: {totalRejects}"
      f"\nTimes Objects Were Created: {j}"
      f"\nTimestep total: {k}"
      f"\nTimes Policy Called: {m}"
      f"\nReward: {reward}")
=======
                    else:
                        if 300 > trash_obj.hitbox['y'] > 200:
                            trash_obj.setSpeed(belt1.belt_speed)
                        elif 500 > trash_obj.hitbox['y'] > 400:
                            trash_obj.setSpeed(belt2.belt_speed)
                        elif 700 > trash_obj.hitbox['y'] > 600:
                            trash_obj.setSpeed(belt3.belt_speed)
                        else:
                            trash_obj.setSpeed(0)
                        # print(f"TrashID: {trash_obj_id}  State: {trash_obj.get_state()}")
                        # f.write(f"\nTrashID: {trash_obj_id}  State: {trash_obj.get_state()}")
                        trash_obj.update_position()
            total_reward += reward

            # print(f"Score: {score}\nTotal Rejects: {totalRejects}"
            #       f"\nTimestep: {k}"
            #       f"\nReward: {reward}\n")
            # f.write('\n------------------------------------------')
            # f.write(f"\nTimestep: {k}"
            #         f"\nScore: {score}"
            #         f"\nReward: {reward:.1f}"
            #         f"\nAction Taken:")
            # if deletecalled:
            #     f.write(" Dispose non-recyclable from middle\n\n")
            # else:
            #     f.write(" none\n\n")

    # print(f"Score: {score}\nTotal Rejects: {totalRejects}"
    #       f"\nTimes Objects Were Created: {j}"
    #       f"\nTimestep total: {k}"
    #       f"\nTimes Policy Called: {m}"
    #       f"\nTotal Reward: {total_reward:.1f}")
    # f.write(f"\n\n-----Final Stats-----\nScore: {score}\nTotal Rejects: {totalRejects}"
    #         f"\nTimes Objects Were Created: {j}"
    #         f"\nTimestep total: {k}"
    #         f"\nTimes Policy Called: {m}"
    #         f"\nTotal Reward: {total_reward:.1f}")

    return score, total_reward, fatigue, ybelt_fatigue_tout




def average_policy(policy_n, n):
    avg_score = 0
    avg_reward = 0
    avg_fatigue = 0
    for i in range(n):
        if policy_n == 1:
            curr_score, curr_reward, curr_fatigue, ybelt_fatigue_tout = policy(1)
        elif policy_n == 2:
            curr_score, curr_reward, curr_fatigue, ybelt_fatigue_tout = policy(2)
        elif policy_n == 3:
            curr_score, curr_reward, curr_fatigue, ybelt_fatigue_tout = policy(3)
        elif policy_n == 0:
            curr_score, curr_reward, curr_fatigue, ybelt_fatigue_tout = policy(0)
        avg_score += curr_score
        avg_reward += curr_reward
        avg_fatigue += curr_fatigue
        print(policy_n, f"{int((i/n)* 100)}%")
    return avg_score/n, avg_reward/n, avg_fatigue/n, ybelt_fatigue_tout

policies = {0:'Do nothing', 1:'Drag Non-Recyclable from the middle', 2:"Drag Recyclable from the middle", 3:"Drag all items from middle"}
avgtext = open("averages.txt", 'w')
for a_policy, description in policies.items():
    n_score, n_reward, n_fatigue, ybelt_fatigue_tout = average_policy(a_policy, 2)
    avgtext.write(f"\nPolicy: {policies[a_policy]}"
                  f"\nAverage Score: {n_score}"
                  f"\nFatigue: {n_fatigue}\n")
                  # f"\nAverage Reward: {n_reward}\n")
avgtext.write(f"\nBelt      Fatigue     Timeout(ms)\n")
p = 1
for belt, fatigue_timeout in ybelt_fatigue_tout.items():
    avgtext.write(f"{p}         {fatigue_timeout[0]}         {fatigue_timeout[1]}\n")
    p += 1
>>>>>>> Stashed changes
