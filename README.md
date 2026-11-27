# oca-skills

Claude skills for working with the OCA conventions. Each skill is standalone:
none of them depends on an Odoo skill.

## Skills

| Skill | Status |
| --- | --- |
| `oca-git` | done |
| `oca-security` | done; derived from `odoo-security` and rewritten; rules in `generic.md`, `16-to-19.md` and `20-and-later.md` |
| `oca-guidelines` | done; only `versions/20.0.md` exists so far |
| `oca-web-guidelines` | done: Will handle topics related to JS | 
| `oca-migration` | done: Will handle migrations |
| `oca-review` | pending: Will handle how to make a review |

Planned for a second batch: `oca-module-docs`, `oca-new-module`, `oca-ci`.

## Install (Claude Code)

```bash
scripts/install.sh                          # for all your projects
scripts/install.sh --project ~/src/my-repo  # for one repository only
```

Restart Claude Code or open a new session.

## Test it

```bash
python3 -m unittest discover -s tests -v    # tests of the validator
python3 scripts/check_skills.py             # format, links and anchors of the skills
```

The real test, in Claude Code: ask it to "write the commit message for this
change in an OCA module". It should follow the format in
`skills/oca-git/SKILL.md`.

A GitHub workflow (`.github/workflows/ci.yml`) runs the same checks on every
push and pull request. It has not been run on GitHub yet.

## Why they do not inherit from the Odoo skills

Odoo publishes its skills inside each branch of `odoo/odoo`, and they all have
the same name (`odoo-guidelines` in 20.0, in 21.0...). Only one of them can be
loaded on a machine, and there is no way to ask for "the one of the module's
version". That is why the OCA skills carry their complete rules. The Odoo
skills are useful as reading material when writing a new skill, with no
automatic dependency.