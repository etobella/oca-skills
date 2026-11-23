Rules for the JavaScript tests and the tours of Odoo 16.0 and 17.0, on top of
`generic.md`. In this range the unit tests use QUnit; Hoot starts in 18.0
(see `tests-hoot.md`).

# QUnit tests in 16 and 17

- A test file goes in `static/tests/` of the addon. The runner is QUnit, and
  you reach it at the URL `/web/tests`.
- Declare each test file in the bundle `web.qunit_suite_tests`, in the
  `assets` key of the manifest:

  ```python
  "assets": {
      "web.qunit_suite_tests": [
          "my_addon/static/tests/my_feature_tests.js",
      ],
  },
  ```
- Group related tests with `QUnit.module(...)` and write each one with
  `QUnit.test("name", async function (assert) { ... })`.
- Never commit `QUnit.only(...)`: it stops every other test from running.
  The test suite of Odoo itself fails when it finds one.
- The utilities and the mock server of the web client (which answers the
  usual model methods, such as `read` and `search_read`) come in the bundle
  `web.tests_assets`: use them instead of calling a real server.
- For the rule about absence checks see
  [Pair every absence check with a positive one](generic.md#pair-every-absence-check-with-a-positive-one).

# Tours in 16 and 17

A tour is an integration test: it plays a real scenario, so that the Python
and the JavaScript parts are checked together.

- Register the tour with `tour.register`, imported from `web_tour.tour`, with
  the starting `url` and `test: true`, and the list of steps:

  ```js
  /** @odoo-module **/
  import tour from "web_tour.tour";

  tour.register("my_feature_tour", {
      url: "/web",
      test: true,
  }, [
      // the steps
  ]);
  ```
- A step has a `trigger`, the selector of the element to act on: the tour
  waits until it exists and is visible. It can have an `extra_trigger`, a
  second condition that is waited for but is not acted on, a `run`, the action
  to do on the trigger, and a `content`, which is logged and helps to debug.
- When a step has no `run`, in this range the tour sets the text if the
  trigger is an input, and clicks it otherwise.
- Start the tour from a Python test: make the test class inherit from
  `HttpCase` and call `self.start_tour("/web", "my_feature_tour", login="admin")`.
- Check how the tours of the version you work on are written before you copy
  one: 16.0 and 17.0 do not register them in exactly the same way.
