import os
import re
import shutil

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
                    if versions.index(version) < int(keepVerNum):
                        continue
                    else:
                        versionDir = os.path.join(assetDir, component, historyType, version)
                        # Zip files
                        allFiles = getAllFiles(versionDir)
                        for file in allFiles:
                            # Copy wrong pointed texture and fix path
                            if file.endswith('.ma'):
                                copyWrongPointedTexture(file)

def getAllFiles(dir):
    allFiles = []
    for path, dirs, files in os.walk(dir):
        for file in files:
            allFiles.append(os.path.join(path, file))

    return allFiles

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
                print "Texture path '{0}' is pointing another version of asset".format(texturePath)
                if os.path.exists(texturePath):
                    correctedPath = texturePath.replace(textureVerPath, fileVerPath)
                    print "Copy '{0}' to '{1}'".format(texturePath, correctedPath)
                    shutil.copy(texturePath, correctedPath)
                    print "And redirecting to current asset version"
                    contents = contents.replace(texturePath, correctedPath)
                else:
                    "Texture '{0}' is not exists".format(texturePath)

    with open(filePath, 'w') as f:
        f.write(contents)
