





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

def probability(prob):
    return random.random() < prob


class Mouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speedx = x
        self.speedy = y


def policy(policy_n):
    j = 0
    k = 0
    m = 0
    totalReward = 100
    reward = 0
    score = 100
    fatigue = 0
    timeout = 0
    # f = open('MRE-Simulator-Project/rollout.txt', 'w')
    for i in range(180000):  # 180000 ms in 3 minutes

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
                    trash_obj.deleted = True

                if not trash_obj.deleted:

                    if timeout > 0:
                        timeout -= 1
                    else:
                        ybelt_fatigue_tout = {650:[0.001, 300], 450:[0.003, 600], 250:[0.005, 1000]  }
                        if policy_n == 0:
                            pass
                        elif policy_n == 1:
                            for ybelt, fatigue_tout in ybelt_fatigue_tout.items():
                                if trash_obj.checkCoordinateIntersection(cnvwidth / 2, ybelt) and trash_obj.obj_class == 'reject' and not deletecalled:
                                    if probability(1-fatigue):
                                        trash_obj.dragToTrash()
                                        deletecalled = True
                                    fatigue += fatigue_tout[0]
                                    timeout += fatigue_tout[1]
                                    m += 1
                        elif policy_n == 2:
                            for ybelt, fatigue_tout in ybelt_fatigue_tout.items():
                                if trash_obj.checkCoordinateIntersection(cnvwidth / 2, ybelt) and trash_obj.obj_class != 'reject' and not deletecalled:
                                    if probability(1 - fatigue):
                                        trash_obj.dragToTrash()
                                        deletecalled = True
                                    fatigue += fatigue_tout[0]
                                    timeout += fatigue_tout[1]
                                    m += 1
                        elif policy_n == 3:
                            for ybelt, fatigue_tout in ybelt_fatigue_tout.items():
                                if trash_obj.checkCoordinateIntersection(cnvwidth / 2, ybelt) and not deletecalled:
                                    if probability(1 - fatigue):
                                        trash_obj.dragToTrash()
                                        deletecalled = True
                                    fatigue += fatigue_tout[0]
                                    timeout += fatigue_tout[1]
                                    m += 1



                    if trash_obj in trash_bin and trash_obj.obj_class != 'reject':
                        score -= 1
                        reward -= 1
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
                        # print(f"TrashID: {trash_obj_id}  State: {trash_obj.get_state()}")
                        # f.write(f"\nTrashID: {trash_obj_id}  State: {trash_obj.get_state()}")
                        trash_obj.update_position()
            totalReward += reward

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
    #       f"\nTotal Reward: {totalReward:.1f}")
    # f.write(f"\n\n-----Final Stats-----\nScore: {score}\nTotal Rejects: {totalRejects}"
    #         f"\nTimes Objects Were Created: {j}"
    #         f"\nTimestep total: {k}"
    #         f"\nTimes Policy Called: {m}"
    #         f"\nTotal Reward: {totalReward:.1f}")

    return score, totalReward, fatigue, ybelt_fatigue_tout




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