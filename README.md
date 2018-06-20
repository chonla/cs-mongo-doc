# Convert mongodb models in C# files to markdown document

1. Open main.py and set project_path to project path to be scanned and doc_title to markdown title.
2. Save changes to main.py.
3. Run `python main.py`

# Idea behind

* Script will scan for model classes containing mongodb ObjectID field, and start from those models.
* All types referred in model will be collectively scanned.