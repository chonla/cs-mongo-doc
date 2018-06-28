from finder.code import code
from export.markdown import markdown
from export.html import html

project_path = "../246/R246-API/R246-API"
doc_title = "Form246"

c = code(project_path)
s, o = c.classes()

md = markdown(doc_title)
md.create(s, o)

h = html(doc_title)
h.create(s, o)
print("done.")
