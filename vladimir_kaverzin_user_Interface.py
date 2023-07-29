import maya.cmds as cmds


def create_object():
    object_name = cmds.textField("myWindow_textField", q=1, text=True)

    object_sphere = cmds.radioButton("myWindow_textField_radio_button_sphere", q=1, select=True)
    object_cube = cmds.radioButton("myWindow_textField_radio_button_cube", q=1, select=True)

    option_group = cmds.checkBox("myWindow_textField_check_box_group", q=1, value=True)
    option_move = cmds.checkBox("myWindow_textField_check_box_move", q=1, value=True)
    option_layer = cmds.checkBox("myWindow_textField_check_box_layer", q=1, value=True)

    poly_object = None

    if not object_name:
        object_name = "generated_object"

    if object_sphere:
        poly_object = cmds.polySphere(n=object_name + "_Sphere")[0]
    elif object_cube:
        poly_object = cmds.polyCube(n=object_name + "_Cube")[0]
    else:
        poly_object = cmds.polyCone(n=object_name + "_Cone")[0]

    if option_group:
        group = cmds.group(n=poly_object + "_group", em=True)
        cmds.parent(poly_object, group)
        poly_object = "|{}|{}".format(group, poly_object)

    if option_move:
        cmds.xform(poly_object, t=[10, 0, 0])

    if option_layer:
        display_layer = cmds.createDisplayLayer(noRecurse=True, name=object_name + '_Template_Layer')
        cmds.setAttr(display_layer + '.displayType', 1)
        cmds.editDisplayLayerMembers(display_layer, poly_object)


def main():
    if cmds.window("MyWindow", exists=True):
        cmds.deleteUI("MyWindow")

    if cmds.windowPref("MyWindow", exists=True):
        cmds.windowPref("MyWindow", remove=True)

    cmds.window("MyWindow", title="Object Generator", width=250, tlb=True)

    main_Layout = cmds.columnLayout(adjustableColumn=1, columnAttach=('both', 5), rowSpacing=10)

    cmds.textField("myWindow_textField", placeholderText="Object Name", parent=main_Layout,
                   backgroundColor=(0.5, 0.5, 0.48))

    # object_layout = cmds.rowLayout(numberOfColumns = 3, parent = main_Layout, columnWidth3=[82, 82, 82], columnAttach3=["both", "both", "both"], columnAlign=[1, "center"])
    object_layout = cmds.formLayout(numberOfDivisions=100)
    cmds.radioCollection(parent=object_layout)

    radio_button_sphere = cmds.radioButton("myWindow_textField_radio_button_sphere", label='Sphere', select=True)
    radio_button_cube = cmds.radioButton("myWindow_textField_radio_button_cube", label='Cube')
    radio_button_cone = cmds.radioButton("myWindow_textField_radio_button_cone", label='Cone')

    cmds.formLayout(object_layout, e=1, attachForm=[(radio_button_sphere, 'left', 5)])
    cmds.formLayout(object_layout, e=1, attachForm=[(radio_button_cone, 'right', 5)])
    cmds.formLayout(object_layout, e=1, attachForm=[(radio_button_cube, 'top', 0)])

    cmds.formLayout(object_layout, e=1, attachPosition=[(radio_button_sphere, 'right', 0, 33)])
    cmds.formLayout(object_layout, e=1, attachPosition=[(radio_button_cone, 'left', 0, 66)])

    cmds.formLayout(object_layout, e=1, attachControl=[(radio_button_cube, 'left', 2, radio_button_sphere),
                                                       (radio_button_cube, 'right', 2, radio_button_cone)])

    cmds.columnLayout(adjustableColumn=True, columnAlign="left", columnAttach=('both', 5), rowSpacing=10,
                      parent=main_Layout, columnOffset=["both", 10])

    cmds.checkBox("myWindow_textField_check_box_group", label="Put into a group")
    cmds.checkBox("myWindow_textField_check_box_move", label="Move x by 10 units")
    cmds.checkBox("myWindow_textField_check_box_layer", label="Display Layer / Template")

    button_layout = cmds.formLayout(numberOfDivisions=100)

    create_button = cmds.button(label="Create", width=125, command="create_object()", parent=button_layout)
    cancel_button = cmds.button(label="Cancel", width=125, command="cmds.deleteUI('MyWindow')", parent=button_layout)

    cmds.formLayout(button_layout, e=1, attachForm=[(create_button, 'left', 0)])
    cmds.formLayout(button_layout, e=1, attachForm=[(cancel_button, 'right', 0)])

    cmds.formLayout(button_layout, e=1, attachPosition=[(create_button, 'right', 0, 49)])
    cmds.formLayout(button_layout, e=1, attachPosition=[(cancel_button, 'left', 0, 51)])

    cmds.showWindow("MyWindow")

main()