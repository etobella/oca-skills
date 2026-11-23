# Module names

- Use the singular in the module name, or `multi`, except when it contains
  the name of an Odoo module or object that is already plural
  (`mrp_operations_...`).
- A module that serves as a base for others starts with `base_`:
  `base_location_nuts`.
- A localization starts with `l10n_CC_`, `CC` being the country code:
  `l10n_es_pos`.
- A module that extends an Odoo module starts with that module's name:
  `mail_forward`.
- A module that combines an Odoo module with another OCA module puts the
  Odoo name first: `crm_partner_firstname` for `crm` plus `partner_firstname`.
- File and folder names use only `[a-z0-9_]`.

# Which module the code goes in

Recommended; the OCA guide only fixes the names above. Decide for each piece
of a feature, in this order:

1. A module already owns the concern: extend that module.
2. No module owns it and other modules may use it: a module of its own,
   depending only on what the capability needs, never part of one business
   module.
3. It connects two modules: a module that depends on both, named after both
   (Odoo's first), with `auto_install` on them so that it is installed
   exactly when both are.

A reusable capability buried in a business module drags that module into
every database that wants the capability.

# Manifest

- No empty keys.
- It has the `license` and `images` keys.
- The `author` text ends with `,Odoo Community Association (OCA)`.
- `website` is `https://github.com/OCA/<repo>`, which shows the repository
  README. It may also be `https://github.com/OCA/<repo>/tree/<branch>/<addon>`
  to point at the README of the addon, with its credits and links.
- Do not use your company logo or branding. The author and the contributors
  list say who you are.
- The long description comes from the `readme/` fragments (see
  [Translations and readme](#translations-and-readme)); remove the sections
  that have no meaningful content.

# Version numbers and migrations

- The version is the Odoo version followed by `x.y.z`: `20.0.1.0.0` for the
  first release of a module in 20.0.
- `x` (major): significant changes to the data model or the views. They may
  need data migration and can affect modules that depend on this one.
- `y` (minor): new features that keep backward compatibility. Upgrading the
  module is probably needed.
- `z` (patch): bug fixes. Usually a server restart is enough.
- A breaking change comes with a migration script, in
  `migrations/<version>/` (`pre-migration.py`, `post-migration.py`), so that
  existing installations can upgrade.
- For a migration to another Odoo major version a script is probable, and
  appreciated. A note in the README about the changes that need migration
  is also enough, so that later contributors can write the script without
  analyzing every change again.

# Directories and file names

A module uses these directories and files:

| Path | Holds |
| --- | --- |
| `controllers/` | HTTP routes |
| `data/` | data XML |
| `demo/` | demo XML |
| `examples/` | external files (`lib/`, CSV...) |
| `i18n/` | translations |
| `migrations/` | one folder per version, with scripts run before or after the update |
| `models/` | model definitions |
| `readme/` | the fragments the `README.rst` is built from |
| `reports/` | reporting models, print report templates |
| `security/` | groups, access rows, record rules |
| `static/` | web assets, in `src/js`, `src/css`, `src/xml`, `img/`, `lib/` |
| `templates/` | web templates, when there are several |
| `tests/` | tests |
| `views/` | views, and QWeb print report templates |
| `wizards/` | wizard models and views |
| `README.rst` | generated: never create or edit it |
| `__init__.py`, `__manifest__.py` | loading and metadata |
| `exceptions.py` | validation errors |
| `hooks.py` | installation hooks |

- **One file per model**, created or inherited, named after the model. Files
  of a category carry a suffix: `models/<model>.py`,
  `data/<model>_data.xml`, `demo/<model>_demo.xml`,
  `templates/<model>_template.xml`, `views/<model>_views.xml`. For example
  `demo/res_partner_demo.xml` and `views/res_partner_views.xml`.
- A model used only as the one2many lines of a main model may be defined in
  the main model's file: `sale.order.line` in `models/sale_order.py`.
- **Controllers:** `main.py` when there is only one file; split them when
  there are several classes or functions.
- **Static files** are named after the module (`static/src/js/<module>.js`,
  `static/src/css/<module>.css`). Do not link images or libraries from
  outside Odoo by URL: copy them into the repository.
- Folders have mode 755 and files 644.

# Installation hooks

- `pre_init_hook`, `post_init_hook`, `uninstall_hook` and `post_load` live in
  `hooks.py` at the root of the module. The manifest keys keep those names.
- Import them in `__init__.py` as needed:
  `from .hooks import pre_init_hook, post_init_hook`.
- Apply monkey patches in `post_load`, so that they apply only when the
  module is installed.

# External dependencies

- Declare Python packages and binaries in `external_dependencies` in the
  manifest, under `python` and `bin`. A `bin` entry must be on `PATH`
  (`which <name>`) and a `python` entry importable.
- Never pin an exact version of a dependency. Set a lower bound only when the
  module needs a recent feature of the library, and no higher than needed.
  Set an upper bound only if you know of an incompatibility with recent
  versions and it is not feasible to fix it. Exact pins and tight bounds
  cause unresolvable conflicts for the integrator, who is the one that pins
  versions for a project.
- Explain how to install the dependency in the Installation section of the
  readme (`readme/INSTALL.rst`).
- A `try`/`except ImportError` around the import is not needed since Odoo
  12.0: a missing dependency of an uninstalled module no longer blocks the
  server.
- The repository has a `requirements.txt` at its root with the Python
  packages, and an `oca_dependencies.txt` with the OCA repositories the
  addons need, one per line: `sale-workflow`; or with a URL
  (`sale-workflow https://github.com/OCA/sale-workflow`); or with a branch
  (`... branchname`); or with a branch and a commit (`... branchname f848e37`).

# Translations and readme

- OCA translates in Weblate. A pull request never modifies `.po` files:
  that would conflict with what Weblate pushes. A PR that adds a new module
  may bring its own `.po` files.
- The `README.rst` is built from the files in `readme/` (`DESCRIPTION.rst`,
  `USAGE.rst`, `CONTRIBUTORS.rst`, ...). Edit those, not the generated file.
  The long description explains why, not what: the diff shows what.
