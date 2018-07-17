from exporter.base import base
import re
import os
from datetime import datetime


class html(base):
    def __init__(self, title, objects, output):
        super().__init__(objects)
        self.output = output
        self.title = title
        self.template = ''
        template_file = f"./assets/template.html"
        if os.path.isfile(template_file):
            with open(template_file, 'r') as tmpl:
                self.template = tmpl.read()

    def dump_model(self, model):
        self.push('<div class="card mb-3"><div class="card-body">')
        self.push(f'<a name="{model["classname"]}"></a>')
        self.push(f'<h5 class="card-title">{model["classname"]}</h5>')

        self.push('<div class="card-text"><table class="table table-striped">')
        self.push('<thead><tr class="d-flex">')
        self.push(
            '<th class="col-4">Name</th><th class="col-2">Type</th><th class="col-6">Description</th>')
        self.push('</tr></thead><tbody>')
        for v in model['variables']:
            var_type = self.render_link(v[0])
            self.push(f'<tr class="d-flex"><td class="col-4">{v[1]}</td><td class="col-2">{var_type}</td><td class="col-6">{v[2]}</td></tr>')
        self.push('</tbody></table></div>')
        self.push('</div></div>')

    def export(self):
        self.referenced = []
        self.printed = []

        self.push(f'<h1>{self.title}</h1>')

        for m in self.mongo_objects:
            self.printed.append(m["classname"])
            self.dump_model(m)

        referenced_classes = list(
            map(lambda c: self.class_list[c], self.referenced))

        while len(self.referenced) > 0:
            classname = self.referenced.pop(0)
            m = self.class_list[classname]
            self.dump_model(m)

        content = self.flush()

        ts = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

        content = self.template.format(
            title=self.title, content=content, timestamp=ts)

        self.save(content, f'{self.output}/{self.title}.html')

    def render_link(self, var_type):
        match = re.search(
            '([a-zA-Z][a-zA-Z0-9_\\.]+)<([a-zA-Z][a-zA-Z0-9_\\.]+)>', var_type)
        if match:
            classname = match[2]
            if classname in self.class_keys:
                href = classname.lower()
                if classname not in self.referenced:
                    self.referenced.append(classname)
                return f'{match[1]}&lt;<a href="#{href}">{classname}</a>&gt;'
            return f'{match[1]}&lt;{classname}&gt;'
        else:
            if var_type in self.class_keys:
                href = var_type.lower()
                if var_type not in self.referenced:
                    self.referenced.append(var_type)
                return f'<a href="#{href}">{var_type}</a>'
            return var_type
