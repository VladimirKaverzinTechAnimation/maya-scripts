import maya.cmds as cmds
import math

pi = 3.14159265359
class Rocket(object):

    def __init__(self, body_parts=0, nose_height=0, fuel_tanks=0, rocket_radius=0, body_height=0, fuel_tanks_height=0, fuel_tanks_radius=0):

        self.body_parts = body_parts
        self.nose_height = nose_height
        self.fuel_tanks = fuel_tanks
        self.rocket_radius = rocket_radius
        self.body_height = body_height
        self.fuel_tanks_height = fuel_tanks_height
        self.fuel_tanks_radius = fuel_tanks_radius

        self.calculate()

    def calculate(self):"

        # [{"origin_y":0, "radius":2, "height":4}, {}, ... {}]

        self.rocket_parts = []

        global_height = 0

        for i in range(self.body_parts + 1):

            part = {}

            part_origin_y = i * self.body_height + self.fuel_tanks_height + self.body_height/2

            part["type"] = "cylinder"
            part["OrigY"] = part_origin_y
            part["radius"] = self.rocket_radius
            part["height"] = self.body_height

            self.rocket_parts.append(part)

        self.rocket_parts[-1]["height"] = self.nose_height
        self.rocket_parts[-1]["type"] = "cone"
        self.rocket_parts[-1]["OrigY"] = self.rocket_parts[-1]["OrigY"] + self.nose_height/2.0 - self.body_height/2.0

    def create_model(self):

        for i in self.rocket_parts:

            obj = None

            if i ["type"] == "cylinder":
                obj = cmds.polyCylinder(radius=i["radius"], height=i["height"])[0]

            elif i ["type"] == "cone":
                obj = cmds.polyCone(radius=i["radius"], height=i["height"])[0]

            cmds.xform(obj, t = [0, i["OrigY"], 0])

        for i in range(self.fuel_tanks):

            deg = (360 / self.fuel_tanks) * i
            rad = deg * (pi / 180.0)

            x = math.sin(rad) * self.rocket_radius
            z = math.cos(rad) * self.rocket_radius

            con = cmds.polyCone(radius = self.fuel_tanks_radius, height = self.fuel_tanks_height)[0]

            cmds.xform(con, t = [x,self.fuel_tanks_height/2,z])

    def set_nose_height(self, nose_height=0):

        self.rocket_parts[-1]["height"] = nose_height
        self.rocket_parts[-1]["OrigY"] = self.rocket_parts[-1]["OrigY"] - nose_height

class Rocket_New(Rocket):
    def __init__(self, body_parts=0,
                       nose_height=0,
                       rocket_radius=0,
                       body_height=0,
                       fuel_tanks_height=0,
                       fuel_tanks=0,
                       fuel_tanks_radius=0,
                       escape_height=0):

        super(Rocket_New, self).__init__(body_parts=body_parts,
                                         nose_height=nose_height,
                                         rocket_radius=rocket_radius,
                                         body_height=body_height,
                                         fuel_tanks_height=fuel_tanks_height,
                                         fuel_tanks=fuel_tanks,
                                         fuel_tanks_radius=fuel_tanks_radius)

        escape_system_Y_origin = self.rocket_parts[-1]["OrigY"] + self.nose_height / 2.0 + escape_height / 2.0

        escape_obj = cmds.polyCylinder(radius=0.2, height=escape_height)[0]

        cmds.xform(escape_obj, t=[0, escape_system_Y_origin, 0])

        wings = 4

        for i in range(wings):

            deg = 360 / wings * i
            cube_obj = cmds.polyCube(w=0.2, d=1, h=self.body_height/2.0)[0]

            cmds.setAttr(cube_obj + ".rotateY", deg)

            offset_Z = self.rocket_radius + 0.5
            offset_Y = self.rocket_parts[0]["OrigY"]

            cmds.xform (cube_obj, t = [0, offset_Y, offset_Z], os = 1)


def main():

    #space_rocket = Rocket(body_parts=4, nose_height=10, rocket_radius=2, body_height=6, fuel_tanks_height=2, fuel_tanks=5, fuel_tanks_radius=1)
    #space_rocket.create_model()

    space_rocket = Rocket_New(body_parts=4, nose_height=2, rocket_radius=2, body_height=3, fuel_tanks_height=5, fuel_tanks=5, fuel_tanks_radius=1, escape_height = 1)
    space_rocket.create_model()

main()