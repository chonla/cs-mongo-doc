from finder.code import code
from export.markdown import markdown
from export.html import html
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help='project path', default='')
parser.add_argument('-t', '--title', help='document title', default='')
parser.add_argument('-o', '--output', help='output path', default='.')
parser.add_argument('--md', help='export markdown',
                    action='store_true', default=False)
parser.add_argument('--html', help='export html',
                    action='store_true', default=False)

args = parser.parse_args()

if args.path == "" or args.title == "":
    parser.print_help()
    exit()

project_path = args.path  # "../246/R246-API/R246-API"
doc_title = args.title  # "Form246"
output = args.output

c = code(project_path)
s, o = c.classes()

if args.md:
    md = markdown(doc_title, output)
    md.create(s, o)
    print("markdown is exported")

if args.html:
    h = html(doc_title, output)
    h.create(s, o)
    print("html is exported")

if not args.md and not args.html:
    print("nothing is exported.")

print("done.")
