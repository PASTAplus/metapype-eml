# Metapype change log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.3] 2021-07-16
### Added
- Test for non-valid EML in `test_eml.py`.
### Changed/Fixed
- Changed from using protected methods/attributes to public
  methods/attributes in method `_validate_children` of `rule.py`.
- Fixed case where children index values may be out of range in method
  `_validate_children_choice` of `rule.py`.

## [0.0.4] 2021-08-30
### Added
- New method `Rule._validate_rule_child()` for verifying node child cardinality. 
### Changed/Fixed
- Refactored `Rule._validate_children` using recursion to simplify logic, including
  rewriting key `Rule` methods `_validate_choice()` and `_validate_sequence()`.
- Refactored `Rule.get_child_index()` to use `_rule_children_names` when
  calculating the insertion index of new node children.

## [0.0.5] 2021-09-01
### Changed/Fixed
- Converted build CI to use GitHub Actions from Travis CI.

## [0.0.6] 2021-09-08
### Changed/Fixed
- Reverted roleRule to allow any string content.
- Fixed mixed content type textRule where zero length content was allowed; zero
  length content should result in a MetapypeException.