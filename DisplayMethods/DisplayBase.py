class DisplayBase:
    def __init__(self):
        self.w, self.h = (0, 0)

    def draw(self, x, y):
        pass

    def get_size(self):
        return self.w, self.h
