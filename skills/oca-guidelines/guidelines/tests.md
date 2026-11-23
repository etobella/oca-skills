# What to test

- A bug fix comes with a test that fails without the fix. It proves the
  fix works in every case and that the bug does not return.
- A new module, or an addition, should ideally test all the functions it
  defines. The coverage report comments on the pull request: if coverage
  went down, a test is probably missing.
- Use `TransactionCase` (`HttpCase` for the web). Assert behavior, not
  implementation.

# Tests that silently do not run

- The file is named `test_*.py` **and** is imported from `tests/__init__.py`.
- The test class is defined in that file: a class only imported into it is
  skipped.
- A test with a typo in its name, or without the `test_` prefix, never runs.

# Avoid flaky tests

A flaky test passes and fails on different runs without a change in the
code, because of races, external services or non-deterministic behavior.

- **`subTest` pollution.** The database transaction and the cache are not
  reset between subtests, and some decorators (such as `@users`) are
  implemented with subtests. A test that creates a record with a fixed login
  fails on the second run with a duplicate key.

  ```python
  class TestSomething(TransactionCase):
      @users("admin", "demo")
      def test_something(self):
          # bad: the second run fails with a duplicate key on login
          self.env["res.users"].create({"name": "Foo", "login": "foo"})
  ```
- **Dynamic dates.** Do not depend on `datetime.now()` or `datetime.today()`.
  Fix the date, for example with `freezegun`:

  ```python
  @freeze_time("2024-01-01 10:10:10")
  def test_creation_time(self):
      ...
  ```

  A frozen Python clock does not move the time the cursor reports: a record
  created in a `TransactionCase` can keep the real time of the start of the
  test class in `create_date` or `write_date`. Where the test case offers
  `mock_datetime_and_now`, use it to freeze both (see
  [Check the version before using an API](python.md#check-the-version-before-using-an-api)).
- **External services.** Mock them, so that a slow or down service does not
  fail the test. Use `unittest.mock.patch`, the patch helpers of the test
  case where the version has them (`self.patch`, `cls.classPatch`), or
  `vcrpy` to record and replay HTTP. What you test is your code, not the
  service; to cover a bug of the service, test the buggy behavior with a
  mock.
- **A test that must use the real service** (to detect that its API
  changed) is marked with the standard tags `-standard` (skipped by default)
  and `external` (`external_l10n` for localizations), and is run on its own:
  `odoo -i my_module -d my_database -u my_module --test-tags=external,external_l10n`.
- **Demo data.** Another module can change it, so a test that relies on it
  gets false results. Create the data inside the test.

# Test with the lowest permissions

Tests run without permission restrictions by default, which gives false
positives: the real users that follow the same flow can hit access errors.
Test with the lowest permissions that can do the action:
`new_test_user` and `users` help with that, and setting `uid` or `env` in
`setUpClass` constrains the rest of the test.

Beware of the `env` that a record carries. A record kept in a class variable
has an `env` with the cursor, the user, the sudo state and the context it
was created with, and changing the test user does not change it:

```python
@users("test_portal")
def test_cannot_read(self):
    # KO: self.partner.env.uid is not self.uid, and nobody notices
    self.assertRaises(AccessError, self.partner.read)
    # OK: bring the record into the environment of the test
    partner = self.partner.with_env(self.env)
    self.assertRaises(AccessError, partner.read)
```

# Example modules

An example module that showcases the features of a module is named
`<module_name>_example` (`cms_form` and `cms_form_example`), so that the
coverage analysis ignores it by default.
