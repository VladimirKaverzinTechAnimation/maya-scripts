import maya.cmds as cmds
import json


def get_all_controls(rig_name):
    
    """

    Get all control curves from a current rig
    :param rig: rig name
    :return: list of control curves

    """

    children = cmds.listRelatives(rig_name, children=True, fullPath=True, allDescendents=True)

    result = []

    for i in children:

        if cmds.nodeType(i) == "nurbsCurve":
            transform = cmds.listRelatives(i, parent=True, fullPath=True)[0]

            result.append(transform)

    return result


def load_animation(rig_name="rig_group", filePath=None):
    
    json_data = None

    with open(filePath, 'r') as infile:

        json_data = json.load(infile)

    # print (json_data)

    controls = get_all_controls(rig_name)

    for crv, crv_value in json_data.items():

        for ch, ch_values in crv_value.items():

            for k_value in ch_values:
                
                F = k_value[0]
                V = k_value[1]
                inW = k_value[2]
                inA = k_value[3]
                outW = k_value[4]
                outA = k_value[5]

                cmds.setKeyframe(crv, attribute=ch, t=(F, F), v=V)
                cmds.keyTangent(crv, edit=1, t=(F, F), attribute=ch, inWeight=inW)
                cmds.keyTangent(crv, edit=1, t=(F, F), attribute=ch, inAngle=inA)                
                cmds.keyTangent(crv, edit=1, t=(F, F), attribute=ch, outWeight=outW)
                cmds.keyTangent(crv, edit=1, t=(F, F), attribute=ch, outAngle=outA)


path = "C:/Users/Sperasoft Home/Desktop/rigPoses/animation.json"
load_animation(filePath=path)