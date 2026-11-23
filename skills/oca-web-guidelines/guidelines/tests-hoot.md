Rules for the JavaScript tests and the tours of Odoo 18.0 and later, on top
of `generic.md`. From 18.0 the unit tests use Hoot, the test framework of the
web client. The helper names below come from the newest Odoo: check that the
version you work on has each one in its source before you use it.

# Hoot unit tests in 18 and later

- A test file goes in `static/tests/` of the addon, and its name ends in
  `.test.js`. A `.hoot.js` file is not a test: it is a module shared by the
  whole test run. Any other JavaScript file is read as production code or as
  a test helper.
- Include the files in the bundle `web.assets_unit_tests`, with a glob:

  ```python
  "assets": {
      "web.assets_unit_tests": [
          "my_addon/static/tests/**/*",
      ],
  },
  ```
- Run the tests at the URL `/web/tests`, which the debug menu opens with "Run
  Unit Tests".
- Import the test framework from `@odoo/hoot`, only in unit tests. Import
  the DOM helpers from `@odoo/hoot-dom`: they can also be used in tours.
- Each test file runs in an isolated environment, wrapped in a `describe`
  named after the path of the file:

  ```js
  import { describe, expect, test } from "@odoo/hoot";

  test("my first test", () => {
      expect(1 + 1).toBe(2);
  });
  ```
- In 18.0 the QUnit suite and Hoot can coexist while the tests are migrated.
  Write new tests in Hoot, and do not convert existing QUnit tests only
  because you touch their file.

# Tours in 18 and later

- Register the tour in the registry, with its steps as a function:

  ```js
  import { registry } from "@web/core/registry";

  registry.category("web_tour.tours").add("my_feature_tour", {
      steps: () => [
          // the steps
      ],
  });
  ```
- Do not write `test: true,` in the definition. Do not use `extra_trigger`:
  add an independent step that has that condition as its `trigger`.
- A step needs a `trigger`. `run` is optional and **with no `run` nothing is
  done on the trigger**: write `run: "click"` when the step must click. (In 16.0
  and 17.0 a step with no `run` clicks.) `content` is logged and helps to
  debug, and `timeout` is how long the step waits, 10 seconds by default.
- Start the tour from a Python test, a class that inherits from `HttpCase`:
  `self.start_tour("/web", "my_feature_tour", login="admin")`.
- For the rule about absence checks see the next section.

# Pair every absence check with a positive one

In a Hoot test or a tour, a check that an element is absent (`toHaveCount(0)`,
`not.toHaveCount()`, `waitForNone`, `{ count: 0 }`, a trigger built on
`:not(:has(...))`) comes after a positive check in the same test, on an
element that only the state under test produces: the same element before the
step that removes it, or the result of the step after which the element must
not show.

An absence is true from the start. Checked before the code under test ran, it
passes; on a misspelled or renamed selector, it passes forever. The positive
check proves that the step happened and, on the same element, that the
selector matches real markup.

When the element must never show, the positive check alone is not enough: the
step can render its result in one animation frame and the forbidden element in
the next. Wait one more frame (`await animationFrame()`) before the absence
check, and run the test once on the broken code to see it fail: here, that run
is the only proof that the selector matches real markup.

```js
// bad: passes before the error had a chance to show
await contains(".o_send").click();
expect(".o_error").toHaveCount(0);

// good: the message is sent, one more frame is rendered, and still no error
await contains(".o_send").click();
await waitFor(".o_message");
await animationFrame();
expect(".o_error").toHaveCount(0);
```

# Freeze the time when a test meets a timer

A Hoot test that triggers a debounced or delayed call (a search as you type,
an autosave, a popover that opens after a delay) calls `freezeTime()` before
the action, then fires the timer with `advanceTime`. When the timer fires is
decided by `advanceTime`, never by the real clock.

```js
// bad: green only while the 250 ms debounce has not fired yet
await contains(".o_library_search input").edit("Dune", { confirm: false });
expect.verifySteps([]);

// good: the search runs when the test says so
freezeTime();
await contains(".o_library_search input").edit("Dune", { confirm: false });
expect.verifySteps([]);
await advanceTime(250);
expect.verifySteps(["search_books"]);
```

Hoot replaces the timers of the code, but they keep running on the real
clock until the test calls `freezeTime()`; `mockDate` does not stop them. On a
developer machine the test ends before a 250 ms debounce and passes; on a
loaded build the timer fires in the middle and the test fails at random.

- Once the time is frozen, every timer waits for `advanceTime`, a 0 ms one
  too: freeze it after the steps that need one, or advance the time after
  them.
- A test that only waits for the final state, with `waitFor` and the final
  count, needs no frozen time, as long as no earlier state matches that wait.
