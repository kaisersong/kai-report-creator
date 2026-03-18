# Theme CSS

When generating HTML, load theme CSS from `templates/themes/` (relative to this skill file's directory).

**CSS assembly order in `<style>`:**
1. Read `templates/themes/[theme-name].css` — embed everything **before** `/* === POST-SHARED OVERRIDE */`
2. Read `templates/themes/shared.css` — embed in full
3. From `[theme-name].css` — embed everything **after** `/* === POST-SHARED OVERRIDE */` (if present)
4. If `theme_overrides` is set in frontmatter, append `:root { ... }` override block last

**Theme names:** `corporate-blue`, `minimal`, `dark-tech`, `dark-board`, `data-story`, `newspaper`

**Themes with POST-SHARED OVERRIDE sections:** `dark-board`, `data-story`, `newspaper`

**Special code block note:** `dark-tech` and `dark-board` use `github-dark.min.css` instead of `github.min.css` for highlight.js.