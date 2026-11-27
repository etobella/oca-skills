# Record format

- Indent with four spaces.
- In a `record`, put `id` before `model`. In a `field`, put `name` first,
  then the value (in the tag or in `eval`), then the other attributes
  (`widget`, `options`...) by importance.
- Group the records by model. Dependencies between action, menu and views
  may force another order.
- Use the `<data>` tag only to mark part of a file with `noupdate="1"` when
  the file mixes updatable and non-updatable data. Otherwise use `<odoo>`
  (for `noupdate=0` or demo data, which is non-updatable by default) or
  `<odoo noupdate="1">`.
- A change to a `noupdate` record does not reach existing databases: see
  [noupdate data and existing databases](modules.md#noupdate-data-and-existing-databases).
- Do not prefix the id of a record with the name of the current module:
  `<record id="view_id"...>`, not `<record id="current_module.view_id"...>`.

```xml
<record id="view_id" model="ir.ui.view">
    <field name="name">view.name</field>
    <field name="model">object_name</field>
    <field name="priority" eval="16"/>
    <field name="arch" type="xml">
        ...
    </field>
</record>
```

# XML ids

`<model_name>` is the name of the model with underscores instead of dots
(`res.users` is `res_users`).

| Record | Pattern |
| --- | --- |
| data | `<model_name>_<record_name>`, for example `res_users_important_person` |
| menu | `<model_name>_menu` |
| view | `<model_name>_view_<type>` (`form`, `tree` or `list`, `kanban`, `search`...), for example `res_users_view_form` |
| main action | `<model_name>_action` |
| other action | `<model_name>_action_<detail>`, a short lowercase detail, only when the model has several actions |
| group | `<model_name>_group_<group_name>`, the name being generally `user` or `manager` |
| rule | `<model_name>_rule_<group>`, the group being `user`, `public`, `company` (multi-company)... |
| demo record | the id of a data record with the suffix `_demo`, for example `res_users_not_a_real_user_demo` |

# Inheriting views

- A module extends a view only once.
- Keep the naming rules when you inherit. If the inherited view has a name
  that breaks them, name yours after the original: that makes it easy to find
  the original and the other inheritances. The id of the original view is
  referenced by `inherit_id`:

  ```xml
  <record id="original_id" model="ir.ui.view">
      <field name="inherit_id" ref="original_module.original_id"/>
      ...
  </record>
  ```
- Anchor the inheritance on a field `name` or another stable attribute,
  never on a position such as `//group[2]/field[3]`: the parent view belongs
  to another module that reorders it freely.
- Avoid `position="replace"`: it can raise `Element ... cannot be located in
  parent view` in the other views that inherit the same field. If you must
  use it, comment why it is absolutely necessary and give the view a high
  `priority` (greater than 100):

  ```xml
  <record id="view_id" model="ir.ui.view">
      <field name="priority">110</field> <!-- greater than 100 -->
      <field name="arch" type="xml">
          <!-- Necessary because ... -->
          <xpath expr="//field[@name='my_field_1']" position="replace"/>
      </field>
  </record>
  ```
- To hide an element, `invisible="1"` is usually enough.

# Data, demo data and filters

- Demo data lives in `demo/`, apart from `data/`, and its ids end in `_demo`.
- A record of `ir.filters` sets `user_id` explicitly, so that it is clear
  whether the filter is personal or shared. `eval="False"` makes it global:

  ```xml
  <record id="filter_id" model="ir.filters">
      <field name="name">Filter name</field>
      <field name="model_id">filter.model</field>
      <field name="user_id" eval="False"/>
  </record>
  ```

# Security files

- Access rows go in the CSV file of `security/` and groups and record rules
  in `security/<model>_security.xml`; ids follow [XML ids](#xml-ids).
- The format of the access rows depends on the version: from 20.0 it is
  `ir.access`. See `versions/20.0.md`.
- To audit a security file use the `oca-security` skill when it is loaded.

# JavaScript and CSS

- JavaScript: `"use strict";` in every file, ESLint with the configuration
  of OCA, never a minified library, UpperCamelCase for classes.
- CSS: prefix every class with `o_<module_name>`, `module_name` being the
  technical name of the module (`im_chat`), or the main route reserved by the
  module for website modules (`o_forum` for `website_forum`). Only the web
  client uses a bare `o_`. Do not use ids, use native bootstrap classes, and
  name classes in lowercase with underscores.
