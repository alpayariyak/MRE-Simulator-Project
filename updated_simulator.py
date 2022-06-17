import math
import random
import copy

#
game_length = 180
s_to_ms = 1000
timestep = 0.1
create_interval = 0.5 * s_to_ms  # 5 seconds
fatigue_constant = 0.0000018
timeout_constant = 0.4
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
aluminumCan_visibility = [2, 3, 3, 2, 3, 3, 3, 2, 3, 3]
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
trash_visibility = aluminumCan_visibility + cardboard_visibility + carton_visibility + glassBottle_visibility + paper_visibility + paperBag_visibility + plasticBag_visibility + reject_visibility


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
        self.visibility = trash_visibility[trash_classes.index(obj)]

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


score = 100


def probability(prob):
    return random.random() < prob


ybelt_fatigue_timeout = {650: [0.001, 300], 450: [0.003, 600], 250: [0.005, 1000]}


def reward_function(state, action):
    reward = 0
    for trash_id, trash_obj in state['trash_objects'].items():
        if trash_obj.x > cnvwidth and trash_obj.obj_class == 'reject' and not trash_obj.deleted:
            reward += -1
        elif trash_obj in trash_bin and trash_obj.obj_class != 'reject':
            reward += -1
    if action and action.obj_class != 'reject':
        reward += -1
    return reward


speed_probability = {belt2.belt_speed: 0.96, belt1.belt_speed: 0.92, belt3.belt_speed: 0.85}
visibility_probability = {1: 0.85, 2: 0.9, 3: 0.98}


def get_dist_from_trash(x, y):
    return math.sqrt((y - 90) ** 2 + (cnvwidth / 2 - x) ** 2)


def timeout_function(action):
    dist = get_dist_from_trash(action.x, action.y)
    t = 0
    if action.speedx == belt1.belt_speed:  # belt 1
        t = 0.26 * dist + 533.24
    if action.speedx == belt2.belt_speed:  # belt 2
        t = 0.15 * dist + 752.35
    if action.speedx == belt3.belt_speed:  # belt 3
        t = 0.08 * dist + 1140.88
    return int(math.ceil((t/s_to_ms)/timestep))


def transition(state, action=False):
    new_state = state

    if new_state['timestep'] % create_interval == 0:
        makeRandomTrash(1)
        makeRandomTrash(2)
        makeRandomTrash(3)

    if new_state['timestep'] % (timestep * s_to_ms) == 0:

        if action:
            new_state['fatigue'] += action.y * fatigue_constant
            new_state['timeout'] += timeout_function(action)
            if probability(1 - state['fatigue']) and probability(speed_probability[action.speedx]) and probability(
                    visibility_probability[action.visibility]):
                action.dragToTrash()
                action.deleted = True

        for trash_obj_id, trash_obj in new_state['trash_objects'].items():
            if trash_obj.x > cnvwidth:

                if trash_obj.obj_class == 'reject' and not trash_obj.deleted:
                    new_state['score'] -= 1
                trash_obj.deleted = True

            if trash_obj in trash_bin and trash_obj.obj_class != 'reject':
                new_state['score'] -= 1
                trash_obj.deleted = True

            if not trash_obj.deleted:
                if 300 > trash_obj.hitbox['y'] > 200:
                    trash_obj.setSpeed(belt1.belt_speed)
                elif 500 > trash_obj.hitbox['y'] > 400:
                    trash_obj.setSpeed(belt2.belt_speed)
                elif 700 > trash_obj.hitbox['y'] > 600:
                    trash_obj.setSpeed(belt3.belt_speed)
                else:
                    trash_obj.setSpeed(0)

                trash_obj.update_position()

        new_state['trash_objects'] = trash_objects
    return new_state


def policy(state, policy_n=0):
    action = False
    deletecalled = False
    ybelts = [650, 450, 250]
    for trash_obj_id, trash_obj in state['trash_objects'].items():
        if policy_n == 0:
            action = False
        elif policy_n == 1:
            for ybelt in ybelts:
                if trash_obj.checkCoordinateIntersection(cnvwidth / 2,
                                                         ybelt) and trash_obj.obj_class == 'reject' and not deletecalled:
                    action = trash_obj
        elif policy_n == 2:
            for ybelt in ybelts:
                if trash_obj.checkCoordinateIntersection(cnvwidth / 2,
                                                         ybelt) and trash_obj.obj_class != 'reject' and not deletecalled:
                    action = trash_obj
        elif policy_n == 3:
            for ybelt in ybelts:
                if trash_obj.checkCoordinateIntersection(cnvwidth / 2, ybelt) and not deletecalled:
                    action = trash_obj
        elif policy_n == 4:
            if trash_obj.checkCoordinateIntersection(cnvwidth / 2,
                                                     650) and trash_obj.obj_class == 'reject' and not deletecalled:
                action = trash_obj
    return action


if __name__ == '__main__':
    total_reward = 100
    reward = 0
    score = 100
    fatigue = 0
    timeout = 0
    i = 0
    state = {'trash_objects': trash_objects, 'score': score, 'fatigue': fatigue,
             'timeout': timeout, 'timestep': i}
    new_state = state

    for i in range(180000):  # 180000 ms in 3 minutes
        
        state['timestep'] = i
        timestep_bool = new_state['timestep'] % (timestep * s_to_ms) == 0
        old_state = state
        state = new_state

        if state['timeout'] > 0:
            state['timeout'] -= 1
            action_t = False
        else:
            action_t = policy(state, 1)

        new_state = transition(state, action_t)

        if timestep_bool:
            reward = reward_function(new_state, action_t)
            total_reward += reward
            for trash_id, trash_obj in copy.copy(state['trash_objects']).items():
                if trash_obj.deleted:
                    del new_state['trash_objects'][trash_id]

<<<<<<< Updated upstream
    print(new_state['fatigue'], new_state['score'], total_reward)
    print(new_state)
=======
    return A, X, total_reward, timeouts


def sigmoid_function(x):
    return 1 / (1 + np.exp(-x))



def baseline(X_T, total_reward_T, theta):
    b = np.zeros((len(theta),))
    for k in range(theta.shape[0]):
        theta_k = theta[k]
        numerator_sum = 0
        denomenator_sum = 0
        i = 1

        for X in X_T:
            sum_grad_thetak_log_policy_k_run = 0
            for x_t in X:
                x_k_t = x_t[k]
                sum_grad_thetak_log_policy_k_run += (1 - sigmoid_function(theta.T.dot(x_t))) * x_k_t
                #print(f"{k}         {i}         {(1 - sigmoid_function(theta.T.dot(x_t))) * x_k_t}")
            numerator_sum += np.square(sum_grad_thetak_log_policy_k_run) * total_reward_T[i-1]
            denomenator_sum += np.square(sum_grad_thetak_log_policy_k_run)
            i += 1
        b[k] = (numerator_sum/i) / (denomenator_sum/i)

    return b


def grad_theta(X_T, total_reward_T, theta, b):
    gradient = np.zeros((len(theta),))
    for k in range(theta.shape[0]):
        theta_k = theta[k]
        grad_sum = 0
        i = 1
        for X in X_T:
            sum_grad_thetak_log_policy_k_run = 0
            for x_t in X:
                x_k_t = x_t[k]
                sum_grad_thetak_log_policy_k_run += (1 - sigmoid_function(theta.T.dot(x_t))) * x_k_t

            grad_sum += np.square(sum_grad_thetak_log_policy_k_run) * total_reward_T[i - 1]

        gradient[k] = (sum_grad_thetak_log_policy_k_run * (total_reward_T[i - 1] - b[k])) / len(X_T)
    return gradient


def train(epochs, minibatches, epsilon):
    theta = np.random.randn(3, )
    print(score_difference_in_reward(theta, 3))
    for epoch in range(epochs):

        A_T, X_T, total_reward_T, timeouts_T = [], [], [], []

        for minibatch in range(1, minibatches + 1):
            total_reward = 100
            A, X, total_reward, timeouts = simulator(theta)
            A_T.append(A), X_T.append(X), total_reward_T.append(total_reward), timeouts_T.append(timeouts)

        b = baseline(X_T, total_reward_T, theta)
        gradient = grad_theta(X_T, total_reward_T, theta, b)
        theta += epsilon * gradient
        print(score_difference_in_reward(theta, 3), theta)
    return theta


def score_difference_in_reward(theta, folds, pol=4):
    metrics = []
    for fold in range(folds):
        metrics.append(metric_function(theta, folds))
    return np.average(metrics)


def metric_function(theta, folds, pol=4):
    metric = 0
    A_train, X_train, total_reward_train, timeouts = simulator(theta, 1)
    for t in range(len(A_train)):
        if X_train[t][0] == 1 and A_train[t] == 1:
            metric -= 1
        elif X_train[t][1] == 1 and A_train[t] == 0 and not timeouts[t]:
            metric -= 1
        elif X_train[t][1] == 0 and  X_train[t][0] == 0 and A_train[t] == 1 and not timeouts[t]:
            metric -= 1
    return metric


if __name__ == '__main__':
    train(4, 10, 0.6)
    X_T = [ [[0,0,1], [0,1,1], [1,0,1], [1,1,1]],
            [[0,0,1], [0,0,1], [1,0,1], [1,0,1]],
            [[1,0,1], [0,0,1], [0,0,1], [0,0,1]]]

    A_T = [ [0, 1, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 0, 1] ]

    arewardlist = [-2, -1, 4]
    atheta = np.random.randn(3, )

    #print(f"k         run            grad_theta_k log pi(u_k | x_k)")
    b = baseline(X_T, arewardlist, atheta)
    print(grad_theta(X_T, arewardlist, atheta, b))
>>>>>>> Stashed changes
