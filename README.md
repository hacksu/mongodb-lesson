# mongodb-lesson

_n.b. although MongoDB is used mostly in the context of JavaScript and Node.JS servers, the Python library is also good and I've most recently used it in Python and I feel like Python is better known and regarded by a larger number of people, especially among students. But it would not be hard to switch to JavaScript._

So as we all know, normally when we write and run a program all of the variables and objects and whatnot we've created evaporate as soon as it finishes, and the next time we run that program it's completely back to square one. That's why we need to use databases to store our program's thoughts and ideas persistently. A database will receive stuff from our program, hold on to it even when our program's not running, and probably store it in some files somewhere in a very efficiently retrievable-from format, so we have it even after losing power during a once-in-a-century thunderstorm.

There's a language for giving commands to databases called SQL. We won't be using it, but it was really popular for some time, and some people claim they can still hear its voice. Instead we'll be using a NoSQL database; the technical definition of the term NoSQL is, it's a database that doesn't use SQL. [MongoDB is the most popular NoSQL database.](https://survey.stackoverflow.co/2022/#section-most-popular-technologies-databases) It stores data in documents. Documents have other names in other contexts, like "dicts" in pure Python and "objects" in JavaScript, but I'm just going to call them documents here; you will become extremely tired of the word. Documents look like this:

### Document example: data for a person

```json
{
  "name": "Mitch",
  "balance": -10.17,
  "happy": False,
  "brain_cells_gone_forever": 10245
}
```

So this pattern of storing data entries with labels that indicate their meaning is a common one in programming. In fact, you could say that whenever you make a variable in a programming language, you're storing a data entry with a label - the variable name - attached. In the context of a database, though, we're going to go one step further and store multiple documents like this, each with their own value attached to these labels, like for this example each document would have a different value for "name"; MongoDB is set up to store collections of documents, meaning a whole bunch of, for example, people, and there's an obvious use case for a database like this.

This is how you connect to a database that contains Pokemon:

```python
from pprint import pprint  # not a mongodb thing, but useful for displaying documents
from pymongo import MongoClient

client = MongoClient(
    host="mitch.website",
    username="student",
    password="[[[PASSWORD]]]"
)
database = client.pokemon  # get the database called "pokemon" on this server
collection = database.pokedex  # get the collection called "pokedex" in that database
```

And this is how you retrieve the document corresponding to a Pokemon and print it:

```python
pikachu = collection.find_one({"name": "Pikachu"})
pprint(pikachu)
```

So. Do you all see Pikachu?

You've just retrieved a MongoDB document, and it's giving you information about a Pokemon. If you want information about some other Pokemon, feel free to replace "Pikachu" with its name. The data, the variables that we retrieved are inside the document, but we can get them out pretty easily. If you want to see Pikachu's base HP, just do this:

```
pprint(pikachu["HP"])
```

So in MongoDB, you create queries by creating sort of mini-documents that specify what you're looking for, like the one we have here. This was a really really simple one: we had one key and one value; that pair had to be present in a document in the database for it to match. But we can do more subtle things as well; for example, instead of looking for a `"name"` that is `"Pikachu"`, we could look for a `"HP"` that is `greater than 45`. So the first part of requesting that looks pretty familiar:

```python3
good_hp = collection.find_one({"HP":           })
```

But to specify the exact condition we're looking for, we're going to need to express the concept "greater than" and the number "45". We can do that by making another mini-document, with that first thing as the key and the second thing as the value:

```python
good_hp = collection.find_one({ "HP": {"$gt": 45} })
```

So this introduces us to the wonderful world of operators, which are things that start with dollar signs.

Did that work for everyone? It's okay that only one result showed up.

So there are a lot of operators, and we're not going to test out all of them, but they follow pretty much what you'd expect, given our $gt greater-than operator: there's $gte (greater than or equal to), $lt (less than), and even $ne (not equal to), and the other usual suspects from conditional statements. By the way, we're only getting one Pokemon at a time because we're using `find_one`. To get more, you can just use `find`, but that returns a thing called a cursor which you can go study if you want but we're going to want to turn it into a list to easily read the results. Like this:

```python
bad_hp = list(collection.find({ "HP": {"$lt": 45} }))
```

So yeah, to get multiple Pokemon, you just switch `find_one` to `find`, and then wrap the whole thing in list().

We just learned about operators that act on individual values. There is actually another type of operator that takes in entire queries of the type we've just been using. One pretty normal one is called "$or". If you want to get documents that match this query OR that query, you take both of them, put them in a list by going `[query1, query2]`, and make that list the value in a document with the key "$or":

```python
multiple_queries = [
    { "HP": {"$gt": 120}},
    {"Defence": {"$gt": 210}}
]
good_hp_or_good_defence = list(collection.find({ "$or": multiple_queries }))
pprint(good_hp_or_good_defence)
```

That might look kind of alien and complicated, but we can break it down. These two initial queries, we know about those: one sets a criterion for the value that corresponds to HP in the Pokemon documents, and one sets a criterion for the Defense, which we haven't used in a query before but we've seen it in our printed results. Those are both in a list. Because the list is there as the value for the "$or" operator, we get back documents where the first thing matches OR the second thing matches. And so here are our results.

So those are all the basics of querying and retrieving. There are other value operators than "greater than" and there are other query operators than "or" (like. there is "and") but if you squint, all the operators within those two types act pretty much the same way. Here is our completed Python code which prints out all these different guys: [queries.py](queries.py)

And now I'm going to ask you to make a new file; for this one, you're going to learn how to insert.

The initial connection is the same, but you're going to connect to a different collection from this time. You're going to connect to the PC, a collection that you have permission to write to, where individual Pokemon are stored:

```python
from pprint import pprint  # not a mongodb thing, but useful for displaying documents
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")  # TODO: real database URI  # connect to a database server
database = client.pokemon  # get the database called "pokemon" on this server
collection = database.PC  # get the collection called "PC" in that database
```

And the code for inserting is actually really simple:

```python
collection.insert_one({
  "name": "Squinchy",
  "species": "Wartortle",
  "currentHP": 10,
  "mood": "bemused"
})
```

So that's the basic idea; that's how you take data and store it somewhere where it will persist outside of your program. We're going to add one thing, though. MongoDB assigns a unique ID to every document that's inserted, and we're going to print the unique ID of our documents like this:

```python
result = collection.insert_one({
  "name": "Squinchy",
  "species": "Wartortle",
  "currentHP": 10,
  "mood": "bemused"
})
print(result.inserted_id)
```

You can follow the format that I have for my Pokemon here if you want, but you can also put any strings for keys and pretty much any values that aren't objects. Here I have MongoDB Compass, which is a great program that lets you monitor a MongoDB database, and we can see what you're inserting here. Or if no one wants to insert anything I will just stare forlornly at this empty screen.

And finally, it would be dumb if you could insert a document but then could never modify it once it was there. We need to be able to update the stored information about our Pokemon, or else we would never be able to do anything Pokemonish with them. We'll want to make yet another new file for updating, so we're not re-running our inserts and making a new document every time we want to update; but we want to copy the ID we got from running an insert, because that's how you are going to identify the Pokemon you're going to modify.

An update consists of two parts: one query to identify the document that will be modified, and one mini-document specifying the action to be taken. In addition to the querying operators we looked at before, there are update operators. We're going to stick with a simple one here: $set. $set just lets you list new data that you want to add to your document, overriding old data if it exists. It looks like this:

```python
collection.update_one({"_id": "paste your document's id"}, {"$set": {"owner": "enter your name here."}})
```

So as you can see, the update operation is represented as another nested document. The inner document has a key ("owner") and a value (your name); it itself is the value in the outer document, where the key is "$set", meaning the inner document is just used to set values in the document that's being updated.

So that shows us how to store, update, and retrieve documents in MongoDB. At this point, you might be interested to know that you can download MongoDB Community Edition and connect to a database running on your very own computer, to use it for persistent data in any program you may write. This example is in Python, but you can connect to it in a very similar way with its official libraries for JavaScript, Java, C++, and even Rust, and some other ones. This is a very popular software among new developers, so there are a ton of tutorials online for lots of different languages that can help you set up or learn more on your own.
