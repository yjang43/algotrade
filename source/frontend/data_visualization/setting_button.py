from PyQt5.QtWidgets import *


class SettingButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self.setting_popup)

    def setting_popup(self):
        setting_dialog = self.SettingBox()
        setting_dialog.exec()

    class SettingBox(QDialog):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            layout = QGridLayout()
            self.setLayout(layout)
            self.setFixedSize(200, 300)
            self.setWindowTitle('settings')
            l1 = QLabel("graph type")
            l2 = QLabel("interval")
            layout.addWidget(l1)
            layout.addWidget(l2)

