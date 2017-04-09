from PyQt5.QtCore import QSettings


class Settings:

    instance = None
    inner = None

    def __init__(self):
        super().__init__()
        self.inner = QSettings("desktop\settings.ini", QSettings.IniFormat)

    @staticmethod
    def getInstance():
        if Settings.instance is None:
            Settings.instance = Settings()
        return Settings.instance

    def read(self, key):
        return self.inner.value(key, None)

    def write(self, key, value):
        self.inner.setValue(key, value)

class SettingsUtil:

    @staticmethod
    def writeList(settings, data, dataName):

        settings.setValue(dataName + "_name", dataName)
        settings.setValue(dataName + "_len", len(data))

        for i in range(len(data)):
            settings.setValue(dataName + "_" + str(i), data[i])


    @staticmethod
    def readList(settings, name):

        data = []

        name = settings.value(name + "_name", "")
        if len(name) == 0: return data

        length = int(settings.value(name + "_len"))
        for i in range(length):
            data.append(settings.value(name + "_" + str(i)))

        return data
