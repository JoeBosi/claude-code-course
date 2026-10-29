# Brief for translating a course page Italian → English

Repo: /root/Developer/Claude-Course (Astro Starlight). Source: `src/content/docs/<path>.mdx`.
Target: `src/content/docs/en/<same path>.mdx` (create the folder if needed). Do not edit Italian files.

1. Read `docs/glossary-en.md` first and use its renderings, headings and anchor links everywhere.
2. Translate ONLY prose: frontmatter `title` and `description`, headings, paragraphs, list items, table text,
   `<Zero title="...">` titles, Aside/details/summary text, Mermaid node labels (text inside the diagram),
   image alt text, and the Italian comments inside code blocks (`# ...`, `// ...`).
3. Keep byte-identical: code, commands, command output, file names, paths, flags, env vars, JSON/YAML keys,
   import lines, component names and props other than titles, URLs to external sites, `syncKey="os"`,
   TabItem labels (macOS/Windows/Linux). Prompts already in English stay as they are; the Italian one-line
   paraphrase that follows a prompt is translated normally.
4. Internal links: `/x/y/` → `/en/x/y/`; cross-page anchors per the glossary table; same-page `#anchors`
   must match your translated headings (Starlight slug: lowercase, spaces → `-`, punctuation removed,
   an em dash surrounded by spaces gives `--`). `/downloads/*.zip` links stay unchanged.
5. Style: natural, clear technical English for developers and beginners, same tone and structure as the
   Italian; do not add, drop or summarize content; no apologies or hedging. Dates as "16 August 2026".
   The author is "Prof. Giuseppe Bosi"; never write M.Sc., Ing., or "licensed engineer".
6. When done, check: `grep -c '' ` similar line counts; no Italian sentences left (`grep -nE " (il|che|della|perché|sono) "`
   on the new file should return only code lines). Do not run the build (another process may be running it).
Report: files written, line counts IT vs EN, and any anchor/link you were unsure about.
