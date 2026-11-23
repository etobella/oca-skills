Rules for Odoo 20.0 and later, on top of `generic.md`. A module of this range
has `version` starting with `20.0.` or a higher number. For 21.0 and later the
constructs below were written against 20.0: check each one in the source of
the version.

# Access control in 20 and later

From 20.0 the access rows and the record rules are one model, `ir.access`,
loaded from `security/ir.access.csv`. A module with `ir.model.access.csv`
rows or `ir.rule` records that was not converted is a migration left
unfinished: say so, and check whether those files still load.

Columns as Odoo documents them for its newest version: `id`, `name`,
`model_id`, `group_id/id`, `operation` and `domain`. Check the header of an
existing file in the source of the version.

- `operation` is a subset of the letters `c`, `r`, `u`, `d` (`r`, `cru`,
  `crud`...). A row applies to exactly the operations it lists.
- `domain` limits the row to the records that match, as a record rule did.
- **Rows with a group are permissions.** They add up over the groups the
  user belongs to, and the domain of a row limits only what that row grants.
- **Rows with no group are restrictions.** They apply to every user, all of
  them must match, and they never grant anything. Restrictions that do not
  overlap can lock everyone out.
- A model with no permission row is inaccessible. Granting to everyone,
  portal and public users included, is done with the everyone group.

What to flag:

- Any `c`, `u` or `d` granted to the everyone, portal or public group; look
  closely at `r` on a model with sensitive data.
- A restriction that lists only some operations (see
  [Access control principles](generic.md#access-control-principles)): the
  operations it does not list are governed by the permissions alone.
- A multi-company model with no restriction row whose domain is
  `[('company_id', 'in', company_ids)]`. `company_ids` is the user's allowed
  companies; add `+ [False]` when the company is optional.
- A sensitive model with permissions only: add a restriction with a domain.

# Where to check create values in 20 and later

Do the check in an override of `_prepare_create_values`, on what its
`super()` returns. That runs before the record is created and the values
already hold the defaults of the context and the `ir.default` ones, so you
do not handle them by hand. Check that the method exists in the version.

# Constructs in 20 and later

These come from the newest Odoo guidelines. Check each one in the source of
the module's version before you recommend it.

| Construct | Use |
| --- | --- |
| `fields.Domain` | Combine domains with `domain &= Domain(...)`, `|`, `~`, or `Domain.AND` and `Domain.OR` for a list. Never concatenate lists or write `'&'` and `'|'` by hand. |
| `groups=fields.NO_ACCESS` | Hides a secret field from everyone, administrators included. Otherwise `base.group_system`. |
| `@api.private` | Marks a public-named method as not callable by RPC when renaming it would break callers. The RPC guard also refuses names with a `_`, class methods and static methods. |
| `odoo.tools.SQL`, `SQL.identifier`, `Query.select(SQL(...))` | Build SQL with parameters. `SQL.identifier` validates a name with `assert`, so a run with `-O` skips the check: never feed it raw user input. `_search(...)` with `Query.select` keeps the access rules and `active`. |
| `_allow_sudo_commands = False` | On the comodel, stops x2many commands from running with sudo. |
| `t-raw` | Does not exist in the server QWeb or in OWL: any occurrence is broken legacy code. The raw-HTML path is a `Markup` value that reaches `t-out`. |
| `t-esc` | A deprecated alias in OWL that still escapes. The server QWeb ignores it and prints nothing: a bug, though not an XSS. |
| Route `type` | `'jsonrpc'` and `'json2'`. They have no CSRF token by design; the JSON content type protects them. `'json'` is a deprecated alias (19.0). |
| `safe_eval` | The extra whitelist sandbox of the newest versions (`--unsafe-policy`) only observes by default: do not count on it as protection. |
| Invalidating the cache in a test | `self.env.invalidate_all()`. |