# Audiobooks Setup Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deploy a static HTML/CSS setup page at `tom.irish/audiobooks` that walks family members through installing Spine and connecting to `books.tom.irish`.

**Architecture:** Single self-contained `audiobooks/index.html` with embedded CSS and minimal inline JS (clipboard copy only). No frameworks, no external CSS, no build step. Deployed via GitHub Pages on the `tomirish/tom.irish` repo with a custom domain.

**Tech Stack:** HTML5, CSS3 (custom properties, flexbox, grid), minimal vanilla JS, GitHub Pages, Cloudflare DNS.

## Global Constraints

- No external CSS frameworks or fonts — system font stack only
- No images — all visuals are pure CSS/HTML
- Phone number for sms link: `+12536702623`
- App Store link: `https://apps.apple.com/app/id6764636615`
- Server URL: `https://books.tom.irish`
- GitHub username: `tomirish`
- Custom domain: `tom.irish`
- All files in `tom.irish/` repo root or `audiobooks/` subdirectory

---

## File Map

| File | Purpose |
|---|---|
| `CNAME` | GitHub Pages custom domain declaration |
| `index.html` | Root redirect to `/audiobooks/` |
| `audiobooks/index.html` | The setup page — all HTML, CSS, and JS |
| `README.md` | Repo description |

---

### Task 1: Create GitHub repo and enable Pages

**Files:**
- Create: `CNAME`
- Create: `README.md`
- Create: `index.html` (root redirect)

- [ ] **Step 1: Authenticate gh CLI**

```bash
gh auth login -h github.com
```
Follow the prompts. Choose HTTPS and authenticate via browser.

- [ ] **Step 2: Create the GitHub repo**

```bash
cd /Users/tom/github/tom.irish
gh repo create tomirish/tom.irish --public --description "tom.irish personal site" --source . --remote origin
```

- [ ] **Step 3: Create CNAME file**

```bash
echo "tom.irish" > /Users/tom/github/tom.irish/CNAME
```

- [ ] **Step 4: Create README**

Write `/Users/tom/github/tom.irish/README.md`:
```markdown
# tom.irish

Personal site for tom.irish. Hosted on GitHub Pages.

- `/audiobooks` — Audiobook library setup guide for family
```

- [ ] **Step 5: Create root index.html redirect**

Write `/Users/tom/github/tom.irish/index.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=/audiobooks/">
  <title>tom.irish</title>
</head>
<body>
  <a href="/audiobooks/">Redirecting…</a>
</body>
</html>
```

- [ ] **Step 6: Create audiobooks directory**

```bash
mkdir -p /Users/tom/github/tom.irish/audiobooks
```

- [ ] **Step 7: Commit and push**

```bash
cd /Users/tom/github/tom.irish
git add CNAME README.md index.html audiobooks/
git commit -m "feat: initial repo setup with GitHub Pages config"
git push -u origin main
```

- [ ] **Step 8: Enable GitHub Pages**

```bash
gh api repos/tomirish/tom.irish/pages \
  --method POST \
  -f build_type=legacy \
  -f source.branch=main \
  -f source.path=/
```

Expected output: JSON with `"status": "queued"` or `"built"`.

- [ ] **Step 9: Set custom domain**

```bash
gh api repos/tomirish/tom.irish/pages \
  --method PUT \
  -f cname=tom.irish
```

---

### Task 2: Page shell and design system

**Files:**
- Create: `audiobooks/index.html`

- [ ] **Step 1: Create the HTML shell with embedded design system**

Write `/Users/tom/github/tom.irish/audiobooks/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Set up your audiobook library — download Spine and connect to Tom's collection.">
  <title>Tom's Audiobook Library</title>
  <style>
    /* ── Design tokens ── */
    :root {
      --bg: #faf8f5;
      --surface: #ffffff;
      --text: #1a1a1a;
      --text-muted: #6b6b6b;
      --accent: #c97d2e;
      --accent-light: #fdf3e7;
      --border: #e8e4de;
      --phone-bg: #111111;
      --phone-screen: #f5f5f7;
      --radius-lg: 20px;
      --radius-phone: 36px;
      --shadow: 0 4px 24px rgba(0,0,0,0.08);
      --shadow-phone: 0 24px 64px rgba(0,0,0,0.25);
      --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* ── Reset ── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: var(--font);
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }
    a { color: var(--accent); text-decoration: none; }
    a:hover { text-decoration: underline; }

    /* ── Layout ── */
    .page { max-width: 900px; margin: 0 auto; padding: 0 24px; }

    /* ── Phone frame ── */
    .phone {
      width: 180px;
      height: 360px;
      background: var(--phone-bg);
      border-radius: var(--radius-phone);
      padding: 14px 8px 12px;
      box-shadow: var(--shadow-phone);
      position: relative;
      flex-shrink: 0;
    }
    .phone::before {
      content: '';
      position: absolute;
      top: 10px;
      left: 50%;
      transform: translateX(-50%);
      width: 60px;
      height: 5px;
      background: #333;
      border-radius: 3px;
    }
    .phone-screen {
      background: var(--phone-screen);
      border-radius: 28px;
      height: 100%;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    /* ── Steps ── */
    .steps { display: flex; flex-direction: column; gap: 64px; padding: 48px 0 80px; }

    .step {
      display: flex;
      align-items: center;
      gap: 40px;
    }
    .step:nth-child(even) { flex-direction: row-reverse; }

    .step-content { flex: 1; }

    .step-number {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 36px;
      height: 36px;
      background: var(--accent);
      color: white;
      border-radius: 50%;
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 12px;
    }

    .step-title {
      font-size: 22px;
      font-weight: 700;
      margin-bottom: 8px;
      color: var(--text);
    }

    .step-body {
      font-size: 16px;
      color: var(--text-muted);
      line-height: 1.7;
      margin-bottom: 20px;
    }

    /* ── Buttons ── */
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 12px 24px;
      border-radius: 100px;
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      border: none;
      text-decoration: none;
      transition: opacity 0.15s;
    }
    .btn:hover { opacity: 0.85; text-decoration: none; }
    .btn-primary { background: var(--accent); color: white; }
    .btn-outline { background: transparent; color: var(--text); border: 2px solid var(--border); }

    /* ── Server URL block ── */
    .url-block {
      display: flex;
      align-items: center;
      gap: 12px;
      background: var(--accent-light);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px 18px;
      font-family: monospace;
      font-size: 15px;
      color: var(--text);
    }
    .url-text { flex: 1; word-break: break-all; }
    .copy-btn {
      background: var(--accent);
      color: white;
      border: none;
      border-radius: 8px;
      padding: 6px 14px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: opacity 0.15s;
    }
    .copy-btn:hover { opacity: 0.85; }

    /* ── App Store badge ── */
    .appstore-badge {
      display: inline-block;
      margin-top: 4px;
    }
    .appstore-badge img {
      height: 44px;
      width: auto;
    }

    /* ── Responsive ── */
    @media (max-width: 640px) {
      .step, .step:nth-child(even) {
        flex-direction: column;
        align-items: center;
        text-align: center;
      }
      .url-block { flex-direction: column; align-items: flex-start; }
      .step-title { font-size: 20px; }
    }
  </style>
</head>
<body>

  <!-- Header, steps, footer go here in later tasks -->

  <script>
    function copyUrl() {
      navigator.clipboard.writeText('https://books.tom.irish').then(() => {
        const btn = document.querySelector('.copy-btn');
        const original = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(() => btn.textContent = original, 2000);
      });
    }
  </script>
</body>
</html>
```

- [ ] **Step 2: Open in browser and verify shell loads**

```bash
open /Users/tom/github/tom.irish/audiobooks/index.html
```

Expected: blank warm off-white page, no console errors.

- [ ] **Step 3: Commit**

```bash
cd /Users/tom/github/tom.irish
git add audiobooks/index.html
git commit -m "feat: page shell and design system"
git push
```

---

### Task 3: Header section

**Files:**
- Modify: `audiobooks/index.html` — add header between `<body>` and the script tag

- [ ] **Step 1: Add the header HTML**

Replace `<!-- Header, steps, footer go here in later tasks -->` with:

```html
  <!-- ── Header ── -->
  <header style="background: var(--surface); border-bottom: 1px solid var(--border); padding: 48px 24px 40px;">
    <div class="page" style="text-align: center;">
      <div style="margin-bottom: 20px;">
        <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <rect width="56" height="56" rx="16" fill="#fdf3e7"/>
          <path d="M14 20C14 17.8 15.8 16 18 16H22C22 16 22 22 18 22C15.8 22 14 21.1 14 20Z" fill="#c97d2e"/>
          <path d="M42 20C42 17.8 40.2 16 38 16H34C34 16 34 22 38 22C40.2 22 42 21.1 42 20Z" fill="#c97d2e"/>
          <path d="M22 16H34V30C34 34.4 31.3 38 28 38C24.7 38 22 34.4 22 30V16Z" fill="#c97d2e" opacity="0.3"/>
          <rect x="12" y="18" width="4" height="10" rx="2" fill="#c97d2e"/>
          <rect x="40" y="18" width="4" height="10" rx="2" fill="#c97d2e"/>
          <path d="M16 26C16 26 16 38 28 40C40 38 40 26 40 26" stroke="#c97d2e" stroke-width="2" stroke-linecap="round" fill="none"/>
        </svg>
      </div>
      <h1 style="font-size: 32px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 10px;">
        Tom's Audiobook Library
      </h1>
      <p style="font-size: 18px; color: var(--text-muted); max-width: 480px; margin: 0 auto;">
        Listen to great books, anywhere — on your phone, in the car, wherever.
      </p>
    </div>
  </header>

  <!-- Steps wrapper -->
  <main class="page">
    <div class="steps">
      <!-- Steps go here -->
    </div>
  </main>

  <!-- Footer goes here -->
```

- [ ] **Step 2: Open in browser and verify**

```bash
open /Users/tom/github/tom.irish/audiobooks/index.html
```

Expected: warm header with headphone icon, title "Tom's Audiobook Library", tagline beneath.

- [ ] **Step 3: Commit**

```bash
cd /Users/tom/github/tom.irish
git add audiobooks/index.html
git commit -m "feat: header section"
git push
```

---

### Task 4: Step 1 (Get an account) and Step 2 (Download Spine)

**Files:**
- Modify: `audiobooks/index.html` — replace `<!-- Steps go here -->` with steps 1 and 2

- [ ] **Step 1: Add Steps 1 and 2 HTML**

Replace `<!-- Steps go here -->` with:

```html
      <!-- Step 1: Get an account -->
      <div class="step">
        <div class="step-content">
          <div class="step-number">1</div>
          <h2 class="step-title">Get an account</h2>
          <p class="step-body">
            Message Tom to get set up. He'll send you a username and password to access the library.
          </p>
          <a href="sms:+12536702623&body=Hi Tom, can I get access to the audiobook library?" class="btn btn-primary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 2H4C2.9 2 2 2.9 2 4v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
            Message Tom
          </a>
        </div>
        <div class="phone" aria-hidden="true">
          <div class="phone-screen" style="padding: 20px 14px; align-items: center; justify-content: center; gap: 12px;">
            <div style="width: 52px; height: 52px; background: var(--accent); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="white"><path d="M12 12c2.7 0 5-2.3 5-5s-2.3-5-5-5-5 2.3-5 5 2.3 5 5 5zm0 2c-3.3 0-10 1.7-10 5v2h20v-2c0-3.3-6.7-5-10-5z"/></svg>
            </div>
            <div style="font-size: 11px; font-weight: 700; color: #1a1a1a; text-align: center;">Welcome!</div>
            <div style="font-size: 9px; color: #6b6b6b; text-align: center; line-height: 1.4;">Message Tom to get your username and password</div>
            <div style="width: 100%; height: 28px; background: #c97d2e; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
              <span style="font-size: 9px; font-weight: 700; color: white;">Message Tom</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 2: Download Spine -->
      <div class="step">
        <div class="step-content">
          <div class="step-number">2</div>
          <h2 class="step-title">Download Spine</h2>
          <p class="step-body">
            Spine is a free audiobook player that connects directly to the library. Download it from the App Store.
          </p>
          <a href="https://apps.apple.com/app/id6764636615" class="appstore-badge" target="_blank" rel="noopener" aria-label="Download Spine on the App Store">
            <img src="https://tools.applemediaservices.com/api/badges/download-on-the-app-store/black/en-us" alt="Download on the App Store" height="44">
          </a>
        </div>
        <div class="phone" aria-hidden="true">
          <div class="phone-screen" style="padding: 14px 10px; gap: 10px; align-items: center;">
            <div style="font-size: 8px; font-weight: 700; color: #6b6b6b; text-transform: uppercase; letter-spacing: 0.5px; align-self: flex-start;">App Store</div>
            <div style="width: 100%; background: white; border-radius: 10px; padding: 10px; display: flex; align-items: center; gap: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
              <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #1a1a1a, #444); border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <span style="color: white; font-weight: 800; font-size: 14px;">S</span>
              </div>
              <div style="flex: 1; min-width: 0;">
                <div style="font-size: 10px; font-weight: 700; color: #1a1a1a;">Spine</div>
                <div style="font-size: 8px; color: #6b6b6b;">Audiobook Player</div>
              </div>
              <div style="background: #c97d2e; color: white; font-size: 8px; font-weight: 700; padding: 4px 8px; border-radius: 100px;">GET</div>
            </div>
            <div style="width: 100%; display: flex; gap: 6px; flex-direction: column; margin-top: 4px;">
              <div style="height: 6px; background: #e0e0e0; border-radius: 3px; width: 80%;"></div>
              <div style="height: 6px; background: #e0e0e0; border-radius: 3px; width: 60%;"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Steps 3 and 4 go here -->
```

- [ ] **Step 2: Open in browser and verify**

```bash
open /Users/tom/github/tom.irish/audiobooks/index.html
```

Expected: Step 1 shows "Get an account" with message button and phone mockup. Step 2 shows "Download Spine" with App Store badge and phone mockup. Badge image may not load locally (external URL) — that's fine, verify on GitHub Pages.

- [ ] **Step 3: Commit**

```bash
cd /Users/tom/github/tom.irish
git add audiobooks/index.html
git commit -m "feat: steps 1 and 2 — get account and download Spine"
git push
```

---

### Task 5: Step 3 (Add server) and Step 4 (Log in)

**Files:**
- Modify: `audiobooks/index.html` — replace `<!-- Steps 3 and 4 go here -->`

- [ ] **Step 1: Add Steps 3 and 4 HTML**

Replace `<!-- Steps 3 and 4 go here -->` with:

```html
      <!-- Step 3: Add the server -->
      <div class="step">
        <div class="step-content">
          <div class="step-number">3</div>
          <h2 class="step-title">Add the server</h2>
          <p class="step-body">
            Open Spine, tap the <strong>+</strong> button, and enter the server address below. Tap <strong>Add</strong> to connect.
          </p>
          <div class="url-block">
            <span class="url-text">https://books.tom.irish</span>
            <button class="copy-btn" onclick="copyUrl()">Copy</button>
          </div>
        </div>
        <div class="phone" aria-hidden="true">
          <div class="phone-screen" style="padding: 14px 10px;">
            <div style="font-size: 11px; font-weight: 700; color: #1a1a1a; margin-bottom: 12px; text-align: center;">Add Server</div>
            <div style="font-size: 8px; color: #6b6b6b; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.4px;">Server Address</div>
            <div style="background: white; border: 1.5px solid #c97d2e; border-radius: 6px; padding: 6px 8px; margin-bottom: 10px;">
              <span style="font-size: 8px; color: #1a1a1a; font-family: monospace;">books.tom.irish</span>
            </div>
            <div style="font-size: 8px; color: #6b6b6b; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.4px;">Nickname (optional)</div>
            <div style="background: white; border: 1.5px solid #e0e0e0; border-radius: 6px; padding: 6px 8px; margin-bottom: 16px; height: 22px;"></div>
            <div style="background: #c97d2e; border-radius: 8px; padding: 7px; text-align: center;">
              <span style="font-size: 9px; font-weight: 700; color: white;">Add Server</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 4: Log in -->
      <div class="step">
        <div class="step-content">
          <div class="step-number">4</div>
          <h2 class="step-title">Log in</h2>
          <p class="step-body">
            Enter the username and password Tom sent you. Your audiobooks will appear automatically.
          </p>
        </div>
        <div class="phone" aria-hidden="true">
          <div class="phone-screen" style="padding: 20px 14px; justify-content: center;">
            <div style="font-size: 13px; font-weight: 700; color: #1a1a1a; margin-bottom: 4px; text-align: center;">Sign In</div>
            <div style="font-size: 8px; color: #6b6b6b; text-align: center; margin-bottom: 16px;">books.tom.irish</div>
            <div style="font-size: 8px; color: #6b6b6b; margin-bottom: 4px;">Username</div>
            <div style="background: white; border: 1.5px solid #e0e0e0; border-radius: 6px; padding: 6px 8px; margin-bottom: 8px; height: 22px;"></div>
            <div style="font-size: 8px; color: #6b6b6b; margin-bottom: 4px;">Password</div>
            <div style="background: white; border: 1.5px solid #e0e0e0; border-radius: 6px; padding: 6px 8px; margin-bottom: 16px; height: 22px;
            display: flex; align-items: center; gap: 4px;">
              <span style="font-size: 10px; color: #999; letter-spacing: 2px;">••••••••</span>
            </div>
            <div style="background: #1a1a1a; border-radius: 8px; padding: 7px; text-align: center;">
              <span style="font-size: 9px; font-weight: 700; color: white;">Sign In</span>
            </div>
          </div>
        </div>
      </div>
```

- [ ] **Step 2: Open in browser and verify**

```bash
open /Users/tom/github/tom.irish/audiobooks/index.html
```

Expected: Step 3 shows server URL with copy button and Add Server phone mockup. Step 4 shows login phone mockup with username/password fields. Click "Copy" button — should copy `https://books.tom.irish` and button text should change to "Copied!" for 2 seconds.

- [ ] **Step 3: Commit**

```bash
cd /Users/tom/github/tom.irish
git add audiobooks/index.html
git commit -m "feat: steps 3 and 4 — add server and log in"
git push
```

---

### Task 6: Footer and mobile polish

**Files:**
- Modify: `audiobooks/index.html` — add footer after `</main>`, verify responsive layout

- [ ] **Step 1: Add footer**

Replace `<!-- Footer goes here -->` with:

```html
  <!-- ── Footer ── -->
  <footer style="border-top: 1px solid var(--border); padding: 32px 24px; text-align: center;">
    <div class="page">
      <p style="color: var(--text-muted); font-size: 15px;">
        Having trouble?
        <a href="sms:+12536702623&body=Hi Tom, I need help with the audiobook app." style="color: var(--accent); font-weight: 600;">Message Tom</a>
      </p>
    </div>
  </footer>
```

- [ ] **Step 2: Open in browser at mobile width and verify**

```bash
open /Users/tom/github/tom.irish/audiobooks/index.html
```

In browser DevTools, set viewport to 375px wide (iPhone). Expected:
- All steps stack vertically (phone frame below text)
- Text is centred on mobile
- URL block wraps cleanly
- No horizontal scroll
- Phone frames don't overflow

- [ ] **Step 3: Commit**

```bash
cd /Users/tom/github/tom.irish
git add audiobooks/index.html
git commit -m "feat: footer and mobile layout"
git push
```

---

### Task 7: DNS setup and live verification

**Files:** None — Cloudflare DNS configuration only

- [ ] **Step 1: Add A records in Cloudflare for tom.irish**

Go to Cloudflare dashboard → tom.irish → DNS → Add records:

| Type | Name | Content | Proxy |
|---|---|---|---|
| A | `@` | `185.199.108.153` | DNS only |
| A | `@` | `185.199.109.153` | DNS only |
| A | `@` | `185.199.110.153` | DNS only |
| A | `@` | `185.199.111.153` | DNS only |
| CNAME | `www` | `tomirish.github.io` | DNS only |

**Critical:** Set all records to **DNS only (grey cloud)** — GitHub Pages breaks with Cloudflare proxy enabled.

- [ ] **Step 2: Wait for GitHub Pages to confirm the domain**

In GitHub repo Settings → Pages, wait for the domain status to show "DNS check successful". May take up to 10 minutes.

- [ ] **Step 3: Verify the page loads**

```bash
curl -s -o /dev/null -w "%{http_code}" https://tom.irish/audiobooks/
```

Expected: `200`

- [ ] **Step 4: Verify redirect from root**

```bash
curl -s -o /dev/null -w "%{http_code}" https://tom.irish/
```

Expected: `200` (the meta-refresh redirect page)

- [ ] **Step 5: Check HTTPS is enforced**

```bash
curl -s -o /dev/null -w "%{http_code}" http://tom.irish/audiobooks/
```

Expected: `301` (redirect to HTTPS)

If not yet redirecting, go to GitHub Pages settings and tick **Enforce HTTPS** once it becomes available (requires DNS propagation).
