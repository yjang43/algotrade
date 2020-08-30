from PyQt5.QtWidgets import QSizePolicy, QListWidget


class NotificationLog(QListWidget):
    def __init__(self, file_path):
        super().__init__()
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSizePolicy(size_policy)
        self.load_notification(file_path)

    def load_notification(self, file_path):
        notification_list = list()
        with open(file_path) as f:
            for line in f:
                notification_list.insert(0, line.rstrip())
        self.addItems(notification_list)


