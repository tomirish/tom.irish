# Microsoft 365 Branding

How the tom.irish Microsoft 365 tenant is branded, where each setting lives, and how each image
was made. Everything here is set by hand in two admin portals. Nothing in this repo deploys it;
the repo only keeps the images and this record.

Set up 2026-10-30.

---

## Where it shows up

| Surface | Comes from | Admin portal |
|---|---|---|
| Top navigation bar in Outlook on the web, microsoft365.com, etc. | Org theme | Microsoft 365 admin center |
| Account icon in Outlook for iOS/Android ("Show As → Work or School Logo") | Entra ID square logo | Microsoft Entra admin center |
| Microsoft sign-in page | Entra ID company branding | Microsoft Entra admin center |

The org theme and Entra company branding are separate systems. Changing one never changes the other.

---

## Org theme (navigation bar)

**Microsoft 365 admin center → Settings → Org settings → Organization profile → Custom themes →
Default Theme.**

| Tab | Setting | Value |
|---|---|---|
| General | Prevent users from overriding their theme | Off |
| Logos | Default logo | **Upload** `assets/images/m365-default-logo.png` |
| Logos | Alternate logo (dark mode) | `https://raw.githubusercontent.com/tomirish/tom.irish/73adcb3/assets/images/m365-logo.png` |
| Logos | On-click link | `https://tom.irish` |
| Colors | Navigation bar color | `#9B2335` |
| Colors | Text and icon color | `#FAF9F7` |
| Colors | Accent color | `#9B2335` |
| Copilot Chat | Branded footer | Off |

The three colors are the site's own `--accent` and `--bg` tokens from `src/main.css`. Cream on
crimson is about 8:1 contrast, above Microsoft's 4.5:1 recommendation.

### Logo rules learned the hard way

- **The alternate logo is URL-only, and tom.irish cannot serve it.** The admin center checks the URL
  from Microsoft's own servers, and the `tom.irish` URL was rejected while the same file from
  `raw.githubusercontent.com` was accepted. The likely cause is Cloudflare Bot Fight Mode, which
  challenges datacenter traffic and cannot be exempted per path on the free plan.
- **Pin the URL to a commit, not `main`.** GitHub's raw CDN caches `main` for 5 minutes per edge,
  so a fresh push can show the old image in every browser on the same network. A commit-pinned URL
  can only ever return one file. Changing the dark logo means committing it, then pasting the new
  commit's URL into the admin center.
- **Microsoft scales a logo to the bar's full height.** Any padding must be inside the image.
  Both logos put the cream ring at 80% of the image height, so the bar shows a thin margin above
  and below, and the two modes look the same size.
- **Limits:** upload under 10 KB; JPG, PNG, GIF or SVG; scaled to fit 200×48.

---

## Entra company branding

**Microsoft Entra admin center → Entra ID → Custom Branding → Default sign-in → Edit.**

| Tab | Setting | Value |
|---|---|---|
| Sign-in form | Square logo (light theme) | `assets/images/entra-square-logo.png` |
| Sign-in form | Square logo (dark theme) | Not set — the crimson tile reads on both |
| Sign-in form | Banner logo | Not set (shows Microsoft's logo) |

Everything else is left at Microsoft's defaults.

The square logo is what Outlook mobile shows as the account icon. Outlook crops it to a circle,
so it has no ring or border. A ring would read as a clipped edge. Changes can take up to 24
hours to reach the app.

Limits: 240×240, PNG or JPG, under 50 KB.

---

## The images

All are derived from the master mark, `assets/images/ti-element.png`. Each keeps the site's exact
`#9b2335` and `#faf9f7`. Each has a test in `tests/test_m365_logo.py`, because a rename or swap breaks
the Microsoft 365 branding with no error anywhere on this site.

| File | Size | Used as | Made by |
|---|---|---|---|
| `m365-default-logo.png` | 96×96 | Org theme default logo (uploaded) | The full mark, centered at 87% of a transparent canvas, so its cream ring lands at 80% |
| `m365-logo.png` | 96×96 | Org theme alternate logo (by URL) | The mark cropped to the outer edge of the cream ring (inset 4% of the mark), masked to the ring's corner radius (13.75% of the crop), centered at 80% |
| `entra-square-logo.png` | 240×240 | Entra square logo | `favicon.png` resized — solid crimson tile, no ring |

The default logo keeps the mark's outer crimson band because it sits on the crimson bar, where
the band disappears into the background and only the ring shows. The alternate logo drops the
band because, on a dark bar, it would read as a dark frame around the ring.
