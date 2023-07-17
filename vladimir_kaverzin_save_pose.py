import maya.cmds as cmds
import json

PATH = 'C:/Users/Sperasoft Home/Desktop/rigPoses'

def get_all_controls(rig_name):
    
    """

    Get all control curves from a current rig
    :param rig: rig name
    :return: list of control curves

    """

    children = cmds.listRelatives(rig_name="rig_group", children=True, fullPath=True, allDescendents=True)

    result = []

    for i in children:

        if cmds.nodeType(i) == "nurbsCurve":
            transform = cmds.listRelatives(i, parent=True, fullPath=True)[0]

            result.append(transform)

    return result

    
def save_pose_to_file(path_to_file = None):
    
    curves = get_all_controls()
    
    data = {}
    
    # ---
    
    for crv in curves:
        
        nodeAttrs = cmds.listAttr(crv, k=True)
        
        attrDict = {}
        
        if nodeAttrs:
            
            for at in nodeAttrs:
                
                if 'translate' in at or 'rotate' in at or 'scale' in at:
                    
                    value = cmds.getAttr(crv + '.' + at)
                    
                    attrDict[at] = value

            data[crv] = attrDict   
    # ---    
    
    if data:
        with open(path_to_file, 'w') as f:
            json.dump(data, f, indent = 4)

def main():
    
    path_to_save = cmds.fileDialog2(fileFilter = '*.json', dialogStyle = 2, caption = 'Save Rig Pose', startingDirectory = path)[0]
    
    save_pose_to_file(path_to_file = path_to_save)
    

main()

    

    
        