# Nuvolar Fleet API: How To
Try the following in you play with a linux compatible machine:
```
$> git clone nuvolar-fleet
$> cd nuvolar-fleet
$> sudo docker-compose up
```
This previous commands will spawn the docker stuff and setup the django webserver and postgresql db.

You may want to run the migration command just after the initial `docker-composer up` command as:
```
$> sudo docker exec -it nuvolar-fleet_web_1 python manage.py migrate
```

You can also load the dummy data to quick check the rest api as:
```
$> sudo docker exec -it nuvolar-fleet_web_1 python manage.py loaddata fleet/fixtures/dummydata.json
```

Also, You can run the Unit Tests as:
```
$> sudo docker exec -it nuvolar-fleet_web_1 python manage.py test
```

The nuvolar-fleet_web_1 is the default docker name for the django webserver.
The nuvolar-fleet_db_1 docker instance is the postgresql db instance.

## Let's check the API
If you already created the docker instances and already have run the migrations command, and the load dummy data, then a default user has been created for you, check the django-admin with **nuvolar** as username and password **nuvolar**.

If we check the root api url as:
`$> curl -s -X GET "http://localhost:8000/airport/" | jq .`
you will get  a response like:
```
{
  "detail": "Authentication credentials were not provided."
}
```
That is because you need a token, any user already registered in the django-admin and with a token can query the api, so if you already loaded the dummy data there is a token ready as:
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
But if you want to retrieve the toke by yourself you will need to query the default DRF api-token-auth as:
```
curl -s -X POST "http://localhost:8000/api-token-auth/" -H "Content-Type: application/json" -d'{"username":"nuvolar", "password":"nuvolar"}' | jq .
{
  "token": "019002f7168aa2534e9134a5177addc3b8d3b7d9"
}
```
Note: as you may already noticed I've been using the jq command line tool to pretty print the json output in the console output, feel free to use any other rest client if you feel more comfortable, the api should be available just like that. ... or I think so !! :upside_down_face:

Let's keep on moving, so what's next, let's try to add an ICAO as:
```
$> curl -s -X POST "http://localhost:8000/airport/" -H "Content-Type: application/json" -H "Authorization: Token 019002f7168aa2534e9134a5177addc3b8d3b7d9" -d'{"icao":"nu07"}' | jq .
{
  "id": 3,
  "icao": "nu07"
}
```
The same for an aircraft as:
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
And finally with the flight as:
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
You can query this end-point with query param in the url as :
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