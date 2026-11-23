---
name: oca-web
description: >-
  Conventions for the JavaScript, Owl templates and CSS of an OCA addon, Odoo
  16.0 to 20.0, Owl components only: where files go, hooks and reactivity of
  Owl 2 and Owl 3, patching, RPC calls, assets, icons, SCSS, and tour and test
  rules. Use when you write, review or move files under static/src/ or
  static/tests/ of an OCA repository, add an Owl component, a template or a
  tour, or ask how to extend the web client, even if the user does not say
  "JavaScript".
---

# OCA web guidelines

Rules for the web framework code an OCA addon ships in `static/src/` and
`static/tests/`: JavaScript, Owl templates (XML) and SCSS. They do not apply to
`static/lib/`, which holds vendored libraries. They are complete on their own
and do not depend on any Odoo skill.

Only Owl components are covered. If the code is a legacy widget (it extends
`Widget` or `AbstractField`, or uses the old `odoo.define` classes instead of
an Owl component), say so and do not apply these rules to it.

## Protocol

1. Find the Odoo version the code targets, in this order:
   - the git branch: OCA names it after the version, `20.0` or `20.0-<topic>`
     (for a pull request, its base branch);
   - else `version` in the module's `__manifest__.py` (`20.0.1.0.0` is 20.0);
   - else, if you have an Odoo checkout, `version_info` in `odoo/release.py`
     (that is the version of the checkout, which may not be the module's).
   If they disagree, trust the branch (in a migration the manifest keeps the
   old version until it is bumped), and say which source you used.
2. Read [guidelines/generic.md](guidelines/generic.md): the rules that hold in
   every version. Read the sections that match the code you touch, not the
   whole file.
3. Read the file of the version. It says which Owl you are writing for and
   what is specific to that range.

   | Module version | Read |
   | --- | --- |
   | 16.0, 17.0, 18.0, 19.0 | [guidelines/16-to-19.md](guidelines/16-to-19.md) |
   | 20.0 and later | [guidelines/20-and-later.md](guidelines/20-and-later.md) |
   | 15.0 or older, or unknown | none: say the version is not covered and apply only `generic.md` |

4. If you write or change a JavaScript test or a tour, read also the tests
   file of the version. Its limit is not the one of Owl:

   | Module version | Read |
   | --- | --- |
   | 16.0, 17.0 (QUnit) | [guidelines/tests-qunit.md](guidelines/tests-qunit.md) |
   | 18.0 and later (Hoot) | [guidelines/tests-hoot.md](guidelines/tests-hoot.md) |

5. Before you use an API of the constructs table of the version, check that
   the source of the module's Odoo version has it.

| Guideline | Read it when |
| --- | --- |
| [JavaScript basics](guidelines/generic.md#javascript-basics) | writing or formatting any JS file |
| [File layout](guidelines/generic.md#file-layout) | creating a file, or deciding where new code lives |
| [Patching Odoo code](guidelines/generic.md#patching-odoo-code) | extending or overriding behavior that already exists |
| [Batch RPCs](guidelines/generic.md#batch-rpcs) | calling the server from a loop, or twice for one user action |
| [Order concurrent calls](guidelines/generic.md#order-concurrent-calls) | sending a request each time the user acts on the same state |
| [End a sort comparator on a unique key](guidelines/generic.md#end-a-sort-comparator-on-a-unique-key) | writing a comparator for `sort()` or `toSorted()` |
| [Avoid getters](guidelines/generic.md#avoid-getters) | adding a computed value to a class or a component |
| [Give every icon a role and a label](guidelines/generic.md#give-every-icon-a-role-and-a-label) | adding or changing an icon in a template |
| [Assets](guidelines/generic.md#assets) | adding an image, a font or a library |
| [CSS and SCSS](guidelines/generic.md#css-and-scss) | touching `*.scss` or `*.css` |
| [Pair every absence check with a positive one](guidelines/generic.md#pair-every-absence-check-with-a-positive-one) | asserting in a test or a tour that an element is absent |
| [QUnit tests in 16 and 17](guidelines/tests-qunit.md#qunit-tests-in-16-and-17) | adding or registering a JS unit test in 16.0 or 17.0 |
| [Tours in 16 and 17](guidelines/tests-qunit.md#tours-in-16-and-17) | writing a tour in 16.0 or 17.0 |
| [Hoot unit tests in 18 and later](guidelines/tests-hoot.md#hoot-unit-tests-in-18-and-later) | adding or registering a JS unit test in 18.0 or later |
| [Tours in 18 and later](guidelines/tests-hoot.md#tours-in-18-and-later) | writing a tour in 18.0 or later |
| [Hoot: absence checks](guidelines/tests-hoot.md#pair-every-absence-check-with-a-positive-one) | asserting absence in a Hoot test or a tour of 18.0 or later |
| [Freeze the time when a test meets a timer](guidelines/tests-hoot.md#freeze-the-time-when-a-test-meets-a-timer) | a Hoot test that types in a search, opens a delayed popover or debounces |

## If an Odoo skill is also loaded

`odoo-web-guidelines` is written for the Odoo repository and for its newest
version. For an OCA addon use this skill. Where they disagree (patching,
formatting, file names), this one wins.