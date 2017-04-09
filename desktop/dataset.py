import collections


class DataSet(collections.Iterable, list):

    data = collections.deque()
    index = 0
    max = 3

    def __add__(self, other):
        self.append(other)

    def append(self, item):


        if len(self.data) >= self.max:
            self.data.popleft()

        self.data.append(item)

    def __next__(self):

        if self.index < len(self.data):

            ret = self.data[self.index]
            self.index += 1
            return ret

        raise StopIteration

    def __getitem__(self, i):
        return self.data[i]

    def __iter__(self):
        self.index = 0
        return self

    def setMax(self, max):
        self.max = max

    def __len__(self):
        return len(self.data)

