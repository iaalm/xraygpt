# X-Ray DB adaptor lib

X-Ray operates like a concordance for kindle device, listing most commonly used character names, locations, themes, or ideas, which are sorted into the two main categories of "People" and "Terms".


## X-Ray DB file
Assume you have a file named `name.epub`, then the X-Ray DB file should be store as name.sdr/XRAY.entities.{ASIN}.asc, with [ASIN](https://en.wikipedia.org/wiki/Amazon_Standard_Identification_Number) of the book. This file is a sqlite3 database file.


## DB schema

```sql
CREATE TABLE string(id INTEGER, language TEXT, text TEXT);
CREATE TABLE source(id INTEGER, label INTEGER, url INTEGER, license_label INTEGER, license_url INTEGER, PRIMARY KEY(id));
CREATE TABLE entity(id INTEGER, label TEXT, loc_label INTEGER, type INTEGER, count INTEGER, has_info_card TINYINT, PRIMARY KEY(id));
CREATE TABLE entity_description(text TEXT, source_wildcard TEXT, source INTEGER, entity INTEGER, PRIMARY KEY(entity));
CREATE TABLE type(id INTEGER, label INTEGER, singular_label INTEGER, icon INTEGER, top_mentioned_entities TEXT, PRIMARY KEY(id));
CREATE TABLE entity_excerpt(entity INTEGER, excerpt INTEGER);
CREATE TABLE excerpt(id INTEGER, start INTEGER, length INTEGER, image TEXT, related_entities TEXT, goto INTEGER, PRIMARY KEY(id));
CREATE TABLE occurrence(entity INTEGER, start INTEGER, length INTEGER);
CREATE TABLE book_metadata(srl INTEGER, erl INTEGER, has_images TINYINT, has_excerpts TINYINT, show_spoilers_default TINYINT, num_people INTEGER, num_terms INTEGER, num_images INTEGER, preview_images TEXT);
CREATE INDEX idx_occurrence_start ON occurrence(start ASC);
CREATE INDEX idx_entity_excerpt ON entity_excerpt(entity ASC);
CREATE INDEX idx_entity_type ON entity(type ASC);
```

## Reference
This project highly inspired by:
[X-Ray Creater](https://github.com/szarroug3/X-Ray_Calibre_Plugin/tree/master)
[WordDumb](https://github.com/xxyzz/WordDumb/blob/master/x_ray.py)
