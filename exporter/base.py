from functools import reduce


class base():
    def __init__(self, objects):
        self.buffer = []
        self.objects = objects
        self.mongo_objects = list(
            filter(lambda m: m['is_mongo_object'], self.objects))
        self.class_keys = list(
            map(lambda m: m['classname'], self.objects))
        self.class_list = reduce(self.remap, self.objects, {})

    def remap(self, object_map, object):
        object_map[object['classname']] = object
        return object_map

    def push(self, text):
        self.buffer.append(text)

    def flush(self):
        content = "\n".join(self.buffer)
        self.buffer = []
        return content

    def save(self, content, filename):
        with open(filename, 'w') as f:
            f.write(content)
