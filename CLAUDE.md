# מירב מאור, האתר

Static Hebrew (RTL) website for Meirav Maor: spiritual guide, shamanic healer, couples coach. No server, no dependencies.
Published with GitHub Pages from the `main` branch (https://aviramo.github.io/meiravlove/), so a push to `main` goes live within a minute or two.

**Standing instruction from the owner (applies to every session): after every change, push it to `main` (not only to a work branch) so she always sees the changes live on the site. Don't wait to be asked.**

**Talk to the user in Hebrew.** The owner of the site is not a developer: explain what you changed in plain language, never ask her to run commands, and do the work yourself (edit, build, check, commit, push).

## How the site is built

- `build.py` generates every `.html` page from shared pieces (header + nav, footer, hero, image slots, one template for the four "space" pages). **Never edit the `.html` files by hand.** Edit `build.py`, then run `python3 build.py`, then commit the regenerated pages together with it.
- `style.css` and `site.js` are edited directly. `build.py` adds a cache-buster derived from their content, so re-run it after changing either.
- `images/` holds the real photos and the home video. Every image slot on a page expects a specific file name (e.g. `images/gate-kol.jpg`); a dashed placeholder shows only while the file is missing. To replace a photo, save the new file under the same name; to add a new slot, add it in `build.py` with `slot(...)`. The home hero video is `images/hero-video.mp4` (desktop/landscape) with `hero-video-mobile.mp4` for phones, plus `hero-poster*.jpg`; it autoplays muted and loops. Keep photos light (web-sized JPG) and the videos short.
- To check your work, screenshot with the preinstalled Chromium (Playwright) at 1280px and 390px wide, and look at the result.

## Design rules (decided with the owner, keep them)

- Look: soft and feminine (blush, rose, plum, gold), arches/rings/waves. Image frames use varied organic shapes (egg, petal, blob, capsule, circle); never the same silhouette twice in a row and no flat bottoms.
- **Exactly four text sizes** site-wide: `--t1` (main title), `--t2` (section titles), `--t3` (sub-titles, lead), `--t4` (everything else). Do not add other `font-size` values.
- Buttons are always horizontally centered in their block, on every page.
- On inner pages the `h1` starts at the same height on every page, with clear space below the floating header. The small "kicker" line hangs above the `h1`.
- The header is a floating glass capsule that shrinks smoothly on scroll. The site name and tagline use the handwritten Gveret Levin font with a drawn line-heart (no logo ring); on phones the name is centered with the burger button on the right. On phones the menu is a full-screen sheet that blooms from the burger button, and all spaces are listed in it. Page changes play a circle-bloom transition (curtain), handled in `site.js`.
- The tagline "אהבה זה כל הסיפור" appears once per page, in the header. Don't repeat it in the page body or footer.
- No browser-blue tap/focus box: press feedback is a small scale-down; keep the keyboard focus ring (`:focus-visible`).
- One footer, identical on every page. Contact links live there only, not duplicated on the contact page.
- Respect `prefers-reduced-motion`.

## Content rules (from the site brief)

- Warm, human, spiritual but accessible Hebrew. Address women and men. Use words like חיבור, הקשבה, לב, גוף, אהבה, היזכרות. Few emojis.
- Never promise medical healing or certain results. Show credentials and testimonials only if the owner approved them, and participants' photos only with their consent.
- Don't invent dates, prices, event details, testimonials or addresses. Placeholders are marked in yellow (`.draft`) or as sample cards.
- The contact details published on the site are the phone number and the WhatsApp, Instagram and Facebook links in the footer. **The owner's email is deliberately not on the site.** Don't publish new personal details without being asked.
- Names: the four spaces are קול הנשמה, דרך האהבה, בחזרה לאהבה, ואהבת לך; the physical space is המשכן (Raanana). Final naming and WhatsApp group structure are still open, so don't fix them on the site.

## Known open items

- The contact form does not send anything yet (needs a form service connected).
- Final text for the personal story and the privacy policy.
- Real events with dates (the event cards are still samples).
