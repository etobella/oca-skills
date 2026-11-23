# Imports

Let the pre-commit configuration of the repository sort the imports
(`isort` or its replacement) and keep what it produces. The groups, each
sorted alphabetically:

1. standard library
2. known third-party libraries, one per line
3. `odoo` (`from odoo import api, fields, models`)
4. `odoo.addons.*`, rarely and only if necessary
5. local imports, in the relative form (`from . import utils`)
6. unknown third-party libraries

`__init__.py` may keep imports that look unused (`F401`); nowhere else.

# Naming and model layout

- A class is UpperCamelCase: `class AccountInvoice(models.Model)`.
- A model `_name` is dotted, lowercase and singular: `sale.order`, not
  `sale.orders`.
- Variables are `snake_case` and meaningful. One letter only in a lambda, a
  loop index or a pure maths expression. Constants are `UPPER_SNAKE_CASE`.
- A variable that holds a model is **not** CamelCase. Do not suffix a
  variable with `_id` or `_ids` unless it holds ids:

  ```python
  res_partner = self.env["res.partner"]
  partners = res_partner.browse(ids)
  partner_id = partners[0].id
  ```
- A `Many2one` ends in `_id`; a `One2many` or `Many2many` ends in `_ids`.
- Do not write `string=` on a field when the automatic label (the name with
  underscores as spaces, capitalized) is the label you want.
- A default is a lambda that calls a method, so that it can be inherited:
  `default=lambda self: self._default_name()`. A direct function reference
  cannot be overridden.
- Method patterns: `_compute_<field>`, `_inverse_<field>`,
  `_search_<field>`, `_default_<field>`, `_onchange_<field>`,
  `_check_<constraint>`. An action method starts with `action_` and, when it
  works on one record, with `self.ensure_one()`.
- Order inside a model class:
  1. private attributes (`_name`, `_inherit`, `_description`, `_order`)
  2. field declarations
  3. SQL constraints
  4. default methods and `default_get`
  5. compute and search methods, in the order of the fields
  6. constraint methods (`@api.constrains`), then onchange methods
  7. CRUD overrides
  8. action methods
  9. other business methods

# Idioms

- Readability beats concision and cleverness.
- Use list and dict comprehensions, `map`, `filter` and `sum`, and the
  recordset methods (`filtered`, `mapped`, `sorted`): they are clearer and
  usually faster.
- Raise `UserError`, or a more appropriate class of `odoo.exceptions`.
- A docstring says the purpose of a method, not a summary of its code. A
  comment explains what is not obvious. Many comments usually mean code
  that needs refactoring.
- A function that is too long, or too indented because of loops, is split
  into smaller functions.
- Names, comments and docstrings are in English. Text shown to users in
  other languages goes through the translation system.
- When a call, dict, list or tuple does not fit on a line, break after the
  opening symbol, indent by four spaces, and end every line with a comma,
  the last one included, so that adding an element changes one line:

  ```python
  partner_id = fields.Many2one(
      "res.partner",
      required=True,
  )
  ```
- Use a named argument when its meaning is not obvious at the call.
- Prefer `%` with named placeholders (`"%(name)s"`) over `.format()`: it
  translates better and is safer.

# Translate only static literals

- Translate a literal string and pass the values as arguments, with named
  placeholders when there are several, so that translators can reorder them:

  ```python
  # good
  raise UserError(_("Record %s cannot be modified", record.display_name))
  # bad: formats before the lookup, so no exported term matches
  raise UserError(_("Record %s cannot be modified" % record.display_name))
  # bad: formats after the lookup, so the placeholder is not validated
  raise UserError(_("Record %s cannot be modified") % record.display_name)
  ```
- No concatenation, f-string or `%` inside the call: the translated term is
  keyed on the exact source string.
- Never translate at module or class level: it runs at import, with no user
  language, and silently does not translate. Translate inside the method.
- A field value is translated with the `translate` flag of the field, not
  with `_()`.
- Which translation API to call (`_` or `self.env._`) depends on the
  version: see [Check the version before using an API](#check-the-version-before-using-an-api).

# SQL and the cursor

- **No SQL injection.** Never build a query with string concatenation (`+`)
  or interpolation (`%`, `.format`, f-strings). Pass the values as
  parameters: the driver (psycopg2) decides how to format them, including a
  tuple for `IN %s`.

  ```python
  # very bad
  cr.execute("SELECT DISTINCT child_id FROM account_account_consol_rel "
             "WHERE parent_id IN (" + ",".join(map(str, ids)) + ")")
  # good
  cr.execute("SELECT DISTINCT child_id FROM account_account_consol_rel "
             "WHERE parent_id IN %s", (tuple(ids),))
  ```
- **Never commit the transaction.** The framework opens a cursor per call,
  commits when the call returns and rolls back if it fails. A manual
  `cr.commit()` causes partial commits and unclean rollbacks: inconsistent
  data, documents stuck, tests that pollute the database.
  - It is acceptable only on a cursor you created yourself, which you must
    then roll back on error and close, and with a comment saying why it is
    necessary, why it is correct and why it does not break the transaction.
    Without that comment it can be removed.
  - You do not need it in `_auto_init`, in reports or in transient models.
  - To protect a block that may fail, use a savepoint:

    ```python
    try:
        with cr.savepoint():
            method1()
            method2()
    except UserError:
        _logger.debug("why this failure is safe to ignore", exc_info=True)
    ```
  - Needing a separate transaction that does commit: use a new cursor from
    the registry, a new environment on it, and explain in a comment why the
    isolated transaction is required.
- **Do not bypass the ORM.** Never use the cursor when the ORM does the same
  thing: you skip access rights, transactions and the cache, and the code is
  harder to read and less secure.

  ```python
  # wrong
  cr.execute("SELECT id FROM auction_lots WHERE auction_id IN %s "
             "AND state = %s AND obj_price > 0", (tuple(ids), "draft"))
  # better
  lots = self.env["auction.lot"].search([
      ("auction_id", "in", ids),
      ("state", "=", "draft"),
      ("obj_price", ">", 0),
  ])
  ```

# Exceptions

- Do not write `except ...: pass`. It assumes the algorithm can go on after
  the failure.
- If you really need to ignore an exception, log it with the reason:
  `_logger.debug("why this is safe", exc_info=True)`.
- Catch the specific exception over the smallest block, and let the rest
  propagate to the framework.

# Check the version before using an API

Some constructs exist only in some versions of Odoo. Before you write one,
check that the Odoo source of the module's version has it: search it
(`grep -rn "<name>"` in the Odoo checkout). If you cannot look, say that you
did not check. Never use an API the version does not have, and never assume
a rule from a different version.

| Construct | What to know |
| --- | --- |
| `ir.access`, `security/ir.access.csv` | From 20.0 they replace access rows and record rules. See `versions/20.0.md`. |
| `_sql_constraints` or `models.Constraint` and `models.Index` | Newer versions declare constraints and indexes as model attributes, and a recent master ignores `_sql_constraints`. Use what the version's source uses. |
| `_` or `self.env._` | Newer versions offer `self.env._`; the bare `_` is the older, backward-compatible form. |
| `fields.Domain` | Newer versions combine domains with it; older ones use `odoo.osv.expression`. |
| `<list>` or `<tree>` | The name of the list view tag changed between versions: use what the base views of the version use. |
| route `type` | `'jsonrpc'` and `'json2'` exist in recent versions; `'json'` is the older name (renamed in 19.0). |
| `mock_datetime_and_now`, `BaseCommon` | Test helpers of recent versions: check that they exist. |
