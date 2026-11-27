# oca-skills

Claude skills for working with the OCA conventions. Each skill is standalone:
none of them depends on an Odoo skill.

## Skills

| Skill | Status |
| --- | --- |
| `oca-git` | done |
| `oca-security` | done; derived from `odoo-security` and rewritten; rules in `generic.md`, `16-to-19.md` and `20-and-later.md` |
| `oca-guidelines` | done; versions 16.0 to 20.0 in `versions/` |
| `oca-web-guidelines` | done; JavaScript, Owl templates and CSS |
| `oca-migration` | done; migrating a module between 16.0 and 20.0 |
| `oca-review` | done; drafts a review for a person to verify and post |

Planned for a second batch: `oca-module-docs`, `oca-new-module`, `oca-ci`.
`oca-ci` would run pre-commit and the module tests locally as the CI does. Two
lessons to start from: use the Python version the CI pins, and read the
`tests.result` line rather than the tail of the log.

## Install (Claude Code)

```bash
scripts/install.sh --project ~/src/my-repo  # for one repository only (recommended)
scripts/install.sh                          # for all your projects
```

Prefer `--project` if you work on more than OCA. The global install removes and
replaces `~/.claude/skills/<name>` for each OCA skill.

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