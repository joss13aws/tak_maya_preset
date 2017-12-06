"""
Author: LEE SANGTAK
Contact: chst27@gmail.com

Usage:
    import takShapeDivider

    shapeDivider = takShapeDivider.ShapeDivider(baseGeo='face', targetGeo='eyebrows_up')
    shapeDivider.build()

    # Fit border using leftBorderPlane

    shapeDivider.divide(numberOfDivision=6)
"""

import pymel.core as pm


class ShapeDivider(object):
    def __init__(self, baseGeo=None, targetGeo=None):
        self.baseGeo = None
        self.targetGeo = None
        self.outGeo = None
        self.rampBS = None
        self.centerPlane = None
        self.leftBorderPlane = None
        self.rightBorderPlane = None
        self.refPlaneRootGrp = None
        self.targetGeoBoundingBox = None

        if not pm.pluginInfo('rampBlendShape', q=True, loaded=True):
            pm.loadPlugin('rampBlendShape')

        if not baseGeo or not targetGeo:
            selLs = pm.ls(sl=True)
            if not len(selLs) == 2:
                raise RuntimeError('Select baseGeo and targetGeo')
            self.baseGeo = selLs[0]
            self.targetGeo = selLs[1]
        else:
            if isinstance(baseGeo, str):
                baseGeo = pm.PyNode(baseGeo)
            if isinstance(targetGeo, str):
                targetGeo = pm.PyNode(targetGeo)

            self.baseGeo = baseGeo
            self.targetGeo = targetGeo

    def build(self):
        self.outGeo = self.baseGeo.duplicate(n='%s_rampBS' % self.targetGeo.name())[0]
        pm.delete(pm.parentConstraint(self.targetGeo, self.outGeo, mo=False))

        self.createRefPlanes()

        self.rampBS = pm.createNode('rampBlendShape')

        self.connectNodes()

        self.targetGeo.hide()

    def createRefPlanes(self):
        self.refPlaneRootGrp = pm.group(n='refPlaneRoot_grp', empty=True)
        pm.parentConstraint(self.outGeo, self.refPlaneRootGrp, mo=False)

        self.targetGeoBoundingBox = self.targetGeo.boundingBox()
        boundingBoxWidth = self.targetGeoBoundingBox.width()
        boundingBoxHeight = self.targetGeoBoundingBox.height()

        self.centerPlane = pm.polyPlane(n='centerPlane', w=boundingBoxWidth, h=boundingBoxHeight, sw=1, sh=1, axis=[1, 0, 0], ch=False)[0]
        self.leftBorderPlane = self.centerPlane.duplicate(n='leftBorderPlane')[0]
        self.rightBorderPlane = self.centerPlane.duplicate(n='rightBorderPlane')[0]

        self.refPlaneRootGrp | self.centerPlane
        self.centerPlane | self.leftBorderPlane
        self.centerPlane | self.rightBorderPlane

        self.centerPlane.translate.set(0, 0, 0)

        leftBorderPlaneInvXMul = pm.createNode('multiplyDivide', n='leftBorderPlaneInvX_mul')
        leftBorderPlaneInvXMul.input2X.set(-1)

        self.leftBorderPlane.translateX >> leftBorderPlaneInvXMul.input1X
        leftBorderPlaneInvXMul.outputX >> self.rightBorderPlane.translateX

        self.leftBorderPlane.translateX.set(boundingBoxWidth / 2)

    def connectNodes(self):
        self.baseGeo.getShape().worldMesh >> self.rampBS.baseGeo
        self.targetGeo.getShape().worldMesh >> self.rampBS.targetGeo
        self.rampBS.outGeo >> self.outGeo.inMesh

        self.centerPlane.translateX >> self.rampBS.attr('center')
        self.leftBorderPlane.translateX >> self.rampBS.range

    def divide(self, numOfDivision=6):
        wholeRange = self.rampBS.range.get() * 2
        divisionRange = wholeRange / (numOfDivision-1)
        startCenter = -(wholeRange / 2)

        self.leftBorderPlane.translateX.set(divisionRange)

        dividedGeoXOrigin = self.targetGeo.translateX.get()
        dividedGeoXOffset = self.targetGeoBoundingBox.width()

        for i in xrange(numOfDivision):
            self.centerPlane.translateX.set(startCenter)

            dividedGeo = self.outGeo.duplicate(n='%s%s' % (self.targetGeo, i+1))[0]
            dividedGeoXPos = dividedGeoXOrigin + (dividedGeoXOffset*(i+1))
            dividedGeo.translateX.set(dividedGeoXPos)

            startCenter += divisionRange

        self.targetGeo.show()

        pm.delete(self.outGeo, self.refPlaneRootGrp)

