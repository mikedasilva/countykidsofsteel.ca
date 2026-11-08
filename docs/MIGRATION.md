# Squarespace to GitHub Pages migration

## Phase 1: migrate as-is to GitHub Pages

All 20 Squarespace pages rebuilt as plain HTML, keeping their URLs, text, links and layout.

### Intentional differences from the old site

- **Newsletter forms** (home, registration) are now a "Sign Up" button that opens an email to
  info@countykidsofsteel.ca. A static site has no backend to receive form posts. Needs a decision
  before Phase 3, see below.
- **Button font**: Proxima Nova is licensed through Squarespace, so secondary buttons and the
  header Register button use Aileron.
- **Background videos** are re-encoded to MP4 with no audio, and served from `videos/`.
- **Scroll-in animations** were dropped. Section divider shapes and the hand-drawn underline are
  close approximations rather than exact copies.

## Phase 2: move galleries to Cloudflare R2

**Galleries still load from Squarespace's CDN** (`images.squarespace-cdn.com`). This must be finished
before the Squarespace subscription ends, or those photos disappear.

- `docs/gallery-manifest.json` lists each gallery photo: page, section, source URL, filename, size.
- 291 entries, 253 unique photos: all 253 are on `/photos`, and the 38 on `/volunteer` repeat photos from there.
- Steps: download originals, generate web sizes, upload to R2, serve from a custom domain, then
  rewrite the `<img>` URLs in `photos.html` and `volunteer.html`.

## Phase 3: DNS cutover

Add a `CNAME` file only at this point. Adding it earlier makes the github.io preview redirect to the
domain, which still points at Squarespace.

**Do not disturb email.** The domain's nameservers are `ns-cloud-d*.googledomains.com`, and its MX
records point to Google Workspace. Change only the apex A/AAAA records and the `www` CNAME. Leave the
MX records and the `google-site-verification` TXT record as they are.

Before cancelling Squarespace:

- [ ] Galleries moved to R2 (Phase 2)
- [ ] Decide where newsletter signups go, and export existing subscribers from Squarespace
- [ ] Decide the canonical host. Pages currently declare the apex (`countykidsofsteel.ca`), matching
      countykidsclub. The old site's primary host is `www`.
- [ ] Confirm where the domain is registered, so it does not lapse with the Squarespace plan
- [ ] Enforce HTTPS in the GitHub Pages settings once the certificate is issued
- [ ] Resubmit `sitemap.xml` in Google Search Console

## Phase 4: optimization backlog

Existing issues, kept unchanged during the as-is migration:

### Broken or outdated content

- Home "LET'S DO THIS!" button links to `/2025-kids-of-steel-triathlon-2`, which is a 404 on the
  old site too.
- "Misson Statement" typo on the home page.
- Home and sponsor text mention 2025 ("sponsors for the 2025 triathlon", "Thank You to Our 2025
  Sponsors" alongside a 2026 heading).
- Home still says "Early Bird Pricing ends April 14th" and promotes June 7, 2026, which has passed.

### SEO and metadata

- `/photos` has the title "Volunteer | Join & Inspire Youth" and the volunteer description.
- `/contact` has the title "Contact 3". Several pages share "Participant Guide".
- Most images have empty alt text.
- Tracking parameters (`gclid`, `gbraid`) are hard-coded in the Home Hardware and Albert College links.

### Structure

- Pages not in the navigation: `faq-2`, `bike-safety`, `new-page`, `first-time-guide-1`,
  `participant-guide-1`. `faqs-3` links to `bike-safety`, so check before removing it.
- Awkward slugs (`faqs-3`, `our-team-1`, `new-page`) could be renamed, with redirects.

### Performance

- Large PNGs: `images/kos-parking-map-2026.png` (6 MB) and `images/kos-drop-go-map.png` (4 MB).
- Most images are 1500px wide with no `srcset` or modern formats.
- Inline layout variables in each block could become shared classes as pages get reworked.
