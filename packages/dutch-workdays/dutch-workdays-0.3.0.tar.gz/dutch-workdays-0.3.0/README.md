Dutch Workdays
==============

A very small library that handles with Dutch calendars and holidays 🇳🇱

Installing
----------

```
pip install dutch-workdays
```
    
Usage
-----

```python
from dutch_workdays import Calendar
cal = Calendar()
cal.get_king_queen_day(2018)
# (datetime.date(2018, 4, 27), "King's day")
```

`dutch-workdays` works as a drop-in replacement of workalendar_, so for the
rest of the API please refer to
the `workdays documentation`_.

Why not just using Workalendar instead?
---------------------------------------

Workalendar is an awesome library, it's very complete and very well maintained
but it's, unfortunately, quite a big dependency as well. It not only includes
Python code to handle calendars from most of the world, but it also requires C
libraries to calculate high-precision astronomy computations. It's an overkill
if you only need to know about Dutch holidays.

Differences from Workalendar
----------------------------

- All the codebase is type annotated.
- Zero dependencies
- Dateutil easter calculation is vendorized.


.. _workalendar: https://github.com/peopledoc/workalendar
.. _workdays documentation: https://peopledoc.github.io/workalendar/
