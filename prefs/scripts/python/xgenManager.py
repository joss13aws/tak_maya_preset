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

XGEN_ICON_PATH = r'C:\Program Files\Autodesk\Maya2018\plug-ins\xgen\icons'
ICON_PATH = r'D:\Tak\Program_Presets\tak_maya_preset\prefs\icons'


def getMayaMainWin():
    mayaWinPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaWinPtr), QWidget)


class XGenManager(QMainWindow):
    def __init__(self):
        super(XGenManager, self).__init__()
        self.setWindowTitle('XGen Manager')
        self.setParent(getMayaMainWin())
        self.setWindowFlags(Qt.Tool)

        self.buildUI()
        self.setMinimumWidth(250)

    def buildUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QVBoxLayout()
        centralWidget.setLayout(mainLayout)

        # Guide tools section
        guideToolGrpBox = QGroupBox('Guide Tools')
        mainLayout.addWidget(guideToolGrpBox)

        guideMainLayout = QVBoxLayout()
        guideToolGrpBox.setLayout(guideMainLayout)

        guideToolBar = QToolBar()
        guideToolBar.setIconSize(QSize(32, 32))
        guideMainLayout.addWidget(guideToolBar, 0, 1)

        addGuideAction = QAction(QIcon(os.path.join(XGEN_ICON_PATH, 'xgGuideContext.png')), 'Add or Move Guides', self)
        guideToolBar.addAction(addGuideAction)

        sculptGuideAction = QAction(QIcon(os.path.join(XGEN_ICON_PATH, 'fx_sculpt.png')), 'Sculpt Guides', self)
        guideToolBar.addAction(sculptGuideAction)

        convertToPolyAction = QAction(QIcon(os.path.join(XGEN_ICON_PATH, 'xgConvertToPoly.png')), 'Convert Primitives to Polygons', self)
        guideToolBar.addAction(convertToPolyAction)

        guideLayout = QGridLayout()
        guideMainLayout.addLayout(guideLayout)

        numOfCVsLabel = QLabel('Number of CP')
        guideLayout.addWidget(numOfCVsLabel, 0, 0)

        minusButton = QPushButton('-')
        guideLayout.addWidget(minusButton, 0, 1)

        plusButton = QPushButton('+')
        guideLayout.addWidget(plusButton, 0, 2)

        normalizeButton = QPushButton('Normalize')
        guideLayout.addWidget(normalizeButton, 1, 0)

        bakeButton = QPushButton('Bake')
        guideLayout.addWidget(bakeButton, 1, 1, 1, 2)

        # Description section
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        mainLayout.addWidget(scrollArea)

        scrollWidget = QWidget()
        scrollWidget.setContentsMargins(0, 0, 0, 0)
        scrollArea.setWidget(scrollWidget)

        scrollLayout = QVBoxLayout()
        scrollWidget.setLayout(scrollLayout)

        collections = xg.palettes()
        for collection in collections:
            descriptions = xg.descriptions(collection)
            for description in descriptions:
                descriptionWidget = DescriptionWidget(collection, description)
                scrollLayout.addWidget(descriptionWidget)

        # Connections
        addGuideAction.triggered.connect(lambda: pm.mel.eval('XgGuideTool;'))
        sculptGuideAction.triggered.connect(lambda: xgui.createDescriptionEditor(False).guideSculptContext(False))
        convertToPolyAction.triggered.connect(XGenManager.showWarningDialog)
        minusButton.clicked.connect(lambda: XGenManager.editNumGuideCP('decrease'))
        plusButton.clicked.connect(lambda: XGenManager.editNumGuideCP('increase'))
        normalizeButton.clicked.connect(lambda: pm.mel.eval('xgmNormalizeGuides();'))
        bakeButton.clicked.connect(lambda: pm.mel.eval('xgmBakeGuideVertices;'))

    @staticmethod
    def showWarningDialog():
        warningDialog = QMessageBox()
        warningDialog.setWindowTitle('Warning')
        warningDialog.setIcon(QMessageBox.Warning)
        warningDialog.setText('Primitives are converted to polygons!\nAre you sure?')
        warningDialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = warningDialog.exec_()

        if result == QMessageBox.Ok:
            cpp.convertPrimToPolygon(False)

    @staticmethod
    def editNumGuideCP(command):
        guides = pm.selected()
        minCPCount = 5
        for guide in guides:
            currentNumOfCPs = guide.getShape().controlPoints.numElements()
            addingValue = 2 if command == 'increase' else -2
            val = max(minCPCount, currentNumOfCPs+addingValue)
            pm.mel.eval('xgmChangeCVCount({0});'.format(val))
        pm.select(guides, r=True)


class DescriptionWidget(QWidget):
    def __init__(self, collection, description):
        super(DescriptionWidget, self).__init__()
        self.collection = collection
        self.description = description
        self.de = xgg.DescriptionEditor

        self.renderableButton = None
        self.renderableIcon = None
        self.disRenderableIcon = None

        self.setDefaultSettings()
        self.buildUI()

        self.de.refresh('Description')

    def buildUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        descriptionGrpBox = QGroupBox(self.description)
        layout.addWidget(descriptionGrpBox)

        descriptionGrpBoxLayout = QVBoxLayout()
        descriptionGrpBox.setLayout(descriptionGrpBoxLayout)

        # Description Toolbar
        descriptionToolBar = QToolBar()
        descriptionToolBar.setIconSize(QSize(32, 32))
        descriptionGrpBoxLayout.addWidget(descriptionToolBar)

        guideDisplayToggleAction = QAction(QIcon(os.path.join(XGEN_ICON_PATH, 'xgToggleGuide.png')), 'Guide Display Toggle', self)
        descriptionToolBar.addAction(guideDisplayToggleAction)

        xgPreviewRefreshAction = QAction(QIcon(os.path.join(XGEN_ICON_PATH, 'xgPreviewRefresh.png')), 'Refresh Primitive', self)
        descriptionToolBar.addAction(xgPreviewRefreshAction)

        xgPreviewClearAction = QAction(QIcon(os.path.join(XGEN_ICON_PATH, 'xgPreviewClear.png')), 'Clear Primitive', self)
        descriptionToolBar.addAction(xgPreviewClearAction)

        # Renderable Button
        self.renderableButton = QPushButton()

        renderablePixmap = QPixmap(os.path.join(ICON_PATH, 'renderable.png'))
        self.renderableIcon = QIcon(renderablePixmap)
        disRenderablePixmap = QPixmap(os.path.join(ICON_PATH, 'disRenderable.png'))
        self.disRenderableIcon = QIcon(disRenderablePixmap)

        self.renderableButton.setIcon(self.renderableIcon)
        self.renderableButton.setIconSize(renderablePixmap.rect().size())
        self.renderableButton.setCheckable(True)
        self.renderableButton.setStyleSheet("background-color: white")
        descriptionGrpBoxLayout.addWidget(self.renderableButton)

        # Density Widget
        densityLayout = QHBoxLayout()
        descriptionGrpBoxLayout.addLayout(densityLayout)

        densityLabel = QLabel('Density')
        densityLayout.addWidget(densityLabel)

        densityValue = xg.getAttr("density", self.collection, self.description, "RandomGenerator")

        densityLineEdit = QLineEdit()
        densityLineEdit.setText(densityValue)
        densityLineEditValidator = QDoubleValidator(0.000, 3000.000, 6, densityLineEdit)
        densityLineEdit.setValidator(densityLineEditValidator)
        densityLayout.addWidget(densityLineEdit)

        # Connect Widgets
        guideDisplayToggleAction.triggered.connect(lambda: xg.toggleGuideDisplay(self.description))
        xgPreviewRefreshAction.triggered.connect(lambda: pm.mel.eval('xgmPreview -progress {"%s"};' % self.description))
        xgPreviewClearAction.triggered.connect(lambda: pm.mel.eval('xgmPreview -clean {"%s"};' % self.description))
        densityLineEdit.returnPressed.connect(lambda: self.setDensity(densityLineEdit.text()))
        self.renderableButton.toggled.connect(lambda checked: self.renderableButtonToggledSlot(checked))

    def renderableButtonToggledSlot(self, checked):
        if checked:
            self.renderableButton.setIcon(self.disRenderableIcon)
            xg.setAttr("percent", xge.prepForAttribute(str(0)), self.collection, self.description, "RendermanRenderer")
        else:
            self.renderableButton.setIcon(self.renderableIcon)
            xg.setAttr("percent", xge.prepForAttribute(str(100)), self.collection, self.description, "RendermanRenderer")
        self.de.refresh('Description')

    def setDensity(self, val):
        xg.setAttr("density", xge.prepForAttribute(str(val)), self.collection, self.description, "RandomGenerator")
        pm.mel.eval('xgmPreview -progress {"%s"};' % self.description)
        self.de.refresh('Description')

    def setDefaultSettings(self):
        xg.setAttr("inCameraOnly", xge.prepForAttribute(str(False)), self.collection, self.description, "GLRenderer")
        xg.setAttr("splineSegments", xge.prepForAttribute(str(1)), self.collection, self.description, "GLRenderer")
        xg.setAttr("renderer", xge.prepForAttribute('Arnold Renderer'), self.collection, self.description, "RendermanRenderer")
        xg.setAttr("custom__arnold_rendermode", xge.prepForAttribute(str(1)), self.collection, self.description, "RendermanRenderer")
        xg.setAttr("custom__arnold_minPixelWidth", xge.prepForAttribute(str(0.5)), self.collection, self.description, "RendermanRenderer")
