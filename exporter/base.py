class base():
    def __init__(self):
        self.buffer = []

    def push(self, text):
        self.buffer.append(text)

    def flush(self):
        content = "\n".join(self.buffer)
        self.buffer = []
        return content
