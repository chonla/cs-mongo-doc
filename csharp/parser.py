import os
from glob import glob
from pprint import pprint
from csharp.model import model
import operator
from functools import reduce
from exporter.md import md


class parser():
    def __init__(self, path):
        self.files = self.get_scan_list(path)
        self.objects = self.models(self.files)
        # self.files = [
        #     '/Users/chonla/work/sec/246/R246-API/R246-API/Models/Form.cs']

    def models(self, files):
        l = list(filter(lambda m: m.ok(), map(lambda f: model(f), files)))
        objs = reduce(operator.concat, list(map(lambda m: m.objects(), l)))
        objs = list(filter(lambda o: len(o['variables']) > 0, objs))
        return objs

    def get_scan_list(self, path):
        return [y for x in os.walk(path)
                for y in glob(os.path.join(x[0], '*.cs'))]

    def to_md(self, title, path):
        out = md(title, self.objects, path)
        out.export()
