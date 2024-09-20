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
    ObjectId("66c6eaf12cf336807d76e9c9"), ObjectId("66c6ece92cf336807d76e9e5"), ObjectId("66e2a0a3a0618dad2faa8399"), ObjectId("66e7a70c36d3ff50b1285d3c"), ObjectId("66e7a7ab36d3ff50b1285d49"), ObjectId("66e7abeb5189253e15a89bc0"), ObjectId("66e7ac555189253e15a89bce"), ObjectId("66e8179e4c3bed6b4bd205b4"), ObjectId("66e8189a4c3bed6b4bd205c5"), ObjectId("66e818d94c3bed6b4bd205d3"), ObjectId("66e819094c3bed6b4bd205db"), ObjectId("66e81a6c3911dba77b4492a1"), ObjectId("66e81aa03911dba77b4492ac")
  ]
});
