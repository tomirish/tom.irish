# todo

- braces (GHSA-vfj7-8cjw-p6xm, high, pulled in by stylelint) has no fixed release yet (checked
  2026-10-21). When Dependabot opens the PR, merge it, then add `npm audit` to `build.yml` and
  `nightly.yml` (with a nightly summary block) so the npm tree fails CI like pip does. Not before:
  an unfixable finding would block every deploy.
