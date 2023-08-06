import os


class File(object):
    def __init__(self, file_name, contents, binary=False):
        self.file_name = file_name
        self.contents = contents
        self.write_mode = 'wb' if binary else 'w'

    def write(self, d):
        if not os.path.exists(d):
            os.makedirs(d)

        with open(os.path.join(d, self.file_name), self.write_mode) as f:
            f.write(self.contents)
