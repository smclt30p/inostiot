import collections


class DataSet(collections.deque):

    max = 0

    def append(self, item):

        if len(self) >= self.max:
            self.popleft()

        super().append(item)

    def setMax(self, max):
        self.max = max

