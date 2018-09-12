import sys
import maya.api.OpenMaya as om


VENDOR = 'Tak'
VERSION = '1.0'


def maya_useNewAPI():
    pass


class Line(om.MPxNode):
    # Attributes
    name = 'line'
    id = om.MTypeId(0x00002735)

    len = None
    nPoints = None
    vector = None
    outCurve = None

    def __init__(self):
        om.MPxNode.__init__(self)

    @staticmethod
    def creator():
        return Line()

    @staticmethod
    def initialize():
        nAttrFn = om.MFnNumericAttribute()
        typedAttrFn = om.MFnTypedAttribute()

        # Create attributes
        Line.len = nAttrFn.create('length', 'length', om.MFnNumericData.kFloat, 10.0)
        nAttrFn.keyable = True

        Line.nPoints = nAttrFn.create('numOfPoints', 'numOfPoints', om.MFnNumericData.kInt, 5)
        nAttrFn.keyable = True

        Line.vector = nAttrFn.createPoint('vector', 'vector')
        nAttrFn.keyable = True

        Line.outCurve = typedAttrFn.create('outCurve', 'outCurve', om.MFnData.kNurbsCurve)
        typedAttrFn.writable = False
        typedAttrFn.storable = False

        # Add attributes
        Line.addAttribute(Line.len)
        Line.addAttribute(Line.nPoints)
        Line.addAttribute(Line.vector)
        Line.addAttribute(Line.outCurve)

        # Set attributes dependency
        Line.attributeAffects(Line.len, Line.outCurve)
        Line.attributeAffects(Line.nPoints, Line.outCurve)
        Line.attributeAffects(Line.vector, Line.outCurve)

    def compute(self, plug, block):
        # Check requested plug
        if (plug != Line.outCurve):
            return None

        # Get inputs
        len = block.inputValue(Line.len).asFloat()
        nPoints = block.inputValue(Line.nPoints).asInt()

        # Calculate
        deg = 1
        spans = nPoints - deg
        nknots = spans + 2 * deg - 1
        increment = len / nPoints
        vector = om.MVector(1, 1, 0)

        cvs = om.MPointArray()
        for i in range(nPoints):
            cvs.append(om.MPoint() + increment * i * vector)

        knotSeq = []
        for i in range(0, nknots):
            knotSeq.append(i)

        curveData = om.MFnNurbsCurveData()
        curveFn = om.MFnNurbsCurve()
        curve = curveFn.create(cvs, knotSeq, deg, om.MFnNurbsCurve.kOpen, 0, 0)
        
        outCurveHandle = block.outputValue(Line.outCurve)
        outCurveHandle.setMObject(curve)
        block.setClean(plug)

def initializePlugin(obj):
    plugin = om.MFnPlugin(obj, VENDOR, VERSION, 'Any')

    try:
        plugin.registerNode(Line.name, Line.id, 
                            Line.creator, Line.initialize, 
                            om.MPxNode.kDependNode)
    except:
        sys.stderr.write('Failed to register {0} node\n'.format('line'))
        raise


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    try:
        plugin.deregisterNode(Line.id)
    except:
        sys.stderr.write('Failed to deregister {0} node\n'.format('line'))
        raise