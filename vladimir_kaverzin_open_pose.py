import maya.cmds as cmds
import json

PATH = 'C:/Users/Sperasoft Home/Desktop/rigPoses'

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

def load_pose(rig_name, filePath=None):

    json_data = None
    
    with open(filePath, 'r') as inFile:
        
        json_data = json.load(inFile)

    control_curves = get_all_controls(rig_name)

    for ctrl, ch in json_data.items():

        for channelName, channelValue in ch.items():
            
            cmds.setKeyframe(ctrl, at=channelName, v=channelValue) 


json_file_path = 'C:/Users/Sperasoft Home/Desktop/rigPoses/pose3.json'

load_pose('rig_group', filePath=json_file_path)
            
#WHY DOESN'T WORK?!?!?!?!?!

#def main():
    
    #json_file_path = cmds.fileDialog2(fileFilter='*.json', dialogStyle=2, fileMode=1, caption='Open Rig Pose', okCaption='Load', startingDirectory=PATH) [0]

    #load_pose(pathToFile = json_file_path)

#main()