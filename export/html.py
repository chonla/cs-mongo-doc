from pprint import pprint
import re
from datetime import datetime
from export.exporter import exporter


class html(exporter):
    def __init__(self, name):
        super().__init__(name, f"{name}.html")
        pass

    def print_doc_title(self, name):
        return ["<h1>", f"{name}", "</h1>"]

    def print_timestamp(self):
        ts = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        return ["<div class='footer'>", f"auto-generated on {ts}", "</div>"]

    def print_table_title(self, title):
        return [f"<a name='{title}'></a>", "<h2>", title, "</h2>"]

    def print_table_header_columns(self, header_columns):
        cols = "<table><thead><tr><th>" + \
            "</th><th>".join(header_columns) + "</th></tr></thead><tbody>"
        return [cols]

    def print_link(self, text, href):
        return f"<a href='#{href}'>{text}</a>"

    def print_row(self, data):
        row = "<tr><td>" + "</td><td>".join(data) + "</td><tr>"
        return row

    def print_end_table(self, header_columns):
        return "</tbody></table>"
