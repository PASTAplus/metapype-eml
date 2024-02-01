# Metapype change log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## (0.0.28) 2024-01-31
### Changed/Fixed
- Fix bug in `metapype_io.to_xml()` where recursive call did not include `skip_ns` argument.

## (0.0.27) 2024-01-18
### Changed/Fixed
- Add parameter to to_xml() to allow skipping rendering of namespaces. Used by ezEML when
  displaying XML in complex text editing.

## (0.0.26) 2023-11-29
### Changed/Fixed
- Add checking for missing data table Record Delimiter, Size, MD5 Checksum, and/or Number of Records.

## (0.0.25) 2023-04-18
### Changed/Fixed
- Add tab character (x09) to list of whitespace characters to ignore in element content. 

## (0.0.24) 2023-01-05
### Changed/Fixed
- Renamed RULE_NONEGATIVEFLOAT to RULE_ANYNONNEGATIVEFLOAT for pattern consistency.
- Changed validation rule used by PRECISION node from RULE_ANYSTRING to RULE_ANYNONNEGATIVEFLOAT.
- Add RULE_ANYFLOAT validation rule.
- Test for PRECISION node.

## (0.0.23) 2022-12-19
### Changed/Fixed
- Drop logging from INFO to DEBUG in `validate.py`

## (0.0.22) 2022-12-09
### Changed/Fixed
- Evaluate `title` node only if in `dataset` subtree (`evaluate.py`).

## (0.0.21) 2022-10-11
### Changed/Fixed
- Add explicit "collapse" param to _process_element and from_xml functions.

## (0.0.20) 2022-09-01
### Changed/Fixed
- Update environment.
- Add test for provenance-based datasource metadata.

## (0.0.19) 2022-04-22
### Changed/Fixed
- Remove studyAreaDescription element from the parent project in EML. This
  allows downstream clients (i.e., ezEML) where this element was not currently 
  supported.

## [0.0.18] 2022-04-16
### Changed/Fixed
- Support leaf-node with empty content in  `metapype_io.to_xml()`.

## [0.0.17] 2022-03-01
### Changed/Fixed
- Fix extra space issue in `metapype_io.to_xml()` when model has inconsistent nsmap.

## [0.0.16] 2022-02-24
### Changed/Fixed
- Coerce all Node.content to be of type str unless it is None.

## [0.0.15] 2022-02-24
### Changed/Fixed
- Revert "remove extraneous space prefix for nsmap and extras in `metapype_io.to_xml()`"

## [0.0.14] 2022-02-20
### Changed/Fixed
- Support `Node.shift` to occur outside the same sibling type
- Remove extraneous space prefix for nsmap and extras in `metapype_io.to_xml()`

## [0.0.13] 2022-02-20
### Changed/Fixed
- Update environment

## [0.0.12] 2022-02-20
### Changed/Fixed
- ~~Support `Node.shift` to occur outside the same sibling type~~
- ~~Remove extraneous space prefix for nsmap and extras in `metapype_io.to_xml()`~~

## [0.0.11] 2022-02-04
### Added
- Add `metapype_io` support to import XML "tail" content into a Node.tail attribute
- Add `metapype_io` support to export Node.tail attribute content to export XML
- Add support to retain literal content in source XML.

## [0.0.10] 2021-12-16
### Added
- Add the "annotation" child element to dataTable and otherEntity rules.
### Changed/Fixed
- Change logging to debug in prune function.

## [0.0.9] 2021-11-03
### Added
- Add support for text type elements.
### Changed/Fixed
- Fixed the "prune" capabilities to better create metapype-valid models from imported
  EML XML documents.

## [0.0.8] 2021-09-22
### Added
- Add support for geographic coverage altitude.
### Changed/Fixed
- Fixed interpretation of 0 in `is_float()`.

## [0.0.7] 2021-09-15
### Changed/Fixed
- Add taxonIdRule validation support.
- Improve rule failure analysis for validation of choice actions.

## [0.0.6] 2021-09-08
### Changed/Fixed
- Reverted roleRule to allow any string content.
- Fixed mixed content type textRule where zero length content was allowed; zero
  length content should result in a MetapypeException.

## [0.0.5] 2021-09-01
### Changed/Fixed
- Converted build CI to use GitHub Actions from Travis CI.

## [0.0.4] 2021-08-30
### Added
- New method `Rule._validate_rule_child()` for verifying node child cardinality. 
### Changed/Fixed
- Refactored `Rule._validate_children` using recursion to simplify logic, including
  rewriting key `Rule` methods `_validate_choice()` and `_validate_sequence()`.
- Refactored `Rule.get_child_index()` to use `_rule_children_names` when
  calculating the insertion index of new node children.

## [0.0.3] 2021-07-16
### Added
- Test for non-valid EML in `test_eml.py`.
### Changed/Fixed
- Changed from using protected methods/attributes to public
  methods/attributes in method `_validate_children` of `rule.py`.
- Fixed case where children index values may be out of range in method
  `_validate_children_choice` of `rule.py`.

## [Unreleased]
