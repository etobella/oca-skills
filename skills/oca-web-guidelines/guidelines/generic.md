Rules that hold in every Odoo version, for Owl components. The hooks and the
reactivity depend on the version: see `16-to-19.md` and `20-and-later.md`. The
tests and the tours depend on it too, with another limit: see `tests-qunit.md`
(16.0 and 17.0) and `tests-hoot.md` (18.0 and later).

# JavaScript basics

- Format and lint with the pre-commit configuration of the repository (ESLint
  and prettier), and keep what it produces. Never reformat a whole file with a
  formatter run outside that configuration: with its own defaults it reflows
  every line.
- A file that the configuration ignores keeps its own format: only the lines
  you write follow the one of the repository.
- Never add a minified JavaScript library. Libraries go in `static/lib/`,
  unminified (see [Assets](#assets)).
- Name classes in UpperCamelCase: `class BookList extends Component`.

# File layout

Group the files of `static/src/` by type: one folder per type, named in the
plural. A component has a folder of its own, with its template, its code and
its styles; a service is a single file.

```
static/src/
    components/
        component_1/
            component_1.xml
            component_1.esm.js
            component_1.scss
    services/
        service_1.esm.js
        service_2.esm.js
```

- Name the folder of a component after the component, and give its three
  files the same name: `component_1.xml`, `component_1.esm.js` and
  `component_1.scss`.
- Name a service file after the service, and keep it directly in
  `services/`.
- A JavaScript file that is an ES module ends in `.esm.js`.

# Patching Odoo code

An OCA addon extends Odoo from outside, so patching code of Odoo is often
the only way. Still, a patch makes the code hard to follow (reading the
original no longer says what runs) and the patch and the code it targets
drift apart.

- Look for an extension point first: a registry, a prop, a slot, a plugin or
  a service, a method designed to be overridden. Patch only when there is
  none.
- Patch the smallest thing that does the job, and call the original
  behavior; do not rewrite it.
- Say in a comment which behavior the patch changes and why.
- Do not patch code of your own addon: change the code.

# Batch RPCs

- Do not make an RPC (an `orm` call, `rpc()`) inside a loop, and do not
  await a second RPC after the first one for the same user action. Send one
  call for all the records (`orm.read` and `orm.write` take a list of ids,
  `orm.webSave` writes and reads back in one call), or add a server method
  that does the whole action and returns what the client needs.
- Each RPC is a network round trip and its own transaction. A loop of
  awaited calls costs one round trip per item, so the action gets slower as
  the data grows. Two calls in a row double the wait, and if the second one
  fails the first one is already committed. It is the client side of the
  batching of ORM calls of `oca-guidelines`.
- Calls that are independent and cannot become one server call run in
  parallel (`Promise.all`). A device or an external service that takes one
  item at a time is an exception, and so is a second call that needs the
  answer of the first when no server method can do both.

# Order concurrent calls

When a call can start before the previous one ended and the calls or their
answers change the same state (a request on each key of a search, or on each
save), order them with a helper of `@web/core/utils/concurrency`, never with a
promise chain kept by hand. Calls that share no state, such as starring two
different records, need no helper.

- `KeepLast` when only the last answer matters, as in a search: `add(promise)`
  returns a promise that never settles if a newer promise is added before it
  settled.
- `Mutex` when every call must run, one after the other, as in a save:
  `exec(fn)` starts `fn` once the previous call has settled, resolved or
  rejected.

```js
// bad: after one failed request, no later request is ever sent
this.lastSave = this.lastSave.then(() => this.saveQuantity(quantity));

// good
return this.saveMutex.exec(() => this.saveQuantity(quantity));
```

Without a helper the answers come back in any order: the screen shows the
answer of an older request, or two calls change the same state at once. A
chain kept by hand rewrites `Mutex` badly, and a `then` with no rejection
handler stops it for good at the first error.

Never let `Mutex.exec` wait for a `KeepLast` promise added outside of it: once
a newer call adds its own promise, the first one never settles and the mutex
stays locked. When the calls must run one after the other and only the last
answer matters, put the `KeepLast` around the mutex:

```js
// bad: the saves run at once, and the mutex stays locked
const totalPromise = this.keepLast.add(this.saveQuantity(quantity));
await this.saveMutex.exec(() => totalPromise);

// good
const total = await this.keepLast.add(
    this.saveMutex.exec(() => this.saveQuantity(quantity))
);
```

Check that `@web/core/utils/concurrency` exists in the version before you use it.

# End a sort comparator on a unique key

A comparator given to `sort()` or `toSorted()` returns 0 for two equal
arguments and the opposite sign when they are swapped. When the values it
compares can be equal, end it on a unique key of the items, usually `id`.

```js
// bad: answers -1 both ways for two books with the same title
books.sort((a, b) => (a.title > b.title ? 1 : -1));

// bad: two books with the same title keep the order they came in
books.sort((a, b) => a.title.localeCompare(b.title));

// good
books.sort((a, b) => a.title.localeCompare(b.title) || a.id - b.id);
```

A comparator that is not anti-symmetric gives an order that depends on the
engine and on the input: Chrome and Firefox do not sort the same way. One
that returns 0 for two different items keeps the order they came in, which
changes with another load or a list updated by a notification. The user sees
rows swap, and a test that reads the first item fails on one browser or at
random. No fallback is needed when the key is already unique, nor for `sort()`
without a comparator on strings. Numbers always need a comparator
(`(a, b) => a - b`): the default sort compares them as strings.

# Avoid getters

A getter hides that a computation runs and only saves a pair of parentheses.
Write a plain function: the call shows that code runs, and it can take an
argument the day the computation needs one. For derived state, the version
file says what to use.

# Give every icon a role and a label

An element that shows an icon carries `role="img"` and one of:

- `aria-hidden="true"` when the icon is decorative: it repeats the text next to
  it, or it is the content of a button or a link that has its own label. This
  is the usual case.
- `aria-label` when the icon alone tells something, with a `title` for
  sighted users when nothing else on screen says it.

Which element and classes draw the icon depends on the version (see the file
of the version). The rule is the same:

```xml
<!-- decorative: the text says it -->
<a href="#"><i class="ICON" role="img" aria-hidden="true"/> Open</a>
<!-- icon-only button: the label goes on the button -->
<button class="btn" title="Delete" aria-label="Delete">
    <i class="ICON" role="img" aria-hidden="true"/>
</button>
<!-- the icon alone tells it -->
<i class="ICON" role="img" title="Private" aria-label="Private"/>
```

Screen readers read the content drawn by the icon font, so without a label
or `aria-hidden` they say the name of the glyph. No role, or
`role="presentation"`, does not stop it. An icon that acts as a button is
focusable, so it cannot be `aria-hidden`: write a real `<button>` with the
label and hide the icon inside it.

# Assets

- Every resource a page needs ships in the addon: copy images, fonts and
  libraries into it instead of linking them by URL.
- Third-party libraries go in `static/lib/`, unminified, so they can be read
  and diffed.

# CSS and SCSS

OCA rules:

- Prefix every class with `o_<module_name>`, `module_name` being the technical
  name of the module (`im_chat`), or the main route reserved by the module for
  website modules (`o_forum` for `website_forum`). Only the web client itself
  uses a bare `o_`.
- Do not use `id` selectors. Use the native classes of Bootstrap.
- Name classes in lowercase with underscores. Use the flat approach
  (`o_element_entry`), not hyper-specific nested names.

Recommended; the OCA guide does not write these down:

- Indent with 4 spaces, no tabs; keep lines near 80 columns; one declaration
  per line; the opening brace on the selector line.
- Order the properties from the outside in: start at `position`, end with the
  decorative ones such as `font` and `filter`.
- Name SCSS variables `$o-<root>-<element>-<property>-<modifier>`, with
  hyphens, scoped ones `$-<name>` and mixins and functions `o-<name>`.
- Do not define CSS variables on `:root`: use SCSS for global design. CSS
  variables are for adapting the DOM in context.

# Pair every absence check with a positive one

In a test or a tour, a check that an element is absent comes after a positive
check in the same test, on an element that only the state under test
produces: the same element before the step that removes it, or the result of
the step after which the element must not show.

An absence is true from the start. Checked before the code under test ran, it
passes; on a misspelled or renamed selector, it passes forever. The positive
check proves that the step happened and, on the same element, that the
selector matches real markup.

In a tour the absence is a step whose trigger is built on `:not(:has(...))`,
or that waits for the element to go: put a step that waits for the positive
element before it. The Hoot version of this rule, with the extra frame to
wait for, is in `tests-hoot.md`.
