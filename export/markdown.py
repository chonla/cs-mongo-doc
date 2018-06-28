from pprint import pprint
import re
from datetime import datetime


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
            print(f"> {o}")
            buffer.extend(self.print_object(o, classes))

        buffer.extend(self.print_timestamp())

        with open(f"{name}.md", "w") as f:
            f.write("\n".join(buffer))

    def print_timestamp(self):
        ts = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        return ["---", f"auto-generated on {ts}"]

    def print_table_title(self, title):
        return ["", f"## {title}", ""]

    def print_table_header_columns(self, header_columns):
        cols = "| " + " | ".join(header_columns) + " |"
        breaks = "|" + (" - |" * len(header_columns))
        return [cols, breaks]

    def print_link(self, text, href):
        return f"[{text}](#{href})"

    def print_row(self, data):
        row = "| " + " | ".join(data) + " |"
        return row

    def print_end_table(self, header_columns):
        return ""

    def print_object(self, object_name, classes):
        buffer = []

        if object_name not in classes:
            return buffer

        title = self.remove_namespace(object_name)

        buffer.extend(self.print_table_title(title))
        buffer.extend(self.print_table_header_columns(
            ['Name', 'Type', 'Definition']))

        for k in classes[object_name]:
            t, d = classes[object_name][k][0], classes[object_name][k][1]
            bare_type = self.remove_namespace(t)
            encoded_type = ""
            actual_type = t
            type_match = re.search("([^<\\.]+)<([^>]+)>", t)
            if type_match:
                generic = type_match.group(1)
                bare_type = type_match.group(2)
                actual_type = self.get_namespace(
                    t) + "." + bare_type
                if actual_type in classes:
                    link = self.print_link(bare_type, bare_type.lower())
                    encoded_type = f"{generic}&lt;{link}&gt;"
                else:
                    encoded_type = f"{generic}&lt;{bare_type}&gt;"
            else:
                if t in classes:
                    link = self.print_link(bare_type, bare_type.lower())
                    encoded_type = link
                else:
                    encoded_type = bare_type

            buffer.append(self.print_row([k, encoded_type, d]))

            print(f"found new type: {actual_type}")

            if actual_type in classes and actual_type not in self.to_be_printed:
                print(f"put in queue")
                self.to_be_printed.append(actual_type)

        buffer.append(self.print_end_table(["", "", ""]))

        return buffer

    def remove_namespace(self, name):
        return name.split(".")[-1]

    def get_namespace(self, name):
        return ".".join(name.split(".")[0:-1])
