# HyperCode Homepage (Single-File)

This is a **production-ready, dependency-free** homepage for HyperCode.

## Edit & ship

Open `index.html` and edit the **CONFIG** block near the bottom:

- `CONFIG.site.url` — your real domain (or GitHub Pages URL)
- `CONFIG.links.githubRepo` — your repo
- `CONFIG.links.discord` — your Discord invite
- Optional: fill `CONFIG.stats` or leave them `null` to show “—”

## Deploy (fast)

### GitHub Pages
1. Put `index.html` at repo root (or `/docs`)
2. GitHub → Settings → Pages → set source to your branch/folder
3. Done

### Netlify
Drag-and-drop `index.html` into Netlify (it will host a static site instantly).

### Cloudflare Pages
Create a Pages project → upload as static.

### IPFS
Pin `index.html` (or a folder containing it) and point your domain at the CID.

## Add an OG image (optional)
Create `og.png` at your site root and set `CONFIG.site.ogImage`.

---
Made for clarity + accessibility + flow.
