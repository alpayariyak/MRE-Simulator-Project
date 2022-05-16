import math

# page height, easier to reference js code
cnvheight = 1230  # or 800
cnvwidth = 3024

#
totalObjects = -11
totalRejects = 0
detectedRejects = 0
detectedFp = 0
#
trash_classes = ['aluminumCan',
                 'cardboard',
                 'carton',
                 'glassBottle',
                 'paper',
                 'paperBag',
                 'plasticBag',
                 'reject']


# might not need these

class Simulator_Object:
    def __init__(self, obj_class, x, y, speedx=0, speedy=0, rot=0, width=100, height=100):
        self.obj_class = obj_class
        self.rot = (rot * math.pi) / 180
        self.height = height
        self.width = width
        self.speedx = speedx
        self.speedy = speedy
        self.x = x
        self.y = y
        self.state = [x, y, width, height, speedx, speedy, rot]


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

#belts

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

