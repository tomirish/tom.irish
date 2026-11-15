// WebFinger (RFC 7033) for tom@tom.irish: points Tailscale at the OpenID
// Connect issuer that signs Tom into the tailnet.
//
// Tailscale's custom OIDC setup asks https://tom.irish/.well-known/webfinger
// for acct:tom@tom.irish and reads the issuer link from the answer. It reads
// it once, when the identity provider is switched, so this response must be
// right before that switch and stay stable after it.
//
// A Pages Function rather than a static file so it can answer only for the
// one account it describes (404 for anything else) and honour `rel`, as the
// RFC requires. It deploys with the site, from this repo.
//
// ISSUER is public by design: publishing it is this endpoint's whole job. It
// must equal the "issuer" in ISSUER/.well-known/openid-configuration exactly.
// Empty means "not configured yet", and the endpoint answers 404.

export const ACCOUNT = "acct:tom@tom.irish";
export const ISSUER_REL = "http://openid.net/specs/connect/1.0/issuer";
export const ISSUER = "";

const HEADERS = {
  "Content-Type": "application/jrd+json",
  "Access-Control-Allow-Origin": "*",
  "Cache-Control": "public, max-age=3600",
};

export function respond(url, issuer = ISSUER) {
  const resource = url.searchParams.get("resource");
  if (!resource) {
    return new Response("resource parameter required\n", { status: 400 });
  }
  if (!issuer || resource.toLowerCase() !== ACCOUNT) {
    return new Response("not found\n", { status: 404 });
  }
  const rels = url.searchParams.getAll("rel");
  const links = [{ rel: ISSUER_REL, href: issuer }].filter(
    (link) => rels.length === 0 || rels.includes(link.rel),
  );
  return new Response(JSON.stringify({ subject: ACCOUNT, links }), {
    status: 200,
    headers: HEADERS,
  });
}

export function onRequestGet({ request }) {
  return respond(new URL(request.url));
}
