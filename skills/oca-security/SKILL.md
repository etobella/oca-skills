---
name: oca-security
description: >-
  Security audit of an OCA addon for Odoo 16.0 to 20.0: access control
  (ir.model.access, record rules, ir.access, field groups, sudo), SQL and
  domain injection, eval and pickle, public methods and RPC, controller auth
  and CSRF, XSS, file access, cr.commit, swallowed errors, and access tests.
  Use when reviewing a pull request or auditing a module in an OCA
  repository, or when judging whether a specific construct (a sudo, raw SQL,
  a route, a commit) is safe, even if the user does not say "security".
---

# Security audit of an OCA addon

Audit an addon for the Odoo-specific ways access control and injection go
wrong. When a feature needs more access than the access rules give, it gets
the least access, in the narrowest scope, with a comment that says why. A
silent widening (a bare `sudo()`, a loosened access row) is a finding.

These rules are complete on their own. They do not depend on any Odoo skill.

## Protocol

1. Find the Odoo version the code targets, in this order:
   - the git branch: OCA names it after the version, `20.0` or `20.0-<topic>`
     (for a pull request, its base branch);
   - else `version` in the module's `__manifest__.py` (`20.0.1.0.0` is 20.0);
   - else, if you have an Odoo checkout, `version_info` in `odoo/release.py`
     (that is the version of the checkout, which may not be the module's).
   If they disagree, trust the branch (in a migration the manifest keeps the
   old version until it is bumped), and say which source you used.
2. Read [guidelines/generic.md](guidelines/generic.md): the rules that hold
   in every version.
3. Read the file of the version. It has the access model of that version and
   a table of constructs, with what to check before recommending each one.

   | Module version | Read |
   | --- | --- |
   | 16.0, 17.0, 18.0, 19.0 | [guidelines/16-to-19.md](guidelines/16-to-19.md) |
   | 20.0 and later | [guidelines/20-and-later.md](guidelines/20-and-later.md) |
   | 15.0 or older, or unknown | none: say the version is not covered and apply only `generic.md` |

4. Sweep the addon for every pattern in the table, and judge each hit
   against its section. A hit is not a finding by itself: the section says
   what makes it one.
5. Report each finding with a severity, the exact file and line, and the
   smallest fix. A fix must use only what the version has.

6. For a finding that an outsider could exploit, read
   [guidelines/reporting.md](guidelines/reporting.md) before writing a public
   PR, issue or comment about it.

The audit is complete when every pattern has been swept and every hit judged.

| Sweep for | Judge against |
| --- | --- |
| `security/` files: `ir.model.access.csv`, record rules, groups | [Access control principles](guidelines/generic.md#access-control-principles) and [Access control in 16 to 19](guidelines/16-to-19.md#access-control-in-16-to-19) |
| `security/ir.access.csv` | [Access control principles](guidelines/generic.md#access-control-principles) and [Access control in 20 and later](guidelines/20-and-later.md#access-control-in-20-and-later) |
| `base.default_user`, or `groups_id` / `implied_ids` in a data file that is not `noupdate` | [Access control principles](guidelines/generic.md#access-control-principles) (groups on the default user template) |
| a check on `vals` in `def create(` before `super().create(` | [Create overrides that check vals](guidelines/generic.md#create-overrides-that-check-vals) |
| `sudo(`, `with_user(`, `with_company(` | [Do not over-sudo](guidelines/generic.md#do-not-over-sudo) |
| `cr.execute`, `SQL(`, `.format`, `%` or an f-string near SQL | [Use the ORM and parameterize SQL](guidelines/generic.md#use-the-orm-and-parameterize-sql) |
| `cr.commit(`, `cr.rollback(` | [Never commit the transaction](guidelines/generic.md#never-commit-the-transaction) |
| `except` with `pass`, or a broad `except Exception` | [Do not swallow errors](guidelines/generic.md#do-not-swallow-errors) |
| a domain built from a request, an RPC call or a stored value | [Domain injection](guidelines/generic.md#domain-injection) |
| public (no `_`) model methods | [Default to private methods](guidelines/generic.md#default-to-private-methods) |
| `@http.route(`, `@route(` | [Routes, auth, POST and CSRF](guidelines/generic.md#routes-auth-post-and-csrf) |
| `innerHTML`, `insertAdjacentHTML`, `markup(`, `Markup(`, `t-raw` | [Prevent XSS](guidelines/generic.md#prevent-xss) |
| password, token or secret fields | [Field-level access](guidelines/generic.md#field-level-access) |
| `related=` that crosses models | [Field-level access](guidelines/generic.md#field-level-access) |
| `open(` | [Open files with file_open](guidelines/generic.md#open-files-with-file_open) |
| `eval(`, `exec(`, `safe_eval` | [Never eval](guidelines/generic.md#never-eval) |
| `pickle` | [Never pickle](guidelines/generic.md#never-pickle) |
| `getattr(`, `setattr(` on records | [getattr and setattr](guidelines/generic.md#getattr-and-setattr) |
| `==` comparing a secret or a token | [Timing attacks](guidelines/generic.md#timing-attacks) |
| `def f(..., x=[])`, `x={}` | [Mutable default arguments](guidelines/generic.md#mutable-default-arguments) |
| methods that return rich objects | [Do not return complex objects](guidelines/generic.md#do-not-return-complex-objects) |
| tests of a feature that grants or refuses access | [Test the access as the user who has it](guidelines/generic.md#test-the-access-as-the-user-who-has-it) |

## If an Odoo skill is also loaded

`odoo-security` is written for the Odoo repository and for its newest
version. For an OCA addon use this skill. If you apply something from the
Odoo one, check it against the constructs table of the module's version
first.