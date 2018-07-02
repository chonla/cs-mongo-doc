from pprint import pprint
import re
from datetime import datetime
from export.exporter import exporter


class sql(exporter):
    def __init__(self, name, output):
        self.relations = []
        super().__init__(name, "sql", output)
        pass

    def print_doc_title(self, name):
        return [f"--- {name} migration script"]

    def print_timestamp(self):
        ts = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        return [f"--- auto-generated on {ts}"]

    def print_table_title(self, title):
        return ["", f"CREATE TABLE {title}", "(",
                "    pk_id INTEGER UNSIGNED,"]

    def print_table_header_columns(self, header_columns):
        return []

    def print_link(self, text, href):
        return f" LinkTo:{text} "

    def print_row(self, data, object_name=""):
        data_type = data[1]
        custom_match = re.search("LinkTo:([^\\s+]+)", data_type)
        if custom_match:
            self.add_relationship(
                [object_name, data[0], custom_match.group(1)])
            return []
        if data_type == "string":
            data_type = "VARCHAR(500)"
        elif data_type == "int":
            data_type = "INTEGER"
        elif data_type == "bool":
            data_type = "TINYINT"
        elif data_type == "DateTime":
            data_type = "DATETIME"
        data_field_name = self.normalize_field_name(data[0])
        row = f"    {data_field_name} {data_type},"
        return [row]

    def print_end_table(self, header_columns):
        rels = self.get_relations()
        end_table = ["    PRIMARY KEY (pk_id)",
                     ")", "ENGINE=InnoDB",
                     "DEFAULT CHARSET=utf8", "COLLATE=utf8_general_ci;"]
        end_table.extend(rels)
        return end_table

    def normalize_field_name(self, name):
        name = re.sub("([a-z])([A-Z])", "\\1_\\2", name)
        name = re.sub("([a-z])([0-9])", "\\1_\\2", name, flags=re.IGNORECASE)
        name = re.sub("([0-9])([A-Z])", "\\1_\\2", name, flags=re.IGNORECASE)
        return name.lower()

    def add_relationship(self, tuple):
        self.relations.append(tuple)

    def get_relations(self):
        rels = []
        for rel in self.relations:
            # "_".join(rel).upper()
            name = "".join(map(lambda t: t.capitalize(), rel)) + "Relation"
            fr = self.normalize_field_name(rel[0]).lower()
            to = self.normalize_field_name(rel[1]).lower()
            tab = ["", f"CREATE TABLE {name}", "(",
                   f"    {fr}_id INTEGER UNSIGNED,",
                   f"    {to}_id INTEGER UNSIGNED",
                   ")",
                   "ENGINE=InnoDB",
                   "DEFAULT CHARSET=utf8",
                   "COLLATE=utf8_general_ci;"]
            rels.extend(tab)
        self.relations = []
        return rels
