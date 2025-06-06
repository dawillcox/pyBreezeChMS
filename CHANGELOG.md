# Change log for breeze_chms_api

## 1.0.1
Initial version. Derived from  [PyBreezeChMS](https://github.com/alexortizrosado/pyBreezeChMS).
* Release: 29 Apr 2023
* Version 1.0.1.1 is identical, just fixing urls in PyPI.

## 1.1.0
Adding some new methods for profile fields.
* Release: 29 Aug 2023

## 1.2.0
Adding profile_helper with methods to simplify extracting field values from profiles.

## 1.3.0 6 Nov 2023
Adding config_file_list()

## 1.3.0 13 Dec 2023
Cleaning up some unit tests.
Adding list_form_fields() method.

## 1.4.0
Add support for config_file_list()
Much cleanup of unit tests.

## 1.4.1 18 Jan 2024
Adding remove_form_entry() method.

## 1.4.2 21 Mar 2024
Issue #4: Fix exception in list_funds() with no parameter.

## 1.4.3 28 Aug 2024
Add some parameters to list_events().

## 1.4.4 10 Dec 2024
Deal with name when only first is present. (Issue #7.)

## 1.4.4.1 15 Dec 2024
Fix misunderstanding about how Breeze sets the "first_name" profile field. (Issue #8.)

## 1.4.4.2 6 Jan 2025
Fix mishandling of two-line address field. (Issue #9.)
Don't use this version.

## 1.4.4.3 6 Jan 2025
Fix mishandling of two-line address field,
handle both old and new Breeze coding. (Issue #9.)
