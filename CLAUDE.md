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
| Build system | **Zig** 0.13.0+ |
| Static site generator | **Zine** (Zig-based, via `build.zig.zon`) |
| Content format | `.smd` (Spaced Markdown / SuperMD) |
| Template format | `.shtml` (SuperHTML) |
| Styling | CSS3 with Srcery color palette |
| CSS reset | normalize.css |
| Deployment | GitHub Pages via GitHub Actions |

### Zine

[Zine](https://github.com/kristoff-it/zine) is a Zig-native static site generator. It introduces two custom file formats:

- **`.smd` (SuperMD)** — Markdown with YAML-like frontmatter using Zig object notation syntax
- **`.shtml` (SuperHTML)** — HTML templates with Zine-specific attribute directives (`:text=`, `:html=`, etc.) and template variables (`$page`, `$site`)

---

## Repository Structure

```
kassane.github.io/
├── CLAUDE.md                  # This file
├── README.md                  # Minimal readme
├── build.zig                  # Zine site configuration
├── build.zig.zon              # Zig package manifest (declares Zine as dependency)
├── .gitignore                 # Ignores zig-* build artifact directories
├── .github/
│   └── workflows/
│       └── website.yml        # CI/CD: builds and deploys to GitHub Pages
├── assets/                    # Static assets (served as-is)
│   ├── favicon.ico
│   ├── normalize.css          # CSS reset
│   └── style.css              # Main stylesheet (Srcery theme, syntax highlighting)
├── content/                   # Source content (Zine renders these to HTML)
│   ├── index.smd              # Homepage — lists recent posts
│   ├── about.smd              # About page — author profile
│   └── blog/                  # Blog posts directory
│       ├── qt_for_windows.smd # Post: Qt for Windows tips (pt-BR, 2019)
│       └── zig_pkg.smd        # Post: Zig Package Manager v0.11.x (en-US, 2023)
└── layouts/                   # HTML templates used by Zine
    ├── index.shtml            # Layout for the homepage
    ├── about.shtml            # Layout for the about page
    └── article.shtml          # Layout for blog posts
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

This is the only build configuration needed. Zine handles all content processing.

### `build.zig.zon`

Declares Zig 0.13.0 as the minimum version and pins Zine to a specific Git commit. To update Zine, change the `url` commit hash and update `.hash` using `zig build --fetch`.

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
| `$page.date.format('January 02, 2006')` | Formatted date |
| `$page.content()` | Rendered HTML body of the page |

### Grid layout classes (CSS)

The `about.shtml` and `article.shtml` layouts use a CSS grid system:

- `.static_grid` — grid container
- `.static_double_column1` — navigation column (home/about links)
- `.static_double_column2` — title/metadata column
- `.static_double_column3` — main content column

---

## Styling

`assets/style.css` uses **Srcery**, a terminal-inspired dark color palette, defined as CSS custom properties:

```css
:root {
    --srcery-black: #1C1B19;
    --srcery-white-bright: #FCE8C3;   /* page background */
    --srcery-red: #EF2F27;
    --srcery-green: #519F50;
    --srcery-yellow: #FBB829;
    --srcery-blue: #2C78BF;
    /* ... and more */
}
```

### Code syntax highlighting

CSS classes for syntax tokens (used by Zine's code block renderer):
`.attribute`, `.boolean`, `.comment`, `.constant`, `.function`, `.keyword`, `.string`, `.type`, `.variable`, etc.

Code blocks use a dark background (`--srcery-black`) with light text.

---

## Adding a New Blog Post

1. Create a new `.smd` file under `content/blog/`:

```
content/blog/my_post.smd
```

2. Add the required frontmatter at the top:

```
---
.title = "My Post Title",
.date = @date("2026-02-20T00:00:00"),
.author = "Matheus Catarino",
.draft = false,
.layout = "article.shtml",
.description = "A brief description for meta tags",
.tags = ["article", "zig", "topic"]
---

## Post content here

Write Markdown as usual...
```

3. Add a link to the new post in `content/index.smd`:

```md
## Recent Posts
* 2019-07-07 - [Qt for Windows](/blog/qt_for_windows)
* 2023-05-02 - [zig-pkg](/blog/zig_pkg)
* 2026-02-20 - [My Post Title](/blog/my_post)
```

4. Build locally to verify: `zig build`

The generated site is placed in `zig-out/`.

---

## Development Workflow

### Prerequisites

- [Zig 0.13.0](https://ziglang.org/download/) installed and in `PATH`
- Internet access on first build (Zine is fetched automatically by Zig)

### Local build

```sh
zig build
```

Output is written to `zig-out/`. To serve locally, use any static file server:

```sh
# Python example
python3 -m http.server --directory zig-out 8080
```

### Build with summary

```sh
zig build --summary new
```

### Fetching/updating dependencies

```sh
zig build --fetch
```

---

## CI/CD: GitHub Actions

**File:** `.github/workflows/website.yml`

**Triggers:**
- Manual (`workflow_dispatch`)
- Push to `main` branch
- Published release

**Pipeline steps:**
1. `actions/checkout@v4` — full history (`fetch-depth: 0`)
2. `mlugg/setup-zig@v1` — installs Zig 0.13.0
3. `zig build --summary new` — builds the site
4. `actions/upload-pages-artifact@v3` — uploads `zig-out/` as GitHub Pages artifact
5. `actions/deploy-pages@v4` — deploys to the `github-pages` environment

**Required GitHub repository settings:**
- GitHub Pages source must be set to "GitHub Actions"
- The `GITHUB_TOKEN` needs `pages: write` and `id-token: write` permissions (already configured in the workflow)

---

## Existing Content

| File | URL path | Language | Date | Topic |
|---|---|---|---|---|
| `content/index.smd` | `/` | — | 2025-01-19 | Homepage / post index |
| `content/about.smd` | `/about/` | en-US | 2025-01-19 | Author profile |
| `content/blog/qt_for_windows.smd` | `/blog/qt_for_windows/` | pt-BR | 2019-07-07 | Qt development on Windows |
| `content/blog/zig_pkg.smd` | `/blog/zig_pkg/` | en-US | 2023-05-02 | Zig package manager v0.11.x |

---

## Key Conventions for AI Assistants

### Do

- **Preserve all existing content** — posts, about page, and user profile information must never be deleted or altered without explicit instruction
- **Use `.smd` format** for all new content files
- **Use `.shtml` format** for new or modified layout templates
- **Place blog posts** in `content/blog/` and link them from `content/index.smd`
- **Use `article.shtml`** as the layout for all blog posts
- **Keep frontmatter complete** — all fields (`.title`, `.date`, `.author`, `.draft`, `.layout`, `.description`, `.tags`) should be present
- **Follow the Srcery color palette** when adding new CSS — use existing CSS variables, do not hardcode colors
- **Test with `zig build`** before committing

### Do not

- Do not create a `package.json` or add Node.js/npm tooling — this project uses Zig only
- Do not add a `_config.yml` or Jekyll configuration — this is not a Jekyll site
- Do not modify `build.zig.zon` dependency hashes manually — use `zig build --fetch` to update them
- Do not push to `main` directly — use pull requests
- Do not set `.draft = true` on published posts unless intentionally hiding them
- Do not use JavaScript frameworks or bundlers — the site is intentionally minimal static HTML

### When modifying layouts

- The homepage (`index.shtml`) uses `.container` with max-width 900px
- Article and about pages use `.static_grid` with three column divs
- Navigation always includes links to Home (`/`) and About (`/about/`)
- Assets are referenced via `$site.asset('filename').link()` — never hardcode asset paths

### When modifying CSS

- Add new color variables to the `:root` block at the top of `style.css`
- Follow the `--srcery-<name>` naming convention for new variables
- Syntax highlighting classes go under `code .classname` selectors

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
