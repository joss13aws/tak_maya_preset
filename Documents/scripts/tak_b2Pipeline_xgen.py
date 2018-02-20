"""
Author: Sang-tak Lee
Contact: chst27@gmail.com
Created: 06/23/2017
Updated: 10/18/2017

Description:
XGen utils for b2Pipeline.
"""


import pymel.core as pm
import os
import re
import shutil


def submitXGen(pathes):
    """
    Used in b2PipelineAsset.mel to copy xgen data to server

    Args:
        pathes: "Source scene path, Target scene path"

    Returns:
        None
    """
    xgCols = pm.ls(type="xgmPalette")

    if xgCols:
        for xgCol in xgCols:
            srcSceneFilePath = pathes.split(",")[0]
            trgSceneFilePath = pathes.split(",")[1]

            # Copy xgen file and collection directory
            trgXgFilePath, trgXgColDirPath = copyXgenFiles(
                xgCol, srcSceneFilePath, trgSceneFilePath)

            # Edit xgen file and maya scene file contents
            editFiles(xgCol, trgSceneFilePath, trgXgFilePath, trgXgColDirPath)
    else:
        return


def copyXgenFiles(xgCol, srcSceneFilePath, trgSceneFilePath):
    """
    Copy .xgen file and xgen collection directory.
    """

    srcSceneDirPath = os.path.dirname(srcSceneFilePath)
    trgSceneDirPath = os.path.dirname(trgSceneFilePath)

    srcXgFilePath = srcSceneDirPath + "/" + \
        os.path.basename(srcSceneFilePath).split(".")[
            0] + "__" + xgCol + ".xgen"
    srcXgColDirPath = getXgenColDirPath(srcXgFilePath)

    trgXgFilePath = trgSceneDirPath + "/" + \
        os.path.basename(trgSceneFilePath).split(".")[
            0] + "__" + xgCol + ".xgen"
    trgXgColDirPath = trgSceneDirPath + "/xgen" + \
        "/collections/" + os.path.basename(srcXgColDirPath)

    if not os.path.exists(trgXgColDirPath):
        shutil.copytree(srcXgColDirPath, trgXgColDirPath)
    if not os.path.exists(trgXgFilePath):
        shutil.copy(srcXgFilePath, trgXgFilePath)

    return trgXgFilePath, trgXgColDirPath


def getXgenColDirPath(srcXgFilePath):
    """
    Return xgen collection directory path.
    """

    srcXgColDirPath = ""

    f = file(srcXgFilePath, "r")
    contents = f.read()
    f.close()

    xgDataPath = re.search(r"xgDataPath\s+(.*)\n", contents)
    xgProjectPath = re.search(r"xgProjectPath\s+(.*)\n", contents)

    if "${PROJECT}" in xgDataPath.group(1) and xgProjectPath:
        srcXgColDirPath = re.sub(
            r"\${PROJECT}", xgProjectPath.group(1), xgDataPath.group(1))
    else:
        srcXgColDirPath = xgDataPath.group(1)

    return srcXgColDirPath


def editFiles(xgCol, trgSceneFilePath, trgXgFilePath, trgXgColDirPath):
    """
    Change xgen file name in maya scene file and collection directory path in xgen file.
    """

    editSceneFile(trgSceneFilePath, xgCol, trgXgFilePath)

    editXgenFile(trgXgFilePath, trgXgColDirPath)


def editSceneFile(trgSceneFilePath, xgCol, trgXgFilePath):
    with open(trgSceneFilePath, "r") as f:
        sceneContents = f.read()

    editedSceneContents = re.sub(r'("\.xfn" -type "string"\s+).*%s.xgen"(;\n)' % xgCol, r'\1"{0}"\2'.format(os.path.basename(trgXgFilePath)), sceneContents)

    with open(trgSceneFilePath, "w") as f:
        f.write(editedSceneContents)


def editXgenFile(trgXgFilePath, trgXgColDirPath):
    with open(trgXgFilePath, 'r') as f:
        xgContents = f.read()

    editedXgContents = re.sub(r"(xgDataPath\s+).*(\n)", r"\1{0}\2".format(trgXgColDirPath), xgContents)

    with open(trgXgFilePath, "w") as f:
        f.write(editedXgContents)


def downRenameXgenFile(targetFilePath):
    """
    Renaming when download xgen file through b2Pipeline.
    """

    newName = ""

    if ".xgen" in targetFilePath:
        targetFilePath = targetFilePath.split("_checkedOut")[0] + ".xgen"
        newName = targetFilePath.split("__", 1)[0] + "_checkedOut" + "__" + targetFilePath.split("__", 1)[-1]
    else:
        newName = targetFilePath
    print ">>> Downloaded XGen File Name: " + newName
    return newName


def downEditMayaFile(filePath, type):
    """
    Edit maya scene file for pointing correct xgen file path.
    """

    if ".ma" in filePath:
        f = file(filePath, "r")
        contents = f.read()
        f.close()

        if type == "asset":
            editedContents = re.sub(r'("\.xfn" -type "string"\s+)(.*)(__.*;\n)', r'\1\2_checkedOut\3', contents)
        elif type == "shot":
            editedContents = re.sub(r'("xgFileName" .*?)(__.*")', r'\1_checkedOut\2', contents)

        f = file(filePath, "w")
        f.write(editedContents)
        f.close()


if __name__ == "__main__":
    submitXGen()
