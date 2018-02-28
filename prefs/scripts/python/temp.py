# b1XGen Module Test Code #
import b2Pipeline.python.b1XGen as b1XGen
reload(b1XGen)

b1xgC = b1XGen.B1XGenCreate('charA', r'P:\1801_A71\A71_maya')

b1xgC.createDescription('mainHair')
b1xgC.createDescription('subHair')
b1xgC.createDescription('beard')

b1xgC.assignHairShader('black', 'charA_mainHair_desc')
b1xgC.assignHairShader('black', 'charA_subHair_desc')
b1xgC.assignHairShader('brown', 'charA_beard_desc')

b1xgP = b1XGen.B1XGenPublish('charA', 'd:/temp')
b1xgP.publishScalp()
b1xgP.publishCollection()
b1xgP.publishShader()



import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.cmds as cmds
import maya.mel as mel

# poly mesh and skinCluster name
shapeName = 'pSphere1'
clusterName = 'skinCluster1'

# get the MFnSkinCluster for clusterName
selList = OpenMaya.MSelectionList()
selList.add(clusterName)
clusterNode = OpenMaya.MObject()
selList.getDependNode(0, clusterNode)
skinFn = OpenMayaAnim.MFnSkinCluster(clusterNode)

# get the MDagPath for all influence
infDags = OpenMaya.MDagPathArray()
skinFn.influenceObjects(infDags)

# create a dictionary whose key is the MPlug indice id and
# whose value is the influence list id
infIds = {}
infs = []
for x in xrange(infDags.length()):
	infPath = infDags[x].fullPathName()
	infId = int(skinFn.indexForInfluenceObject(infDags[x]))
	infIds[infId] = x
	infs.append(infPath)

# get the MPlug for the weightList and weights attributes
wlPlug = skinFn.findPlug('weightList')
wPlug = skinFn.findPlug('weights')
wlAttr = wlPlug.attribute()
wAttr = wPlug.attribute()
wInfIds = OpenMaya.MIntArray()

# the weights are stored in dictionary, the key is the vertId,
# the value is another dictionary whose key is the influence id and
# value is the weight for that influence
weights = {}
for vId in xrange(wlPlug.numElements()):
	vWeights = {}
	# tell the weights attribute which vertex id it represents
	wPlug.selectAncestorLogicalIndex(vId, wlAttr)

	# get the indice of all non-zero weights for this vert
	wPlug.getExistingArrayAttributeIndices(wInfIds)

	# create a copy of the current wPlug
	infPlug = OpenMaya.MPlug(wPlug)
	for infId in wInfIds:
		# tell the infPlug it represents the current influence id
		infPlug.selectAncestorLogicalIndex(infId, wAttr)

		# add this influence and its weight to this verts weights
		try:
			vWeights[infIds[infId]] = infPlug.asDouble()
		except KeyError:
			# assumes a removed influence
			pass
	weights[vId] = vWeights











from maya import OpenMaya
from maya import OpenMayaAnim

selLs = OpenMaya.MSelectionList()

selLs.add('skinCluster124')
skinNode = OpenMaya.MObject()
selLs.getDependNode(0, skinNode)
skinFn = OpenMayaAnim.MFnSkinCluster(skinNode)

selLs.add('nose_primary_jnt')
infDagPath = OpenMaya.MDagPath()
selLs.getDagPath(1, infDagPath)

affectedPoints = OpenMaya.MSelectionList()
weights = OpenMaya.MDoubleArray()

skinFn.getPointsAffectedByInfluence(infDagPath, affectedPoints, weights)

dagPath = OpenMaya.MDagPath()
component = OpenMaya.MObject()
print component.apiTypeStr()
affectedPoints.getDagPath(0, dagPath, component)

vtxIter = OpenMaya.MItMeshVertex(dagPath, component)
counter = 0
while not vtxIter.isDone():
	print vtxIter.index(), weights[counter]
	counter += 1
	vtxIter.next()
	
OpenMaya.MGlobal.select(dagPath, component, OpenMaya.MGlobal.kReplaceList)





from maya import cmds


def testWin():
	win = 'testWindow'
	if cmds.window(win, exists=True):
		cmds.deleteUI(win)
	
	cmds.window(win)
	buildUI()
	cmds.showWindow()


def buildUI():
	# 윈도우의 메인 레이아웃
	mainLo = cmds.columnLayout(adj=True)
	
	# 전체 컨트롤하는 위젯 만들기
	allWidgetObject = AllWidget()

 	spheres = cmds.ls(sl=True)
	for sphere in spheres:
		# 선택한 오브젝트 각각에 대해서 커스텀위젯 만들기
		sphereWidgetObject = SphereWidget(sphere)
		# allWidget의 sphereWidgetObjcets 리스트에 추가하기
		allWidgetObject.sphereWidgetObjects.append(sphereWidgetObject)


class AllWidget(object):
	def __init__(self):
		# sphereWidgetObject들을 담아둘 수 있는 리스트 Attribute 추가
		self.sphereWidgetObjects = []
		self.buildUI()

	
	def buildUI(self):
		cmds.rowColumnLayout(numberOfColumns=2)
		cmds.checkBox(label='', cc=self.allVisChkBox)
		cmds.checkBox(label='', cc=self.allSelCmd)
	
	
	def allVisChkBox(self, val):
		for sphereWidgetObject in self.sphereWidgetObjects:
			cmds.checkBox(sphereWidgetObject.visChkBoxName, e=True, v=val)
			sphereWidgetObject.chkBoxCC(val)
	
	
	def allSelCmd(self, val):
		sphereWidgetObjectSpheres = []
		for sphereWidgetObject in self.sphereWidgetObjects:
			sphereWidgetObjectSpheres.append(sphereWidgetObject.sphereName)
		
		if val:
			cmds.select(sphereWidgetObjectSpheres)
		else:
			cmds.select(cl=True)


class SphereWidget(object):
	def __init__(self, sphere):
		self.sphereName = sphere
		self.buildUI()
	
	
	def buildUI(self):
		cmds.rowColumnLayout(numberOfColumns=2)
		self.visChkBoxName = cmds.checkBox(label='', cc=self.chkBoxCC)
		cmds.button(label=self.sphereName, c=self.btnCmd)

	
	def chkBoxCC(self, val):
		cmds.setAttr('%s.visibility' % self.sphereName, val)
	
	
	def btnCmd(self, *args):
		cmds.select(self.sphereName)


testWin()
