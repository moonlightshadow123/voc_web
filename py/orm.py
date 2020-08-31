from peewee import *
from datetime import datetime
timeformat = "%Y/%m/%d %H:%M:%S"

db = SqliteDatabase('voc.db')

class BaseModel(Model):
    class Meta:
        database = db

class Entry(BaseModel):
    word = CharField(unique=True)
    note = CharField(max_length=1024, null=True, default="")
    last_update = DateTimeField(null=True)

def lookup(word):
	entry, created = Entry.get_or_create(word=word)
	return {"word":word, "note":entry.note, "last_update":entry.last_update.strftime(timeformat) if entry.last_update != None else "None"}

def update(word, note):
	now = datetime.now()
	count = Entry.update(note=note, last_update=now).where(Entry.word==word).execute()
	return count, now.strftime(timeformat)

def delete(word):
	count = Entry.delete().where(Entry.word==word).execute()
	return count

if __name__ == "__main__":
	db.connect()
	# db.create_tables([Entry])
	# entry = Entry.create(word='good', note="Hello, This is the note", last_update=datetime.now())
	# entry.save()
	print(lookup("some"))
	#print(update("some", "This is 'some' notes!"))
	print(delete("some"))
	print(lookup("some"))