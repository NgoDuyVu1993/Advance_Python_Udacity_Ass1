# Assignment 1 Near-Earth Objects
Task 1:
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

Task 2: 
```
python3 -m unittest --verbose tests.test_extract tests.test_database
```

Task 3: