# Tasks to do in every migration

- Bump the version of the module to `<target>.1.0.0` (`19.0.1.0.0`).
- Remove the migration scripts of the previous version: the `migrations`
  folder of the module, if it exists.
- Remove the references in `CREDITS.rst` to past migrations financed by other companies.
- Squash the administrative commits (those of bots) into the commit before
  them, to reduce the noise. It is optional, and for someone comfortable with
  squashing in git.
- Apply the framework changes of the target version: the rules of the
  `oca-guidelines` skill for that version, and then the file of the version
  of this skill.
- Add tests to increase the code coverage of the module.
- For each method that calls `super`, check that the method still exists in
  the upstream dependencies and is not dead code. For each overridden method,
  check that its signature and keywords are kept in this version, or adapt it.
- A migration to another major version of Odoo probably needs a migration
  script for the data (the path of OpenUpgrade). If you do not write it, leave
  a note in the README about the changes that need migration, so that a later
  contributor can write it without analyzing every change again.
- Do the rest of the changes the module needs to work in the new version.
- When you jump several versions, do the tasks of every version in between.
  Check also the guides of the past versions for things that were not done in
  earlier migrations.

# Tasks not to do

- **Change the copyright year.** A line like `# Copyright 2024 ACME Ltd -
  Johnny Glamour` says "copyright from 2024". There is no need to change the
  year to the current one.
- **Change the original authors.**

# Check before the pull request

- Run `pre-commit run -a` again once the module is adapted, and fix what it
  reports, the pylint errors you ignored at the formatting step included.
- Run the tests of the module.
- Check that the commit that adapts the module is `[MIG] <module>: Migration
  to <version>`, and the formatting one `[IMP] <module>: pre-commit auto
  fixes`.
