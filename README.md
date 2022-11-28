# mongodb-lesson

_n.b. although MongoDB is used mostly in the context of JavaScript and Node.JS servers, the Python library is also good and I've most recently used it in Python and I feel like Python is better known and regarded by a larger number of people, especially among students. But it would not be hard to switch to JavaScript._

Intro text on screen: you should open a new Python file while you're waiting :D you can also run `pip install pymongo` in the command line if you want

So as we all know, normally when we write and run a program all of the variables and objects and whatnot we've created evaporate as soon as it finishes, and the next time we run that program it's completely back to square one. That's why we need to use databases to store our program's thoughts and ideas persistently. A database will receive stuff from our program, hold on to it even when our program's not running, and probably store it in some files somewhere in a very efficiently retrievable-from format, so we have it even after losing power during a once-in-a-century thunderstorm.

There's a language for giving commands to databases called SQL. We won't be using it, but it was really popular for some time, and some people claim they can still hear its voice. Instead we'll be using a NoSQL database; the technical definition of the term NoSQL is, it's a database that doesn't use SQL. [MongoDB is the most popular NoSQL database.](https://survey.stackoverflow.co/2022/#section-most-popular-technologies-databases) It stores data in documents. Documents look like this:

#### Document example: data on a person

```json
{
  "name": "Mitch",
  "balance": -10.17,
  "happy": false,
  "brain_cells_gone_forever": 10245
}
```

So this pattern of storing data entries with labels that indicate their meaning is a common one in programming. In fact, you could say that whenever you make a variable in a programming language, you're storing a data entry with a label - the variable name - attached. In the context of a database, though, we're going to go one step further and store multiple documents like this, each with their own value attached to the label "name"; MongoDB is set up to store collections of documents, meaning a whole bunch of, for example, people, and there's an obvious use case for a database like this.

_TODO: create database with pokedex.json from this repo_

This is how you connect to a database that contains Pokemon:

```python
from pprint import pprint  # not a mongodb thing, but useful for displaying documents
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")  # TODO: real database URI  # connect to a database server
database = client.pokemon  # get the database called "pokemon" on this server
collection = database.pokedex  # get the collection called "pokedex" in that database
```

And this is how you retrieve the document corresponding to a Pokemon and print it:

```python
pikachu = collection.find_one({"name": "Pikachu"})
pprint(pikachu)
```

So. Do you all see Pikachu?

So in MongoDB, you create queries by creating sort of mini-documents that specify what you're looking for. This was a really really simple one: we had one key and one value; that pair had to be present in a document in the database for it to match. But we can do more subtle things as well; for example, instead of looking for a name that is Pikachu, we could look for a HP that is greater than 45. So the first part of requesting that looks pretty familia:

```python3
good_hp = collection.find_one({"HP":           })
```

But to specify the exact condition we're looking for, we're going to need to express the concept "greater than" and the number "45". We can do that by making another mini-document, with that first thing as the key and the second thing as the value:

```python
good_hp = collection.find_one({ "HP": {"$gt": 45} })
```

So this introduces us to the wonderful world of operators.

Did that work for everyone? It's okay that only one result showed up.

So there are a lot of operators, and we're not going to test out all of them, but they follow pretty much what you'd expect, given our $gt greater-than operator: there's $gte (greater than or equal to), $lt (less than), and even $ne (not equal to), and the other usual suspects from conditional statements. By the way, we're only getting one Pokemon at a time because we're using `find_one`. To get more, you can just use `find`, but that returns a thing called a cursor which you can go study if you want but we're going to want to turn it into a list to easily read the results. Like this:

```python
bad_hp = list(collection.find({ "HP": {"$lt": 45} }))
```

So yeah, to get multiple Pokemon, you just switch `find_one` to `find`, and then wrap the whole thing in list().

We just learned about operators that act on individual values. There is actually another type of operator that takes in entire queries of the type we've just been using. One pretty normal one is called "$or". If you want to get documents that match this query OR that query, you take both of them, put them in a list by going `[query1, query2]`, and make that list the value in a document with the key "$or":

```python
# TODO: check if there are any/too many results for this
good_hp_or_good_defence = list(collection.find({ "$or": [{ "HP": {"$gt": 45}}, {"Defense": {"$gt": 50}] }))
```

That might look kind of alien and complicated, but we can break it down. These two inner queries, we know about those: one sets a criterion for the value that corresponds to HP in the Pokemon documents, and one sets a criterion for the Defense, which we haven't used in a query before but we've seen it in our printed results. Those are both in a list. Because the list is there as the value for the "$or" operator, we get back documents where the first thing matches OR the second thing matches. And so here are our results.

So those are all the basics of querying and retrieving. There are other value operators than "greater than" and there are other query operators than "or" (like. there is "and") but if you squint, the other ones of those types all act pretty much the same way. Here is our completed Python code which prints out all these different guys:

And now I'm going to ask you to make a new file; for this one, you're going to learn how to insert.
