"""Read data from file."""


class LoadTheData:
    def __init__(self, file):
        with open(file) as f:
            area = f.readline().split(',')
            self.a, self.b, self.c, self.d = [float(x) for x in area]
            print(self.a, self.b, self.c, self.d)
            """and so on ..."""