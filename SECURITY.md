# Security Policy

## Scope

tom.irish is a static personal website with no backend, no user accounts, and no data collection. The attack surface is limited to:

- The build pipeline (GitHub Actions, Python scripts)
- Third-party dependencies (see `requirements.txt`)
- Cloudflare Pages configuration

## Supported versions

Only the current live deployment at [tom.irish](https://tom.irish) is supported.

## Reporting a vulnerability

Please use GitHub's [private vulnerability reporting](https://github.com/tomirish/tom.irish/security/advisories/new) to report security issues. This keeps the details confidential until a fix is in place.

I'll acknowledge reports within a few days and aim to resolve confirmed issues promptly.

## Out of scope

- Theoretical vulnerabilities with no practical impact on a static site
- Issues in GitHub's or Cloudflare's own infrastructure
- Self-XSS or issues that require physical access to my machine
