class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.map = []
        for y in range(0, h):
            self.map.append([])
            for x in range(0, w):
                self.map[y].append('.')

    def __contains__(self, pos):
        return 0 <= pos.y <= len(self.map[0]) and 0 <= pos.x <= len(self.map[0])

    def __getitem__(self, key):
        return self.map[key]

    def __len__(self):
        return len(self.map)