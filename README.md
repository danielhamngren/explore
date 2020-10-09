# Places GIS project

This is a small project based for a project course in a Geographical IT program I attended in the fall of 2020.

It is using Geodjango and PostGIS. The data is from openstreetmap.

## Setup

The secrets are stored in `.env`.

Add the shp-files to `places/data`.

Run the following in the django python shell (`./manage.py shell`) to load the data in the `places/data`-folder.

```python
from places import load
load.run()
```

## Running

```$ ./manage.py runserver```
