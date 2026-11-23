`$repo` is the OCA repository that hosts the module, `$module` its name,
`$user_org` your GitHub login or organization, `$to` the target version
(`19.0`) and `$from` the version of the branch the module comes from (`18.0`).

# Before migrating

- Update yourself with the latest OCA conventions:
  <https://odoo-community.org/page/contributing>.
- Subscribe to the mailing list of the project that owns the repository:
  <https://odoo-community.org/groups>.
- On the GitHub issue of the repository named "Migration to version `$to`",
  announce which modules you want to migrate.
- Install pre-commit:
  <https://github.com/OCA/maintainer-tools/wiki/Install-pre-commit>.

# The git process

The module is brought from the branch of the previous version, with its
history, and then adapted.

```
git clone https://github.com/OCA/$repo -b $to
cd $repo
git checkout -b $to-mig-$module origin/$to
git format-patch --keep-subject --stdout origin/$to..origin/$from -- $module | git am -3 --keep
pre-commit run -a   # linters and formatters; ignore the pylint errors at this stage
git add -A
git commit -m "[IMP] $module: pre-commit auto fixes" --no-verify
```

- Do all the formatting in that one commit, the first time.
- There may be nothing to commit after pre-commit. Then ignore the message
  "nothing to commit".
- To reduce the commits that come from "OCA Transbot", see
  <https://github.com/OCA/maintainer-tools/wiki/Merge-commits-in-pull-requests>.

Then adapt the module to the target version (see the tasks in `tasks.md` and
the file of the version), and upload it:

```
git add --all
git commit -m "[MIG] $module: Migration to $to"
git remote add $user_org git@github.com:$user_org/$repo.git   # needs an SSH key in your GitHub account
# or
git remote add $user_org https://github.com/$user_org/$repo.git   # asks for user and password each time
git push $user_org $to-mig-$module --set-upstream
```

# If the module is renamed

Rename the whole commit history. If you do not, the next version brings only
the latest commit, because the commands above follow the old name.

With older versions of git:

```
git filter-branch --tree-filter 'if [ -d $module ]; then mv $module $new_module_name; fi' HEAD
git rebase origin/$to
```

With newer ones:

```
git filter-repo --path-rename $module/:$new_module_name/ --refs HEAD --force
```

# A patch that does not apply

The process can stop with `error: ...: patch does not apply`. One cause is a
patch that removes a whole file, which `git am` cannot resolve. Add
`--ignore-whitespace` to the `git am` command: the conflicts that remain are
solved the usual way.

```
git am --abort
git format-patch --keep-subject --stdout origin/$to..origin/$from -- <module path> | git am -3 --keep --ignore-whitespace
# resolve the conflicts (for example git rm <file>)
git add --all
git am --continue
```

# Open the pull request

Follow the link that git prints after the push, or see how to create a pull
request from a fork in the GitHub documentation. Name it
`[$to][MIG] <module>: Migration to $to`, so that it can be found and nobody
duplicates the work.
