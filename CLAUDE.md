# CLAUDE.md — kassane.github.io

Personal portfolio/blog for Matheus Catarino (@kassane), a systems programmer. Built with **Zig 0.15 + Zine 0.11.2** (Zig-native SSG), deployed to GitHub Pages.

- Live: https://kassane.github.io  
- Contacts: [GitHub](https://github.com/kassane) · matheus-catarino@hotmail.com · [LinkedIn](https://www.linkedin.com/in/matcf/) · [@theucatarino](https://twitter.com/theucatarino)

---

## Stack

| Layer | Tech |
|---|---|
| Build | Zig 0.15.0 via `build.zig` |
| SSG | Zine 0.11.2 (`build.zig.zon` pin) |
| Content | `.smd` (SuperMD — Markdown + Ziggy frontmatter) |
| Templates | `.shtml` (SuperHTML — HTML + `:text`/`:html`/`:loop`/`:attr-*` directives) |
| CSS | Srcery palette, CSS custom properties, `assets/style.css` |
| RSS | `tools/gen_rss.py` → `zig-out/feed.xml` |

---

## Repo layout

```
content/          # .smd source pages
  index.smd       # homepage (layout: index.shtml)
  about.smd       # about page (layout: about.shtml)
  blog/           # posts (layout: article.shtml)
layouts/          # .shtml templates
assets/           # CSS, favicon (served as-is)
tools/gen_rss.py  # generates RSS feed
build.zig         # calls zine.website(b, .{})
build.zig.zon     # pins Zine commit hash
zine.ziggy        # Zine site config (v0.11+)
```

---

## Frontmatter (every `.smd`)

```
---
.title = "Post Title",
.date = @date("2026-01-01T00:00:00"),
.author = "Matheus Catarino",
.draft = false,
.layout = "article.shtml",
.description = "Under 160 chars for meta/RSS.",
.tags = ["article", "zig", "en-US"]
---
```

- Language convention: include `"en-US"` or `"pt-BR"` in `.tags`
- `.draft = true` hides the page from the build output
- Do **not** use `.custom = .{ ... }` — Zine's Ziggy parser rejects struct literals in frontmatter

---

## SuperHTML directives

| Directive | Purpose |
|---|---|
| `:text="expr"` | Set element text content |
| `:html="expr"` | Render HTML (e.g. `$page.content()`) |
| `:loop="expr"` | Repeat element for each item; use `$loop.it` / `$loop.idx` |
| `:if="expr"` | Conditional render; unwrapped value via `$if` |
| `:attr-name="expr"` | Set arbitrary HTML attribute dynamically |

### Key Scripty variables

| Variable | Value |
|---|---|
| `$site.title` | Site title |
| `$site.asset('f').link()` | URL to asset in `assets/` |
| `$page.title` | Frontmatter `.title` |
| `$page.author` | Frontmatter `.author` |
| `$page.description` | Frontmatter `.description` |
| `$page.date.format('January 02, 2006')` | Formatted date |
| `$page.link()` | Canonical URL |
| `$page.content()` | Rendered page body HTML |
| `$page.tags` | Array of tag strings (use with `:loop`) |

---

## CSS conventions

- **Always use CSS variables** — `var(--color-*)` semantic aliases or `var(--srcery-*)` raw palette; never hardcode colors.
- Semantic aliases: `--color-bg`, `--color-text`, `--color-link`, `--color-accent`, `--color-muted`, `--color-border`, `--color-code-bg`, `--color-code-text`.
- Layout tokens: `--content-max-width: 860px`, `--nav-width: 160px`, `--page-padding: clamp(1rem, 4vw, 2.5rem)`.
- Responsive breakpoints at `640px` (collapse sidebar) and `420px` (small phones).

### Tag badges (`.tag` in `article.shtml`)

Tags rendered via `:loop="$page.tags"` with `:attr-data-tag="$loop.it"`. Language tags get distinct colours:
- `.tag[data-tag="pt-BR"]` → green badge
- `.tag[data-tag="en-US"]` → blue badge

---

## Adding a blog post

1. Create `content/blog/slug.smd` with complete frontmatter (all fields required).
2. Add link in `content/index.smd` under Recent Posts.
3. Build: `zig build` then optionally `python3 tools/gen_rss.py`.

---

## Layouts

| File | Used by |
|---|---|
| `index.shtml` | `content/index.smd` |
| `about.shtml` | `content/about.smd` |
| `article.shtml` | All `content/blog/*.smd` |

Every layout must keep:
- `<a class="skip-link" href="#main">` at top of `<body>`
- `id="main"` on the main content element
- Nav links: Home (`/`), About (`/about/`), RSS (`/feed.xml`)
- `<link rel="alternate" ...>` for RSS in `<head>`
- OpenGraph + Twitter Card meta tags in `<head>`

---

## Existing posts

| File | Lang | Date | Topic |
|---|---|---|---|
| `blog/qt_for_windows.smd` | pt-BR | 2019-07-07 | Qt on Windows |
| `blog/zig_pkg.smd` | en-US | 2023-05-02 | Zig package manager |
| `blog/vibe_coding_with_claude.smd` | en-US | 2026-02-21 | AI-assisted dev |
| `blog/local_llm_ollama.smd` | pt-BR | 2026-03-04 | Local LLMs / Ollama |

---

## Key rules

**Do:**
- Use `.smd` for content, `.shtml` for templates
- Keep all frontmatter fields present
- Reference assets via `$site.asset('name').link()`
- Use `var(--color-*)` in CSS

**Do not:**
- Push to `main` directly — use PRs
- Modify `.hash` in `build.zig.zon` manually — use `zig fetch --save`
- Add Node.js/npm, Jekyll config, or JS frameworks
- Hardcode colors or asset paths
- Use `.custom = .{ ... }` struct syntax in frontmatter (Zine rejects it)
- Enable Giscus comments until the GitHub App is installed

---

## Author

**Matheus Catarino** (@kassane) — Systems/embedded developer, focus on Zig, C/C++, Rust.  
Notable projects: [qml-zig](https://github.com/kassane/qml_zig), [zig-esp-idf-sample](https://github.com/kassane/zig-esp-idf-sample), [llvm-zig](https://github.com/kassane/llvm-zig), [libvlc-zig](https://github.com/kassane/libvlc-zig), [openssl-zig](https://github.com/kassane/openssl-zig).
