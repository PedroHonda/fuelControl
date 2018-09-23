# fuelControl
Created by Pedro Honda
August 28th, 2018

## HTTP Request / Response

### Home Page

- Method : `GET /`
- Home Page needs to provide relevant information to access/input data from/into Car databases

### Accessing Database Information

- Method : `GET /<carName>`
- Should connect to database `fuelControl.db` and show all information by default

_**Response**_

- `404 Not Found`
  - If there is no <carName> table in current database
- `200 OK`
  - If the request was a success
  - Should also return the information in a JSON format
```json
[
  {
      "date" : "2018-09-20",
      "mileage" : 10000,
      "pricePerLitre" : 4.000,
      "litreTotal" : 20.0,
      "payTotal" : 80.00,
      "fuelType" : "Gasolina Comum",
      "mileageDiff" : 0,
      "efficiency" : 0.00,
      "pricePerKm" : 0.00,
      "comments" : "..."
  },
  {
      "date" : "2018-09-23",
      "mileage" : 10500,
      "pricePerLitre" : 4.000,
      "litreTotal" : 25.0,
      "payTotal" : 100.00,
      "fuelType" : "Gasolina Comum",
      "mileageDiff" : 500,
      "efficiency" : 20.00,
      "pricePerKm" : 0.20,
      "comments" : "insert comment"
  }
]
```

### Inputing data to Database

- Method : `POST /<carName>`
- Should connect to `fuelControl.db` database and input information into it
- The format of the data to be provided in this method is also a JSON
```json
{
    "date" : "2018-09-20",
    "mileage" : 10000,
    "pricePerLitre" : 4.000,
    "litreTotal" : 20.0
}
```

_**Response**_

- `400 Bad Request`
  - If the data type for some of the input values is wrong
- `201 Created`
  - If the table for `<carName>` was not yet created
- `200 OK`
  - If the request was a success

## Database Schema
```
CREATE TABLE <carName> (
    date DATE,           
    mileage INTEGER,     
    pricePerLitre REAL,  
    litreTotal INTEGER,  
    payTotal REAL,       
    fuelType VARCHAR(20),
    mileageDiff INTEGER, 
    efficiency REAL,     
    pricePerKm REAL,     
    comments)            
```

## Future implementation
- Docker