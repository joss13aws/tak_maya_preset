# coding: euc-kr

"""
Author: Sang-tak Lee
Contact: chst27@gmail.com

Description:
b2Pipeline Additional python functions.
"""


import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMaya as OpenMaya
import re
import os
import sys
import shutil
import glob
import pprint
import logging
import zipfile
import tak_lib_b1

logging.basicConfig()
logger = logging.getLogger('tak_b2Pipeline_add_logger')
logger.setLevel(logging.DEBUG)

def customAttrAbcMel(assetNamespace):
    '''
    Return mel code that adding custom attributes to alembic cache when release.
    '''

    assetRoot = assetNamespace + ':lod03_GRP'
    customAttrLs = ["renMdlVer"]

    chlds = cmds.listRelatives(assetRoot, ad = True, ni = True, path = True, type = 'transform')

    for chld in chlds:
        udAttrs = cmds.listAttr(chld, ud = True)
        if udAttrs:
            for udAttr in udAttrs:
                customAttrLs.append(udAttr)

    # Remove repeated items.
    customAttrs = list(set(customAttrLs))

    joinStr = " -attr "
    melCode = "-attr " + joinStr.join(customAttrs)

    print melCode
    return melCode


def setUpMdlShot():
    '''
    Set up modeling environment.
    '''

    # Start new shot
    confirmSaveCurScene()

    # Working unit
    cmds.currentUnit(linear = 'centimeter')
    cmds.currentUnit(time = 'ntsc')

    # set time slider and current frame to 1
    cmds.playbackOptions(min = 1)
    cmds.currentTime(1)

    # Make group hierarchy
    pipeHier()

    cmds.select(cl = True)


def pipeHier():
    '''
    Build group hierarchy structure proper to pipeline.
    '''

    # Create pipeline hierarchy structure.
    hierDic = { 'wip_GRP': ['base_body_grp', 'light_cam_grp'],
                'root': ['geometry'],
                'geometry': ['lod03_GRP', 'dyn_hair_fur_grp'],
                'lod03_GRP': ['facial_grp', 'body_grp', 'cloth_grp', 'misc_grp', 'place3dTexture_grp', 'polyHair_grp'],
                'dyn_hair_fur_grp': ['renderHair_grp', 'hairSystem_grp', 'input_crv_grp', 'output_crv_grp']}

    for item in hierDic.keys():
        if not cmds.objExists(item):
            cmds.createNode('transform', n = item)
        for child in hierDic[item]:
            if not cmds.objExists(child):
                cmds.createNode('transform', n = child, p = item)
            else:
                cmds.parent(child, item)


def confirmSaveCurScene():
    '''
    Show confirm window to user for asking to save current scene before start a new scene.
    '''

    if cmds.file(q = True, amf = True):
        answer = cmds.confirmDialog(title = 'Save', message = '현재 열려있는 Scene를 저장 하시겠습니가?', button = ['Yes', 'No'], defaultButton = 'Yes', cancelButton = 'No', dismissString = 'No')

        if answer == 'Yes':
            tak_misc_b1.saveCWD()
            cmds.file(force = True, new = True)
        else:
            cmds.file(force = True, new = True)


def chkFrameRangeWithShotCam(shotCamLsStr):
    '''
    Chek timeline frame range fit to shot camera.
    '''

    if shotCamLsStr:
        shotCamLs = shotCamLsStr.split(',')

        matchObj = re.match(r'.*_(\d*)_(\d*)', shotCamLs[0])

        if matchObj:
            camStart = int(matchObj.group(1))
            camEnd = int(matchObj.group(2))

            timelineStart = int(cmds.playbackOptions(q = True, min = True))
            timelineEnd = int(cmds.playbackOptions(q = True, max = True))

            if camStart == timelineStart and camEnd == timelineEnd:
                return 1
            else:
                answer = cmds.confirmDialog(title = 'Confirm Dialog',
                                            message = '카메라의 프레임 정보와 타임라인의 프레임 레인지가 일치하지 않습니다.\n계속 진행 하시겠습니까?',
                                            button = ['Yes', 'No'], defaultButton = 'No', cancelButton = 'No', dismissString = 'No')

                if answer == 'Yes':
                    return 1
                else:
                    return 0
        else:
            cmds.confirmDialog(title = 'Warning', message = '카메라에서 프레임 정보를 찾을 수 없습니다.\n"카메라이름_시작프레임_종료프레임" 형식으로 이름을 변경하고 다시 시도해 보세요.')
            return 0
    else:
        return 1


def niceNameForDeliver(prjName, fileName):
    """
    Retrun nice file name for delivery to santa.
    Pattern: 'ProjectName_AssetName_DataType_r###.mb'
    """

    print prjName, fileName

    # Rename depend on type.
    if 'mdl' in fileName:
        niceName = re.sub(r"(\w+?)(_.+_)(mdl)(.+)", r"%s\2mdl\4" %prjName, fileName)
    elif 'rig' in fileName:
        niceName = re.sub(r"(\w+?)(_.+_)(rig_lod03)(.+)", r"%s\2rig\4" %prjName, fileName)

    return niceName


def renameAsset(oriAssetFldrPath):
    # Prompt to user whether backup
    answer = cmds.confirmDialog(
            title='Warning',
            message='Do you want to back up for safty?\nBackup folder is placed in project folder.',
            button=['Yes', 'No'],
            defaultButton='Yes',
            cancelButton='No',
            dismissString='No')
    if answer == 'Yes':
        backupFldrPath = re.sub(r'(.+?/.+?/)(.*)', r'\1backup/\2', oriAssetFldrPath)
        if os.path.exists(backupFldrPath):
            shutil.rmtree(backupFldrPath, ignore_errors = True)
        shutil.copytree(oriAssetFldrPath, backupFldrPath, ignore = shutil.ignore_patterns('*.db', 'tmp*'))
    else:
        pass

    print 'Back up process is done.'

    oriAssetName = oriAssetFldrPath.rsplit('/')[-2]

    result = cmds.promptDialog(
            title='Rename Asset',
            message='Enter New Name: ',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel',
            text = oriAssetName)

    if result == 'OK':
        newAssetName = cmds.promptDialog(query = True, text = True)

        # Rename folders and files
        for path,dirs,files in os.walk(oriAssetFldrPath, topdown=False):
            for oriDir in dirs:
                # Rename folder name.
                if oriAssetName in oriDir:
                    newDirName = re.sub(oriAssetName, newAssetName, oriDir)
                    os.rename(path + '\\' + oriDir, path + '\\' + newDirName)

            for oriFile in files:
                if '.ma' in oriFile or '.xgen' in oriFile and not 'swatches' in oriFile:
                    filePath = path + '\\' + oriFile
                    fR = open(filePath, 'r')
                    contents = fR.read()
                    fR.close()

                    print "> Modifying... %s" %oriFile
                    try:
                        newFileContents = re.sub(oriAssetName, newAssetName, unicode(contents, "cp949")) # Convert 'cp949 ascii' format to 'unicode' format.
                    except:
                        print 'Check whether the file "%s" is binary. Skipped this file.' %oriFile
                        continue
                    fW = open(filePath, 'w')
                    fW.write(newFileContents.encode("cp949")) # Convert 'unicode' foramt to 'cp949 ascii' format
                    fW.close()

                # Rename file name.
                if oriAssetName in oriFile:
                    newFileName = re.sub(oriAssetName, newAssetName, oriFile)
                    os.rename(path + '\\' + oriFile, path + '\\' + newFileName)

        newAssetFldrPath = re.sub(oriAssetName, newAssetName, oriAssetFldrPath)
        try:
            os.rename(oriAssetFldrPath, newAssetFldrPath)
        except:
            cmds.confirmDialog(title = 'Error', message = '하위폴더 또는 파일이 다른 프로그램에서 열려 있어 에셋 폴더의 이름을 바꿀 수 없습니다.\n열려있는 폴더/프로그램을 종료하고 시도해 보십시오.', button = ['OK'])
            assetFldr = re.match(r'(.+)/.+/', oriAssetFldrPath).group(1)
            os.startfile(assetFldr) # Open asset folder.

    else:
        pass


def sortByBufferLength(fileNameStr):
    """ Sorting filenames by buffer length """
    fileNames = fileNameStr.split(',')
    fileNames.sort(key=lambda item: len(fileNameIntoBuffer(item)))
    return fileNames

def fileNameIntoBuffer(fileName):
    if '_cam_' in fileName:
        matObj = re.match(r'(.+?)_(.+?)_(.+?)_(.+?)_(.+?)_(.+)_(r\d+)\.\w+', fileName) # sequence_shotName_component_layer_assetType_camName_releaseNumber.ext
    else:
        matObj = re.match(r'(.+?)_(.+?)_(.+?)_(.+?)_(.+?)_(.+)_(\d+)_(r\d+)\.\w+', fileName) # sequence_shotName_component_layer_assetType_assetName_Numbering_releaseNumber.ext
    if not matObj:
        matObj = re.match(r'(.+?)_(.+?)_(.+?)_(.+?)_(.+?)_(.+)_(\d+)_(.+)_(r\d+)\.\w+', fileName) # sequence_shotName_component_layer_assetType_assetName_Numbering_xgenDescriptionName_releaseNumber.ext

    if matObj:
        joinStr = ','
        melBufferStr = joinStr.join(matObj.groups())
        return melBufferStr


def parsingAssetFileName(baseName):
    srchObj = re.search(r'(.+?)_(.+)_(rig|mdl|lod)_(.+)', baseName)

    if srchObj:
        joinStr = ','
        melBufferStr = joinStr.join(srchObj.groups())
        return melBufferStr


def parseRplcAstName(baseName):
    srchObj = re.search(r'(.+?)_(.+)_(\d+)', baseName)
    if srchObj:
        joinStr = ','
        melBufferStr = joinStr.join(srchObj.groups())
        return melBufferStr


def parseAstNamespace(baseName):
    melBufferStr = ''
    
    srchObj = re.search(r'(.+)_(\d{3})', baseName)
    if srchObj:
        joinStr = ','
        melBufferStr = joinStr.join(srchObj.groups())
    
    return melBufferStr


def chkTexNameConflict():
    fileNodes = cmds.ls(type = 'file')

    fileTexPathLs = []
    for fileNode in fileNodes:
        if cmds.nodeType(fileNode) == "mentalrayIblShape":
            filePathAttrName = fileNode + ".texture"
        else:
            filePathAttrName = fileNode + ".fileTextureName"
        fileTexPath = cmds.getAttr(filePathAttrName)
        fileTexPathLs.append(fileTexPath)

    fileNameLs = []
    for filePath in list(set(fileTexPathLs)):
        fileName = os.path.basename(filePath)
        fileNameLs.append(fileName)

    nameConflictTexLs = []
    for i in xrange(len(fileNameLs)):
        checker = fileNameLs[i]
        examineeLs = fileNameLs[i+1:]
        for examinee in examineeLs:
            if checker != examinee:
                pass
            elif checker == examinee:
                nameConflictTexLs.append(checker)

    if nameConflictTexLs:
        joinStr = '\n'
        dividerStr = '=' * 30
        nameConflictTexStr = dividerStr + '\n' + joinStr.join(nameConflictTexLs) + '\n' + dividerStr
        cmds.confirmDialog(title = "Warning!", message = """The following textures\n%s\nare exists in multiple location.\nClean up texture file node trying following manner.\nPoint to right path(latest version) or rename conflicting file.""" %nameConflictTexStr)
        return 0
    else:
        return 1


def chkSameFilePathNode(filePath):
    '''
    Check whether exists the file node that having same file path.
    If exists on other words given file path exists more than 1 then return input filePath.
    If not exists on other words the same file name exists in another location, rename and return it.
    '''

    fileNodes = cmds.ls(type = 'file')

    fileTexPathLs = []
    for fileNode in fileNodes:
        if cmds.nodeType(fileNode) == "mentalrayIblShape":
            filePathAttrName = fileNode + ".texture"
        else:
            filePathAttrName = fileNode + ".fileTextureName"
        fileTexPath = cmds.getAttr(filePathAttrName)
        fileTexPathLs.append(fileTexPath)

    numOfPath = fileTexPathLs.count(filePath)

    if numOfPath > 1:
        return filePath
    elif numOfPath == 1:
        newFilePath = filePath.rsplit('.', 1)[0] + '_ver02.' + filePath.rsplit('.', 1)[-1]
        return newFilePath


def findLatestFile(curPath, trgPath):
    '''
    Compair given two pathes and return latest file path.
    '''

    curPathTime = os.path.getmtime(curPath)
    trgPathTime = os.path.getmtime(trgPath)

    if curPathTime > trgPathTime:
        return curPath
    else:
        return trgPath


def fileCopyHandleUI(srcPath, trgPath):
    '''
    Handling when file exists in target directory.
    '''

    cmds.window('fileCopyHandleWin', title = 'Warning', mmb = False, mxb = False)
    cmds.columnLayout('mainColLo', adj = True)

    cmds.text(label = 'The file \'%s\' is already exists in target directory \'%s\'.' %(fileName, trgPath))
    cmds.text(label = 'Source File Modified Time: %d.%d.%d %d:%d       Target File Modified Time: %d.%d.%d %d:%d' %(srcYear, srcMonth, srcHour, srcMinute, trgYear, trgMonth, trgHour, trgMinute))
    cmds.text(label = 'Source File Size: %f       Target File Size: %f' %(srcSize, trgSize))

    cmds.rowColumnLayout('openFldrRowColLo', numberObColumns = 2)
    cmds.button(label = 'Open Source Folder')
    cmds.button(label = 'Open Target Folder')

    cmds.setParent('..')
    cmds.separator(style = 'in', h = 5)

    cmds.checkbox('assignAllFileChkBox', label = 'Assign to All Files: ')
    cmds.rowColumnLayout('decisionRowColLo', numberObColumns = 2)
    cmds.button(label = 'Overwrite')
    cmds.button(label = 'Skip')

    cmds.window('fileCopyHandleWin', e = True, w = 100, h = 100)
    cmds.showWindow('fileCopyHandleWin')


def lod03AllShpVisOn(nameSpace):
    '''
    When target shape visibility is off blendshape will raise error.
    So before export alembic cache, lod03_GRP's all shapes needed visibility set to on.
    '''

    cacheMdlShapeLs = cmds.ls(nameSpace + ':lod03_GRP', dag = True, type = 'mesh', ni = True)

    for cacheMdlShape in cacheMdlShapeLs:
        cmds.setAttr('%s.visibility' %cacheMdlShape, 1)


def removeConstraintInLod03GRP(nameSpace):
    '''
    Move constraint nodes in lod03_GRP to the world to match render model hierarchy.
    '''

    cnstOnCacheGeo = cmds.ls(nameSpace + ':lod03_GRP', dag = True, type = 'constraint')
    if cnstOnCacheGeo:
        try:
            cmds.parent(cnstOnCacheGeo, world = True)
        except:
            pass


def cleanUpRefMdlUI(*args):
    winName = 'cleanUpRefMdlWin'

    if cmds.window(winName, exists = True):
        cmds.deleteUI(winName)

    cmds.window(winName, title = 'Clean Up Referenced Render Model', mnb = False, mxb = False)

    cmds.columnLayout(adj = True)
    cmds.optionMenu('refNamespace', label = 'Namespace: ')
    refNodeList = cmds.ls(references = True)
    for refNode in refNodeList:
        try:
            namespace = cmds.referenceQuery(refNode, namespace = True, shortName = True)
            if 'abc' in namespace or 'cam' in namespace:
                pass
            else:
                cmds.menuItem(label = namespace)
        except:
            pass

    cmds.button(label = 'Clean Up!', h = 50, c = cleanUpRefMdl)

    cmds.window(winName, e = True, w = 100, h = 50)
    cmds.showWindow(winName)


def cleanUpRefMdl(*args):
    '''
    Clean up refereced render model before update cache.
    '''

    mdlNamespace = cmds.optionMenu('refNamespace', q = True, v = True)

    delRenMdlBs(mdlNamespace)

    disableParallelBlender(mdlNamespace)

    # delInterMediObj(mdlNamespace)


def delRenMdlBs(nameSpace):
    '''
    Delete all blendshape nodes(include parallelBlender) assigned to render model.
    This is needed before reconnect alembic cache to render model using new blendshape.
    '''

    renMdlBsLs = []

    renMdlMeshLs = cmds.ls(nameSpace + ':lod03_GRP', dag = True, type = 'mesh', ni = True)

    for mesh in renMdlMeshLs:
        bsLs = cmds.ls(cmds.listHistory(mesh), type = 'blendShape')

        if bsLs:
            for bs in bsLs:
                renMdlBsLs.append(bs)

    for bsNode in list(set(renMdlBsLs)):
        if (nameSpace + ':') in bsNode:
            continue
        else:
            try:
                cmds.setAttr('%s.envelope' %bsNode, 0)
                cmds.delete(bsNode)
            except:
                pass


def disableParallelBlender(nameSpace):
    '''
    Prallel blend shape node overwrite under blendshape node.
    So set envelope to 0.
    '''

    renMdlParallelLs = []

    renMdlMeshLs = cmds.ls(nameSpace + ':lod03_GRP', dag = True, type = 'mesh', ni = True)

    for mesh in renMdlMeshLs:
        bsLs = cmds.ls(cmds.listHistory(mesh), type = 'blendShape')

        if bsLs:
            for bs in bsLs:
                if 'parallelBlender' in bs:
                    renMdlParallelLs.append(bs)

    for parallelBlender in list(set(renMdlParallelLs)):
        if (nameSpace + ':') in parallelBlender:
            continue
        else:
            try:
                cmds.setAttr('%s.envelope' %parallelBlender, 0)
                cmds.delete(parallelBlender)
            except:
                pass


def delInterMediObj(nameSpace):
    '''
    When deformer assigned to referenced model it has two case.
    
    In first case 'absolute name + Deformed' shape is created and referenced shape is be intermediateObject.
    In this case deformed shape should be delete and turn off intermediateObject attribute of referenced shape.
    
    Another case referenced shape is keep and 'absolute name + Orig' shape is created as intermediateObject.
    In this case when Orig shape deleted lost material information assigned to face.
    '''

    cmds.select(nameSpace + ':lod03_GRP', hi = True, r = True)
    renMdlShpList = cmds.ls(sl = True, dag = True, s = True, long = True)

    for shp in renMdlShpList:
        if 'Orig' in shp:
            try:
                cmds.delete(shp)
            except:
                pass
        elif 'Deformed' in shp:
            cmds.delete(shp)
            print 'Deformed object "%s" is deleted.' %shp
        elif 'Parallel' in shp:
            cmds.delete(shp)
            print 'Parallel object "%s" is deleted.' %shp
        else:
            intmResult = cmds.getAttr('%s.intermediateObject' %(shp))
            if intmResult and ':' in shp:
                cmds.setAttr('%s.intermediateObject' %(shp), 0)
            elif intmResult:
                cmds.delete(shp)
                print 'Intermediate object "%s" is deleted.' %shp


def isLatestAsset(nameSpace):
    '''
    If the asset in the scene is latest asset, return 1.
    '''

    curAstFileName = cmds.referenceQuery((nameSpace + 'RN'), f = True)

    # release directory
    try:
        releaseDir = re.search(r'\w:/.*/release', curAstFileName).group()
    except:
        return 0

    # current release version
    currentRelease = re.search(r'r\d\d\d', curAstFileName).group()

    # get latest release version
    releaseList = os.listdir(releaseDir)
    latestRelease = max(releaseList)

    if currentRelease != latestRelease:
        return 0
    else:
        return 1


def deleteHistory(historyPath):
    '''
    Delete selected history.
    '''

    # Confirm delete.
    answer = cmds.confirmDialog(title = 'Caution!', message = 'Are you sure?\nThis is not undoable!\nBackup directory is placed in project directory.', button = ['Yes', 'No'], defaultButton = 'Yes', cancelButton = 'No', dismissString = 'No')

    if answer == 'Yes':
        # Back up history folder
        histoyBackupFldr = re.sub(r'(.+?/.+?/)(.*)', r'\1backup/\2', historyPath)
        if os.path.exists(histoyBackupFldr):
            shutil.rmtree(histoyBackupFldr, ignore_errors = True)
        shutil.copytree(historyPath, histoyBackupFldr, ignore = shutil.ignore_patterns('*.db', 'tmp*'))

        # Back up info folder
        componentPath = '/'.join(historyPath.rsplit('/')[:-3])
        infoFldr = componentPath + '/_info/'
        infoBackupFldr = re.sub(r'(.+?/.+?/)(.*)', r'\1backup/\2', infoFldr)

        if os.path.exists(infoBackupFldr):
            shutil.rmtree(infoBackupFldr, ignore_errors = True)
        shutil.copytree(infoFldr, infoBackupFldr, ignore = shutil.ignore_patterns('*.db', 'tmp*'))

        # Modify xml information file.
        infoXmlPath = glob.glob(componentPath + '/_info/*.xml')[0]
        publishedType = historyPath.rsplit('/')[-3]
        ver = historyPath.rsplit('/')[-2]
        verNum = re.search(r'\D(\d+)', ver).group(1)

        fR = open(infoXmlPath, 'r')
        xmlCntns = fR.read()
        fR.close()

        historyInfoLs = re.findall(r'\t<note>.*?</note>\n', xmlCntns, re.DOTALL)
        for historyInfo in historyInfoLs:
            result = re.search(r'.*%s.*%s.*' %(publishedType, verNum), historyInfo, re.DOTALL)
            if result:
                newXmlCntns = xmlCntns.replace(historyInfo, '')
            else:
                pass

        fW = open(infoXmlPath, 'w')
        fW.write(newXmlCntns)
        fW.close()

        # Delete history folder.
        shutil.rmtree(historyPath, ignore_errors = True)

        cmds.confirmDialog(title = "Confirm", message = "삭제가 완료되었습니다.\n UI Refresh를 위해서 Component를 클릭해 주세요.")

    else:
        return



def isReleasedWithLatestVer(releaseInfo):
    '''
    This function do checking for pulished animation scene.
    Whether released animation cache is come from with latest asset.
    '''

    relDirPath = releaseInfo.split(',')[0]
    selRelFileLs = releaseInfo.split(',')[1:]

    devFilePath = getDevFilePath(relDirPath)

    if os.path.isfile(devFilePath):
        fR = open(devFilePath, 'r')
        contents = fR.read()
        fR.close()

        refInfos = re.search(r'//Codeset: 949\n(.*?)\nfile -r -ns', contents, re.DOTALL).group(1).split(';\n')

        while 'develop' in str(refInfos):
            for refInfo in refInfos:
                if 'develop' in refInfo:
                    refInfos.remove(refInfo)

        noLatestAssetLs = getNolatestAssets(refInfos, selRelFileLs)

        if noLatestAssetLs:
            noLatestAssetStr = '\n'.join(noLatestAssetLs)
            cmds.confirmDialog(title = 'Notice', message = '\n%s\n\n위의 에셋들이 최신버전이 아닌 상태로 릴리즈 되었습니다.\n랜더모델이 캐쉬를 따라가지 않을 수 있습니다.\n문제 발생 시 애니메이션팀에 에셋 업데이트 및 릴리즈를 요청해 주세요.' %noLatestAssetStr, button = ['OK'])
    else:
        pass

def getDevFilePath(relDirPath):
    """
    Extract develop scene file path from .xml file
    
    Parameters:
        relDirPath(str): e.g) 'p:/1701_Animal/5.Shot/EP001/S010-C004/EP001_S010-C004_maya/scenes/ani/master/release/r004'
    
    Returns:
        devFilePath(str): Animation scene file path that work in progress
    """
    publishedType = relDirPath.rsplit('/')[-2]
    print 'publishedType: ', publishedType
    ver = relDirPath.rsplit('/')[-1]
    # print 'ver: ', ver
    verNum = re.search(r'\D(\d+)', ver).group(1)
    print 'verNum: ', verNum

    layerPath = '/'.join(relDirPath.rsplit('/')[:-2])
    # print 'layerPath: ', layerPath
    infoXmlPath = glob.glob(layerPath + '/_info/*.xml')

    with open(infoXmlPath[0], 'r') as f:
        xmlCntns = f.read()

    print 'xmlCntns: ', xmlCntns
    
    historyInfoLs = re.findall(r'\t<note>.*?</note>\n', xmlCntns, re.DOTALL)
    print 'historyInfoLs: ', historyInfoLs
    devFilePath = ''
    for historyInfo in historyInfoLs:
        result = re.search(r'.*<event>%s</event>.*<version>%s</version>.*' % (publishedType, verNum), historyInfo, re.DOTALL)
        if result:
            print 'historyInfo: ', historyInfo
            devSceneFileName = re.search(r'.*\.ma', historyInfo).group()
            print 'devSceneFileName: ', devSceneFileName
            devVer = re.search(r'_(v\d{3})_', devSceneFileName).group(1)
            print 'devVer: ', devVer
            devFilePath = layerPath + '/develop/%s/' %devVer + devSceneFileName
        else:
            pass

    return devFilePath

def getReferenceInfo(maFilePath):
    """
    Extract reference information used in maya scene file

    Parameters:
        maFilePath(str): Maya ascii scene file path
    
    Returns:
        refInfoDict(dict): {'assetName': {'nameSpace': '', 'referenceNode': '', 'filePath': ''}, 
                            'assetName': {...}...}
    """
    refInfoDict = {}

    with open(maFilePath, 'r') as f:
        contents = f.read()

    # extract referenceDepthInfo of assets from the contents
    refInfos = re.search(r'//Codeset: 949\n(.*?)\nfile -r -ns', contents, re.DOTALL).group(1).split(';\n')

    # remove develop in refInfos
    while 'develop' in str(refInfos):
        for refInfo in refInfos:
            if 'develop' in refInfo:
                refInfos.remove(refInfo)

    for refInfo in refInfos:
        matchObj = re.search(r'-ns "(.+?)" .+? "(.+?)".+"(.+?)"', refInfo, re.DOTALL)
        
        tmpDict = {}
        tmpDict['namespace'] = matchObj.group(1)
        tmpDict['referenceNode'] = matchObj.group(2)
        tmpDict['filePath'] = matchObj.group(3)
        
        assetName = matchObj.group(1).rsplit('_', 1)[0]
        refInfoDict[assetName] = tmpDict
    
    return refInfoDict

def getFilePathUsedInAni(relDirPath, assetName):
    """
    Parameters:
        relDirPath(str): Path that contain release file
        assetName(str): Name of the asset
    
    Returns:
        filePath(str): Asset file path that used in animation shot
    """
    filePath = None

    devFilePath = getDevFilePath(relDirPath)
    print 'devFilePath: ', devFilePath
    refInfoDict = getReferenceInfo(devFilePath)
    # pprint.pprint(refInfoDict)
    filePath = refInfoDict.get(assetName).get('filePath')

    return filePath



def getNolatestAssets(refInfos, selRelFileLs):
    noLatestAssetLs = []

    for refInfo in refInfos:
        if 'develop' in refInfo:
            continue

        # Get latest release version.
        try:
            releaseDir = re.search(r'\w:/.*/release', refInfo).group()
        except:
            return False
        releaseList = os.listdir(releaseDir)
        latestRelease = max(releaseList)

        currentRelease = re.search(r'r\d\d\d', refInfo).group()

        # Get asset name.
        match = re.search(r'-ns "(.*)_\d+"', refInfo, re.DOTALL)
        if match:
            assetName = match.group(1)

        if currentRelease != latestRelease and assetName in str(selRelFileLs):
            noLatestAssetLs.append(assetName)

    return noLatestAssetLs


def setPivotToWsOrigin():
    trsfLs = ['root', 'geometry', 'lod03_GRP']
    for trsf in trsfLs:
        cmds.xform(trsf, rp = [0, 0, 0], ws = True)
        cmds.xform(trsf, sp = [0, 0, 0], ws = True)





def chkFaceAssignedMat():
    '''
    Separate face by material main function.
    '''

    selObjLs = cmds.ls(sl = True)

    selGeoFaceMatLs = faceAssignedMat(selObjLs)

    faceAssignedMatGeoLs = []

    for mat in selGeoFaceMatLs:
        cmds.hyperShade(objects = mat)
        matAssignGeoLs = cmds.ls(sl = True)
        faces = cmds.filterExpand(matAssignGeoLs, ex = False, sm = 34)

        if faces:
            matAssignedFaceShapes = getShapesFromFaces(faces)

            for faceShp in matAssignedFaceShapes:
                trsf = cmds.listRelatives(faceShp, p = True)
                if trsf[0] in selObjLs:
                    faceAssignedMatGeoLs.extend(trsf)

    if faceAssignedMatGeoLs:
        cmds.select(faceAssignedMatGeoLs, r = True)
        cmds.confirmDialog(title = 'Error', message = '선택된 오브젝트들이 Face 단위로 Material이 적용 되어 있습니다.\n오브젝트 단위로 Material을 적용하고 릴리즈를 재시도 해 주세요.')
        cmds.error()


def faceAssignedMat(geoLs):
    matLs = []
    for geo in geoLs:
        shapeName = cmds.listRelatives(geo, ni = True, path = True, s = True)

        if shapeName:
            sgName = cmds.listConnections('%s.instObjGroups.objectGroups' %shapeName[0], d = True, type = "shadingEngine")
            matName = cmds.ls(cmds.listConnections(sgName), materials = True)
            matLs.extend(matName)

    return list(set(matLs))


def getShapesFromFaces(faces):
    faceShpLs = []
    for face in faces:
        faceShpLs.extend(cmds.listRelatives(face, p = True, path = True))
    return list(set(faceShpLs))


def getLatestVer(dirPath):
    """
    Get latest version in given directory path.
    """

    vers = os.listdir(dirPath)
    if vers:
        return max(vers)
    else:
        vers = 'r001'
        return vers


def getRelatedRenMdlPath(nameSpace, version):
    curAstFileName = cmds.referenceQuery((nameSpace + 'RN'), f = True)

    # release directory
    try:
        releaseDir = re.search(r'\w:/.*/release', curAstFileName).group()
    except:
        return False

    relatedRenMdlDir = releaseDir + '/' + version + '/'
    if not os.path.exists(relatedRenMdlDir):
        OpenMaya.MGlobal.displayError('"%s" path is not exists. Please check the asset\'s namespace and referencing file path in develop file.' %relatedRenMdlDir)
        return
    relatedRenMdlPath = os.path.normcase(glob.glob(relatedRenMdlDir + '*.ma')[0])

    return relatedRenMdlPath


def releaseMdlVerUI(namespace, version):
    # Get model versions of release directory
    curAstFileName = cmds.referenceQuery((namespace + 'RN'), f = True)
    try:
        releaseDir = re.search(r'\w:/.*/release', curAstFileName).group()
    except:
        raise IOError('No such directory: %s' % releaseDir)
    releaseMdlVers = os.listdir(releaseDir)

    # UI
    winName = 'relMdlVerWin'

    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)

    cmds.window(winName, title='Select Released Model')
    cmds.columnLayout()
    radioBtnCollection = cmds.radioCollection()
    populateReleaseMdlVerUI(releaseMdlVers, version)
    cmds.button(label='Load', c=partial(loadSelVer, radioBtnCollection, releaseDir, namespace, winName))
    cmds.showWindow()


def populateReleaseMdlVerUI(releaseMdlVers, version):
    for mdlVer in releaseMdlVers:
        radioBtn = cmds.radioButton(label=mdlVer)
        if mdlVer == version:
            cmds.radioButton(radioBtn, e=True, select=True)


def loadSelVer(radioBtnCollection, releaseDir, namespace, winName, *args):
    selRadioBtn = cmds.radioCollection(radioBtnCollection, q=True, select=True)
    selMdlVer = cmds.radioButton(selRadioBtn, q=True, label=True)

    selRenMdlDir = releaseDir + '/' + selMdlVer + '/'
    if not os.path.exists(selRenMdlDir):
        OpenMaya.MGlobal.displayError('"%s" path is not exists. Please check the asset\'s namespace and referencing file path in develop file.' %selRenMdlDir)
        return
    selRenMdlPath = os.path.normcase(glob.glob(selRenMdlDir + '*.ma')[0])

    cmds.file(selRenMdlPath, loadReference=namespace+'RN', type='mayaAscii', options='v=0')

    cmds.deleteUI(winName)


def parseRefFilePath(refFilePath):
    # filePath format is 'P:/1705_ZRO/4.Asset/set/bg_oohiroma/mdl/develop/v005/set_bg_oohiroma_mdl_v005_ymjoo.ma'
    searchObj = re.search(r'(.*Asset)/(.+)/(.+)/(.+)/(.+)/(.+)/(.+)', refFilePath)
    if searchObj:
        return searchObj.groups()


def checkAssetVersion():
    refNodes = [node for node in pm.ls(type='reference') if 'RN' in node.name()]

    developAssets = []
    noLatestAssets = []

    for refNode in refNodes:
        refFile = refNode.referenceFile()
        
        if not refFile:
            refNode.unlock()
            pm.delete(refNode)
            continue
        
        assetDir, assetType, assetName, component, publishType, version, fileName = parseRefFilePath(refFile.path)

        if publishType == 'develop':
            developAssets.append(refNode.name())
        else:
            releaseDir = os.path.join(assetDir, assetType, assetName, component, publishType)
            latestReleaseVer = getLatestVer(releaseDir)
            if version < latestReleaseVer:
                noLatestAssets.append(refNode.name())

    if developAssets or noLatestAssets:
        result = cmds.confirmDialog(
                title='Warning',
                message='최신 릴리즈를 사용하지 않은 에셋이 있습니다.\n에셋 업데이트가 필요 합니다.\n릴리즈를 계속 진행 하시겠습니까?',
                button=['Yes', 'No'],
                defaultButton='Yes',
                cancelButton='No',
                dismissString='No')

        if result == 'Yes':
            return 1
        else:
            return 0

    return 1



def copyAssetUsedInScene(mayaFilePath, targetDirectoryPath):
    """
    Copy referenced assets in maya scene file

    Parameters:
        mayaFilePath(str): Maya ascii scene file path that contain reference
        targetDirectoryPath(str): Destination directory path
    """
    refInfoDict = getReferenceInfo(mayaFilePath)
    for assetName, assetInfoDict in refInfoDict.items():
        src = os.path.dirname(assetInfoDict.get('filePath'))
        dst = re.sub(r'\w:/', targetDirectoryPath, src)
        if not os.path.exists(dst):
            shutil.copytree(src, dst)


def sendAsset(src, dst):
    dst = re.sub(r'\w:/', dst, src)
    if not os.path.exists(dst):
        shutil.copytree(src, dst)


def sendLatestAsset(releaseDirPath, targetDirPath):
    if os.path.exists(releaseDirPath):
        latestReleaseDirPath = '%s/%s' % (releaseDirPath, getLatestVer(releaseDirPath))
        if os.path.exists(latestReleaseDirPath):
            sendAsset(latestReleaseDirPath, targetDirPath)
        else:
            logger.warning("'%s' is not exists" % latestReleaseDirPath)
    else:
        logger.warning("'%s' is not exists" % releaseDirPath)


def refreshAssetNameList(searchStr):
    """
    Refresh `assetNameList` textScrollList widget by searching string
    
    Parameters:
        searchStr(str): String that user input
    """

    # Get asset directory path through UI
    curProjPath = cmds.textFieldButtonGrp('currentProjPath', q=True, text=True)
    selAssetType = cmds.textScrollList('assetTypeList', q=True, selectItem=True)[0]
    assetDirPath = os.path.join(curProjPath, '4.Asset', selAssetType)
    
    # Delete items in assetNameList before fill in searching result
    if cmds.textScrollList('assetNameList', q=True, allItems=True):
        cmds.textScrollList('assetNameList', e=True, removeAll=True)
     
    # Get only directories in the asset directory path
    dirsInAssetDir = [dir for dir in os.listdir(assetDirPath) if os.path.isdir(os.path.join(assetDirPath, dir))]
    
    # Filter valid directory. Valid directory contains 'direcotryName_def.xml'
    assetDirs = [dir for dir in dirsInAssetDir if dir+'_def.xml' in os.listdir(os.path.join(assetDirPath, dir))]
    
    for asset in assetDirs:
        if re.search(searchStr, asset, re.IGNORECASE):
            cmds.textScrollList('assetNameList', e=True, append=asset)


def refreshShotList(searchStr):
    """
    Refresh `shotList` textScrollList widget by searching string
    
    Parameters:
        searchStr(str): String that user input
    """

    # Get asset directory path through UI
    curProjPath = cmds.textFieldButtonGrp('currentProjPath', q=True, text=True)
    selSequence = cmds.textScrollList('seqList', q=True, selectItem=True)[0]
    shotDirPath = os.path.join(curProjPath, '5.Shot', selSequence)
    
    # Delete items in assetNameList before fill in searching result
    if cmds.textScrollList('shotList', q=True, allItems=True):
        cmds.textScrollList('shotList', e=True, removeAll=True)
     
    # Get only directories in the asset directory path
    dirsInShotDir = [dir for dir in os.listdir(shotDirPath) if os.path.isdir(os.path.join(shotDirPath, dir))]
    
    # Filter valid directory. Valid directory contains 'direcotryName_def.xml'
    shotDirs = [dir for dir in dirsInShotDir if dir+'_def.xml' in os.listdir(os.path.join(shotDirPath, dir))]
    
    for shot in shotDirs:
        if re.search(searchStr, shot, re.IGNORECASE):
            cmds.textScrollList('shotList', e=True, append=shot)


def enableVrayFileGamma():
    """Add vray file gamma attribute and set to sRGB for all file textures"""
    if pm.pluginInfo('vrayformaya', q=True, loaded=True):
        allTextures =  pm.ls(type='file')
        for tex in allTextures:
            pm.mel.eval('vray addAttributesFromGroup {0} vray_file_gamma 1;'.format(str(tex)))
            pm.setAttr('{0}.vrayFileColorSpace'.format(str(tex)), 2)


def setGammaCorrectedColor():
    """Create gamma node and connect to color attribute for all shaders"""
    allMaterials = pm.ls(mat=True)
    for mat in allMaterials:
        colorAttr = 'outColor' if isinstance(mat, pm.nodetypes.SurfaceShader) else 'color'
        if not pm.objExists(mat.attr(colorAttr)):
            print '{} has no attribute {}, skip this.'.format(str(mat), mat.attr(colorAttr))
            continue
        colorInput = mat.attr(colorAttr).connections(d=False)
        if not colorInput:
            color = mat.attr(colorAttr).get()
            gammaNode = pm.createNode('gammaCorrect')
            gammaNode.value.set(*color)
            gammaNode.gamma.set(0.454, 0.454, 0.454)
            try:
                gammaNode.outValue >> mat.attr(colorAttr)
            except:
                pass


def setPreviewDivisionLevelToDefault():
    """Set display and render subdivision preview to default value"""
    meshes = pm.ls(type='mesh')
    for mesh in meshes:
        if not mesh.smoothLevel.connections():
            mesh.smoothLevel.set(2)


def replaceStringForAssetFiles(assetDir, search, replace):
    """
    Search and replace given string for asset files in assetDir

    Parameters:
        assetDir(str): Asset directory path
        search(str): A word for searching
        replace(str): A word to replace
    """

    # Make a list of '.ma' files
    maFiles = []
    for path, dirs, files in os.walk(assetDir):
        for file in files:
            if os.path.splitext(file)[-1] == '.ma':
                maFiles.append(os.path.join(path, file))
    
    if maFiles:
        pm.progressWindow(title=assetDir.split('/')[-1], maxValue=len(maFiles), isInterruptable=True, status='')
        for maFile in maFiles:
            if pm.progressWindow(query=True, isCancelled=True):
                break
            pm.progressWindow(edit=True, progress=maFiles.index(maFile)+1, status=os.path.basename(maFile))

            with open(maFile, 'r') as f:
                newContents = f.read().replace(search, replace)
            with open(maFile, 'w') as f:
                f.write(newContents)

    pm.progressWindow(endProgress=True)


def removeUnusedPluginRequires(assetDir):
    maFiles = []
    for path, dirs, files in os.walk(assetDir):
        for file in files:
            if os.path.splitext(file)[-1] == '.ma':
                maFiles.append(os.path.join(path, file))

    if maFiles:
        pm.progressWindow(title=assetDir.split('/')[-1], maxValue=len(maFiles), isInterruptable=True, status='')
        for file in maFiles:
            if pm.progressWindow(query=True, isCancelled=True):
                break
            pm.progressWindow(edit=True, progress=maFiles.index(file)+1, status=os.path.basename(file))

            with open(file, 'r') as f:
                fileContents = f.read()

            modifiedFileContents = re.sub(r'requires ".+;', '', fileContents)

            with open(file, 'w') as f:
                f.write(modifiedFileContents)
    
    pm.progressWindow(endProgress=True)


def archiveAsset(assetDir, keepVerNum):
    assetFiles = os.listdir(assetDir)
    components = ['mdl', 'rig']
    historyTypes = ['develop', 'release']

    for component in components:
        if component in assetFiles:
            for historyType in historyTypes:
                versions = os.listdir(os.path.join(assetDir, component, historyType))
                versions.sort(reverse=True)
                for version in versions:
                    versionDir = os.path.join(assetDir, component, historyType, version).replace('\\', '/')
                    allFiles = getAllFiles(versionDir)
                        
                    # Correct texture path
                    for file in allFiles:
                        if file.endswith('.ma'):
                            copyWrongPointedTexture(file)
                        
                    if versions.index(version) < int(keepVerNum):
                        continue

                    # Zip files
                    zipFileName = os.path.join(assetDir, component, historyType, version, version)+'.zip'
                    with zipfile.ZipFile(zipFileName, 'w') as zip:
                        for file in allFiles:
                            if file == zipFileName:
                                os.remove(file)
                            zip.write(file, file.split(version, 1)[-1], zipfile.ZIP_DEFLATED)
                            
                            os.remove(file)
                    
                    # Remove directories
                    allDirs = [os.path.join(versionDir, dir) for dir in os.listdir(versionDir) if os.path.isdir(os.path.join(versionDir, dir))]
                    for dir in allDirs:
                        shutil.rmtree(dir)

def getAllFiles(dir):
    allFiles = []
    for path, dirs, files in os.walk(dir):
        for file in files:
            allFiles.append(os.path.join(path, file).replace('\\', '/'))

    return allFiles

def unZip(versionDir):
    zipFiles = glob.glob('%s/*.zip' %versionDir)
    for zipFile in zipFiles:
        with zipfile.ZipFile(zipFile, 'r') as zip:
            zip.extractall(os.path.dirname(zipFile))
        os.remove(zipFile)

def copyWrongPointedTexture(filePath):
    # Read file contents
    with open(filePath, 'r') as f:
        contents = f.read()
        f.seek(0)
        fileLines = f.readlines()

    # Find texture pathes
    fileNodeLines = [line for line in fileLines if '.ftn' in line]
    if fileNodeLines:
        for line in fileNodeLines:
            texturePath = re.search(r'.* "(.*)";', line).group(1)
            textureVerPath = re.search(r'(.*\w\d\d\d).*', texturePath).group(1)
            fileVerPath = os.path.dirname(filePath)

            # Compare with version texture directory path
            if os.path.normcase(textureVerPath) != os.path.normcase(fileVerPath):
                print os.path.normcase(textureVerPath)
                print os.path.normcase(fileVerPath)
                print "Texture path '{0}' is pointing another version of asset".format(texturePath)
                if os.path.exists(texturePath):
                    correctedPath = texturePath.replace(textureVerPath, fileVerPath)
                    print "Copy '{0}' to '{1}', and fix path".format(texturePath, correctedPath)
                    shutil.copy(texturePath, correctedPath)
                    contents = contents.replace(texturePath, correctedPath)
                else:
                    "Texture '{0}' is not exists".format(texturePath)

    with open(filePath, 'w') as f:
        f.write(contents)




def copyLatestAssetsUI(targetDir):
    winName = 'copyLatestAssetsWin'
    if pm.window(winName, q=True, exists=True):
        pm.deleteUI(winName)
    win = pm.window(winName, title='Copy Latest Assets', mnb=False, mxb=False)
    
    pm.columnLayout(adj=True)
    pm.textFieldButtonGrp('srcDir', label='Source Directory: ', buttonLabel='...', bc=populateSrcAssetsTxtScrLs)
    pm.textScrollList('srcAssetsTxtScrLs', allowMultiSelection=True)
    pm.button(label='Copy', c=lambda *args: copyLatestVer(targetDir))

    pm.window(win, e=True, w=10, h=10)
    pm.showWindow(win)

def populateSrcAssetsTxtScrLs():
    tak_lib_b1.loadPath('srcDir')

    srcDir = pm.textFieldButtonGrp('srcDir', q=True, text=True)
    for dir in [dir for dir in os.listdir(srcDir) if os.path.isdir(os.path.join(srcDir, dir))]:
        pm.textScrollList('srcAssetsTxtScrLs', e=True, append=dir)

def copyLatestVer(targetDir):
    sourceDir = pm.textFieldButtonGrp('srcDir', q=True, text=True)
    selAssets = pm.textScrollList('srcAssetsTxtScrLs', q=True, selectItem=True)

    historyType = ['develop', 'release']
    for asset in selAssets:
        for path, dirs, files in os.walk(os.path.join(sourceDir, asset)):
            for dir in dirs:
                if dir in historyType:
                    # Copy latest version directory
                    latestVer = getLatestVer(os.path.join(path, dir))
                    srcLatestVer = os.path.join(path, dir, latestVer)
                    trgLatestVer = srcLatestVer.replace(sourceDir, targetDir)
                    shutil.copytree(srcLatestVer, trgLatestVer)

                    # Copy '_info' folder and '.xml' file
                    items = [item for item in os.listdir(path) if not item in historyType]
                    for item in items:
                        srcPath = os.path.join(path, item)
                        trgPath = srcPath.replace(sourceDir, targetDir)
                        if os.path.exists(trgPath):
                            continue
                        if os.path.isdir(srcPath):
                            shutil.copytree(srcPath, srcPath.replace(sourceDir, targetDir))
                        else:
                            shutil.copy(srcPath, srcPath.replace(sourceDir, targetDir))

                    # Copy files in asset directory
                    assetDir = os.path.join(sourceDir, asset)
                    files = [item for item in os.listdir(assetDir) if not os.path.isdir(os.path.join(assetDir, item))]
                    for file in files:
                      srcFilePath = os.path.join(assetDir, file)
                      shutil.copy(srcFilePath, srcFilePath.replace(sourceDir, targetDir))


def sendSeqToDelivery(seqDir, trgDir):
    shotDirs = os.listdir(seqDir)
    
    historyType = ['develop', 'release']

    for shotDir in shotDirs:
        for path, dirs, files in os.walk(os.path.join(seqDir, shotDir)):
            for dir in dirs:
                if dir in historyType:
                    # Copy latest version directory
                    latestVer = getLatestVer(os.path.join(path, dir))
                    srcLatestVer = os.path.join(path, dir, latestVer)
                    trgLatestVer = "\\" + srcLatestVer.replace(seqDir, trgDir).replace('\\scenes\\ani\\master', '')
                    shutil.copytree(srcLatestVer, trgLatestVer)
                    print trgLatestVer