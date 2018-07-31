from pprint import pprint
import re


class model():
    def __init__(self, file):
        self.success = False
        self.objs = []
        self.parse(file)

    def objects(self):
        return self.objs

    def parse(self, file):
        lines = self.readlines(file)
        obj = {'variables': [], '$dirty': False}
        state = ''
        summary = []

        for line in lines:
            if self.is_namespace(line):
                if obj['$dirty']:
                    self.objs.append(obj)
                obj['namespace'] = self.get_namespace(line)
                obj['classname'] = ''
                obj['is_mongo_object'] = False
                obj['$dirty'] = False
                state = 'namespace'
                summary = []
            elif self.is_class(line):
                if obj['$dirty']:
                    self.objs.append(obj)
                obj['is_mongo_object'] = False
                obj['$dirty'] = True
                obj['classname'] = self.get_classname(line)
                state = 'class'
                summary = []
            elif self.is_swagger_summary_open(line):
                if state == 'class':
                    state = 'swagger'
            elif self.is_swagger_summary_close(line):
                if state == 'swagger':
                    state = 'class'
            elif self.is_swagger_summary(line):
                if state == 'swagger':
                    summary.append(self.get_swagger_text(line))
            elif self.is_var(line):
                if state == 'class':
                    vars = self.get_variable(line)
                    if len(summary) > 0:
                        vars = vars + (" ".join(summary), )
                    else:
                        vars = vars + ("", )
                    summary = []
                    obj['variables'].append(vars)
            elif self.is_mongo_id(line):
                obj['is_mongo_object'] = True

        if obj['$dirty']:
            self.objs.append(obj)

        self.success = len(self.objs) > 0

    def ok(self):
        return self.success

    def readlines(self, file):
        with open(file, encoding="utf8") as f:
            content = f.read()
        content = content.replace("\r\n", "\n")
        lines = list(map(lambda l: l.strip(), content.split("\n")))
        return lines

    def is_namespace(self, line):
        return re.search("namespace\\s+[A-Za-z][A-Za-z0-9_\\.]+", line) != None

    def get_namespace(self, line):
        match = re.search("^namespace\\s+([A-Za-z][A-Za-z0-9_\\.]+)", line)
        return match.group(1)

    def is_class(self, line):
        return re.search("class\\s+[A-Za-z][A-Za-z0-9_\\.]+", line) != None

    def get_classname(self, line):
        match = re.search("class\\s+([A-Za-z][A-Za-z0-9_\\.]+)", line)
        return match.group(1)

    def is_var(self, line):
        return re.search(
            "(private\\s+|public\\s+|^)[A-Za-z0-9_\\.<>]+\\s+[A-Za-z0-9_]+(\\s*{|$)", line)

    def get_variable(self, line):
        match = re.search(
            "(private\\s+|public\\s+|^)([A-Za-z0-9_\\.<>]+)\\s+([A-Za-z0-9_]+)(\\s*{|$)", line)
        return (match.group(2), match.group(3))

    def is_swagger_summary_open(self, line):
        return re.search("///\\s+<summary>", line)

    def is_swagger_summary_close(self, line):
        return re.search("///\\s+</summary>", line)

    def is_swagger_summary(self, line):
        return re.search("///\\s+(.*)", line)

    def get_swagger_text(self, line):
        match = re.search("///\\s+(.*)", line)
        return match.group(1).strip()

    def is_mongo_id(self, line):
        return re.search("\\[BsonRepresentation\\(BsonType.ObjectId\\)\\]", line)
