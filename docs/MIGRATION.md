# Squarespace to GitHub Pages migration

## Status (updated 2026-11-14)

| Phase | State |
|---|---|
| 1. Rebuild the site on GitHub Pages | **Done.** Live preview: https://mikedasilva.github.io/countykidsofsteel.ca/ |
| 2. Galleries on Cloudflare R2 | **Done.** Served from https://photos.countykidsofsteel.ca/ |
| 3. Point countykidsofsteel.ca at GitHub Pages | **Next.** Not started; steps below |
| 4. Fix content, SEO, structure, performance | Backlog below |

The preview was checked after publishing: every page, internal link and gallery photo loads (except
the known broken "LET'S DO THIS!" link), and both background videos play.

**Where things live**

- Code: https://github.com/mikedasilva/countykidsofsteel.ca (public). Pages builds from `main` root.
- DNS: the Cloudflare account (zone `countykidsofsteel.ca`). `countykidsofsteel.ca` and `www`
  still point at Squarespace, so the public site is still the Squarespace one.
- Domain registration: Squarespace Domains (Tucows), renews 2027-10-25.
- Photos: R2 bucket `countykidsofsteel-photos`. Uploads use the `r2` rclone remote set up on the
  Mac used for the migration, with an API token limited to that bucket.
- Email: Google Workspace (MX, DKIM and DMARC records in Cloudflare DNS).

**Decisions made**

- Main address is `countykidsofsteel.ca`; `www` redirects to it.
- Newsletter signup stays as an email button until a newsletter service is chosen.

## Phase 1: migrate as-is to GitHub Pages

**Done.** All 20 Squarespace pages rebuilt as plain HTML, keeping their URLs, text, links and layout.

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

**Do not disturb email**: change only the apex and `www` records. Leave the MX, DKIM
(`google._domainkey`), DMARC and `google-site-verification` records as they are.

Steps, in order (the site is briefly unreachable between steps 2 and 3, so do them together):

1. Optional but recommended: in GitHub **Settings → Pages → Verified domains**, verify
   `countykidsofsteel.ca` (adds one TXT record in Cloudflare). This stops anyone else's repo
   claiming the domain.
2. Add a `CNAME` file containing `countykidsofsteel.ca` to the repo root and push. From this moment
   the github.io preview redirects to the domain, so continue straight to step 3.
3. In Cloudflare DNS, replace the Squarespace records, all set to **DNS only** (grey cloud) so
   GitHub can issue the HTTPS certificate:
   - `@` A records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `@` AAAA records: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`,
     `2606:50c0:8003::153`
   - `www` CNAME: `mikedasilva.github.io`
   (These two records are proxied, orange cloud, today. That has to change.)
4. Wait for GitHub's DNS check and certificate (minutes to an hour), then tick **Enforce HTTPS**.
5. Check `https://countykidsofsteel.ca`, `https://www.countykidsofsteel.ca` (should redirect),
   a few old URLs such as `/photos` and `/s/...pdf`, and send a test email to the domain.
6. Resubmit `sitemap.xml` in Google Search Console.

Before cancelling Squarespace:

- [x] Galleries moved to R2 (Phase 2)
- [ ] Keep the domain registration (billed by Squarespace, separate from the website plan) renewing,
      or transfer it to another `.ca` registrar
- [ ] Export existing newsletter subscribers from Squarespace. Decided: signups stay as the email
      button until a newsletter service is chosen later.
- [x] Canonical host decided: the apex, `countykidsofsteel.ca`, with `www` redirecting to it.
      Pages already declare the apex.
- [ ] Phase 3 cutover done and checked (steps above)
- [ ] Download anything else wanted from Squarespace (form submissions, analytics, blog drafts)
- [ ] Then cancel the Squarespace **website** plan only, keeping the domain

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
