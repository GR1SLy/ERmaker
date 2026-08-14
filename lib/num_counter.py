class NumCounter:
    path = "lib/count.count"

    @classmethod
    def read(cls) -> int:
        with open(cls.path, 'r') as f:
            return int(f.read())

    @classmethod
    def increase(cls):
        k = 0
        with open(cls.path, 'r') as f:
            k = int(f.read())
        k += 1
        with open(cls.path, 'w') as f:
            f.write(str(k))

    @classmethod
    def zeroize(cls):
        with open(cls.path, 'w') as f:
            f.write(str(1))