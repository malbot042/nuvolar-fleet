# Nuvolar Fleet API

Please follow the steps below to set up the Nuvolar Fleet API.

## Docker setup

To set up the Docker container, please type the following in a Linux terminal:
```
$> git clone https://github.com/malbot042/nuvolar-fleet.git
$> cd nuvolar-fleet
$> sudo docker-compose up
```

The above commands will spawn the Docker container, and set up the DJango's webserver and PostgreSQL database.

### Migration

To execute the migration command, please type:

```
$> sudo docker exec -it nuvolar-fleet_web_1 python manage.py migrate
```

### Dummy data

Dummy data is provided to test the REST API quickly. Please, load it by typing:

```
$> sudo docker exec -it nuvolar-fleet_web_1 python manage.py loaddata fleet/fixtures/dummydata.json
```

### Unit tests

To run the unit tests, please type:

```
$> sudo docker exec -it nuvolar-fleet_web_1 python manage.py test
```

* **nuvolar-fleet_web_1** is the default Docker name for the DJango's webserver.
* **nuvolar-fleet_db_1** Docker instance is the PostgreSQL database instance.

## Checking the API

After the Docker instances have been created, the migration command has been run, and the dummy data has been loaded, a default user is automatically created.

Check django-admin with user name `nuvolar` and password `nuvolar`.

Optionally I added the **Django Swagger** app (drf-yasg) and did a basic configuration to let you check the auto-generated documentation (with **redoc**) of the available end-points, the access url is located under:
http://localhost:8000/swagger/ and http://localhost:8000/redoc/

### Authentication tokens

When checking the Root API URL, access could be denied.  For example, by typing:

`$> curl -s -X GET "http://localhost:8000/airport/" | jq .`

the petition could be rejected and the following response returned:
```
{
  "detail": "Authentication credentials were not provided."
}
```

The reason for this refusal is the need to provide a valid token.
Any registered user in django-admin with a valid token may query the API. If you have already loaded the dummy data, there is a token available as:
```
curl -s -X GET "http://localhost:8000/" -H "Authorization: Token 019002f7168aa2534e9134a5177addc3b8d3b7d9" | jq .
[
  {
    "id": 1,
    "icao": "NU01"
  },
  {
    "id": 2,
    "icao": "NU02"
  }
]
```

A valid token can also be retrieved by querying the default DRF api-token-auth as:

```
curl -s -X POST "http://localhost:8000/api-token-auth/" -H "Content-Type: application/json" -d'{"username":"nuvolar", "password":"nuvolar"}' | jq .
{
  "token": "019002f7168aa2534e9134a5177addc3b8d3b7d9"
}
```
:information_source: **Note**: Output is filtered by using the `jq` command to pretty-print the JSON format. Any other REST client can be used in place.


### Functional tests

Add an ICAO:

```
$> curl -s -X POST "http://localhost:8000/airport/" -H "Content-Type: application/json" -H "Authorization: Token 019002f7168aa2534e9134a5177addc3b8d3b7d9" -d'{"icao":"nu07"}' | jq .
{
  "id": 3,
  "icao": "nu07"
}
```
Add an aircraft:
```
$> curl -s -X POST "http://localhost:8000/aircraft/" \
-H "Content-Type: application/json" \
-H "Authorization: Token 019002f7168aa2534e9134a5177addc3b8d3b7d9" \
-d'{"serial_number":"Nuvolar AirCraft 700", "manufacturer": "Nuvolar Airlines"}' | jq .
{
  "id": 3,
  "serial_number": "Nuvolar AirCraft 700",
  "manufacturer": "Nuvolar Airlines"
}
```
Add a flight as:
```
$> curl -s -X POST "http://localhost:8000/flight/" -H "Content-Type: application/json" -H "Authorization: Token 019002f7168aa2534e9134a5177addc3b8d3b7d9" -d'{"departure_date":"2022-10-10T00:00", "arrival_date": "2022-10-11T00:00", "departure_airport": 1, "arrival_airport": 2}' | jq .
{
  "id": 4,
  "departure_date": "2022-10-10T00:00:00Z",
  "arrival_date": "2022-10-11T00:00:00Z",
  "departure_airport": 1,
  "arrival_airport": 2,
  "aircraft": null
}
```
:information_source: **Note**: you can update (PUT) or delete any of the previous entries as you will do in any other rest service, just type `curl -s -X DELETE "http://localhost:8000/airport/{id}/" -H "Content-Type: application/json" -H "Authorization: Token 019002f7168aa2534e9134a5177addc3b8d3b7d9"` on any end-point with the `id` entry you want to delete, or the equivalent PUT method, for the purpose of this README we will try to keep it short.

Query above end-point using URL query param:
```
$> curl -s -X GET "http://localhost:8000/flight/?departure_date=2021-08-22T00:00Z" -H "Authorization: Token 019002f7168aa2534e9134a5177addc3b8d3b7d9" | jq .
[
  {
    "id": 3,
    "departure_date": "2021-08-22T10:10:00Z",
    "arrival_date": "2021-08-22T14:12:00Z",
    "departure_airport": 2,
    "arrival_airport": 1,
    "aircraft": 2
  }
]
```
And finally the report api that looks like this:
```
$> curl -s -X GET "http://localhost:8000/report/?departure_date=2021-08-01T00:00Z&arrival_date=2021-08-02T04:00Z" -H "Authorization: Token 019002f7168aa2534e9134a5177addc3b8d3b7d9" | jq .
{
  "NU01": {
    "flights": 1,
    "total": 240,
    "average": 240,
    "aircrafts": {
      "NUVOLAR Aircraft 001": 240
    }
  }
}
```
alternatively you can query for a full report without any query param as:
```
$> curl -s -X GET "http://localhost:8000/report/" -H "Authorization: Token 019002f7168aa2534e9134a5177addc3b8d3b7d9" | jq .
{
  "NU01": {
    "flights": 2,
    "total": 1800,
    "average": 0,
    "aircrafts": {
      "NUVOLAR Aircraft 001": 240,
      "Unknow": 1560
    }
  },
  "NU02": {
    "flights": 1,
    "total": 242,
    "average": 242,
    "aircrafts": {
      "NUVOLAR Aircraft 001": 242
    }
  }
}
```
