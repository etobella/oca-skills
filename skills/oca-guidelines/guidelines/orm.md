Recommended habits. The OCA guide does not write these down, but reviewers
raise them: they avoid bugs and slow code that passes tests and degrades on
real data.

# Recordsets and context

- A recordset or a collection is a boolean: write `if records:`, not
  `if len(records) > 0:`.
- Do not read a non-relational field on a multi-record set (it raises):
  iterate or use `mapped`. Guard a single-record assumption with
  `self.ensure_one()`.
- No record found is an empty recordset, never `None`:
  `return self.env["library.book"]`. `env.ref(xmlid, raise_if_not_found=False)`
  does return `None`: test it before using it.
- Never build `'&'` or `'|'` prefix lists by hand: combine domains with the
  helpers of the version (see
  [Check the version before using an API](python.md#check-the-version-before-using-an-api)).
- Propagate context with `with_context(...)`. Prefix the keys that are
  specific to a module: a stray `default_<field>` in the context leaks into
  unrelated `create` calls.
- Delegation inheritance (`_inherits`) inherits fields, not methods. Avoid
  it when you can.
- A method that another module overrides goes in its own small method;
  do not split code for extension points that do not exist yet.
- Do not use `odoo.http.request` in models: it does not exist in crons, RPC,
  tests or the shell. Pass what the model needs from the controller.

# Computes, onchange and constraints

- `create` accepts a list of values (`@api.model_create_multi`).
- `@api.depends` lists **every** field the compute reads. A stored compute
  needs correct dependencies and no side effects.
- `@api.onchange` only works in the UI: never rely on it for data
  integrity. Enforce invariants with `@api.constrains` or with SQL
  constraints, declared the way the version expects.

# End the order on a unique field

`_order` ends with a field that is unique per record, usually `id`:
`sequence, id`, `name, id`, `date desc, id desc`. The ORM adds no tiebreaker:
records equal on every field of `_order` come back in the order PostgreSQL
chooses, which can change between queries. A paged list then shows a record
on two pages and another on none, and `search(..., limit=1)` or `records[0]`
returns a different record from one run to the next. When records come back
in a random order, add the tiebreaker to `_order`; do not change the test so
that it stops reading the order.

# Set a state, never flip it

A method that changes a state sets a fixed state, named by the method
(`action_confirm`) or passed as an argument. A state that goes both ways has
one method per direction (`action_publish`, `action_unpublish`). No method
reads the current value to write its opposite.

```python
# good
def action_publish(self):
    self.is_published = True

# bad: a double click or a retried call undoes the first one
def action_toggle_published(self):
    for book in self:
        book.is_published = not book.is_published
```

A button that shows both states is two buttons, each visible in one state.
The rule is for new methods: an existing flip method keeps its behavior.

# Batch the ORM calls

An ORM call inside a loop over records is one query per iteration: `search`,
`search_count`, `_read_group` and `create` alike. Make one call for the whole
collection.

```python
# bad: one INSERT per record
for vals in vals_list:
    self.env["library.book"].create(vals)

# good
self.env["library.book"].create(vals_list)
```

```python
# bad: one count query per author
for author in authors:
    author.book_count = Book.search_count([("author_id", "=", author.id)])

# good: one grouped query, then a lookup
counts = {
    author.id: count
    for author, count in Book._read_group(
        [("author_id", "in", authors.ids)], ["author_id"], ["__count"],
    )
}
for author in authors:
    author.book_count = counts.get(author.id, 0)
```

- A loop that only computes in memory on fields already read is fine.
- Iterate the recordset, or `browse` all the ids first, so that the ORM
  prefetches each field for the whole set. A `browse(id)` loop defeats the
  prefetch.
- Put conditions in the search domain, not in `filtered()` on the result.
  Pre-map results into a dict instead of nested loops, and use a `set` for
  membership tests.

# Do not read an x2many that grows without bound

Do not read an x2many that can reach thousands of rows over the life of the
record (messages, followers, logs) to count it, test it or take a few of its
records: reading it loads every id and keeps it in cache, and the cost grows
with the age of the record, so it passes the tests and gets slow in an old
database. Ask the comodel instead: `search_count` to count, `search` with a
`limit` to take a few, `_read_group` for a count per record.

```python
# bad
if len(book.loan_ids) > 25:
    ...
# good
Loan = self.env["library.loan"]
if Loan.search_count([("book_id", "=", book.id)], limit=26) > 25:
    ...
```

An x2many that stays small (tags, lines of a payment term) is read directly,
and so is one that the code needs whole, such as when copying a record with
its lines.
