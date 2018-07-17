from exporter.base import base
import re
from pprint import pprint
import hashlib


class sql(base):
    def __init__(self, title, objects, output):
        super().__init__(objects)
        self.output = output
        self.title = title
        self.relations = []

    def dump_model(self, model):
        table = self.normalize_field_name(model["classname"])
        field_list = self.create_db_fieldlist(model)
        stmt = f'''CREATE TABLE {table} (
    `pk_id` INTEGER UNSIGNED,
{field_list}
    PRIMARY KEY (`pk_id`)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci;'''
        self.push(stmt)

    def dump_relation(self, rel):
        table = f"{self.normalize_field_name(rel[0])}_{self.normalize_field_name(rel[1])}_relation"
        field_list = f'''
    `{self.normalize_field_name(rel[0])}_id` INTEGER,
    `{self.normalize_field_name(rel[2])}_id` INTEGER'''
        stmt = f'''CREATE TABLE {table} (
{field_list}
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci;'''
        self.push(stmt)
        index = f"{self.normalize_field_name(rel[0])}_{self.normalize_field_name(rel[1])}_index_1"
        stmt = f'''CREATE INDEX {index} ON {table} ({self.normalize_field_name(rel[0])}_id) USING BTREE;'''
        self.push(stmt)
        index = f"{self.normalize_field_name(rel[0])}_{self.normalize_field_name(rel[1])}_index_2"
        stmt = f'''CREATE INDEX {index} ON {table} ({self.normalize_field_name(rel[2])}_id) USING BTREE;'''
        self.push(stmt)

    def create_db_fieldlist(self, model):
        buffer = []
        for v in model['variables']:
            if self.has_relation(v[0]):
                self.relations.append(
                    (model['classname'], v[1], self.get_main_data_type(v[0])))
            else:
                datatype = self.map_datatype(v[0])
                fieldname = self.normalize_field_name(v[1])
                buffer.append(f'    `{fieldname}` {datatype},')
        return "\n".join(buffer)

    def map_datatype(self, data_type):
        if data_type == "string":
            data_type = "VARCHAR(500)"
        elif data_type == "int":
            data_type = "INTEGER"
        elif data_type == "bool":
            data_type = "TINYINT"
        elif data_type == "DateTime":
            data_type = "DATETIME"
        elif data_type == "decimal" or data_type == "double":
            data_type = "DOUBLE"
        return data_type

    def export(self):
        self.referenced = []
        self.printed = []

        for m in self.mongo_objects:
            self.printed.append(m["classname"])
            self.dump_model(m)

        referenced_classes = list(
            map(lambda c: self.class_list[c], self.referenced))

        while len(self.referenced) > 0:
            classname = self.referenced.pop(0)
            m = self.class_list[classname]

            self.printed.append(m["classname"])
            self.dump_model(m)

        while len(self.relations) > 0:
            relation = self.relations.pop(0)
            self.dump_relation(relation)

        content = self.flush()

        hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        content = content + f"\n-- hash:{hash}"

        self.save(content, f'{self.output}/{self.title}.sql')

    def get_main_data_type(self, var_type):
        match = re.search(
            '([a-zA-Z][a-zA-Z0-9_\\.]+)<([a-zA-Z][a-zA-Z0-9_\\.]+)>', var_type)
        if match:
            return match.group(2)
        return var_type

    def has_relation(self, var_type):
        match = re.search(
            '([a-zA-Z][a-zA-Z0-9_\\.]+)<([a-zA-Z][a-zA-Z0-9_\\.]+)>', var_type)
        if match:
            return True
        return var_type in self.class_keys

    def render_link(self, var_type):
        match = re.search(
            '([a-zA-Z][a-zA-Z0-9_\\.]+)<([a-zA-Z][a-zA-Z0-9_\\.]+)>', var_type)
        if match:
            classname = match[2]
            if classname in self.class_keys:
                href = classname.lower()
                if classname not in self.referenced:
                    self.referenced.append(classname)
                return f'{match[1]}&lt;[{classname}](#{href})&gt;'
            return f'{match[1]}&lt;{classname}&gt;'
        else:
            if var_type in self.class_keys:
                href = var_type.lower()
                if var_type not in self.referenced:
                    self.referenced.append(var_type)
                return f'[{var_type}](#{href})'
            return var_type

    def normalize_field_name(self, name):
        name = re.sub("([a-z])([A-Z])", "\\1_\\2", name)
        name = re.sub("([a-z])([0-9])", "\\1_\\2", name, flags=re.IGNORECASE)
        name = re.sub("([0-9])([A-Z])", "\\1_\\2", name, flags=re.IGNORECASE)
        return name.lower()
