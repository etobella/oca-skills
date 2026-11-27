# Questions of the OCA review

Answer each one for the change under review. A question that cannot be
answered from the checkout is said so in the report; it is not guessed.

- **Is the module generic enough to be part of the community addons?** A
  change that serves one customer, or one company, belongs somewhere else.
- **Does it duplicate the features of other community addons?** Look in the
  addons paths you have, and say when you could not look further than them.
- **Does the documentation let a reader understand what the module does and
  how to use it?** It lives in the fragments of `readme/` (see
  [What the description says](#what-the-description-says)).
- **Is the problem addressed the right way, with good concepts?** A design
  flaw, technical or of the business, is a finding even when the code is
  clean.
- **Are there use cases?** A new feature without one has no way to be
  judged.
- **Is there any setup in the code?** There should not be: a value an
  integrator must choose is a setting, not a constant.
- **Is there demo data?** If there is, it lives in `demo/` and its ids end in
  `_demo`.
- **Are the commit messages short, clear and clean?** The rules are in
  `oca-git`.
- **Do the rules of the maturity level of the module hold?** They are in
  <https://odoo-community.org/page/development-status>. A change that lowers
  what the level promises is a finding.

# Be strict when

Be strict, and say so with the reason, in these cases:

- the origin, or the reason, of the patch is not documented well;
- the description of the module is missing or does not fit what it does (see
  the next section);
- the tests are not all green, or are not adapted to the change. Having tests
  is very much encouraged: a bug fix without a test that fails without the fix
  is a finding;
- there is an issue with the license, the copyright or the authorship;
- the OCA and Odoo conventions are not respected;
- the code design or the best practices are not.

# What the description says

The description of a module, and the text of a change, explain **why**, not
**what**: the diff already shows what. A description that only repeats what
the code does is not enough.

The description of a pull request should be clear enough for the reader to
understand its purpose and, when it applies, contain a demo, so that other
people can run and test the code.

# Hunt for the input that breaks it

The rules are the floor, not the ceiling. For every changed hunk, look for the
input or the state that makes it wrong:

- edge values, rounding and timezones;
- an empty recordset and a call on several records;
- concurrency, and the second run of the same code;
- what the change costs at scale: a query or an RPC inside a loop that grows
  with the data.

Then check three claims: that what the commit message says is what the code
does, that the tests would fail without the change, and that the PR description
matches the diff. Give this pass the same effort as the rules pass.

# Code the diff never shows

Odoo modules extend each other, and in OCA they are spread over many
repositories that depend on each other (`oca_dependencies.txt`, and the
`depends` of the manifest). Anything the diff changes may be used by code it
never shows: methods are overridden, fields and XML ids are referenced,
templates are called and inherited, and data dictionaries and context keys are
produced in one place and read in another, in Python and in JavaScript. For
each changed method, field, template or key, look for its consumers in every
addons path you have, and confirm they still hold.

- **Overrides.** Search `git grep "def <name>("` and read them: do they still
  call `super()` with valid arguments, and does the new behavior hold with
  what they add?
- **Renamed or removed names.** Search them in Python, XML and JavaScript. A
  stale reference in a view, a domain, an xpath, a `patch()` or an import
  fails only at runtime, or only when the module that holds it is installed.
- **Shared contracts.** A template, a dictionary or a context key read in one
  place is produced in others. A new key, or a changed requirement, must be
  met by every producer, including the JavaScript twin of a Python one.
- **Other repositories.** Say which repositories you could not look into.
