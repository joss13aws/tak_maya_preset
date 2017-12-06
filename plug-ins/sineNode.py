"""
Author: LEE SANGTAK
Contact: chst27@gmail.com
"""

from maya import OpenMaya
from maya import OpenMayaMPx
import math

VENDOR = 'Tak'
VERSION = '1.0'
API_VERSION = 'Any'


class SineNode(OpenMayaMPx.MPxNode):
    name = 'sineNode'
    id = OpenMaya.MTypeId(0x00002733)

    inputAttr = OpenMaya.MObject()
    outputAttr = OpenMaya.MObject()
    amplitudeAttr = OpenMaya.MObject()
    frequencyAttr = OpenMaya.MObject()
    offsetAttr = OpenMaya.MObject()

    def __init__(self):
        super(SineNode, self).__init__()

    def compute(self, plug, dataBlock):
        if not plug == SineNode.outputAttr:
            return OpenMaya.kUnknownParameter

        inputValue = dataBlock.inputValue(SineNode.inputAttr).asFloat()
        amplitudeValue = dataBlock.inputValue(SineNode.amplitudeAttr).asFloat()
        frequencyValue = dataBlock.inputValue(SineNode.frequencyAttr).asFloat()
        offsetValue = dataBlock.inputValue(SineNode.offsetAttr).asFloat()

        outputHandle = dataBlock.outputValue(SineNode.outputAttr)
        outputHandle.setFloat(math.sin(inputValue * frequencyValue) * amplitudeValue + offsetValue)
        dataBlock.setClean(plug)

    @staticmethod
    def creator():
        return OpenMayaMPx.asMPxPtr(SineNode())

    @staticmethod
    def initializer():
        numericAttrFn = OpenMaya.MFnNumericAttribute()

        SineNode.outputAttr = numericAttrFn.create('output', 'output', OpenMaya.MFnNumericData.kFloat)
        numericAttrFn.setWritable(False)
        numericAttrFn.setStorable(False)
        SineNode.addAttribute(SineNode.outputAttr)

        SineNode.inputAttr = numericAttrFn.create('input', 'input', OpenMaya.MFnNumericData.kFloat)
        SineNode.addAttribute(SineNode.inputAttr)
        SineNode.attributeAffects(SineNode.inputAttr, SineNode.outputAttr)

        SineNode.amplitudeAttr = numericAttrFn.create('amplitude', 'amplitude', OpenMaya.MFnNumericData.kFloat, 1)
        SineNode.addAttribute(SineNode.amplitudeAttr)
        SineNode.attributeAffects(SineNode.amplitudeAttr, SineNode.outputAttr)

        SineNode.frequencyAttr = numericAttrFn.create('frequency', 'frequency', OpenMaya.MFnNumericData.kFloat, 1)
        numericAttrFn.setMin(0)
        SineNode.addAttribute(SineNode.frequencyAttr)
        SineNode.attributeAffects(SineNode.frequencyAttr, SineNode.outputAttr)

        SineNode.offsetAttr = numericAttrFn.create('offset', 'offset', OpenMaya.MFnNumericData.kFloat)
        SineNode.addAttribute(SineNode.offsetAttr)
        SineNode.attributeAffects(SineNode.offsetAttr, SineNode.outputAttr)


def initializePlugin(mObj):
    pluginFn = OpenMayaMPx.MFnPlugin(mObj, VENDOR, VERSION, API_VERSION)
    pluginFn.registerNode(SineNode.name, SineNode.id,
                          SineNode.creator, SineNode.initializer,
                          OpenMayaMPx.MPxNode.kDependNode)


def uninitializePlugin(mObj):
    pluginFn = OpenMayaMPx.MFnPlugin(mObj)
    pluginFn.deregisterNode(SineNode.id)
