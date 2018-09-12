import maya.cmds as cmds
import pymel.core as pm
import tak_lib


def tmpFunc():
    # set nHair clumpScale
    hairSystemList = cmds.ls(sl = True)
    for hairSystem in hairSystemList:
        cmds.setAttr('%s.clumpWidthScale[1].clumpWidthScale_Position' %hairSystem, 1)
        cmds.setAttr('%s.clumpWidthScale[1].clumpWidthScale_FloatValue' %hairSystem, 1)

    ### Set Pin Number of Hair Constraint ###
    # get hair constraint list
    hairConsts = cmds.listRelatives(c = True, type = 'transform')
    pin = 0
    # print hairConstraint name and pin number
    for hConst in hairConsts:
            if 'Constraint' in hConst: continue
            print 'connectHairConstraint ' + hConst, str(pin) + ';'
            pin += 1

    ### Select Hair Chain Skin Joints ###
    cmds.select(cl = True)
    cmds.select('*skirt*_Ik*_jnt', add = True)
    cmds.select('*skirt*_bakeOut?_jnt', add = True)

    # Select Hairsystem Shape #
    cmds.select('wing*_Line_hairSystemShape')

    # Set to 0 for '_ctr#_zero' group of selected hair block
    selHairBlock = cmds.ls(sl = True)[0]
    prefix = selHairBlock.split('_Block')[0]
    attrList = ['rotateX', 'rotateY', 'rotateZ']
    for i in range(1, 10, 1):
        for attr in attrList:
            try:
                cmds.setAttr('%s.%s' %('%s_ctr%i_zero' %(prefix, i), attr), 0)
            except:
                break

    # Transfer rotate value of 'hair#_ctr#_crv' attributes to the '_zero group' for selected hair block.
    selList = cmds.ls(sl = True)
    attrList = ['rotateX', 'rotateY', 'rotateZ']
    for sel in selList:
        prefix = sel.split('_Block')[0]
        for i in range(1, 10, 1):
            for attr in attrList:
                try:
                    crvAttrVal = cmds.getAttr('%s.%s' %('%s_ctr%i_crv' %(prefix, i), attr))
                    if crvAttrVal == 0:
                        continue
                    else:
                        zeroAttrVal = cmds.getAttr('%s.%s' %('%s_ctr%i_zero' %(prefix, i), attr))
                        setAttrVal = zeroAttrVal + crvAttrVal
                        cmds.setAttr('%s.%s' %('%s_ctr%i_zero' %(prefix, i), attr), setAttrVal)
                        cmds.setAttr('%s.%s' %('%s_ctr%i_crv' %(prefix, i), attr), 0)
                except:
                    break

    ### Set to Static and Turn Off Use Nucleus Solver ###
    selLs = [x for x in cmds.ls(sl = True) if cmds.nodeType(x) == 'hairSystem']
    for sel in selLs:
        cmds.setAttr('%s.active' %sel, False)
        cmds.setAttr('%s.simulationMethod' %sel, 1)

    # Transfer translate and rotate value to parent group for moved controls'
    ctrlLs = cmds.ls(sl = True)
    attrList = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']
    for ctrl in ctrlLs:
        # Get parent gorup
        prntGrp = cmds.listRelatives(ctrl, p = True)[0]
        for attr in attrList:
            # Get control's attribute value
            attrVal = cmds.getAttr('%s.%s' %(ctrl, attr))

            # If control's attribute value is default value then skip
            if attrVal == 0.0:
                continue
            else:
                # Get parent group value and add control attribute value
                prntAttrVal = cmds.getAttr('%s.%s' %(prntGrp, attr))
                attrVal = prntAttrVal + attrVal
                # Set parent group value
                cmds.setAttr('%s.%s' %(prntGrp, attr), attrVal)
                # Set 0 value for control
                cmds.setAttr('%s.%s' %(ctrl, attr), 0)

    # Hair Width Scale #
    hairSysShps = cmds.ls(sl = True)
    for hairSysShp in hairSysShps:
        cmds.setAttr("%s.hairWidthScale[0].hairWidthScale_FloatValue" %hairSysShp, 200)
        cmds.setAttr("%s.hairWidthScale[1].hairWidthScale_FloatValue" %hairSysShp, 200)
    
    # Hairsystem HiarWidthScale #
    hairSystems = cmds.ls(sl = True)

    startHairWidth = 300
    endHairWidth = 400

    for hairSystem in hairSystems:
        cmds.setAttr(hairSystem + '.hairWidthScale[0].hairWidthScale_FloatValue', startHairWidth)
        cmds.setAttr(hairSystem + '.hairWidthScale[1].hairWidthScale_FloatValue', endHairWidth)


# Set Default Value for Hair Chain Attributes #
def setHairChainDefaultValue():
    hairChainBlockGrps = cmds.ls(sl = True)
    for grp in hairChainBlockGrps:
        hairChainName = grp.rsplit('_Block_GRP')[0]

        # Set nucleus attributes.
        nucName = hairChainName + '_nucleus'
        cmds.setAttr('%s.spaceScale' %nucName, 1)

        # Set endCtr attributes.
        cmds.select('%s*_ctrEnd_crv' %hairChainName, r = True)
        endCtrLs = cmds.ls(sl = True, type = 'transform')
        for endCtr in endCtrLs:
            cmds.setAttr('%s.waveSize' %endCtr, 0.25)
            cmds.setAttr('%s.Damp' %endCtr, 0.1)
            cmds.setAttr('%s.Friction' %endCtr, 0.1)
            cmds.setAttr('%s.startCurveAttract' %endCtr, 0.25)
            cmds.setAttr('%s.bendResistance' %endCtr, 5)

            # Set hair system attributes.
            hairSysName = endCtr.rsplit('_ctrEnd_crv')[0] + '_hairSystemShape'
            cmds.setAttr('%s.stretchResistance' %hairSysName, 200)
            cmds.setAttr('%s.compressionResistance' %hairSysName, 200)
            cmds.setAttr("%s.hairWidthScale[0].hairWidthScale_FloatValue" %hairSysName, 200)
            cmds.setAttr("%s.hairWidthScale[1].hairWidthScale_FloatValue" %hairSysName, 200)

            # Set sine deformer attributes.
            ikCrvName = endCtr.rsplit('_ctrEnd_crv')[0] + '_splineIKCurveShape'
            sine = cmds.listConnections(ikCrvName, s = True, d = False, type = 'nonLinear')[0]
            cmds.setAttr('%s.wavelength' %sine, 3)


def assignSolverToHairChain(name, dynControl):
    """
    Rebuild broken hair chain dynamic system
    Args:
        name: Prefix of 'Block_GRP'
        dynControl: Dynamic controller

    Returns:
        None

    Examples:
        assignSolverToHairChain('coat_bottom', 'dyn_ctr_crv')
    """
    time = pm.PyNode('time1')
    solver = pm.createNode('nucleus', n='%s_nucleus' % name)
    dynControl = pm.PyNode(dynControl)

    time.outTime >> solver.currentTime
    dynControl.attr('%s_startFrame' % name) >> solver.startFrame

    hairSystems = pm.ls('%s*' % name, type='hairSystem')
    for hairSystem in hairSystems:
        solver.startFrame >> hairSystem.startFrame
        index = tak_lib.findMultiAttributeEmptyIndex(solver.name(), 'outputObjects')
        solver.outputObjects[index] >> hairSystem.nextState

        index = tak_lib.findMultiAttributeEmptyIndex(solver.name(), 'inputActive')
        hairSystem.currentState >> solver.inputActive[index]

        index = tak_lib.findMultiAttributeEmptyIndex(solver.name(), 'inputActiveStart')
        hairSystem.startState >> solver.inputActiveStart[index]

    nRigids = pm.ls('%s*' % name, type='nRigid')
    if nRigids:
        for nRigid in nRigids:
            solver.startFrame >> nRigid.startFrame

            index = tak_lib.findMultiAttributeEmptyIndex(solver.name(), 'inputPassive')
            nRigid.currentState >> solver.inputPassive[index]

            index = tak_lib.findMultiAttributeEmptyIndex(solver.name(), 'inputPassiveStart')
            nRigid.startState >> solver.inputPassiveStart[index]

    solver.setParent('%s_GRP' % solver.name())


def recoverHairChainDyn(name):
    """
    When import hairchain if there is no attributes for dynamic on dynamic curve, create attributes and connects

    Parameters:
        name(str): Prefix of hairChain
    """
    dynCtrl = pm.PyNode('dyn_ctr_crv')

    dynCtrl.addAttr('_{0}_'.format(name), niceName='[ {0} ]'.format(name), type='enum', enumName='---------------')
    dynCtrl.setAttr('_{0}_'.format(name), channelBox=True)
    dynCtrl.addAttr('{0}_dynamic'.format(name), type='enum', enumName=['off', 'classicHair', 'nHair'])
    dynCtrl.setAttr('{0}_dynamic'.format(name), channelBox=True)
    dynCtrl.addAttr('{0}_startFrame'.format(name), keyable=True, type='long')

    nucleus = pm.PyNode('{0}_nucleus'.format(name))
    endCtrls = pm.ls('{}*_ctrEnd_crv'.format(name))
    dynamicOffCondition = pm.PyNode('{0}_dynamicOff_condition'.format(name))
    nHairCondition = pm.PyNode('{0}_nHair_condition'.format(name))
    dynCtrlDynamicAttr = dynCtrl.attr('{0}_dynamic'.format(name))
    dynCtrlStartFrameAttr = dynCtrl.attr('{0}_startFrame'.format(name))

    dynCtrlStartFrameAttr >> nucleus.startFrame
    dynCtrlDynamicAttr >> dynamicOffCondition.firstTerm
    dynCtrlDynamicAttr >> nHairCondition.firstTerm

    for endCtrl in endCtrls:
        dynCtrlDynamicAttr >> endCtrl.dynamicType
        dynCtrlStartFrameAttr >> endCtrl.startFrame


def assignNewSolver(solver=None, hairSystems=None):
    """
    Assign new nucleus solver to the selected hair systems or given hairSystem list

    Parameters:
        solver: Nucleus node or nucleus node name
        hairSystems (list): Hair system list

    Examples:
        hairSystems = pm.selected()
        assignNewSolver(solver=None, hairSystems=hairSystems)
    """
    if not hairSystems:
        hairSystems = pm.ls(sl=True)

    # Prepare solver
    if not solver:
        solver = pm.createNode('nucleus')
    if isinstance(solver, basestring):
        solver = pm.PyNode(solver)
    time1 = pm.PyNode('time1')
    time1.outTime.connect(solver.currentTime, f=True)

    for hairSystem in hairSystems:
        if isinstance(hairSystem, basestring):
            hairSystem = pm.PyNode(hairSystem)
        if type(hairSystem) == pm.nodetypes.Transform:
            hairSystem = hairSystem.getShape()

        solver.startFrame.connect(hairSystem.startFrame, f=True)

        index = tak_lib.findMultiAttributeEmptyIndex(node=solver, attribute='outputObjects')
        solver.outputObjects[index].connect(hairSystem.nextState, f=True)

        index = tak_lib.findMultiAttributeEmptyIndex(node=solver, attribute='inputActive')
        hairSystem.currentState.disconnect()
        hairSystem.currentState.connect(solver.inputActive[index])

        index = tak_lib.findMultiAttributeEmptyIndex(node=solver, attribute='inputActiveStart')
        hairSystem.startState.disconnect()
        hairSystem.startState.connect(solver.inputActiveStart[index])


def changeHairSystem(sourceHairSystem, targetHairSystem):
    """
    Reassign source hairsystem to the target hairsystem
    
    Parameters:
        sourceHairSystem(pymel.core.nodetypes.HairSystem): Source hairsystem
        targetHairSystem(pymel.core.nodetypes.HairSystem): Target hairsystem
    """

    availableOutputHairId = tak_lib.findMultiAttributeEmptyIndex(str(targetHairSystem), 'outputHair')
    
    follicles = sourceHairSystem.listConnections(type='follicle', s=False)
    for follicle in follicles:
        targetHairSystem.outputHair[availableOutputHairId] >> follicle.currentPosition
        follicle.outHair >> targetHairSystem.inputHair[availableOutputHairId]
        availableOutputHairId += 1


def connectScalpToPatch(scalp, patch):
    """
    Connect scalp mesh to xgen patch to follow guides to scalp mesh.

    Parameters:
        scalp: string, Scalp mesh name.
        patch: string, Xgen patch name.

    Returns:
        None

    Examples:
        tak_xgenUtils.connectScalpToPatch(scalp="hairScalp_geo", patch="hairScalp_geo_teajung_frontHair")
    """

    patchShp = pm.listRelatives(patch)[0]
    pm.connectAttr(scalp + ".worldMesh", patchShp + ".geometry")
    pm.connectAttr(scalp + ".matrix", patchShp + ".transform")


def connectFollicleToScalp(follicle, scalp):
    """
    Parameters:
        follicle: string, Follicle name.
        scalp: string, Scalp mesh name.

    Returns:
        None

    Examples:
        tak_xgenUtils.connectFollicleToScalp(follicle='follicle1', scalp='hairScalp_geo')
    """

    folShp = pm.listRelatives(follicle)[0]
    pm.connectAttr(scalp + ".outMesh", folShp + ".inputMesh", f=True)
    pm.connectAttr(scalp + ".worldMatrix", folShp + ".inputWorldMatrix", f=True)


def attachGuideToScalp():
    xgGuides = pm.ls(type='xgmSplineGuide')
    for xgGuide in xgGuides:
        xgmMakeGuide = xgGuide.toMakeGuide.connections()[0]
        xgmMakeGuide.outputMesh.connect(xgGuide.inputMesh, f=True)


