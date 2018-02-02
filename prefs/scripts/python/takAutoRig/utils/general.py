import pymel.core as pm


def combineCurves(curves):
    for curve in curves:
        pm.delete(curve, ch=True)
    for curve in curves:
        pm.makeIdentity(curve, apply=True)

    baseCurve = curves[0]
    extraCurves = curves[1:]

    extraCurveShapes = []
    for curve in extraCurves:
        extraCurveShapes.extend(curve.getShapes())

    for extraCurveShape in extraCurveShapes:
        parentCurveShape(extraCurveShape, baseCurve)

    pm.delete(extraCurves)
    pm.select(cl=True)

    return baseCurve


def parentCurveShape(sourceCrv, targetCrv):
    cvPositionDict = {}
    for cv in sourceCrv.cv:
        cvPositionDict[cv] = cv.getPosition(space='world')

    if isinstance(sourceCrv, pm.nodetypes.Transform):
        sourceCrv.getShape().setParent(targetCrv, shape=True, relative=True)
    else:
        pm.parent(sourceCrv, targetCrv, shape=True, relative=True)

    for cv in cvPositionDict:
        cv.setPosition(cvPositionDict.get(cv), space='world')

    targetCrv.updateCurve()


def replaceCurve(origCurve, newCurve):
    origShapes = origCurve.getShapes()
    newShapes = newCurve.getShapes()

    for newShape in newShapes:
        pm.parent(newShape, origCurve, shape=True, relative=True)

    pm.delete(newCurve, origShapes)

    pm.select(cl=True)


def makeGroup(obj, suffix):
    obj = pm.PyNode(obj) if isinstance(obj, str) else obj

    group = obj.duplicate(parentOnly=True, n=obj + suffix)[0]
    obj.setParent(group)

    return group
