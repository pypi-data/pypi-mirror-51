ojextends
==============

``ojextends`` allows you to extend the object class and convert ``JSON Documents`` to nested object parsing.

``ojextends`` provides eight key methods to handle transformations.

* `objectToDict` 
* `objectToStr` 
* `objectsToList` 
* `objectsToStr` 
* `objectFromDict` 
* `objectFromStr` 
* `objectsFromStr` 
* `objectsFromList`



## Getting Started

To install using pip, simply run

```code:shell
pip install ojextends
```

Dependencies
------------
``ojextends`` only uses the json library provided by the python system.



Usage
-----
The code below defines some simple models, and its natural mapping to json.

```python

    from ojextends import JsonSerializable
    
    @JsonSerializable
    class Student(object):
        name = str
        age = int
        books = list
    
    @JsonSerializable
    class Teacher(object):
        name = str
        students = list([Student])
    
    @JsonSerializable
    class School(object):
        name = str
        teachers = list([Teacher])
    
    @JsonSerializable
    class Area(object):
        name = str
        schools = list([School])
        
```
Example of transformations to parse Area lookup response for item:

```python

    import json
    import requests
    from ojextends import JsonSerializable
    
    def get_areas(areaid):
        url = 'https://127.0.0.1/area/lookup?id={}'
        return requests.get(url.format(area_id)).json()

    areajson = get_areas(518000)
    print(areajson)
    
    area = Area.objectToDict(areajson)
    print(area.schools)
    school = area.schools[0] if len(area.schools) else School()
    print(school.name)
```

The code above produces next result:


```json

    {
    "name":"shenzhen",
    "student":{
        "name":"Bob",
        "age":20
    },
    "schools":[
        {
            "name":"Shenzhen university",
            "teachers":[
                {
                    "name":"Mike",
                    "students":[
                        {
                            "name":"Lily",
                            "age":18,
                            "books":[
                                "book1",
                                "book2"
                            ]
                        },
                        {
                            "name":"Stone",
                            "age":21
                        }
                    ]
                }
            ]
        },
        {
            "name":"Shenzhen normal university",
            "teachers":[
                {
                    "name":"Linda1",
                    "students":[
                        {
                            "name":"Bob",
                            "age":20,
                            "books":[]
                        },
                        {
                            "name":"Tom",
                            "age":23
                        }
                    ]
                }
            ]
        }
    ]
}

```

See tests.py for more examples.


Tests
-----
Getting the tests running looks like:

```code:shell

# Install dependencies
$ pip install -r requirements.txt
# Run the test suites
$ python tests.py
```
License
-------

The MIT License (MIT)

Contributed by `Bob Wu <https://github.com/bob4open/>`
