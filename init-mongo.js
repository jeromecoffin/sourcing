db = db.getSiblingDB('sourcingmain');  // Create or switch to "mydatabase"

db.users.insertOne({
  "_id": ObjectId("66c6c0ee5adadf5d5bcb546f"),
  "username": "jcoffin",
  "language": "en",
  "company": "Free",
  "sourcing": "Garments, Accessories",
  "lastname": "COFFIN",
  "phone": "1234567898",
  "address": "56 Van CAO Hanoi",
  "email": "thi.ha@nguyen.com",
  "experience": 1,
  "name": "Jérôme",
  "isFirstLogin": "1",
  "rfi_ids": [
    ObjectId("66c6eaf12cf336807d76e9c9"),
    ObjectId("66c6ece92cf336807d76e9e5")
  ]
});
