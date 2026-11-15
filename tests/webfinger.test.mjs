// Run with: node --test tests/*.test.mjs
import assert from "node:assert/strict";
import { test } from "node:test";

import { ISSUER, ISSUER_REL, respond } from "../functions/.well-known/webfinger.js";

const ACCOUNT = "acct:tom@tom.irish";

const SAMPLE = "https://example.cloudflareaccess.com/cdn-cgi/access/sso/oidc/abc123";

function ask(query, issuer = SAMPLE) {
  return respond(new URL(`https://tom.irish/.well-known/webfinger?${query}`), issuer);
}

test("answers for tom@tom.irish with the issuer link", async () => {
  const res = ask("resource=acct%3Atom%40tom.irish");
  assert.equal(res.status, 200);
  assert.equal(res.headers.get("Content-Type"), "application/jrd+json");
  assert.equal(res.headers.get("Access-Control-Allow-Origin"), "*");
  assert.deepEqual(await res.json(), {
    subject: ACCOUNT,
    links: [{ rel: ISSUER_REL, href: SAMPLE }],
  });
});

test("matches the account case-insensitively", () => {
  assert.equal(ask("resource=acct:Tom@Tom.Irish").status, 200);
});

test("honours rel: the issuer rel keeps the link", async () => {
  const res = ask(`resource=${ACCOUNT}&rel=${encodeURIComponent(ISSUER_REL)}`);
  assert.equal((await res.json()).links.length, 1);
});

test("honours rel: an unrelated rel gets no links", async () => {
  const res = ask(`resource=${ACCOUNT}&rel=http%3A%2F%2Fwebfinger.net%2Frel%2Favatar`);
  assert.equal(res.status, 200);
  assert.deepEqual((await res.json()).links, []);
});

test("any address on tom.irish gets the domain's issuer, as its own subject", async () => {
  const res = ask("resource=acct%3Asomeone%40tom.irish");
  assert.equal(res.status, 200);
  assert.equal((await res.json()).subject, "acct:someone@tom.irish");
});

test("the resource forms clients actually send all resolve", async () => {
  // Tailscale's request (User-Agent Tailscale/1.0) was 404 against an exact
  // "acct:tom@tom.irish" match on 2026-11-15, so the exact form it sends is
  // not that one. Each of these is a form seen in WebFinger clients.
  for (const q of [
    "resource=acct%3Atom%40tom.irish",
    "resource=acct%3Atom%2540tom.irish",
    "resource=mailto%3Atom%40tom.irish",
    "resource=tom%40tom.irish",
    "resource=acct:TOM@TOM.IRISH",
  ]) {
    const res = ask(q);
    assert.equal(res.status, 200, q);
    assert.equal((await res.json()).subject, "acct:tom@tom.irish", q);
  }
});

test("another domain, or something that is not an address, is 404", () => {
  assert.equal(ask("resource=acct:tom@tomirish.com").status, 404);
  assert.equal(ask("resource=acct:tom@evil.tom.irish.example").status, 404);
  assert.equal(ask("resource=acct:tom@xtom.irish").status, 404);
  assert.equal(ask("resource=https://tom.irish/").status, 404);
  assert.equal(ask("resource=acct:@tom.irish").status, 404);
  assert.equal(ask("resource=acct:a@b@tom.irish").status, 404);
});

test("a missing resource is 400", () => {
  assert.equal(ask("").status, 400);
});

test("no issuer configured means 404, not an empty link", () => {
  assert.equal(ask(`resource=${ACCOUNT}`, "").status, 404);
});

test("the published issuer is empty or an Access OIDC issuer URL", () => {
  assert.ok(
    ISSUER === "" ||
      /^https:\/\/[a-z0-9-]+\.cloudflareaccess\.com\/cdn-cgi\/access\/sso\/oidc\/[A-Za-z0-9]+$/.test(ISSUER),
    `unexpected ISSUER: ${ISSUER}`,
  );
});
