Rules that hold in every Odoo version. Where a rule depends on the version,
it says so and points to the file of the version: `16-to-19.md` or
`20-and-later.md`.

# Access control principles

Audit the access rules (`security/`) with an attacker's eyes. How the rules
are written depends on the version: see "Access control" in the file of the
version.

- **Default deny.** A model with no rule that grants access is inaccessible
  to users.
- **Open groups.** Flag any create, write or delete granted to everyone, to
  portal users or to the public user. Look closely at even read access on a
  model with personal or business-sensitive data.
- **Partial restrictions.** A restriction that covers only some operations
  leaves the others to the grants alone. If a grant allows `write`, a
  restriction that only hides records from `read` does not stop an attacker
  from changing them: `write` checks write access, never read access. Cover
  every operation that needs restricting.
- **Multi-company and sensitive models.** A multi-company model needs a
  company restriction. A sensitive model needs a restriction by domain, not
  only a grant by group.

# Create overrides that check vals

A `create` override that validates `vals` before `super().create()` (for
instance to reserve some fields or values for a group) can be bypassed when
it reads only `vals`. The ORM adds values after that code runs:

- the `default_<field>` keys of the context: a caller refused `book_id` in
  `vals` passes `default_book_id` in the context instead;
- the `ir.default` records, which any internal user can add for themselves;
- what an override of `default_get` adds, and the precomputed fields.

So:

- Do the check on the values after the defaults have been added. Where that
  step is depends on the version: see "Where to check create values" in the
  file of the version.
- A check after `super().create()` is too late: the record exists, and a
  caller that catches the `AccessError` keeps it.
- Check the value, not its presence. The values that reach the check hold
  the `default=` of the field, so `if vals.get('book_id'):` also refuses a
  create where the caller gave no `book_id` and the field has a default.
  Check which book it is, and whether this user may set it.
- `write` has no such gap: it adds no defaults.

# Field-level access

- The `groups` attribute of a field removes it from the views and from
  `fields_get`, and makes a direct read or write raise. Use it on sensitive
  fields; do not rely on the view to hide them.
- **Passwords and API tokens:** restrict them to the system group
  (`base.group_system`). A token field on a model with a permissive access
  rule is readable by any user through `search_read`. To hide a field from
  everyone, administrators included, see the constructs table of the version.
- **`related` fields are computed with sudo by default** (`related_sudo`). A
  related field that reaches sensitive data through a many2one the user can
  write lets the user point it at any record and read the related value with
  elevated rights. Set `related_sudo=False` on sensitive chains. (A related
  field made writable runs in the user's environment and is
  access-checked: a different issue.)

# Default to private methods

- A public method (no `_` prefix) is callable by RPC with arguments the
  attacker chooses. Neither the records in `self` nor the parameters can be
  trusted, because access control is enforced on create, read, write and
  delete, not on method calls. Start every method with `_`. Drop the `_`
  only for a method that must be called from outside, and then validate its
  inputs.
- A `_` method is not a control by itself: one that is fed untrusted data
  is still dangerous.
- The RPC layer refuses names that start with `_`. Check that before you
  flag a public-looking method as exposed. If renaming would break callers,
  see the constructs table of the version for a way to mark the method as
  not callable by RPC.

# Use the ORM and parameterize SQL

- Do not use the cursor when the ORM can do the work. Raw SQL skips access
  rules, translations, cache invalidation and `active` handling.
- When SQL is unavoidable, never build it with `+`, `%` or `.format`, or
  with an f-string. Pass the values as parameters and let the driver format
  them (a tuple for `IN %s`). The driver decides how to quote a value, not
  you.

  ```python
  # bad: injection, and it is not your job to format a list of ids
  cr.execute("SELECT id FROM library_book WHERE author_id IN (" +
             ",".join(map(str, ids)) + ")")

  # good
  cr.execute("SELECT id FROM library_book WHERE author_id IN %s",
             (tuple(ids),))
  ```
- Table and column names cannot be parameters. Take them from a fixed list
  in the code, or from the identifier helper of the version if it has one,
  and never feed them raw user input.
- To run your own SQL over rows the ORM already filters, build the query
  with the ORM so that access rules and `active` stay in force.

# Never commit the transaction

- The framework owns the transaction: it commits when the call returns and
  rolls back when it fails. A `cr.commit()` or `cr.rollback()` in the middle
  leaves partial changes that a later error cannot undo. That breaks data
  integrity and, on a security check, can leave an action done that was
  refused.
- It is acceptable only on a cursor you opened yourself, which you must
  then roll back on error and close, with a comment that says why it is
  needed and why it is safe. Without that comment, it is a finding.
- To protect a block that may fail, use `with cr.savepoint():`, not a
  commit. Tests and transient models need no commit either.

# Do not swallow errors

- `except ...: pass` makes the code go on as if nothing failed, and it can
  swallow the `AccessError` or `ValidationError` that was the check. Catch
  the specific exception over the smallest block.
- If ignoring an exception is really safe, log it with the reason, for
  example `_logger.debug("why this is safe", exc_info=True)`.

# Domain injection

- Combine domains with the helpers of the version (see the constructs table
  of the version), never by concatenating a list a user gave with a
  security domain. Domains are in prefix notation: a user list placed first
  can start with `'|'` and turn the whole domain into "anything OR
  security". Placed after, it stays ANDed, but its conditions can still
  follow relations, and under `sudo()` that probes records the user cannot
  read. Validate or whitelist what a user sends, in either order.

# Do not over-sudo

- `sudo()` is the main risk. Review each use twice, above all in
  controllers and public methods, and never use it to silence an access
  error. For each one, make sure an attacker controls no part of:
  - **read:** the model, the record or the field;
  - **create:** the model or the values;
  - **write:** the model, the record or the values;
  - **search:** the model, the domain, or an injection in it.
- In a controller never write `record.sudo().write(post)` with raw request
  parameters. Whitelist the keys:
  `{k: post[k] for k in ("name", "email") if post.get(k)}`.
- Under `sudo()` the x2many command payloads in `vals` also run with sudo on
  the comodel, where the version lets it: a sudo write with raw request
  values moves the privilege into other models. Whitelist command lists
  too, and see the constructs table of the version.
- Avoid a sudo-computed `related` field onto `ir.attachment`: an arbitrary
  `attachment_id` becomes an arbitrary file read. Use a plain `Binary`, or
  create and search `ir.attachment` so the ORM applies its access rights.
- A `with_user` or `with_company` switch must be intentional, never driven
  by the attacker.

# Routes, auth, POST and CSRF

- Match `auth` to the exposure of the route. A `public` or `none` route must
  not expose internal data or do a privileged write.
- A route that writes uses `methods=['POST']`. On an HTTP route keep CSRF
  on: `csrf=False` only for a dedicated webhook. JSON-RPC routes have no
  token by design; the JSON content type is their protection. The name of
  the route `type` for JSON depends on the version.
- A state change on a GET route is a CSRF hole: a crafted link or an
  auto-submitted form performs it as the logged-in victim.
- A template that posts a form includes
  `<input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>`.

# Prevent XSS

- Reflected XSS (a script in the URL or parameters) and stored XSS (a script
  saved by a low-privilege user) both run with the victim's session, which
  is much more than `alert()`.
- **Server side:** render with `t-out`, which escapes. For `t-raw`, which
  prints raw HTML, see the constructs table of the version. The raw-HTML
  path is a `Markup` value that reaches `t-out`. Build HTML by wrapping
  literals in `markupsafe.Markup` and formatting user content into them
  (`Markup` escapes what it formats). An f-string defeats that:
  `Markup(f"<p>{x}</p>")` is unsafe, `Markup("<p>{x}</p>").format(x=x)` is
  not.
- **JavaScript:** the sinks are `el.innerHTML = ...`, `insertAdjacentHTML`
  and OWL `markup()` on a value that is not a literal. Never give them a
  string a user influences. Escape it, use the escaping tagged-template form
  of `markup`, use the framework helpers for HTML, or render with `t-out`.
- **Escaping and sanitizing are different.** Escaping (text to code) is
  always required when data is mixed with code, even trusted data.
  Sanitizing (code to safer code) is for untrusted code only, and works only
  after escaping.

# Open files with file_open

- Never call the builtin `open()` on a path anyone can influence: it can
  read or write any file of the host (configuration, SSH keys, Python that
  runs later). Use `odoo.tools.file_open()`, which limits access to the
  addons paths, the Odoo root and registered temporary directories. It is a
  path limit, not a write protection.

# Never eval

- Never use `eval` or `exec`. To parse data use `json.loads()` or
  `ast.literal_eval()`. At worst `odoo.tools.safe_eval.safe_eval` with a
  narrow namespace and only for trusted, privileged users: it still gives
  broad capabilities.

# Do not return complex objects

- A public model method that returns a rich object (a crypto key, a backend
  handle) can be used from `safe_eval` code, such as server actions and
  automation rules: that code calls the method and walks the
  single-underscore attributes of the result to read files or run code. Do
  not put such logic in a model method. Use a module-level function, or give
  the method a double-underscore name, which `safe_eval` cannot reach.

# getattr and setattr

- Do not read or write a field by a dynamic name with `getattr` or `setattr`:
  that exposes private attributes and methods (`__class__`, then
  `__globals__`, then `__import__`, then remote code). Use `record[name]`,
  and still validate the record and the field name.

# Never pickle

- `pickle` runs arbitrary code when it loads data. Never unpickle data you
  do not fully control. Exchange and store data with `json`.

# Timing attacks

- Compare a secret or a token with `odoo.tools.consteq`, not `==`, which
  stops at the first difference and leaks it through timing. Better still,
  look the token up in the database with a search.

# Mutable default arguments

- Do not use a mutable default (`def f(x, vals=[])`). It persists between
  calls and can leak or accumulate data.

# Test the access as the user who has it

A security feature without a test run as the restricted user is unproven.
Tests run with full rights by default, which hides access errors that real
users hit.

- Write the test with the lowest permissions that can do the action: create
  a user with `new_test_user` and run the step with `@users(...)` or
  `with_user`.
- A record kept in a class attribute carries its own `env` (user, cursor,
  context, sudo state). Changing the test user does not change it: a read on
  that record still runs as the setup user, so the test passes on code that
  fails in production. Bring the record into the test environment first
  (`record.with_env(self.env)`).
- Invalidate the cache right before the restricted step. A field already in
  cache is returned without checking access, and the setup leaves in cache
  what it created. The call to use is in the constructs table of the
  version.
- Test the refusal too: assert that the forbidden operation raises
  `AccessError`, not only that the allowed one works.
