# shader export/ import

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

import json
import os


def getShaderInfo(ref=True, lst=None, uvChoose=None):

    # ref : do not export ref.
    # lst : only lst connectd
    # uvChoose : support multiUV

    _all = []
    if lst:
        _all = cmds.ls(lst, dag=1) 
    else:
        _all = cmds.ls(dag=1) 

    _ex = ['initialParticleSE', 'initialShadingGroup']
    _dict = {}


    uvChooserInfo = {}
    if uvChoose:        
        uvcLst = cmds.ls(type='uvChooser')
        for uvc in uvcLst:
            cons = cmds.listConnections(uvc, s=1, d=0, c=1, p=1)
            if cons:
                curInfo = []
                for i in range( 0, len(cons), 2):                        
                    if cons[i+1].split('.')[0] in _all:
                        curInfo.append( (cons[i], cons[i+1] ) )
                if curInfo:
                    uvChooserInfo[uvc] = curInfo
        # print uvChooserInfo

    place3dTexture = {}
    p3ts = cmds.ls(type='place3dTexture')
    if p3ts:
        for p in p3ts:
            _dic = {}
            # parent = None
            temp = cmds.listRelatives(p, p=1)
            if temp:
                # parent = temp[0]
                _dic['parent'] = temp[0]
            cons = cmds.listConnections(p, s=1, d=0, c=1, p=1)
            if cons:
                curInfo = []
                for i in range( 0, len(cons), 2):                        
                    if cons[i+1].split('.')[0] in _all:
                        curInfo.append( (cons[i], cons[i+1] ) )
                _dic['cons'] = curInfo

            place3dTexture[p] = _dic


    shaders = []
    for sg in cmds.ls(type='shadingEngine'):
        if not sg in _ex:
            if not ref:
                if cmds.referenceQuery( sg, isNodeReferenced=True ):
                    continue
            shaders.append(sg)

    shaderInfo = {}
    for s in shaders:
        items = cmds.sets(s, q=True)            
        # print items
        if items:
            ex = []            
            for item in items:
                if item.split('.')[0] in _all:
                    ex.append(item)
            if ex:
                shaderInfo[s] = items
            else:                   
                print 'not include shader : %s'%s

    if shaderInfo:
        _dict['shadingEngine'] = shaderInfo

    if uvChooserInfo:
        _dict['uvChooser'] = uvChooserInfo
    
    if place3dTexture:
        _dict['place3dTexture'] = place3dTexture
    
    if cmds.pluginInfo('mtoa', query=True, loaded=True ):
        _dict['arnold'] = getArnoldInfo(_all)
        # print len(_dict['arnold'])

    return _dict


def getArnoldInfo(lst):        


    # get default
    pc = cmds.polyCube()
    shape = cmds.listRelatives( pc[0], c=1, s=1)[0]
    # shape = 'aaa:wooden_part_0024Shape'
    k = cmds.listAttr(shape, fp=1)
    aiDefault = {}
    for a in k:
        if 'ai' in a:
            try:
                aiDefault[a] = cmds.getAttr( shape + '.' + a )
            except:
                pass

    cmds.delete(pc[0])



    _dic = {}
    meshes = cmds.ls(lst, type ='mesh')    
    for mesh in meshes:
        optionAi = {}
        for s in aiDefault.keys():
            if cmds.objExists(mesh + '.' + s):
                val = cmds.getAttr(mesh + '.' + s)
                if not aiDefault.get(s) == val:
                    # print s , val , aiDefault.get(s)
                    optionAi[s] = val
                    
        if optionAi: 
            _dic[str(mesh)] = optionAi

    return _dic
    

def exportShader(filePath, _dic):     
    # logger.info('exportShader')
    
    shadingGroup = _dic.get('shadingEngine')
    if not shadingGroup:
        return

    disCon = []
    # if uvChoose:
    uvChooser = _dic.get('uvChooser')
    if uvChooser:
        for uvc in uvChooser:
            for cons in uvChooser[uvc] :   
                print cmds.disconnectAttr( cons[1], cons[0] )
                disCon.append(cons)
    
    p3dT = _dic.get('place3dTexture')
    p3dtGrp = ''
    if p3dT:
        p3dtGrp = cmds.createNode('transform', n='p3Dtex_grp')            
        for p in p3dT:
            # p3dT.get('parent')
            cmds.parent(p, p3dtGrp)


    # export
    pm.select(shadingGroup, r=True, ne=True)
    makeFolder(filePath)
    cmds.file( filePath, force=True, op='v=0;', typ='mayaAscii', pr=False, es=True)
    pm.select(cl=True)

    if disCon:
        for cons in disCon :   
            print cmds.connectAttr( cons[1], cons[0] )

    if p3dT: 
        print p3dT        
        for p, v in p3dT.items():
            if v.get('parent'):
                cmds.parent(p, v.get('parent'))
            else:
                cmds.parent(p, w=1)

        if cmds.objExists(p3dtGrp):
            cmds.delete(p3dtGrp)

    print filePath


def exportShaderJson(filePath, _dict):
    # logger.info('exportShaderJson')
    makeFolder(filePath)
    # Record json
    with open (filePath, 'w') as data: 
        json.dump(_dict, data, sort_keys=True, indent=4, separators=(',', ': '))
    # logger.info('export JSON file : %s'% filePath )





# importAOV(shaderNS)
def importShaderJson(jsonFullPath, shaderFullPath, shaderNS, namespaces):
    # logger.info('importShaderJson')

    
    with open(jsonFullPath) as data: 
        _dict = json.load(data)   

    _Arnold = _dict.get('arnold')
    _SG = _dict.get('shadingEngine')
    _uvChooser = _dict.get('uvChooser')
    _p3Dtex = _dict.get('place3dTexture')
    if _Arnold:
        setRenderer('arnold')   
    if not _SG:
        # old
        _SG = _dict

    suc = 0
    none = 0
    fail = 0

    # if shaderNS in getNamespaceList():
    shaderNS = uniqueNamespace(shaderNS)

    a = cmds.file(shaderFullPath, i=True, mergeNamespacesOnClash=True, namespace=shaderNS )
    # logger.info('shader import : %s'%a)


    # uv chooser connect.
    if _uvChooser:
        print 'arnold set'
        for k, v in _uvChooser.items():
            
            if cmds.objExists( shaderNS + ':' + k ):
                print 'exists. : %s'%shaderNS + ':' + k
                for con in v:                        
                    if namespaces:
                        src = '|'.join([ (namespaces[0] + ':' + u) for u in con[1].split('|') ])                           
                    else:
                        src = [ con[1] ]

                    trg = shaderNS + ':' + con[0]

                    print src, trg
                    if cmds.objExists(src) and cmds.objExists(trg):
                        print cmds.connectAttr( src, trg)
                    else:
                        print 'not exists.'
            else:
                print 'not exists. : %s'%shaderNS + ':' + k

    if _p3Dtex:
        for k, v in _p3Dtex.items():
            if namespaces:
                src = namespaces[0] + ':' + k
            else:
                src = k

            trg = shaderNS + ':' + k

            if cmds.objExists(src):
                cmds.parentConstraint(src, trg)
                cmds.scaleConstraint(src, trg)

    # Assign Shader
    for k, v in _SG.items():
        if v:
            shapes = []
            if namespaces:
                for s in v:                    
                    for namespace in namespaces:
                        shape = '|'.join([ (namespace + ':' + u) for u in s.split('|') ])
                        shapes.append(shape)                                               
            else:
                shapes = v                
            
            targetShape = []
            for shape in shapes:

                if cmds.objExists(shape):
                    targetShape.append(shape)

                    # rigged Deformed shape has no namespace.
                    if cmds.getAttr( shape.split('.')[0] + '.intermediateObject') == 1:
                        shape = '|'.join([ u.split(':')[-1] for u in s.split('|') ])
                        if '.' in shape:        
                            deformed = shape.replace('.', 'Deformed.' )
                        else:
                            deformed = shape + 'Deformed'
                        print deformed
                        if cmds.objExists(deformed):                            
                            targetShape.append(deformed) 

                else:
                    # check deformed -  abc cached deformed shape
                    if '.' in shape:                        
                        deformed = shape.replace('.', 'Deformed.' )
                    else:
                        deformed = shape + 'Deformed'
                    if cmds.objExists(deformed):                            
                        targetShape.append(deformed)
                    else:
                        none += 1
                        print 'not exists : %s'%shape

            # assign
            try     :
                pm.sets((shaderNS + ':' + k), e=True, fe= targetShape)
                suc += 1
                # print 'assigned'
            except  :                   
                print 'failed : %s >> %s' %((shaderNS + ':' + k), shape )
                fail += 1


    # abc reference : when face shader assign abc connection break.
    for namespace in namespaces:
        fixAbcConnectionErrorSetup(namespace)
        # abc = cmds.ls(namespace+':*', type='AlembicNode')
        # if abc:
        #     gp = cmds.listConnections(abc[0], type='groupParts', c=1, sh=1)
        #     for m in range(0, len(gp), 2):       
        #         if not cmds.objExists( gp[m+1] + '.abc' ):
        #             cmds.addAttr(gp[m+1], ln='abc', dt="string")
        #         cmds.setAttr( gp[m+1]+ '.abc' , gp[m] , type='string')
    

    # .inputGeometry
    # for namespace in namespaces:
    #     mesh = cmds.ls(namespace+':*', type='mesh')
    #     for m in mesh:
    #         if cmds.objExists(m + '.abc'):
    #             abc = cmds.listConnections(m +'.inMesh')
    #             if not abc:
    #                 con = cmds.getAttr( m + '.abc')
    #                 cmds.connectAttr(con, m+'.inMesh', f=1 )
    #                 print 'connect abc again : %s'% m

    # arnold set.
    if _Arnold:
        print 'arnold set'
        for k, v in _Arnold.items():
            # node = '|'.join([ (namespace + ':' + s) for s in k.split('|') ])
            nodes = []
            if namespaces:
                for namespace in namespaces:
                    node = '|'.join([ (namespace + ':' + s) for s in k.split('|') ])
                    nodes.append(node)
            else:
                nodes.append(k)

            for node in nodes:
                for attr, value in v.items():                
                    try:
                        attrType = cmds.attributeQuery(attr, node=node, attributeType =True)                
                        if attrType == 'typed':
                            cmds.setAttr( (node + '.' + attr) , value, type='string')
                            # print 'assign arnold Attr :%s >> %s'%((node + '.' + attr), value)
                        elif attrType == 'float3':
                            cmds.setAttr( (node + '.' + attr) , value[0], value[1], value[2], type='float3')
                            # print 'assign arnold Attr :%s >> %s'%((node + '.' + attr), value)
                        elif attrType == 'message':
                            pass
                        else:
                            cmds.setAttr((node + '.' + attr), value)
                            # print 'assign arnold Attr :%s >> %s'%((node + '.' + attr), value)
                    except:
                        print 'cannot assigned arnold Attr :%s >> %s'%((node + '.' + attr), value)


    # connect
    for ns in namespaces:
        top = getTopNamespaceNode(ns)                
        if not cmds.objExists(top + '.lookdev'):
            cmds.addAttr(top, ln='lookdev', dt="string")
        cmds.setAttr(top + '.lookdev', shaderNS, type='string')

    # print 'not exists shape '
    return (suc, fail, none)





def makeFolder(filePath):
    path, fileName = os.path.split(filePath)
    if not os.path.exists(path):
        os.makedirs(path, 0o777)

def uniqueNamespace(namespace):
    NS = getNamespaceList()          
    if namespace in NS:
        i=1
        run = True
        while run:
            result = namespace + str(i) 
            if result in NS:
                i += 1  
            else:
                return result
        else:
            print 'result  : %s'%result
    else:
        return namespace

def getNamespaceList():
    default = [u'UI', u'shared']
    refNS = getReferenceNamespaces()
    pm.namespace(set=":")
    _list = pm.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    result = []
    for d in _list:
        if d in refNS or d in default:
            continue
        result.append(d)               
    return result

def getReferenceNamespaces():
    ns = []
    for r in getReferenceList():
        r_file = r.referenceFile()
        if not r_file:
            continue
        if r_file.isLoaded():
            ns.append(r_file.fullNamespace)
    return ns

def getReferenceList():
    _list = pm.ls(rf=True)
    return _list





if __name__ == '__main__':

    #### export ####
    shaderFile = 'd:/test.ma'
    jsonFile = 'd:/test.json'
    
    # export selected meshes` shader 
    _dic = getShaderInfo()
    print _dic

    # export file
    exportShader(shaderFile, _dic)
    exportShaderJson(jsonFile, _dic)


    # #### import ####

    # # assign shader to namespace list 
    # # multi references can share 1 shader.
    # importShaderJson(jsonFile, shaderFile, 'test_shader', [':'])



