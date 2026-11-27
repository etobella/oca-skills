---
name: oca-review
description: >-
  Review a pull request, a commit or a module of an OCA repository against the
  OCA rules: dispatch each changed file to the matching OCA skill, judge the
  change on its merits with the OCA review questions, and draft the review
  comment with its review type and a proposed verdict. Use when asked to
  review, approve, check or comment a pull request of an OCA addon, a
  migration PR such as "[20.0][MIG] module: Migration to 20.0", or to say
  whether a change is ready to merge, even if the user does not say "review".
---

# Reviewing an OCA addon

A review has two passes. The rules, which live in the OCA skills named below,
are the floor. The change is then judged on its merits, as its author's most
sceptical colleague would; that pass finds most of the blocking defects. The
skill drafts the review: it does not merge, and it does not publish the
comment.

| Skill | Covers |
| --- | --- |
| `oca-guidelines` | every file outside `static/`: manifest, structure, Python, XML, `readme/`, tests, and its file for the version |
| `oca-web-guidelines` | every file under `static/`: JavaScript, Owl templates, SCSS, JS tests and tours |
| `oca-security` | `security/`, `sudo()`, raw SQL, `eval`, public or RPC-callable methods, routes, access tests |
| `oca-git` | commit messages, the title and the branch of the PR, `.po` files and generated files |
| `oca-migration` | a migration PR: branch `<version>-mig-<module>` or title `[<version>][MIG]` |

If one of them is not loaded, say so and ask for it. Do not review that part
from memory.

## Process

1. **Scope.** Work in a local checkout of the revision under review. Pin its
   commit and the base it is compared against, and take the diff from the
   checkout, never from a saved copy: branches move and PRs get force-pushed.
   Every file the review reads, in the diff or around it, comes from that
   checkout. Read the `__manifest__.py` of each touched module (its purpose,
   its `depends`), the commit messages, and the description and the comments
   of the PR.
2. **Version.** The base branch of the PR is the version (see
   [The branch is the version](#the-branch-is-the-version)).
3. **Map.** List every changed file with the skill sections that apply to it,
   taken from the tables of those skills. Every file maps to at least one:
   Python always gets the Imports and the Naming of `oca-guidelines`,
   anything under `static/` gets `oca-web-guidelines`, a file of `tests/`
   gets the Tests, and the commits and the title of the PR get `oca-git`. A
   file left without a section is a mapping mistake to fix, never a file
   without rules.
4. **Read.** Open every mapped section, and the file of the version of each
   skill, before you write the first finding.
5. **Rules pass.** Judge the diff against the sections read. A rule marked
   *Recommended* gives a suggestion, never a blocking finding (see
   [A finding](guidelines/report.md#a-finding)).
6. **Merits pass.** Ask the questions of
   [Questions of the OCA review](guidelines/merits.md#questions-of-the-oca-review),
   hunt for the input that breaks each hunk, and look for the code the diff
   never shows (see the two sections of that file).
7. **Report.** Draft the review as
   [guidelines/report.md](guidelines/report.md) says.

The review is complete when every changed file is mapped, every mapped
section has been read, every hunk has had both passes, and every finding
names its section or its failure scenario.

## The branch is the version

In OCA every branch is one Odoo version. The base branch of the PR (`17.0`)
says which version file each skill reads. For a migration PR the base is the
target version.

Before you flag or write an API or an attribute, confirm that it exists in the
revision under review: search the source, or a usage of it at that revision
(`git grep`), rather than trust a remembered API. The version files of the
skills say which API belongs to which version.

## A migration PR

- The commits that come from the previous branch are not new code. Review the
  commits that adapt it: the formatting one, `[IMP] <module>: pre-commit auto
  fixes`, and `[MIG] <module>: Migration to <version>`.
- Check the migration against `oca-migration`: the tasks that every migration
  has, the tasks that are not to be done (the copyright year and the original
  authors stay as they are), and the file of the target version.

| Guideline | Read it when |
| --- | --- |
| [Questions of the OCA review](guidelines/merits.md#questions-of-the-oca-review) | every review |
| [Be strict when](guidelines/merits.md#be-strict-when) | the change has no reason, no documentation or no tests |
| [What the description says](guidelines/merits.md#what-the-description-says) | reading the PR description or the readme of a new module |
| [Hunt for the input that breaks it](guidelines/merits.md#hunt-for-the-input-that-breaks-it) | the merits pass of every hunk |
| [Code the diff never shows](guidelines/merits.md#code-the-diff-never-shows) | a method, field, name or key changes |
| [Tone](guidelines/report.md#tone) | writing the comment |
| [Review type and verdict](guidelines/report.md#review-type-and-verdict) | choosing how to label the review |
| [Approvals](guidelines/report.md#approvals) | saying whether the PR can be merged |
| [A finding](guidelines/report.md#a-finding) | writing each finding |
| [Close the report](guidelines/report.md#close-the-report) | finishing the comment |

## If an Odoo skill is also loaded

`odoo-review` is written for the Odoo repository. For an OCA addon use this
skill: the OCA questions, the version rules and the way to report replace its
own.