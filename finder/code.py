import os
from glob import glob
import re
from pprint import pprint


class code():
    def __init__(self, path):
        self.scan_path = path
        self.file_list = []
        self.model_list = {}
        self.mongo_object = []
        self.get_scan_list()
        # self.file_list.append(self.scan_path + "/Models/Form.cs")

        for f in self.file_list:
            self.scan(f)

    def get_scan_list(self):
        self.file_list = [y for x in os.walk(self.scan_path)
                          for y in glob(os.path.join(x[0], '*.cs'))]

    def remove_line_comment(self, text):
        lines = text.split("\n")
        buffer = []
        for line in lines:
            if not re.search("^\\s*//", line):
                buffer.append(line)
        text = "\n".join(buffer)
        return text

    def remove_block_comment(self, text):
        text = re.sub(r"/\\*.*\\*/", "", text)
        return text

    def remove_annotation(self, text):
        lines = text.split("\n")
        buffer = []
        for line in lines:
            if not re.search("^\\s*\\[[^\\]]*\\]", line):
                buffer.append(line)
        text = "\n".join(buffer)
        return text

    def scan(self, name):
        with open(name) as f:
            content = f.read()

        content = content.replace("\r\n", "\n")

        match = re.search("public\\s+class\\s+([A-Za-z][A-Za-z0-9]*)", content)
        if match:
            class_name = match.group(1)

            namespace = ""
            ns_match = re.search(
                "namespace\\s+([A-Za-z][A-Za-z0-9\\._]*)\\s+{", content)
            if ns_match:
                namespace = ns_match.group(1)

            constructor_match = re.search(f"public {class_name}\\s*\\(", content)
            if constructor_match:
                return

            method_match = re.search(
                "\\s+[A-Za-z][A-Za-z0-9]*\\s*\\([^\\)]*\\)", content)
            if method_match:
                return

            lines = content.split("\n")
            summary_on = False
            summary = ""
            var_list = {}
            is_mongo_object = False
            for line in lines:
                if re.search("^\\s*/// <summary>\\s*", line):
                    summary = ""
                    summary_on = True
                elif re.search("^\\s*/// </summary>\\s*", line):
                    summary_on = False
                elif re.search("^\\s*/// ([^\\n]+)\\s*", line):
                    if summary_on:
                        m_summary = re.search("^\\s*/// ([^\\n]+)\\s*", line)
                        summary = m_summary.group(1)
                elif line.strip() == "[BsonRepresentation(BsonType.ObjectId)]":
                    is_mongo_object = True
                else:
                    l_match = re.search(
                        "\\s*public\\s+([A-Za-z][<>A-Za-z0-9\\._]*)\\??\\s+([A-Za-z][A-Za-z0-9_]*)", line)
                    if l_match and l_match.group(1) != "class":
                        var_type = l_match.group(1)
                        var_name = l_match.group(2)
                        if not re.search("\\.", var_type):
                            var_type = namespace + "." + var_type
                        var_list[var_name] = [var_type, summary]
                        summary = ""
                        if is_mongo_object:
                            self.mongo_object.append(
                                namespace + "." + class_name)
                        is_mongo_object = False

            self.model_list[namespace + "." + class_name] = var_list

    def classes(self):
        return self.model_list, self.mongo_object
