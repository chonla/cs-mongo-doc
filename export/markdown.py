from pprint import pprint
import re
from datetime import datetime
from export.exporter import exporter


class markdown(exporter):
    def __init__(self, name):
        super().__init__(name, "md")
        pass

    def print_doc_title(self, name):
        return [f"# {name}"]

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
