import pymel.core as pm


def combineCurves(curves):
    baseCurve = curves[0]
    extraCurves = curves[1:]

    for curve in curves:
        pm.delete(curve, ch=True)

    extraCurveShapes = []
    for curve in extraCurves:
        shapeBuffer = curve.getShapes()
        for shape in shapeBuffer:
            extraCurveShapes.append(shape)

    for extraCurveShape in extraCurveShapes:
        pm.parent(extraCurveShape, baseCurve, shape=True, relative=True)
    pm.delete(extraCurves)

    pm.select(cl=True)

    return baseCurve


def replaceCurve(origCurve, newCurve):
    origShapes = origCurve.getShapes()
    newShapes = newCurve.getShapes()

    for newShape in newShapes:
        pm.parent(newShape, origCurve, shape=True, relative=True)

    pm.delete(newCurve, origShapes)

    pm.select(cl=True)


def makeGroup(obj, suffix):
    obj = pm.PyNode(obj) if isinstance(obj, str) else obj

    group = obj.duplicate(parentOnly=True, n=obj+suffix)
    obj.setParent(group)

    return group
