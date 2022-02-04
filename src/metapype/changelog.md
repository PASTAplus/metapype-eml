# Metapype change log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
