import pymel.core as pm
import xgenm as xg


class B1XGen(object):
    b1ProjectRoot = 'p:/'

    def __init__(self, prefix):
        self.prefix = prefix
        self.collectionName = '{0}_collection'.format(self.prefix)
        self.hairFurGrp = '{0}_hairFur_grp'.format(self.prefix)
        self.scalpGrp = '{0}_scalp_grp'.format(self.prefix)


class B1XGenCreate(B1XGen):
    def __init__(self, prefix, xgenRoot=''):
        super(B1XGenCreate, self).__init__(prefix)

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
        assert scalp.startswith(self.prefix), 'Scalp name must start with "{0}_"'.format(self.prefix)

        prefixedDescription = self.prefix+'_'+description
        xg.createDescription(self.collectionName, prefixedDescription, primitive, generator, renderer, method)
        xg.modifyFaceBinding(self.collectionName, prefixedDescription)

        # Cleanup outliner
        pm.parent(scalp, self.scalpGrp)
        pm.parent(self.collectionName, self.hairFurGrp)


class B1XGenPublish(B1XGen):
    def __init__(self, prefix, publishPath):
        super(B1XGenPublish, self).__init__(prefix)
        self.publishPath = pm.Path(publishPath)

    def publishScalp(self):
        pm.select(self.hairFurGrp, r=True)
        pm.system.exportSelected(exportPath=self.publishPath/self.scalpGrp+'.ma', f=True, type='mayaAscii')

    def publishCollection(self):
        xg.exportPalette(self.collectionName, str(self.publishPath/self.collectionName+'.xgen'))

    def publishShader(self):
        pass
