# Planet Information API

This utility reads two JSON files people.json and company.json in certain format from dump folder, generates mongodb collections from them, and then enables user to use APIs to query the data through as a web application.

It supports three API endpoints:
  - Get all employees of a company.
  - Get common friends of two people
  - Get list of fruits and vegetables a person likes

## Prerequisites

* Setup requires valid JSON data in files (people.json, company.json)
* Python 2.7+ should be installed
* MongoDB should be installed and the its path set in the Environment Variable

### Installation

* Install the python package dependencies mentioned in requirements.txt
* Run the following commands in the shell (after changing directory to dump folder) to create and populate the people and company collections in paranuara DB
```bash
mongoimport --db paranuara --collection people --file people.json --jsonArray
mongoimport --db paranuara --collection company --file company.json --jsonArray
```

### Sample JSON (used in the setup)

company.json

```markdown
[
  {
    "index": 0,
    "company": "NETBOOK"
  }
]
```
people.json

```markdown
[
  {
    "_id": "595eeb9b96d80a5bc7afb106",
    "index": 0,
    "guid": "5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
    "has_died": true,
    "balance": "$2,418.59",
    "picture": "http://placehold.it/32x32",
    "age": 61,
    "eyeColor": "blue",
    "name": "Carmella Lambert",
    "gender": "female",
    "company_id": 58,
    "email": "carmellalambert@earthmark.com",
    "phone": "+1 (910) 567-3630",
    "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
    "about": "Non duis dolore ad enim.\r\n",
    "registered": "2016-07-13T12:29:07 -10:00",
    "tags": [
      "id",
      "quis",
      "ullamco",
      "consequat",
      "laborum",
      "sint",
      "velit"
    ],
    "friends": [
      {
        "index": 0
      }
    ],
    "greeting": "Hello, Carmella Lambert! You have 6 unread messages.",
    "favouriteFood": [
      "orange"
    ]
  }
]
```

### Tech

Following packages and technologies are used:
* [Python] -  A widely used high-level programming language for general-purpose programming
* [MongoDB] - A free and open-source cross-platform document-oriented database program
* [Bottle] - A fast, simple and lightweight WSGI micro web-framework for Python

### Todos

 - Write Tests
 - Return pretty API response
 - Add HTML for Swagger style ease in using the APIs
 - Handle invalid page hits and redirections