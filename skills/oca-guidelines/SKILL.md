---
name: oca-guidelines
description: >-
  Coding conventions for OCA addons: module names, manifest, version numbers,
  directories and file names, hooks, external dependencies, Python style and
  model layout, SQL and cursor rules, XML ids and view inheritance, JavaScript
  and CSS basics, tests, and what changes in each Odoo version. Use whenever
  you write, review or restructure code in an OCA repository (github.com/OCA/*),
  create a module, name a file, a model, an XML id or a test, or ask whether
  something follows the OCA rules, even if the user does not say "guidelines".
---

# OCA addon guidelines

Rules for code in OCA addons. They are complete on their own and do not
depend on any Odoo skill. Rules that only matter for Odoo 12.0 or older are
not included.

## Protocol

1. Find the Odoo version the code targets, in this order:
   - the git branch: OCA names it after the version, `20.0` or `20.0-<topic>`
     (for a pull request, its base branch);
   - else `version` in the module's `__manifest__.py` (`20.0.1.0.0` is 20.0);
   - else, if you have an Odoo checkout, `version_info` in `odoo/release.py`
     (that is the version of the checkout, which may not be the module's).
   If they disagree, trust the branch (in a migration the manifest keeps the
   old version until it is bumped), and say which source you used.
2. Read the sections of the table that match the files you are touching,
   not whole files. No rule outranks another.
3. Read `versions/<version>.md` for that version, for example
   `versions/20.0.md`. If there is no file for it, say that the version is
   not covered, apply only the common rules, and treat every construct of
   [Check the version before using an API](guidelines/python.md#check-the-version-before-using-an-api)
   as unverified.

| Guideline | Read it when |
| --- | --- |
| [Module names](guidelines/modules.md#module-names) | naming or renaming a module |
| [Which module the code goes in](guidelines/modules.md#which-module-the-code-goes-in) | starting a feature: extend a module, add one, or add a bridge |
| [Manifest](guidelines/modules.md#manifest) | touching `__manifest__.py` |
| [Version numbers and migrations](guidelines/modules.md#version-numbers-and-migrations) | changing a data model, a view or a `noupdate` record, or writing a migration script (never to bump `version` in a normal PR) |
| [Directories and file names](guidelines/modules.md#directories-and-file-names) | creating, moving or naming files in an addon |
| [Installation hooks](guidelines/modules.md#installation-hooks) | `pre_init_hook`, `post_init_hook`, `uninstall_hook`, `post_load`, monkey patches |
| [External dependencies](guidelines/modules.md#external-dependencies) | a Python or binary dependency, `requirements.txt`, `oca_dependencies.txt` |
| [Translations and readme](guidelines/modules.md#translations-and-readme) | `i18n/`, `.po` files, `README.rst`, `readme/` |
| [Imports](guidelines/python.md#imports) | writing Python |
| [Naming and model layout](guidelines/python.md#naming-and-model-layout) | naming a class, model, field, method or variable; ordering a model class |
| [Idioms](guidelines/python.md#idioms) | writing or reviewing the style of Python code |
| [Translate only static literals](guidelines/python.md#translate-only-static-literals) | a user-facing string in Python |
| [SQL and the cursor](guidelines/python.md#sql-and-the-cursor) | `cr.execute`, `cr.commit`, savepoints |
| [Exceptions](guidelines/python.md#exceptions) | `try` and `except` |
| [Check the version before using an API](guidelines/python.md#check-the-version-before-using-an-api) | using an API that may not exist in the module's version |
| [Recordsets and context](guidelines/orm.md#recordsets-and-context) | reading records, building domains, passing context |
| [Computes, onchange and constraints](guidelines/orm.md#computes-onchange-and-constraints) | computes, onchange, constraints, `create` overrides |
| [End the order on a unique field](guidelines/orm.md#end-the-order-on-a-unique-field) | setting `_order` |
| [Set a state, never flip it](guidelines/orm.md#set-a-state-never-flip-it) | a method or button that changes a state |
| [Batch the ORM calls](guidelines/orm.md#batch-the-orm-calls) | `create`, `search` or aggregates inside a loop |
| [Do not read an x2many that grows without bound](guidelines/orm.md#do-not-read-an-x2many-that-grows-without-bound) | counting or sampling messages, logs, lines that can reach thousands |
| [Record format](guidelines/xml.md#record-format) | writing any XML record |
| [XML ids](guidelines/xml.md#xml-ids) | naming a view, action, menu, group, rule or data record |
| [Inheriting views](guidelines/xml.md#inheriting-views) | extending or replacing an existing view |
| [Data, demo data and filters](guidelines/xml.md#data-demo-data-and-filters) | `data/`, `demo/`, `ir.filters` |
| [Security files](guidelines/xml.md#security-files) | touching `security/` |
| [JavaScript and CSS](guidelines/xml.md#javascript-and-css) | touching `static/` |
| [What to test](guidelines/tests.md#what-to-test) | fixing a bug, adding a module, touching `tests/` |
| [Tests that silently do not run](guidelines/tests.md#tests-that-silently-do-not-run) | adding a test file or class |
| [Avoid flaky tests](guidelines/tests.md#avoid-flaky-tests) | dates, external services, `subTest`, demo data in a test |
| [Test with the lowest permissions](guidelines/tests.md#test-with-the-lowest-permissions) | a test of access, users or groups |
| [Example modules](guidelines/tests.md#example-modules) | adding a module that only showcases a feature |

For a security audit use the `oca-security` skill, and for commits and pull
requests the `oca-git` skill, when they are loaded.

## Minimal action

By default, only modify the necessary files and avoid changes in other files if not necessary for the specific change.

## If an Odoo skill is also loaded

`odoo-guidelines` is written for the Odoo repository and for its newest
version. For an OCA addon use this skill. Where they disagree (names of
variables, order of a model, directory names, XML ids of groups and rules,
`position="replace"`), this one wins.
