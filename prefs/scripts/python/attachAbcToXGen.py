"""
Author: LEE SANGTAK
Contact: chst27@gmail.com
"""

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import xgenm as xg
import xgenm.xgGlobal as xgg
import xgenm.XgExternalAPI as xge
import xgenm.ui as xgui
import xgenm.xmaya.xgmConvertPrimToPolygon as cpp
import pymel.core as pm
import maya.OpenMayaUI as omui

from shiboken2 import wrapInstance
import os


def getMayaMainWin():
    mayaWinPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaWinPtr), QWidget)


class AttachAbcToXGen(QMainWindow):
    # Properties
    toolName = 'Attach Alembic to XGen'

    # Initialize object
    def __init__(self):
        super(AttachAbcToXGen, self).__init__()
        self.setWindowTitle(AttachAbcToXGen.toolName)
        self.setParent(getMayaMainWin())
        self.setWindowFlags(Qt.Tool)

        self.buildUI()

    def buildUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QVBoxLayout()
        centralWidget.setLayout(mainLayout)

        # Namespace widget
        namespaceWidget = QWidget()
        namespaceLayout = QHBoxLayout()
        namespaceWidget.setLayout(namespaceLayout)

        namespaceLabel = QLabel('Namespace: ')
        namespaceLayout.addWidget(namespaceLabel)

        namespaceLineEdit = QLineEdit()
        namespaceLayout.addWidget(namespaceLineEdit)

        mainLayout.addWidget(namespaceWidget)

        # XGen file path widget
        xgFilePathWidget = QWidget()
        xgFilePathLayout = QHBoxLayout()
        xgFilePathWidget.setLayout(xgFilePathLayout)

        xgFilePathLabel = QLabel('XGen File Path: ')
        xgFilePathLayout.addWidget(xgFilePathLabel)

        xgFilePathLineEdit = QLineEdit()
        xgFilePathLayout.addWidget(xgFilePathLineEdit)

        xgFilePathBrowsBtn = QPushButton('Brows...')
        xgFilePathLayout.addWidget(xgFilePathBrowsBtn)

        mainLayout.addWidget(xgFilePathWidget)

        # Cache widgets
        cacheGrpBox = QGroupBox('Caches')
        cacheGrpBoxLayout = QVBoxLayout()
        cacheGrpBox.setLayout(cacheGrpBoxLayout)

        # Scalp cache widgets
        scalpCacheLayout = QHBoxLayout()
        scalpCacheLabel = QLabel('Scalp Cache Path: ')
        scalpCacheLayout.addWidget(scalpCacheLabel)

        scalpCacheLineEdit = QLineEdit()
        scalpCacheLayout.addWidget(scalpCacheLineEdit)

        scalpCacheBrowsBtn = QPushButton('Brows...')
        scalpCacheLayout.addWidget(scalpCacheBrowsBtn)

        cacheGrpBoxLayout.addLayout(scalpCacheLayout)

        # Curve cache widgets
        curveCacheLabel = QLabel('Curve Caches Path: ')
        cacheGrpBoxLayout.addWidget(curveCacheLabel)

        curveCacheBrowsBtn = QPushButton('Brows...')
        cacheGrpBoxLayout.addWidget(curveCacheBrowsBtn)

        curveCacheList = QListWidget()
        cacheGrpBoxLayout.addWidget(curveCacheList)

        mainLayout.addWidget(cacheGrpBox)


