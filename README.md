# Assignment 1 Near-Earth Objects
## Task 1:
Run test on NearEarthObject
```
neo = NearEarthObject(designation='2020 fk', name='Apophis', diameter=0.325, hazardous=True)
print(neo.designation)
print(neo.name)
print(neo.diameter)
print(neo.hazardous)
print(neo)
```

Run test on CloseApproach
```
ca = CloseApproach(designation="2020 FK", datetime="2020-Jan-01 12:30", distance=0.25, velocity=56.78)
print(type(ca.time)
print(ca.time_str)
print(ca.distance)
print(ca.velocity)
```

## Task 2: 
Run Unit Test
```
python3 -m unittest --verbose tests.test_extract tests.test_database
```

Run Manual Test
```
python3 main.py inspect --name Halley

python3 main.py inspect --pdes 433

python3 main.py inspect --verbose --name Ganymed
```

## Task 3:
Run Unit Test
```
python3 -m unittest --verbose tests.test_query
python3 -m unittest tests.test_query tests.test_limit
```

Run Manual Test
```
# Query for close approaches on 2020-01-01
python3 main.py query --date 2020-01-01

# Query for close approaches in 2020.
python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31

# Query for close approaches in 2020 with a distance of <=0.1 au.
python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31 --max-distance 0.1

# Query for close approaches in 2020 with a distance of >=0.3 au.
python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31 --min-distance 0.3

# Query for close approaches in 2020 with a velocity of <=50 km/s.
python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31 --max-velocity 50

# Query for close approaches in 2020 with a velocity of >=25 km/s.
python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31 --min-velocity 25

# Query for close approaches of not potentially-hazardous NEOs between 500m and 600m in diameter.
python3 main.py query --min-diameter 0.5 --max-diameter 0.6 --not-hazardous

# Query for close approaches of potentially-hazardous NEOs larger than 2.5km passing within 0.1 au at a speed of at least 35 km/s
# Hint: There's only one match in the whole dataset :)
python3 main.py query --max-distance 0.1 --min-velocity 35 --min-diameter 2.5 --hazardous
```