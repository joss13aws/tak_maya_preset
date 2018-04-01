"""
Author: LEE SANGTAK
Contact: chst27@gmail.com
"""

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import xgenm
import os

XGEN_ICON_PATH = r'C:\Program Files\Autodesk\Maya2018\plug-ins\xgen\icons'

class XGenManager(QMainWindow):
    def __init__(self):
        super(XGenManager, self).__init__()

        self.setWindowTitle('XGen Manager')

        self.buildUI()

    def buildUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QVBoxLayout()
        centralWidget.setLayout(mainLayout)

        # Guide tools section
        guideToolGrpBox = QGroupBox('Guide Tools')
        mainLayout.addWidget(guideToolGrpBox)

        guideLayout = QGridLayout()
        guideToolGrpBox.setLayout(guideLayout)

        numOfCVsLabel = QLabel('Number of CVs: ')
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

        collections = xgenm.palettes()
        for collection in collections:
            descriptions = xgenm.descriptions(collection)
            for description in descriptions:
                descriptionWidget = DescriptionWidget(description)
                scrollLayout.addWidget(descriptionWidget)


class DescriptionWidget(QWidget):
    def __init__(self, description):
        super(DescriptionWidget, self).__init__()
        self.description = description

        self.buildUI()

    def buildUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        descriptionGrpBox = QGroupBox(self.description)
        layout.addWidget(descriptionGrpBox)

        descriptionGrpBoxLayout = QVBoxLayout()
        descriptionGrpBox.setLayout(descriptionGrpBoxLayout)

        # Description toolbar
        descriptionToolBar = QToolBar()
        descriptionToolBar.setIconSize(QSize(32, 32))
        descriptionGrpBoxLayout.addWidget(descriptionToolBar)

        guideDisplayToggleAction = QAction(QIcon(os.path.join(XGEN_ICON_PATH, 'xgToggleGuide.png')), u'Guide Display Toggle', self)
        descriptionToolBar.addAction(guideDisplayToggleAction)

        xgPreviewRefreshAction = QAction(QIcon(os.path.join(XGEN_ICON_PATH, 'xgPreviewRefresh.png')), u'Preview Refresh', self)
        descriptionToolBar.addAction(xgPreviewRefreshAction)

        xgPreviewClearAction = QAction(QIcon(os.path.join(XGEN_ICON_PATH, 'xgPreviewClear.png')), u'Preview Clear', self)
        descriptionToolBar.addAction(xgPreviewClearAction)

        # Density widget
        densityLayout = QHBoxLayout()
        descriptionGrpBoxLayout.addLayout(densityLayout)

        densityLabel = QLabel('Density')
        densityLayout.addWidget(densityLabel)

        densitySpinBox = QDoubleSpinBox()
        densitySpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        densityLayout.addWidget(densitySpinBox)

        densitySlider = QSlider()
        densitySlider.setOrientation(Qt.Horizontal)
        densityLayout.addWidget(densitySlider)

        # Modifier CV Count widget
        modifierCVCountLayout = QHBoxLayout()
        descriptionGrpBoxLayout.addLayout(modifierCVCountLayout)

        modifierCVCountLabel = QLabel('Modifier CV Count')
        modifierCVCountLayout.addWidget(modifierCVCountLabel)

        modifierCVCountSpinBox = QSpinBox()
        modifierCVCountSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        modifierCVCountLayout.addWidget(modifierCVCountSpinBox)

        # Connect widgets
        densitySlider.valueChanged.connect(densitySpinBox.setValue)
        densitySpinBox.valueChanged.connect(densitySlider.setValue)


    @staticmethod
    def createIconButton(image):
        pixmap = QPixmap(os.path.join(XGEN_ICON_PATH, image))
        icon = QIcon(pixmap)
        button = QPushButton()
        button.setIcon(icon)
        button.setIconSize(pixmap.rect().size())

        return button


