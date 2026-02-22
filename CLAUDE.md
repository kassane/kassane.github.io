# CLAUDE.md — Kassane's GitHub Pages Blog

This file provides context for AI assistants (Claude and others) working with this repository.

## Project Overview

**kassane.github.io** is a personal portfolio and blog website for Matheus Catarino (@kassane), a systems programmer with focus on Zig, C/C++, Rust, and embedded systems. The site is built with the **Zine** static site generator and deployed to GitHub Pages.

- **Live site:** https://kassane.github.io
- **Author:** Matheus Catarino
- **Contacts:** [GitHub](https://github.com/kassane) · matheus-catarino@hotmail.com · [LinkedIn](https://www.linkedin.com/in/matcf/) · [@theucatarino](https://twitter.com/theucatarino)

---

## Technology Stack

| Layer | Technology |
|---|---|
| Build system | **Zig** 0.14.0+ |
| Static site generator | **Zine** 0.11.x (Zig-based, via `build.zig.zon`) |
| Content format | `.smd` (SuperMD) |
| Template format | `.shtml` (SuperHTML) |
| Styling | CSS3 with Srcery color palette |
| CSS reset | normalize.css |
| RSS feed | `tools/gen_rss.py` (Python 3, runs in CI after `zig build`) |
| Deployment | GitHub Pages via GitHub Actions |

### Zine

[Zine](https://github.com/kristoff-it/zine) is a Zig-native static site generator. It introduces two custom file formats:

- **`.smd` (SuperMD)** — Markdown with frontmatter using Zig object notation syntax
- **`.shtml` (SuperHTML)** — HTML templates with Zine-specific attribute directives (`:text=`, `:html=`, etc.) and template variables (`$page`, `$site`)

**Current version:** pinned to commit `7feb9e2` in `build.zig.zon`. The repo also includes `zine.ziggy` (site config for Zine v0.11+ API) ready for when the dependency is upgraded. See [Upgrading Zine](#upgrading-zine).

---

## Repository Structure

```
kassane.github.io/
├── CLAUDE.md                  # This file
├── README.md                  # Minimal readme
├── build.zig                  # Zine site configuration (passes args directly)
├── build.zig.zon              # Zig package manifest (pins Zine commit + hash)
├── zine.ziggy                 # Site config for Zine v0.11+ (activate on upgrade)
├── .gitignore                 # Ignores zig-* build artifact directories
├── .github/
│   └── workflows/
│       ├── website.yml        # CI/CD: build, generate RSS, deploy to GitHub Pages
│       └── update-zine.yml    # Scheduled: auto-update Zine dependency via PR
├── assets/                    # Static assets (served as-is)
│   ├── favicon.ico
│   ├── normalize.css          # CSS reset
│   └── style.css              # Main stylesheet (Srcery theme + syntax highlighting)
├── content/                   # Source content (Zine renders these to HTML)
│   ├── index.smd              # Homepage — lists recent posts
│   ├── about.smd              # About page — author profile
│   └── blog/                  # Blog posts directory
│       ├── qt_for_windows.smd # Post: Qt for Windows tips (pt-BR, 2019)
│       ├── zig_pkg.smd        # Post: Zig Package Manager (en-US, 2023/updated 2026)
│       └── vibe_coding_with_claude.smd  # Post: Vibe Coding with Claude (en-US, 2026)
├── layouts/                   # HTML templates used by Zine
│   ├── index.shtml            # Layout for the homepage
│   ├── about.shtml            # Layout for the about page
│   └── article.shtml          # Layout for blog posts (with Giscus placeholder)
└── tools/
    └── gen_rss.py             # Python script: generates zig-out/feed.xml from .smd files
```

---

## Build Configuration

### `build.zig`

```zig
const std = @import("std");
const zine = @import("zine");

pub fn build(b: *std.Build) void {
    zine.website(b, .{
        .title = "Kassane Website",
        .host_url = "https://kassane.github.io",
        .content_dir_path = "content",
        .layouts_dir_path = "layouts",
        .assets_dir_path = "assets",
    });
}
```

### `build.zig.zon`

Declares Zig 0.14.0 as the minimum version and pins Zine to a specific Git commit hash. Do **not** edit the `.hash` field manually — use `zig fetch --save <url>` to update it.

### `zine.ziggy`

Site configuration for the upcoming Zine v0.11+ API (moves config out of `build.zig`). Currently present but inactive — it becomes active once `build.zig` is updated to `zine.website(b, .{})`.

---

## Upgrading Zine

The `update-zine.yml` workflow handles this automatically (runs on the 1st of each month):

1. Detects the latest Zine release tag
2. Runs `zig fetch --save` to refresh URL + hash in `build.zig.zon`
3. Writes/updates `zine.ziggy`
4. Simplifies `build.zig` to `zine.website(b, .{})`
5. Aligns Zig version in `website.yml` and `build.zig.zon`
6. Opens a PR for review

To trigger manually: **Actions → Update Zine → Run workflow**.

---

## Content Format (`.smd` files)

Every `.smd` file begins with a frontmatter block followed by Markdown content.

### Frontmatter syntax

```
---
.title = "Post Title",
.date = @date("YYYY-MM-DDTHH:MM:SS"),
.author = "Matheus Catarino",
.draft = false,
.layout = "article.shtml",
.description = "Short meta description",
.tags = ["tag1", "tag2"]
---

Markdown content here...
```

- `.draft = true` hides the page from the built site (useful for WIP posts)
- `.layout` must reference a filename in the `layouts/` directory
- `.date` uses the Zine `@date(...)` built-in with ISO 8601 format
- `.tags` is an array of strings for categorization
- `.description` is used for `<meta name="description">`, OpenGraph, and Twitter Card tags — keep it under 160 characters

### Available layouts

| Layout file | Used for |
|---|---|
| `index.shtml` | Homepage (`content/index.smd`) |
| `about.shtml` | About page (`content/about.smd`) |
| `article.shtml` | All blog posts under `content/blog/` |

---

## Template Format (`.shtml` files)

Zine's SuperHTML templates use standard HTML with special attribute directives:

| Directive | Description |
|---|---|
| `:text="expr"` | Set text content from expression |
| `:html="expr"` | Render HTML from expression (e.g., page body) |

### Template variables

| Variable | Description |
|---|---|
| `$site.title` | Site title from `build.zig` |
| `$site.asset('name').link()` | URL to an asset in `assets/` |
| `$page.title` | Page title from frontmatter |
| `$page.author` | Author from frontmatter |
| `$page.description` | Description from frontmatter |
| `$page.date.format('January 02, 2006')` | Formatted date |
| `$page.date.format('2006-01-02T15:04:05Z')` | ISO date for OpenGraph |
| `$page.link()` | Canonical URL of the page |
| `$page.content()` | Rendered HTML body of the page |

**Important:** Zine evaluates `$page.*` expressions inside attribute values (e.g., `content="$page.description"`). This powers the per-article OpenGraph and Twitter Card meta tags in `article.shtml`.

### Layout structure: homepage (`index.shtml`)

```
<div class="home_page">
  <div class="container">          ← max-width 860px, centered
    <header class="header">        ← flex row: site title + nav
      <nav class="main-nav">       ← Home / About / RSS links
    </header>
    <main class="main-content" id="main">
      <div :html="$page.content()">
    </main>
    <footer class="site-footer">
  </div>
</div>
```

### Layout structure: article / about pages (`.static_grid`)

```
<div class="static_grid">         ← CSS Grid: [nav-col] [content-col]
  <div class="static_double_column1">   ← sidebar nav (spans 2 rows)
    <nav><ul class="side-nav">          ← Home / About / RSS
  </div>
  <div class="static_double_column2">   ← page title + article-meta
  </div>
  <div class="static_double_column3">   ← main content + footer
    <main id="main">
      <article>
      </article>
      <section class="comments-section">  ← Giscus placeholder (disabled)
    </main>
    <footer class="site-footer">
  </div>
</div>
```

---

## Styling (`assets/style.css`)

Uses **Srcery**, a terminal-inspired dark color palette, defined as CSS custom properties. Always use these variables — never hardcode colors.

### CSS custom properties

```css
:root {
    /* Srcery palette — raw colors */
    --srcery-black:          #1C1B19;
    --srcery-white-bright:   #FCE8C3;  /* page background */
    --srcery-red:            #EF2F27;
    --srcery-green:          #519F50;
    --srcery-yellow:         #FBB829;
    --srcery-blue:           #2C78BF;
    --srcery-magenta:        #E02C6D;
    --srcery-cyan:           #0AAEB3;
    --srcery-orange:         #FF5F00;
    /* ... xgray1–xgray12 shades ... */

    /* Semantic aliases — use these in new rules */
    --color-bg:              var(--srcery-white-bright);
    --color-text:            var(--srcery-black);
    --color-link:            var(--srcery-blue);
    --color-link-hover:      var(--srcery-blue-bright);
    --color-accent:          var(--srcery-red);
    --color-muted:           var(--srcery-black-bright);
    --color-border:          var(--srcery-white);
    --color-code-bg:         var(--srcery-black);
    --color-code-text:       var(--srcery-white-bright);

    /* Layout tokens */
    --content-max-width: 860px;
    --nav-width:         160px;
    --page-padding:      clamp(1rem, 4vw, 2.5rem);
    --space-xs/sm/md/lg/xl: 0.25rem … 2.5rem;
    --border-radius:     4px;
}
```

### Key CSS classes

| Class | Purpose |
|---|---|
| `.skip-link` | Accessibility: off-screen link shown on focus, jumps to `#main` |
| `.visually-hidden` | Screen-reader-only text (WCAG) |
| `.container` | Max-width 860px centered wrapper (homepage) |
| `.header` | Flex row: site title + nav (homepage) |
| `.main-nav` | Top nav bar (homepage) |
| `.nav-link` | Nav link style |
| `.nav-rss` | RSS icon link (orange, flex) |
| `.static_grid` | CSS Grid layout for article/about pages |
| `.static_double_column1/2/3` | Grid columns: sidebar nav / title / content |
| `.side-nav` | Vertical nav list in sidebar (article/about) |
| `.article-meta` | Author + date line under article title |
| `.avatar` | Round profile photo (about page) |
| `.comments-section` | Giscus comments container (currently empty) |
| `.site-footer` | Centered footer with copyright + links |
| `.footer-tech` | "Built with Zig & Zine" secondary footer line |
| `.main-content` | Content padding on homepage |
| `code .keyword` etc. | Syntax highlighting token classes |

### Responsive breakpoints

- `@media (max-width: 640px)` — collapses `.static_grid` to single column
- `@media (max-width: 420px)` — reduces page padding and code font size

### Syntax highlighting

CSS classes for tokens emitted by Zine's code renderer (compact notation):
```css
code .keyword { color: var(--srcery-red) }
code .string  { color: var(--srcery-green-bright) }
/* ... etc */
```
Full list of token classes: `.attribute`, `.boolean`, `.character`, `.comment`, `.constant`, `.constructor`, `.field`, `.float`, `.function`, `.include`, `.keyword`, `.label`, `.macro`, `.method`, `.namespace`, `.number`, `.operator`, `.parameter`, `.preproc`, `.property`, `.punctuation`, `.repeat`, `.storageclass`, `.string`, `.structure`, `.tag`, `.type`, `.variable`, and their sub-variants.

---

## RSS Feed

**File:** `tools/gen_rss.py`
**Output:** `zig-out/feed.xml` (included in the Pages artifact automatically)
**URL:** `https://kassane.github.io/feed.xml`

The script reads `.smd` frontmatter from `content/blog/`, skips drafts, sorts by date (newest first), and writes a valid RSS 2.0 + Atom namespace feed. It runs in CI after `zig build`.

To generate locally:
```sh
zig build         # must run first — creates zig-out/
python3 tools/gen_rss.py
```

The RSS link (`<link rel="alternate">`) is present in all three layouts.

---

## Comments (Giscus — pending setup)

**File:** `layouts/article.shtml`

A Giscus comments section is scaffolded in every article but the `<script>` is commented out until the GitHub App is installed:

```
Error: "An error occurred: giscus is not installed on this repository"
```

**To enable Giscus:**
1. Enable GitHub Discussions on `kassane/kassane.github.io` (Settings → General → Features)
2. Install the [Giscus GitHub App](https://github.com/apps/giscus) on the repository
3. Visit https://giscus.app, select the repo, and copy the generated `data-repo-id` and `data-category-id`
4. In `layouts/article.shtml`, uncomment the `<script>` block and replace `REPLACE_WITH_REPO_ID` / `REPLACE_WITH_CATEGORY_ID`

---

## Adding a New Blog Post

1. Create `content/blog/my_post.smd` with complete frontmatter:

```
---
.title = "My Post Title",
.date = @date("2026-02-22T00:00:00"),
.author = "Matheus Catarino",
.draft = false,
.layout = "article.shtml",
.description = "A brief description for meta tags and RSS (max ~160 chars).",
.tags = ["article", "zig", "topic"]
---

## Post content here

Write Markdown as usual...
```

2. Add a link to `content/index.smd` under Recent Posts:

```md
* 2026-02-22 - [My Post Title](/blog/my_post)
```

3. Build and verify locally:
```sh
zig build
python3 tools/gen_rss.py   # optional: check the RSS output
python3 -m http.server --directory zig-out 8080
```

---

## Development Workflow

### Prerequisites

- [Zig 0.14.0](https://ziglang.org/download/) installed and in `PATH`
- Python 3.8+ (for RSS generation — standard library only, no extra packages)
- Internet access on first build (Zine is fetched automatically by Zig)

### Local build

```sh
zig build
```

Output is written to `zig-out/`. Serve locally with:

```sh
python3 -m http.server --directory zig-out 8080
```

### Useful build flags

```sh
zig build --summary new    # show build step summary
zig build --fetch          # re-fetch/verify dependencies
```

---

## CI/CD: GitHub Actions

### `website.yml` — Deploy pipeline

**Triggers:** push to `main`, published release, `workflow_dispatch`

**Pipeline steps (build job):**
1. `actions/checkout@v4` — full history (`fetch-depth: 0`)
2. `actions/configure-pages@v5` — signals custom Pages deployment (prevents Jekyll fallback)
3. `mlugg/setup-zig@v1` — installs Zig 0.13.0
4. `zig build --summary new` — builds the site into `zig-out/`
5. `python3 tools/gen_rss.py` — writes `zig-out/feed.xml`
6. `actions/upload-pages-artifact@v3` — uploads `zig-out/` as Pages artifact

**Deploy job:** `actions/deploy-pages@v4` → `github-pages` environment

**Required GitHub settings:**
- Pages source **must** be **"GitHub Actions"** (Settings → Pages → Source). If set to "Deploy from a branch", GitHub also runs `jekyll-build-pages` which fails on `.smd` frontmatter.
- `GITHUB_TOKEN` needs `pages: write` and `id-token: write` (already in the workflow).

**Why `configure-pages` is required:** Without it GitHub Pages may fall back to the `jekyll-build-pages` Docker image on the repository source directory, which fails on `.smd` syntax.

### `update-zine.yml` — Automated dependency updates

**Triggers:** first day of each month (08:00 UTC), `workflow_dispatch`

Checks the latest Zine release, and if it differs from the pinned commit, opens a PR that updates `build.zig.zon`, `zine.ziggy`, `build.zig`, and the Zig version in `website.yml`. Requires `contents: write` and `pull-requests: write` permissions.

---

## Existing Content

| File | URL path | Language | Date | Topic |
|---|---|---|---|---|
| `content/index.smd` | `/` | — | 2026-02-19 | Homepage / post index |
| `content/about.smd` | `/about/` | en-US | 2025-01-19 | Author profile |
| `content/blog/qt_for_windows.smd` | `/blog/qt_for_windows/` | pt-BR | 2019-07-07 | Qt development on Windows |
| `content/blog/zig_pkg.smd` | `/blog/zig_pkg/` | en-US | 2023-05-02 (updated 2026) | Zig package manager |
| `content/blog/vibe_coding_with_claude.smd` | `/blog/vibe_coding_with_claude/` | en-US | 2026-02-19 | AI-assisted development with Claude |

---

## Key Conventions for AI Assistants

### Do

- **Preserve all existing content** — posts, about page, and user profile information must never be deleted or altered without explicit instruction
- **Use `.smd` format** for all new content files
- **Use `.shtml` format** for new or modified layout templates
- **Place blog posts** in `content/blog/` and link them from `content/index.smd`
- **Use `article.shtml`** as the layout for all blog posts
- **Keep frontmatter complete** — all fields (`.title`, `.date`, `.author`, `.draft`, `.layout`, `.description`, `.tags`) must be present; `.description` is used in meta tags and RSS
- **Use CSS custom properties** — `var(--color-*)` semantic aliases preferred over raw `var(--srcery-*)` for new rules
- **Run `zig build` before committing** to catch template or frontmatter errors
- **Reference assets** via `$site.asset('filename').link()` — never hardcode paths

### Do not

- Do not create a `package.json` or add Node.js/npm tooling — this project uses Zig only
- Do not add a `_config.yml` or any Jekyll configuration — this is not a Jekyll site
- Do not modify `.hash` in `build.zig.zon` manually — use `zig fetch --save <url>`
- Do not push to `main` directly — use pull requests
- Do not set `.draft = true` on published posts unless intentionally hiding them
- Do not use JavaScript frameworks or bundlers — the site is intentionally minimal
- Do not hardcode colors — always use `--srcery-*` or `--color-*` CSS variables
- Do not enable Giscus by uncommenting the script unless the GitHub App is installed first (it will show an error to visitors)

### When modifying layouts

- Navigation must always include links to Home (`/`), About (`/about/`), and the RSS feed (`/feed.xml`)
- The `<a class="skip-link" href="#main">` must remain at the top of `<body>` in every layout
- `id="main"` must be present on the main content element (for skip-link target)
- OpenGraph and Twitter Card meta tags are in every layout's `<head>` — keep them when editing
- The RSS `<link rel="alternate">` must remain in every layout's `<head>`

### When modifying CSS

- Add new color variables to the `:root` block at the top of `style.css`
- Follow the `--srcery-<name>` naming convention for raw palette colors
- Add semantic aliases (`--color-<role>`) for new semantic uses
- Syntax highlighting classes go under `code .classname { color: var(...) }` selectors (compact one-liner format)
- Responsive rules go in the existing `@media` blocks at the bottom of the file

### When modifying `gen_rss.py`

- The script uses only Python standard library — do not add pip dependencies
- It reads `content/blog/*.smd`, skips drafts (`.draft = true`), and outputs `zig-out/feed.xml`
- The output file location (`zig-out/`) must match the `path:` in `upload-pages-artifact`

---

## Author Profile (for reference)

**Matheus Catarino** (@kassane)

- **Focus:** Systems programming, embedded systems, performance optimization, cross-platform development
- **Languages:** Zig, C/C++, Rust, Python
- **Tools:** Git, CMake, Meson, Docker
- **OSes:** Linux, Windows, macOS
- **Embedded targets:** ARM, RISC-V

**Notable open-source projects:**
- [qml-zig](https://github.com/kassane/qml_zig) — Zig bindings for Qt Quick
- [zig-esp-idf-sample](https://github.com/kassane/zig-esp-idf-sample) — Zig samples for ESP-IDF
- [llvm-zig](https://github.com/kassane/llvm-zig) — Zig bindings for LLVM
- [libvlc-zig](https://github.com/kassane/libvlc-zig) — Zig bindings for libvlc
- [openssl-zig](https://github.com/kassane/openssl-zig) — Build OpenSSL with zig-build
- [wolfssl-zig](https://github.com/kassane/wolfssl) — Build wolfSSL with zig-build
- [sokol-d](https://github.com/kassane/sokol-d) — D bindings for sokol
