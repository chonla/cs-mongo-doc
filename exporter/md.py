from exporter.base import base
import re
from datetime import datetime


class md(base):
    def __init__(self, title, objects, output):
        super().__init__(objects)
        self.output = output
        self.title = title

    def dump_model(self, model):
        self.push(f'## {model["classname"]}')

        self.push('| Name | Type | Description |')
        self.push('| - | - | - |')
        for v in model['variables']:
            var_type = self.render_link(v[0])
            self.push(f'| {v[1]} | {var_type} | {v[2]} |')

    def export(self):
        self.referenced = []
        self.printed = []

        self.push(f'# {self.title}')

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

        content = self.flush()

        ts = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        content = content + f"\n*generated on {ts}*"

        self.save(content, f'{self.output}/{self.title}.md')

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
