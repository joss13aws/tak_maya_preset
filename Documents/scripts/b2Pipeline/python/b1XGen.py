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
        pm.system.exportSelected(exportPath=self.publishPath/self.scalpGrp+'.ma', f=True, type='mayaAscii')

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
        pm.exportSelected(exportPath=self.publishPath/self.collection+'_shaders.ma', f=True, type='mayaAscii')

        # Write shader assign information
        with open(self.publishPath/self.collection+'_shaders.json', 'w') as f:
            json.dump(shaderAssignInfo, f, indent=4)


class B1XGenRebuild(B1XGen):
    def __init__(self, assetName, sourceDirPath):
        super(B1XGenRebuild, self).__init__(assetName)
        self.sourceDirPath = pm.Path(sourceDirPath)

    def importSources(self):
        pm.importFile(self.sourceDirPath/self.scalpGrp+'.ma')
        xg.importPalette(str(self.sourceDirPath/self.collection+'.xgen').replace('\\', '/'), '')
        pm.importFile(self.sourceDirPath/self.collection+'_shaders.ma')

    def assignShader(self):
        with open(self.sourceDirPath/self.collection+'_shaders.json', 'r') as f:
            shaderAssignInfo = json.load(f)

        for description, shader in shaderAssignInfo.items():
            pm.select(description, r=True)
            pm.hyperShade(assign=shader)
