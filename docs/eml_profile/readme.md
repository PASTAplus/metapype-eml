# Readme.md

## EDI EML Profile

An EML profile is a subset of the EML schema that EDI plans to support. the simplest way to convey this is a list of xpaths.

This dir contains:

1. this readme
1. CSV file with these columns:`concept_name, xpath, frequency`


- **concept_name**: Mark asked for a simple name for the concept the xpath refers to. Currently, this column is a truncated, string version of the xpath itself. I am not sure what is most useful as a concept_name. options might be: 
  - general, e.g., "adminstrativeArea", where ever that node appears (1:many with xpath, a key to an array)  
  - specific, 1:1 with xpath (as it is now), so a key to an individual xpath. 
  - something else.
- **xpath**: leaf nodes only. this draft is a subset of leaf nodes in a snapshot of all contributed datasets (LTER and EDI scopes) available in July 2019. So it reflects xpaths in use.
- **frequency**: count of instances of this xpath in all docs in the snapshot`



This is a first draft to see if the format is acceptable.

Future drafts are anticipated to include
- attribute nodes added
- other xpaths added
- xpaths may be dropped

Also anticipated, here or elsewhere:
- processing scripts (sql, xsl, bash)
- dataset containing the snapshot

