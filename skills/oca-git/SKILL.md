---
name: oca-git
description: >-
  Git conventions for OCA repositories (github.com/OCA/*): commit message
  tags and format, branch and pull request naming, migration PRs, bot and
  Weblate commits. Use this whenever the repository belongs to the Odoo
  Community Association, when writing or amending a commit message,
  choosing a branch, or opening or updating a pull request on an OCA addon,
  including migration PRs such as "[20.0][MIG] module: Migration to 20.0".
---

# OCA git conventions

These rules are complete on their own. They do not depend on any Odoo skill.

## Commit message

The first line is `[TAG] module: summary`.

- **Module:** the technical name of the module the commit changes. Say the
  part of the code touched (module, library, transversal object) in the body
  too, with a description of the change.
- **Summary:** 50 characters or fewer, in the imperative present ("Fix
  formatting", "Remove unused field", never "Fixes" or "Fixed"). "bugfix" or
  "improvements" alone are not summaries.
- **Too long:** GitHub cuts a long first line with an ellipsis in the PR
  (`[FIX] module_foo: and this is my very long m[...]`). Shorten it and move
  the explanation to the body.
- **Body:** lines of 80 characters or fewer, in English. Say why the change
  is made and what it affects: the diff already shows what changed.
- **Tags:** the ones of the Odoo git guidelines, plus `[MIG]`.

  | Tag | Use |
  | --- | --- |
  | `[FIX]` | bug fix |
  | `[IMP]` | improvement |
  | `[ADD]` | new module |
  | `[REF]` | refactoring |
  | `[REM]` | removed resources: dead code, views, modules |
  | `[MOV]` | files or code moved without content change |
  | `[REV]` | revert of an earlier commit |
  | `[PERF]` | performance |
  | `[MIG]` | migration of a module to another Odoo version |

- **One logical change per commit.** Do not add commits like "Fix pep8",
  "Code review" or "Add unittest" to repair commits of the same PR: fold
  them into the commit they fix.
- **Do not mix modules.** Avoid a commit that changes many modules; split by
  module so that one can be reverted alone.
- **Tickets:** OCA has no `task-`, `opw-` or `runbot-` references: never
  write one and never invent one. Link a GitHub issue of the repository with
  `Fixes #123`.
- **Author:** Authors must be real people, not bots, and their name and email
  should be correctly set in the commit metadata. Do not use generic or
  placeholder names and emails. Never put an AI tool in `Co-authored-by:`.
- **AI trailer:** if any AI was involved in the commit, from advice to fully
  autonomous coding, add an `Assisted-by:` trailer, one line per tool or
  model and no blank line between them. It is binary: it either had AI
  involvement or it did not, so never write a percentage or a level.

  ```
  Assisted-by: Claude Opus 4.6
  Assisted-by: GitHub Copilot:gpt-5
  ```
- **Version:** do not change `version` in `__manifest__.py` in a fix or
  feature commit. The bot bumps it at merge. Only a migration sets it (see
  `oca-guidelines`, "Version numbers and migrations").

## Pull requests

- **Title:** `[<version>][<TAG>] <module>: <summary>`. A migration is
  `[20.0][MIG] <module>: Migration to 20.0`, so it can be found and nobody
  duplicates the work.
- **Same rules as a commit:** the title is the first line of the merge
  commit and the description is its body.
- **Target:** the version branch where the change is needed (`17.0`,
  `18.0`, `20.0`...). A change needed on another version is ported by hand,
  with its own PR against that branch.
- **From a fork:** push to a fork, personal or of an organization, and open
  the PR against `OCA/<repo>`.
- **Branch name:** a migration branch is `<version>-mig-<module>`, for
  example `20.0-mig-library_book`.
- **A bug fix comes with a test** that fails without the fix.
- **AI disclosure:** when any AI was used, say so in the description (the
  title does not need it), with the same `Assisted-by:` lines as the commits.
- **A security hole:** do not open a public PR whose test or text shows how
  to exploit it before reading the reporting rules of `oca-security`.
- **Stale:** a PR with no activity for 6 months will be closed automatically.

## AI assistance and the OCA AI policy

The OCA AI policy (`AI_POLICY.md` of the OCA organisation) holds for every
contribution, and an agent working here follows it:

- A human reads, understands and takes responsibility for every line, and
  supervises the agent. Unsupervised agentic work is not permitted.
- Do not post AI-generated review comments or summaries as they are: a
  person verifies and owns them (see `oca-review`).
- A patch is small: the reference point is under 30 lines in a single file.
  More than 500 lines needs a maintainer's agreement beforehand.
- Default red lines, any one of which triggers scrutiny and two of which
  trigger rejection: more than 5 PRs or 10 reviews from one source in 24
  hours; a contribution over 500 lines without prior agreement; repeated
  iterations that regenerate code instead of answering the review. The PSC
  may set other limits: check before a large batch.
- **Pace yourself.** With a backlog of fixes (a queue of PRs to file), never
  open them all at once. Open at most 5 in 24 hours counting the ones the
  same person already opened, keep the rest queued, and wait for a response
  before sending the next. Say what is left in the queue.

## Migration commits

- The migration itself is one commit: `[MIG] <module>: Migration to <version>`.
- The first formatting pass, made once for all files, is a separate commit:
  `[IMP] <module>: pre-commit auto fixes`.
- Commits that come from the history of the previous version keep their
  messages, as `git am --keep` leaves them.

## Bots and generated files

- Translations from Weblate, version bumps and generated files are committed
  by bots. Do not amend them. When asked to reduce the noise of a PR, squash
  the administrative commits into the commit before them.
- Do not touch `.po` files in a PR (Weblate owns them; only a new module may
  bring its own), and do not edit the module's `README.rst` by hand (it is
  built from `readme/`: edit the fragments there). Do commit the `README.rst`
  that the `oca-gen-addon-readme` pre-commit hook regenerates, for instance
  after a migration: without it, pre-commit fails in the CI.

## Merging someone else's work

Keep their authorship (`--author`, as `git log` shows it) and use their
commit message when they wrote a good one.

## If an Odoo skill is also loaded

`odoo-git` is written for the Odoo repository. Where it disagrees with this
skill, this one wins: ignore its `task-` and `opw-` trailers, its
forward-port and target-branch rules, and its stable-branch policy.

## Examples

A fix in an OCA addon. No task reference, and the issue is linked only
because it exists:

```
[FIX] library_book: keep the title when the author is removed

Steps to reproduce:
- Create a book with an author
- Remove the author and save

The title is emptied. It should stay as it was.

The title was computed from the author even when the field had been
written by hand.

Fixes #123
```

A migration: `[MIG] library_book: Migration to 20.0`, in a PR titled
`[20.0][MIG] library_book: Migration to 20.0`.
