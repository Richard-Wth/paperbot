import pymongo
from papersbot.settings import MONGO_DATABASE, MONGO_URI

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]


def remove_item_from_db():
    ignore_fields = [
        "Medicine",
        "Economics",
        "Business",
        "Poliitical Science",
        "Education",
        "Sociology",
        "Art",
        "History",
        "Philosophy",
        "Linguistics",
        "Law",
    ]
    for field in ignore_fields:
        db["geoscience"].delete_many({"fields_of_study": field})


if __name__ == "__main__":
    remove_item_from_db()
