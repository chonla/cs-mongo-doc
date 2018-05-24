from pymongo import MongoClient


class data():
    def __init__(self, dsn):
        self._client = MongoClient(dsn)
        self._entities = {}

    def db(self, dbname):
        self._db = self._client[dbname]
        return self

    def col(self, colname):
        self._col = self._db[colname]
        return self

    def populate_data(self):
        return self._col.find().sort("_id").limit(1)

    def entities(self, dbname, colname):
        self._entities = {}
        cursor = self.db(dbname).col(colname).populate_data()
        self.put_entities(cursor[0], colname)

        return self._entities

    def put_entities(self, doc, name):
        k = []
        for field_name in doc:
            k.append(field_name)
            if type(doc[field_name]).__name__ == "dict":
                self.put_entities(doc[field_name], field_name)
        self._entities[name.capitalize()] = k
