TODO
====

* Import public API in __init__ files.
* Document public API in a User Guide.
* Define public vs private API.


Won't Fix
=========

* Fix bug with etree XML library (not happening anymore, keep and eye on it.).
* Patch in line numbers for etree parser (too fragile).
* Change grammar to directly change paths to pathlib.Path instead of strings (this would break environment variables inside the path).
