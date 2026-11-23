---
name: oca-migration
description: >-
  Migrating an OCA module to another Odoo version, 16.0 to 20.0: the git
  process (format-patch, am, pre-commit, the [MIG] commit, the pull request),
  the tasks to do and not to do, and what is specific to each target version
  (scripts and tools). Use when a module has to be migrated or ported to
  another version, when a branch or a PR is named "<version>-mig-<module>" or
  "[<version>][MIG]", or when asked how to move a module from one OCA branch to
  the next, even if the user does not say "migration".
---

# Migrating an OCA module

The steps to move a module from one version branch of an OCA repository to
the next one, and the chores that go with it. The changes to the framework
code of each version are not here: they are the rules of the `oca-guidelines`
skill, in its `versions/<N>.md` file for each version.

## Protocol

1. Find the Odoo version the code targets, in this order:
   - the git branch: OCA names it after the version, `20.0` or `20.0-<topic>`
     (for a pull request, its base branch);
   - else `version` in the module's `__manifest__.py` (`20.0.1.0.0` is 20.0);
   - else, if you have an Odoo checkout, `version_info` in `odoo/release.py`
     (that is the version of the checkout, which may not be the module's).
   If they disagree, trust the branch (in a migration the manifest keeps the
   old version until it is bumped), and say which source you used.
2. The target is covered when it is over 16.0. For
   another target, say so and apply only the common files.
3. Read [guidelines/procedure.md](guidelines/procedure.md) for the git
   process, and [guidelines/tasks.md](guidelines/tasks.md) for the tasks that
   every migration has.
4. For the target version read its file here: `versions/<target>.md`. 
   Then read `versions/<target>.md` of the
   `oca-guidelines` skill and apply every change in it to the module. If that
   skill is not loaded, say so and ask for it: do not guess the changes.
5. If the module is more than one version behind, repeat step 4 for every
   version in between, in order: for a module of 16.0 that goes to 19.0, the
   versions 17.0, 18.0 and 19.0. OCA asks for the tasks of all of them. Ask
   the user whether to migrate version by version (one pull request each) or
   in one jump: the guides only describe taking the module from the branch of
   the previous version.
6. Finish with [Check before the pull request](guidelines/tasks.md#check-before-the-pull-request).

| Guideline | Read it when |
| --- | --- |
| [Before migrating](guidelines/procedure.md#before-migrating) | starting a migration |
| [The git process](guidelines/procedure.md#the-git-process) | taking the module from the previous branch, committing, pushing |
| [If the module is renamed](guidelines/procedure.md#if-the-module-is-renamed) | the module changes its name in the migration |
| [A patch that does not apply](guidelines/procedure.md#a-patch-that-does-not-apply) | `git am` stops with `patch does not apply` |
| [Open the pull request](guidelines/procedure.md#open-the-pull-request) | the branch is pushed |
| [Tasks to do in every migration](guidelines/tasks.md#tasks-to-do-in-every-migration) | adapting the module |
| [Tasks not to do](guidelines/tasks.md#tasks-not-to-do) | before touching copyright lines or authors |
| [Check before the pull request](guidelines/tasks.md#check-before-the-pull-request) | the module is adapted |
