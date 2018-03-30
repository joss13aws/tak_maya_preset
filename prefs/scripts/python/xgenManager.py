"""
Author: SANGTAK LEE
Contact: chst27@gmail.com
"""

from PySide2.QtWidgets import *


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
        descriptionList = QListWidget()
        mainLayout.addWidget(descriptionList)

        for i in range(5):
            descriptionList.addItem(QListWidgetItem(str(i)))


class DescriptionWidget(QWidget):
    pass
