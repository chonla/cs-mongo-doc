from pprint import pprint
import re
import html


class markdown():
    def __init__(self):
        self.to_be_printed = []
        pass

    def create(self, name, classes, objects):
        buffer = []

        buffer.append(f"# {name}")

        self.to_be_printed.extend(objects)

        while len(self.to_be_printed) > 0:
            o = self.to_be_printed.pop(0)
            buffer.extend(self.print_object(o, classes))

        with open(f"{name}.md", "w") as f:
            f.write("\n".join(buffer))

    def print_object(self, object_name, classes):
        buffer = []

        if object_name not in classes:
            return buffer

        title = self.remove_namespace(object_name)

        buffer.append("")
        buffer.append(f"## {title}")
        buffer.append("")

        buffer.append("| Name | Type | Definition |")
        buffer.append("| - | - | - |")

        for k in classes[object_name]:
            t, d = classes[object_name][k][0], classes[object_name][k][1]
            bare_type = html.escape(self.remove_namespace(t))

            if t in classes:
                link = bare_type.lower()
                bare_type = f"[{bare_type}](#{link})"

            buffer.append(f"| {k} | {bare_type} | {d} |")

            actual_type = t
            type_match = re.search("List<([^>]+)>", t)
            if type_match:
                actual_type = type_match.group(1)

            if actual_type in classes and actual_type not in self.to_be_printed:
                self.to_be_printed.append(actual_type)

        return buffer

    def remove_namespace(self, name):
        return name.split(".")[-1]
