import os

class DbImport:

    def __init__(self, filename, config):
        self.config = config
        self.filename = filename

        base = os.path.basename(self.filename)
        parts = os.path.splitext(base)
        self.file_name = parts[0]

    def run(self):
        pass