Rules for Odoo 20.0 and later, on top of `generic.md`. A module of this range
has `version` starting with `20.0.` or a higher number. 20.0 runs Owl 3 with a
compatibility layer for Owl 2 code (`addons/web/static/src/owl2/` in the Odoo
source), and Owl 3 was still a pre-release in it when this was written. Check
each API in the source of the version, and for 21.0 and later check that the
rule still holds.

# Owl 3 in 20 and later

- The Owl 2 APIs that Owl 3 removed fail at once: `useState`, `useRef` and the
  static `props`. Port the component that uses them.
- A second group of APIs comes from the layer that lets Owl 2 code run on
  Owl 3, and keeps working, so it goes unnoticed: `useLayoutEffect`,
  `useSubEnv`, `useEnv`, `onWillRender` and `render()`. Do not write them in
  new code. Write instead:
  - `useEffect(fn)` for a side effect. It takes no dependency list and runs
    again when anything it reads changes, including what the functions it
    calls read.
  - `useOnChange(() => [deps], callback)` when only some values must run it
    again: only the dependency function is tracked, not the callback.
  - `onMounted` and `onPatched` for work on the DOM after each render, such as
    a measure.
  - `computed` for a value derived from other state.
  - `providePlugins` and `usePlugin` to share something with the child
    components.
  - a `signal` or a `proxy` read by the template, instead of forcing a render.
- The `useEffect` of Owl 3 is not the one of Owl 2, and a hook converted as is
  breaks:
  - It runs once during setup, before the component is in the DOM, then each
    time a signal, proxy or computed that it read changes. What is read inside
    `untrack`, or is not reactive, never runs it again. A render with no
    reactive change does not run it.
  - A second argument is ignored. An element is read through its
    `signal.ref()`: `null` at the first run, and the effect runs again once the
    element is set.
  - An effect may write state, for example to reset a selection when the
    record changes.

  ```js
  // bad: dependencies given by hand, run at mount
  useLayoutEffect(
      (isEditing) => isEditing && this.checkAccess(),
      () => [this.record.isEditing],
  );

  // good: runs at setup, then only when `isEditing` changes,
  // whatever `checkAccess` reads
  useOnChange(
      () => [this.record.isEditing],
      (isEditing) => isEditing && this.checkAccess(),
  );
  ```
- Code that still calls the compatibility hooks can keep them until it is
  ported: a change that only touches nearby lines does not have to convert
  them.
- For derived state, use `computed` instead of a getter (see
  [Avoid getters](generic.md#avoid-getters)): it recomputes only when what it
  reads changes.

# Window members

Write `setTimeout`, `clearTimeout`, `localStorage`, `navigator` or
`addEventListener` without the `browser.` prefix. The one exception is
`window.location`: import `location` from `@web/core/browser/browser`, since
tests cannot patch it on `window`. The `browser` object was a way for tests to
patch these members; Hoot mocks them on `window` itself, so `browser` is
deprecated. Do not copy it from the code around, and leave its existing uses
alone unless your change touches those lines.

# Icons in 20 and later

Icons are Material Design icons: the glyph is the ligature named in
`data-icon`. The Font Awesome icons declared with `class="fa-..."` are
replaced.

```xml
<i class="oi" data-icon="open_in_new" role="img" aria-hidden="true"/>
```

Give them a role and a label as in
[Give every icon a role and a label](generic.md#give-every-icon-a-role-and-a-label).
Check the element and the classes in the source of the version.

# Constructs in 20 and later

Before you use one of these, check that the source of the module's version
has it.

| Construct | What to know |
| --- | --- |
| `signal`, `computed`, `proxy`, `untrack` | Owl 3 reactivity. They are pre-release APIs in 20.0: check them. |
| `useEffect(fn)`, `useOnChange`, `onMounted`, `onPatched` | The hooks of the section above. |
| `Plugin`, `providePlugins`, `usePlugin` | Owl 3 plugins, which take the place of the services of Owl 2. Many services still exist, and the converted ones keep a `useService` alias. |
| Hoot (`freezeTime`, `advanceTime`, `animationFrame`) | The test framework of `tests-hoot.md`. |
