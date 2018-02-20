import maya.cmds as cmds

# Load plugin and create node
cmds.loadPlugin('D:/Tak/Program_Presets/tak_maya_preset/plug-ins/rampBlendShape.py')
cmds.createNode('rampBlendShape')
cmds.connectAttr('baseGeoShape.worldMesh', 'rampBlendShape1.baseGeo', f=True)
cmds.connectAttr('targetGeoShape.worldMesh', 'rampBlendShape1.targetGeo', f=True)
cmds.connectAttr('rampBlendShape1.outGeo', 'outGeoShape.inMesh', f=True)

# Delete nodes and unload plugin
rampBlendShapeNodes = cmds.ls(type='rampBlendShape')
if rampBlendShapeNodes:
    cmds.delete(rampBlendShapeNodes)
cmds.flushUndo()
cmds.unloadPlugin('rampBlendShape')



import tak_shapeDivider
reload(tak_shapeDivider)
shapeDivider = tak_shapeDivider.ShapeDivider(baseGeo='face', targetGeo='eyebrows_up')
shapeDivider.build()
