import maya.cmds as cmds
import json

path = 'C:/Users/Sperasoft Home/Desktop/rigPoses'


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


def save_animation(rig_name="rig_group"):
    
    json_data = {}

    start_frame = cmds.playbackOptions(q=1, minTime=1)
    end_frame = cmds.playbackOptions(q=1, maxTime=1)

    control_curves = get_all_controls(rig_name)

    # print (control_curves)

    for crv in control_curves:

        key_channels = cmds.listAttr(crv, keyable=True)

        dict_channels = {}

        for ch in key_channels:

            allFrames = cmds.keyframe(crv, query=1, attribute=ch, time=(start_frame, end_frame), timeChange=1)
            allValues = cmds.keyframe(crv, query=1, attribute=ch, time=(start_frame, end_frame), valueChange=1)

            if allFrames:

                dict_channels[ch] = []

                for i in range(len(allFrames)):  # [0,1,2,3...]

                    inWeight = cmds.keyTangent(crv, q=1, t=(allFrames[i], allFrames[i]), attribute=ch, inWeight=1)[0]
                    outWeight = cmds.keyTangent(crv, q=1, t=(allFrames[i], allFrames[i]), attribute=ch, outWeight=1)[0]
                    inAngle = cmds.keyTangent(crv, q=1, t=(allFrames[i], allFrames[i]), attribute=ch, inAngle=1)[0]
                    outAngle = cmds.keyTangent(crv, q=1, t=(allFrames[i], allFrames[i]), attribute=ch, outAngle=1)[0]

                    temp_list = [allFrames[i], allValues[i], inWeight, outWeight, inAngle, outAngle]

                    dict_channels[ch].append(temp_list)

        json_data[crv] = dict_channels
        
    # print (json_data)

    json_file_path = "C:/Users/Sperasoft Home/Desktop/rigPoses/animation.json"

    with open(json_file_path, 'w') as outfile:

        json.dump(json_data, outfile, indent=4)


save_animation()