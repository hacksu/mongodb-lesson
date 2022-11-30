db.createRole({
  role: "hacksu",
  privileges: [
    { resource: { db: "pokemon", collection: "pokedex" }, actions: ["find"] },
    {
      resource: { db: "pokemon", collection: "PC" },
      actions: ["find", "update", "insert"],
    },
  ],
  roles: [],
});

db.createUser({
  user: "student",
  pwd: make up a password,
  roles: ["hacksu"],
});
