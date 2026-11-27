# Reporting a security issue

Finding a hole is not the end of the work: say where it goes before anything
is made public.

- **Do not publish the exploit first.** A public PR, issue or comment whose
  test, steps or description show how to exploit the hole discloses it before
  the maintainers can react. Do not open one for a confirmed vulnerability
  until the route below has been followed and the maintainers agree.
- **Use the route OCA publishes.** Look for a `SECURITY.md` in the repository
  (or in the `OCA/.github` repository) and for the security policy of the
  PSC, and follow it: the issue goes privately to the PSC or the security
  contact it names.
- **If none is found, stop and ask the user.** Do not guess an address or
  post the finding anywhere. Give the user the finding (file, line, scenario,
  smallest fix) to send. The reporting route has not been agreed by OCA yet,
  so this is the expected case for now.
- **A hole that comes from Odoo core** (the module only exposes it, or the
  bug is in code outside `addons/` of the repository) is not fixed by an OCA
  PR. Check it against the Odoo version in the revision, and tell the user to
  report it through Odoo's own security policy; do not describe it in public
  first.
- **Weak spots that are not exploitable** (a missing test, a hardening, a
  `sudo` that is safe) are ordinary findings and can go in a normal PR.
- **When the fix is published** the PR is a normal one, with the test that
  fails without the fix (see `oca-git`), once the maintainers have agreed.
