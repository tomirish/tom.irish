// WebFinger (RFC 7033) for tom.irish: points Tailscale at the OpenID
// Connect issuer that signs tom.irish users into the tailnet.
//
// Tailscale's custom OIDC setup asks https://tom.irish/.well-known/webfinger
// about the user's address and reads the issuer link from the answer. It reads
// it once, when the identity provider is switched, so this response must be
// right before that switch and stay stable after it.
//
// The issuer belongs to the domain, not to one person: Tailscale requires
// every user of a domain to sign in through the same provider. So any address
// at tom.irish gets the same issuer, and who may actually sign in is decided
// by the Cloudflare Access policy, not here. Clients write the address in
// several ways (acct:, mailto:, bare, percent-encoded twice); all resolve.
//
// A Pages Function rather than a static file so it can refuse anything that
// is not a tom.irish address (404) and honour `rel`, as the RFC requires. It
// deploys with the site, from this repo.
//
// ISSUER is public by design: publishing it is this endpoint's whole job. It
// must equal the "issuer" in ISSUER/.well-known/openid-configuration exactly.
// An empty value would mean "not configured", and the endpoint answers 404.

export const DOMAIN = "tom.irish";
export const ISSUER_REL = "http://openid.net/specs/connect/1.0/issuer";
export const ISSUER =
  "https://lingering-glade-b425.cloudflareaccess.com/cdn-cgi/access/sso/oidc/d524d666f415e866b7cbe300d1d4f9f8d3cfb1bd416889083ca84719b1f2464c";

const HEADERS = {
  "Content-Type": "application/jrd+json",
  "Access-Control-Allow-Origin": "*",
  "Cache-Control": "public, max-age=3600",
};

// The address a resource names, lower-cased, or null if it is not one
// address at DOMAIN. Decodes at most twice: one extra layer is the
// double-encoding some clients send, more would be guessing.
export function addressOf(resource) {
  let value = resource;
  for (let i = 0; i < 2 && value.includes("%"); i += 1) {
    try {
      value = decodeURIComponent(value);
    } catch {
      return null;
    }
  }
  value = value.trim().toLowerCase().replace(/^(acct|mailto):/, "");
  const match = /^([^@\s/:]+)@([^@\s/:]+)$/.exec(value);
  return match && match[2] === DOMAIN ? value : null;
}

export function respond(url, issuer = ISSUER) {
  const resource = url.searchParams.get("resource");
  if (!resource) {
    return new Response("resource parameter required\n", { status: 400 });
  }
  const address = addressOf(resource);
  if (!issuer || !address) {
    return new Response("not found\n", { status: 404 });
  }
  const rels = url.searchParams.getAll("rel");
  const links = [{ rel: ISSUER_REL, href: issuer }].filter(
    (link) => rels.length === 0 || rels.includes(link.rel),
  );
  return new Response(JSON.stringify({ subject: `acct:${address}`, links }), {
    status: 200,
    headers: HEADERS,
  });
}

export function onRequestGet({ request }) {
  return respond(new URL(request.url));
}
