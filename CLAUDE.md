# County Kids of Steel website

Static site for countykidsofsteel.ca, hosted on GitHub Pages (no build step; `.nojekyll` keeps
Jekyll off). Plain HTML pages share `shared.css` and `site.js`. Changes go straight to `main`.
Same patterns as the sister site, County Kids Club (`mikedasilva/countykidsclub`).

Migrated from Squarespace. See `docs/MIGRATION.md` for phase status and the backlog of known
content issues deliberately kept during the as-is migration.

## Conventions

- **Links are relative** (`about`, `./`, `images/x.jpg`), never root-absolute. Until the custom
  domain goes live (Phase 3) the site is served from a `/countykidsofsteel.ca/` subpath.
- **URLs are preserved from Squarespace**, including odd slugs (`faqs-3`, `our-team-1`, `new-page`).
  GitHub Pages serves `about.html` at `/about`. Do not rename a page without leaving a redirect stub.
- **Redirect stubs** (`home`, `sponsors`, `participant`, `race-day`, `about-1`) reproduce redirects
  from the old site with a meta refresh.
- **The header and footer are repeated in every page.** A nav or footer change must be made in all
  `*.html` files, including `404.html`.
- **PDFs live at `s/<name>.pdf`** so the old `/s/...` URLs keep working.

## Page layout

Each `<section class="sec t-THEME">` has a theme (`t-white`, `t-light`, `t-light-bold`, `t-bright`,
`t-black`) that sets its colours. Inside, `.fe` is a grid mirroring the original layout: 24 columns
on desktop and 8 on mobile. Each `.b` block places itself with inline `--d` (desktop) and `--m`
(mobile) `grid-area` values. `--rd`, `--rm` and `--rf` set row counts and scale on the section.

## Images

- Site images (logos, heroes, maps, team photos) are committed under `images/`.
- Photo galleries (`photos.html`, bottom of `volunteer.html`) are not committed. They live in the
  Cloudflare R2 bucket `countykidsofsteel-photos`, served at `https://photos.countykidsofsteel.ca/`.
  `docs/gallery-manifest.json` lists the migrated photos (`key` is the file name in the bucket).
- Bucket layout: `gallery/750/<key>.webp` and `gallery/1500/<key>.webp` are used by the pages via
  `srcset`; `gallery/full/<key>.jpg` is a 2500px archive copy. Bucket files are cached for a year,
  so never replace a file in place: give a changed photo a new key.
- **Adding photos:** run `python3 tools/gallery.py <photo folder> <out folder> --layout grid`
  (needs Pillow), paste the printed `<figure>` tags into the gallery, then upload with
  `rclone copy <out folder> r2:countykidsofsteel-photos --s3-no-check-bucket --header-upload
  "Cache-Control: public, max-age=31536000, immutable"`. The `r2` rclone remote uses an API token
  limited to that bucket, so `rclone lsd r2:` failing with AccessDenied is expected.

## Fonts

Lora, Asap and Acme come from Google Fonts. Aileron (CC0) is self-hosted in `fonts/`. The old site's
button font, Proxima Nova, is licensed through Squarespace/Adobe, so buttons use Aileron instead.

## Previewing locally

Extensionless links need a server that resolves `.html`, e.g. `npx serve .`
