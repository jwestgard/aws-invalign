class Inventory():

    def __init__(self, path):

        self.invpath = path
        self.filename = os.path.basename(invpath)
        self.lines = []

        with open(path) as handle:
            for n, line in enumerate(handle.readlines(), 1):
                md5, path = line.strip().split(None, 1)
                file_signature = (md5, path, self.invpath, n)
                self.lines.append(file_signature)
