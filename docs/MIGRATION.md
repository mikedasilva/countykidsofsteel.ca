# Squarespace to GitHub Pages migration

## Phase 1: migrate as-is to GitHub Pages

All 20 Squarespace pages rebuilt as plain HTML, keeping their URLs, text, links and layout.

### Intentional differences from the old site

- **Newsletter forms** (home, registration) are now a "Sign Up" button that opens an email to
  info@countykidsofsteel.ca. A static site has no backend to receive form posts. This stays until
  a newsletter service is chosen.
- **Button font**: Proxima Nova is licensed through Squarespace, so secondary buttons and the
  header Register button use Aileron.
- **Background videos** are re-encoded to MP4 with no audio, and served from `videos/`.
- **Scroll-in animations** were dropped. Section divider shapes and the hand-drawn underline are
  close approximations rather than exact copies.

## Phase 2: move galleries to Cloudflare R2

**Done (2026-11-11).** Galleries load from the R2 bucket `countykidsofsteel-photos` at
`https://photos.countykidsofsteel.ca/`. Nothing on the site references Squarespace's CDN any more.

- DNS for the domain moved to Cloudflare (nameservers `deborah`/`kobe.ns.cloudflare.com`), because
  an R2 custom domain must be a zone in the same Cloudflare account. The registration stays with
  Squarespace (Tucows), expiring 2027-10-25. All records were copied: apex A and `www` (still the
  Squarespace site), Google Workspace MX, DKIM (`google._domainkey`), DMARC, and site verification.
- 253 unique photos (all on `/photos`; the 38 on `/volunteer` reuse them), 759 files, about 99 MB.
- **Squarespace's CDN only serves copies up to 2500px wide**, so the true camera originals (up to
  6240px) were not recovered. `gallery/full/` holds the 2500px copies. If the photographer still
  has the originals, keep them somewhere safe.
- One Squarespace filename, `IMG_9061+%281%29`, was renamed `IMG_9061-1`.
- Each image has a 750px and 1500px WebP with `srcset`, so phones load the small one. Pages kept
  their exact layout heights.
- `tools/gallery.py` prepares new photos the same way; see `CLAUDE.md`.

## Phase 3: DNS cutover

Add a `CNAME` file only at this point. Adding it earlier makes the github.io preview redirect to the
domain, which still points at Squarespace.

DNS is now managed in Cloudflare. **Do not disturb email**: change only the apex A record and the
`www` CNAME. Leave the MX, DKIM, DMARC and `google-site-verification` records as they are.

- Apex: replace the Squarespace A record with GitHub Pages' four A records (185.199.108-111.153)
  and the AAAA records (2606:50c0:8000-8003::153), set to **DNS only** (grey cloud) so GitHub can
  issue the HTTPS certificate.
- `www`: CNAME to `mikedasilva.github.io`, DNS only. GitHub redirects it to the apex.
- The apex and `www` records are currently proxied (orange cloud) while still pointing at
  Squarespace. That works today; switch them to DNS only at cutover.

Before cancelling Squarespace:

- [x] Galleries moved to R2 (Phase 2)
- [ ] Keep the domain registration (billed by Squarespace, separate from the website plan) renewing,
      or transfer it to another `.ca` registrar
- [ ] Export existing newsletter subscribers from Squarespace. Decided: signups stay as the email
      button until a newsletter service is chosen later.
- [x] Canonical host decided: the apex, `countykidsofsteel.ca`, with `www` redirecting to it.
      Pages already declare the apex.
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
