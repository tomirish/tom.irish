# Audiobooks Setup Page — Design Spec

**Date:** 2026-06-27
**URL:** `https://tom.irish/audiobooks`
**Repo:** `github.com/tirish/tom.irish` (new)
**Hosting:** GitHub Pages with custom domain `tom.irish`

---

## Purpose

A single static page that walks family members through setting up the Spine iOS app to access Tom's private Audiobookshelf library at `https://books.tom.irish`. No credentials on the page — accounts are issued by Tom directly.

## Audience

Non-technical family members on iOS. Page must work well on mobile.

---

## Stack

- Single `audiobooks/index.html` with embedded CSS
- No JavaScript framework, no external dependencies
- One optional external resource: App Store badge SVG (Apple-supplied)
- Deployed via GitHub Pages from `main` branch
- Custom domain: `tom.irish` via CNAME in Cloudflare

---

## Page Structure

### 1. Header
- Title: "Tom's Audiobook Library"
- Tagline: "Listen anywhere, on any device"
- Simple SVG headphone or open-book icon in the accent colour
- Centred, clean

### 2. Steps (numbered 1–4)

Each step has:
- Step number + title
- 1–2 sentence instruction
- A CSS phone frame mockup beside/below the text (pure CSS, no images)
- Phone frames contain coloured block elements and text labels that represent the app UI — intentional illustration, not placeholders

**Step 1 — Get an account**
- Text: "Message Tom to get set up. He'll send you a username and password."
- CTA: `Message Tom` button → `sms:+12536702623`
- Phone frame: illustrative "Welcome" screen with a person icon

**Step 2 — Download Spine**
- Text: "Download the free Spine app from the App Store."
- CTA: Apple App Store badge → `https://apps.apple.com/app/id6764636615`
- Phone frame: mock App Store card showing Spine icon + name

**Step 3 — Add the server**
- Text: "Open Spine, tap the + button, and paste in the server address below."
- Server URL displayed in a styled code block with a copy button (JS `navigator.clipboard`)
- URL: `https://books.tom.irish`
- Phone frame: mock "Add Server" screen with the URL pre-filled

**Step 4 — Log in**
- Text: "Enter the username and password Tom sent you."
- Phone frame: mock login screen with username/password fields

### 3. Footer
- "Having trouble? [Message Tom]" link
- Minimal — no nav, no branding clutter

---

## Visual Design

- **Background:** Warm off-white (`#faf8f5`)
- **Text:** Dark charcoal (`#1a1a1a`)
- **Accent:** One colour (warm amber or teal — to be chosen during implementation)
- **Font:** System font stack — no Google Fonts, no external load
- **Phone frames:** Pure CSS — rounded rectangle, subtle shadow, notch at top. UI elements inside are coloured `div`s and `span`s with labels. Looks deliberate, not broken.
- **Layout:** Single column on mobile, step text beside phone frame on wider screens
- **No images required** — everything rendered in HTML/CSS

---

## GitHub Pages Setup

### Repo structure
```
tom.irish/
  audiobooks/
    index.html       ← the page
  CNAME              ← contains: tom.irish
  index.html         ← root redirect to /audiobooks (or placeholder)
  README.md
  docs/
    specs/
      2026-06-27-audiobooks-setup-page-design.md
```

### DNS (Cloudflare)
Add four A records pointing the apex domain to GitHub Pages' IPs, plus a CNAME for `www`:

| Type | Name | Content |
|------|------|---------|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `tomirish.github.io` |

Set **Proxy status to DNS only (grey cloud)** on all records — GitHub Pages requires direct DNS, not proxied.

> **GitHub username confirmed:** `tomirish`

### GitHub Pages settings
- Repo: `tirish/tom.irish`
- Source: `main` branch, root `/`
- Custom domain: `tom.irish`
- Enforce HTTPS: enabled (after DNS propagates)

---

## Out of Scope

- Android app recommendations (future)
- Per-user personalisation
- Credentials on the page
- Any server-side logic
