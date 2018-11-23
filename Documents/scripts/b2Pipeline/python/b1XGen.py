import pymel.core as pm
import xgenm as xg
import json


class B1XGen(object):
    b1ProjectRoot = 'p:/'

    def __init__(self, assetName):
        self.assetName = assetName
        self.collection = '{0}_collection'.format(self.assetName)
        self.hairFurGrp = '{0}_hairFur_grp'.format(self.assetName)
        self.scalpGrp = '{0}_scalp_grp'.format(self.assetName)


class B1XGenCreate(B1XGen):
    def __init__(self, assetName, xgenRoot=''):
        super(B1XGenCreate, self).__init__(assetName)

        self.xgenRoot = pm.fileDialog2(fm=3, ds=1, dir=B1XGen.b1ProjectRoot) if xgenRoot == '' else xgenRoot

        if not pm.objExists(self.hairFurGrp):
            pm.group(empty=True, n=self.hairFurGrp)
        if not pm.objExists(self.scalpGrp):
            pm.group(empty=True, n=self.scalpGrp, p=self.hairFurGrp)

        pm.select(cl=True)

    def createDescription(self,
                          description,
                          primitive='Spline',
                          generator='Random',
                          renderer='Renderman',
                          method='Guides'):
        """
        Create xgen description

        Parameters:
             description: Description name
             primitive: Primitive type
             generator: Generate type
             renderer: Renderer that render xgen primitives
             method: Method to control xgen primitives

        Returns:
            None
        """
        # Check user select a scalp mesh that right named
        sels = pm.selected()
        if not sels:
            pm.error('You must select a scalp mesh')
        scalp = sels[0].node()
        assert isinstance(scalp.getShape(), pm.nodetypes.Mesh), 'Need to select a mesh'
        assert scalp.startswith(self.assetName), 'Scalp name must start with "{0}_"'.format(self.assetName)

        prefixedDescription = self.assetName + '_' + description + '_desc'
        xg.createDescription(self.collection, prefixedDescription, primitive, generator, renderer, method)
        xg.modifyFaceBinding(self.collection, prefixedDescription)

        # Cleanup outliner
        pm.parent(scalp, self.scalpGrp)
        pm.parent(self.collection, self.hairFurGrp)

    def assignHairShader(self, name, description):
        hairShader = '{0}_{1}_hairShader'.format(self.assetName, name)
        if not pm.objExists(hairShader):
            hairShader = pm.shadingNode('aiStandardHair', asShader=True, n=hairShader)
        pm.select(description, r=True)
        pm.hyperShade(assign=hairShader)


class B1XGenPublish(B1XGen):
    def __init__(self, assetName, publishPath):
        super(B1XGenPublish, self).__init__(assetName)
        self.publishPath = pm.Path(publishPath)

    def publishScalp(self):
        pm.select(self.scalpGrp, r=True)
        pm.system.exportSelected(exportPath=self.publishPath/self.scalpGrp+'.mb', f=True, type='mayaBinary')

    def publishCollection(self):
        xg.exportPalette(self.collection, str(self.publishPath/self.collection+'.xgen').replace('\\', '/'))

    def publishShader(self):
        hairShaders = []
        shaderAssignInfo = {}

        descriptions = pm.listRelatives(self.collection)
        for description in descriptions:
            hairShader = pm.ls(description.getShape().connections(type='shadingEngine')[0].connections(), materials=True)
            hairShaders.extend(hairShader)
            shaderAssignInfo[str(description)] = str(hairShader[0])

        hairShaders = list(set(hairShaders))
        pm.select(hairShaders, r=True)
        pm.exportSelected(exportPath=self.publishPath/self.collection+'_shaders.mb', f=True, type='mayaBinary')

        # Write shader assign information
        with open(self.publishPath/self.collection+'_shaders.json', 'w') as f:
            json.dump(shaderAssignInfo, f, indent=4)


class B1XGenBuild(B1XGen):
    def __init__(self, assetName, sourceDirPath):
        super(B1XGenBuild, self).__init__(assetName)
        self.sourceDirPath = pm.Path(sourceDirPath)
        self.scalpFilePath = self.sourceDirPath / self.scalpGrp + '.mb'
        self.collectionFilePath = str(self.sourceDirPath/self.collection+'.xgen').replace('\\', '/')
        self.shaderFilePath = self.sourceDirPath/self.collection+'_shaders.mb'

    def importSources(self):
        pm.importFile(self.scalpFilePath)
        pm.importFile(self.shaderFilePath)
        xg.importPalette(self.collectionFilePath, '')

    def assignShader(self):
        with open(self.sourceDirPath/self.collection+'_shaders.json', 'r') as f:
            shaderAssignInfo = json.load(f)

        for description, shader in shaderAssignInfo.items():
            pm.select(description, r=True)
            pm.hyperShade(assign=shader)


class B1XGenCache(B1XGenBuild):
    def __init__(self, assetName, sourceDirPath, cacheDirPath):
        super(B1XGenCache, self).__init__(assetName, sourceDirPath)
        self.cacheDirPath = pm.Path(cacheDirPath)

    def importScalp(self):
        pm.importFile(self.scalpFilePath, namespace=self.assetName)

    def attachToAniModel(self, model):
        pm.select('{0}:{1}'.format(self.assetName, self.scalpGrp), model, r=True)
        pm.mel.eval('CreateWrap;')

    def exportCaches(self):
        scalpGrpRef = pm.PyNode('{0}:{1}'.format(self.assetName, self.scalpGrp))
        minTime = int(pm.playbackOptions(q=True, minTime=True))
        maxTime = int(pm.playbackOptions(q=True, maxTime=True))
        scalpGrpCacheFilePath = (self.cacheDirPath / self.scalpGrp + '.abc').replace('\\', '/')
        pm.mel.eval('AbcExport -j "-frameRange {minTime} {maxTime} -stripNamespaces -uvWrite -worldSpace -writeVisibility -dataFormat ogawa -root {scalpGrpDagPath} -file {scalpGrpCacheFilePath}";'.format(
            minTime=minTime, maxTime=maxTime, scalpGrpDagPath=scalpGrpRef.longName(), scalpGrpCacheFilePath=scalpGrpCacheFilePath))

    def attachCaches(self):
        pm.mel.eval('AbcImport -mode import -fitTimeRange -connect "{0}" "{1}";'.format(self.scalpGrp, (self.cacheDirPath/self.scalpGrp+'.abc').replace('\\', '/')))
