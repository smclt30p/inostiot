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
        value =  self.inner.value(key, None)

        if value is None: return None

        if "false" in value:
            return False
        if "true" in value:
            return True

        return value


    def write(self, key, value):
        self.inner.setValue(key, value)

    def writeList(self, data, dataName):

        self.write(dataName + "_name", dataName)
        self.write(dataName + "_len", len(data))

        for i in range(len(data)):
            self.write(dataName + "_" + str(i), data[i])

    def readList(self, name):

        data = []

        name = self.read(name + "_name")
        if name is None: return data

        length = int(self.read(name + "_len"))
        for i in range(length):
            data.append(self.read(name + "_" + str(i)))

        return data


