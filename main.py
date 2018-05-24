from finder.code import code
from export.markdown import markdown

project_path = "../246/R246-API/R246-API"
doc_title = "Form246"

c = code(project_path)
s, o = c.classes()

md = markdown()
md.create(doc_title, s, o)
print("done.")
