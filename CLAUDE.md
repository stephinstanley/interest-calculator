# Interest Calculator PWA (app name: SSF)

The app is called **SSF** (S.S. Finance) since Mon, 16-Nov-2026: page title, home-screen name, header and all three languages.

Plain HTML/CSS/JS installable web app (no build step) for working out simple interest owed on a personal loan. Used on phones via "Add to Home Screen" instead of an app store.

## Files
- `index.html` — the whole app (markup, styles, script).
- `manifest.json` — install metadata and icons.
- `sw.js` — offline support. Network-first, so fixes reach installed phones on the next online launch. Bump `CACHE` when the `FILES` list changes.
- `icons/logo-source.png` — the app icon source (Mon, 16-Nov-2026): the maroon S.S. Finance "ff" monogram from the pledge receipt, redrawn by ChatGPT for Stephin. The `any` icons (512/192, and the 180 apple-touch) are it padded to a white 1760×1760 square (`sips --padToHeightWidth 1760 1760 --padColor FFFFFF`), then `sips -z`. The `maskable` icons (`icon-maskable-512/192.png`) use a 2420 square, because Android launchers zoom in on maskable icons; at 1500 the installed launcher icon looked too big (Mon, 16-Nov-2026). `icons/logo-mark.png` (58×96, cropped from the source) is the header mark next to "SSF"; its white background disappears on the ivory page through `mix-blend-mode:multiply`. `icons/icon.svg` (old gold ₹ coin) is no longer used. No ImageMagick on this Mac; `qlmanage` hangs, so don't use it.

## Screen design (redesigned Sun, 15-Nov-2026)
Mobile first: mobile is the main platform. Everything fits on one phone screen with no scrolling (checked at 360×640, 390×760 and 412 wide, in all three languages). Stephin asked for less scrolling and no person's name.
Context: this is for a **gold finance** business. The interest rate and type (monthly/yearly) are fixed business settings, so they're never asked for on the main screen.
- **Answer panel on top** (ink card): big total, a one-line summary (principal + interest, period, any discount/round-off). Errors show here too. A **"View details" bar with a bottom-sheet icon (not a chevron) at the bottom of the card** opens the **Details bottom sheet** (`#billSheet`). The sheet scrolls and is grouped like a receipt: the total and words, then **Loan** (principal, dates, period, rate), **Interest** (per day, per month, interest, bank-formula box), and **Settlement** (amount + interest, discount, after discount, round-off, Total to pay). It replaced an in-card expanding list that got too long (Sun, 15-Nov-2026).
- Sheets focus their title on open, never an input, so the phone keyboard doesn't pop up.
- **Rate chip** in the answer panel ("1.5% / month ✎") opens the **Interest setup** bottom sheet (`<dialog>`): rate + Per month | Per year, Save/Cancel. It's saved in localStorage (`interestCfg`), defaults to 1.5% per month, and Clear all doesn't reset it.
- **Input rows** with short left labels: Amount (₹), From, To (+ "Today" link). Nothing else.
- **+ Discount** opens a small panel (× closes and resets it). Round-off isn't on the main screen; it's a setting.
- No name field, subtitle, hint text or footer. The calculation note lives inside Details.
- `[hidden]` is forced to `display:none !important`, because component `display` rules would otherwise override it.

## Visual identity: "Ink & Gold" (Sun, 15-Nov-2026; replaced the dark-green theme)
Tokens are on `:root` in `index.html`; use them, don't hard-code colours.
- **Ink** `#1A1814` is for structure, text, the answer card, primary buttons and selected states (an ink pill with gold text).
- **Gold** is only for money and focus. `--gold-hi` `#F2D27E` is the total and interest on ink; `--gold-deep` `#85600F` is links, chips and ₹/% signs on light; `--gold` `#C9972B` is the focus ring and hairlines.
- **Green** `--good` is money saved (discount). **Red** `--bad` is errors. The background is warm ivory `#F7F4EC` with white cards.
- Text contrast passes WCAG AA (4.5:1) everywhere. The icon is the maroon ff monogram on white (`icons/logo-source.png`); maroon isn't a theme token.


## Calculation
Simple interest, always with **30-day months** (1 month = 30 days, 1 year = 360 days; the father's method, Sun, 15-Nov-2026). The Exact days radio is shown but `disabled`; `METHODS = ['m30']`, so any saved `daily` setting moves to `m30` on load.
**Interest type** (`cfg.mode`, chosen in Interest setup):
- `tiered` **By duration** (the default, including old saved settings with no `mode`). Monthly rates `r1`/`r2`/`r3`, default 1% / 1.5% / 2%. Day limits 90/180/365 are fixed; only the rates can be edited. Rules, confirmed by Stephin:
  - up to 90 days: all days at r1;
  - 91–180 days: first 90 days at r1, the rest at r2 (₹1,00,000 × 150 days = ₹3,000 + ₹3,000);
  - 181–365 days: **all** days at r2; the r1 concession is taken back (so day 180 → 181 jumps ₹7,500 → ₹9,050 per lakh);
  - over 365 days: **all** days at r3 (whole loan, not just the extra days).
  `tierSegments()` in the engine does this; each part is rounded to paise and interest is their sum, so the bill lines add up. The rate chip shows "1% → 2% / month"; the summary line shows days and the rate used; Details shows one formula line per part and a sentence saying which rule applied. When the period is split, Details shows one row per part instead of per-day and per-month: "First [90 days] @ 1% / month ₹3,000" and "Next [60 days] @ 1.5% / month ₹3,000", then the Interest total (Stephin, Mon, 16-Nov-2026). Day counts are highlighted as gold-tint pills (`.dpill`), also on the Period line ("4 months 28 days [150 days]").
- `fixed` **Fixed**: one rate (`cfg.rate`, per month or per year) for the whole loan, as before.
Days are end − start (the From day isn't counted twice). At the 180/181 limit one day is worth ₹1,550 per lakh, so check a real past loan against the app.
Methods (chosen once in Interest setup, saved as `cfg.method`):
- `daily` **Exact days (like banks, e.g. Federal Bank)**: P × yearly rate × days ÷ 365. A monthly rate is ×12 (1.5%/month = 18%/year). Switched off on Sun, 15-Nov-2026 (the radio is disabled); kept in the code.
- `m30` **30-day months**: total days ÷ 30 × monthly interest. 12 × 30 = 360, so a real 365-day year counts as 12.17 months, about 1.4% more than daily.
Example, ₹50,000 at 1.5%/month from 29-Dec-2025 to 15-Nov-2026 (321 days): daily ₹7,915.07 · m30 ₹8,025.
A third method, "Months + days" (calendar months + extra days ÷ 30), was added and then removed on Sun, 15-Nov-2026 because it confused Stephin. Saved settings with `mdays` fall back to the default method.
Details shows interest per month and per day, plus a "How it was worked out" box with labelled steps: the yearly rate (1.5% × 12 = 18%), the formula in words, the numbers, and why 36,500 = 100 × 365. Stephin asked what 18 and 36,500 meant. It uses the bank formula, exact on any calculator: "1,34,000 × 18 × 336 ÷ 36,500 = ₹22,203.62" (daily: P × yearly% × days ÷ 36,500), or "1,34,000 × 1.5 × 336 ÷ 3,000 = ₹22,512" (30-day: P × monthly% × days ÷ 3,000). Per-day is shown with up to 4 decimals (`moneyFine`) so it can be checked on a calculator. Interest is **not** rounded per day, like banks. Stephin chose this on Sun, 15-Nov-2026 after 336 × the rounded ₹66.08 came ₹0.74 short. Older saved settings without a valid method get `m30`; without `round` they get rounding on.
("Once"/full term was removed: gold loans are monthly or yearly.)
Discount panel: ₹ | % | Final amount (what they actually pay; the difference becomes the discount). A box under the input keeps "Total now", "After discount" and the difference (₹ and %) visible while typing.
Round-off is a **saved setting** in Interest setup (`cfg.round`, default **on**). It has its own "Round-off" heading and an on/off **switch** row, so it doesn't look like a third radio option next to the methods: "Round off to nearest ₹1", like banks (50 paise and up rounds up), done last. When it changes the total, the answer card shows a line under the big total: "Before round-off ₹1,56,335.78 · +₹0.22". It's skipped when the discount type is Final amount. History: it was a ₹1/₹10/₹100 panel, then an on/off chip, then (Sun, 15-Nov-2026) a setting, because the father always rounds.
Details shows: principal, interest, interest per month, period as months + days (total days), before discount / discount (%), before round-off / round-off.
Money shows no paise when whole (₹57,530), otherwise 2 decimals. Calculation is live; there is no Calculate button.
Period years/months are calendar-based. The interest method is a setting (see above).

## Money maths: whole paise, no floating point
Floats caused 1-paisa errors (464.985 → 464.98) and wrong ₹1 round-offs (e.g. "₹1,000.50" rounding down) in about 0.5% of cases. That was found with a 300,000-case test on Sun, 15-Nov-2026.
- All money goes through `computePaise()` between `// MONEY-ENGINE-START` and `// MONEY-ENGINE-END` in `index.html`.
- Inputs are read as text and scaled to BigInt (paise; rate × 1e6). Every rounding is half-up, done once, on exact values. No package is needed.
- Order: interest → subtotal → discount → round-off.
- `perDay` is display-only, so it stays a float.
- **Test after any money change:** `python3 -I tests/gen_cases.py /tmp/cases.json && node tests/check_engine.js index.html /tmp/cases.json`. It should print `mismatches: 0 / 80000` (60,000 fixed + 20,000 tiered cases, with the limit days 89/90/91/179/180/181/364/365/366 forced in). The cases come from exact Python `Fraction` maths.

## Amount in words
Shown at the top of the **Details** sheet, under the total and under the Amount box (to catch typos like 5,00,000 vs 50,000). It was under the big total at first, but that crowded the top (Stephin, Sun, 15-Nov-2026). It uses the Indian system: thousand, lakh, crore, plus paise.
- English is spelled out: "Twelve lakh thirty-four thousand five hundred sixty-seven rupees and fifty paise".
- Tamil and Malayalam use digits plus unit words: "12 ലക്ഷം 34 ആയിരം 567 രൂപ 50 പൈസ".

## Languages
English, Tamil, Malayalam (EN | த | മ at the top right; choice saved in localStorage). All text lives in the `I18N` object in `index.html`, and elements use `data-t`. Month names come from `Intl.DateTimeFormat` (en-IN / ta-IN / ml-IN). Translations were written by Claude, so have a native speaker check them. Keep words short; long labels overflow on narrow phones.

## Dates
Typed on the number pad, day first, the way the pledge receipt shows it (`DD/MM/YYYY`). It replaced the native picker and then the day/month/year dropdowns; Stephin found both annoying.
- **Forgiving typing** (Sun, 15-Nov-2026; the father types `1/1/26`, not `01/01/2026`). `tidyTyped()` turns any `.` `-` `,` or space into `/` and adds a slash by itself after a 2-digit day or month, so `1/1/26`, `1.1.26`, `1-1-26`, `1 1 26`, `010126` and `01012026` all work. Leaving the box tidies it to `01/01/2026`. The keypad is `inputmode="decimal"` so it has a `.` key (the iPhone number pad has no `/`).
- The date in words under the box is big and bold (`.okdate`): it's the check he reads. Errors say what's wrong: "Month must be 1 to 12", "Feb has only 28 days".
- **Calendar button** at the right of each date box (added Sun, 15-Nov-2026 at Stephin's request: "we need date picker also"). It's a see-through native `<input type="date">` over a calendar icon, so a tap opens the phone's own picker; it starts on the typed date (or today) and writes the picked date back into the box as DD/MM/YYYY. Typing still works. A custom bottom-sheet calendar was built and removed earlier the same day as "confusing"; don't bring back a custom one.
- A 2-digit year counts straight away (the iPhone decimal pad has no Done key), except `19` and `20`, which wait until leaving the box so typing "2025" doesn't flash 2020. 2-digit years become 20xx (19xx if that would be more than a year ahead).
- Under the box: the date in words (`Mon, 29-Dec-2025`), or red "This date does not exist" for 31/02.
- **To** defaults to a "Today · 15-Nov-2026 ✎" button; tapping it opens the same typed box (prefilled with today) plus a "Use today" link.
- Until From is complete, the answer panel says "Type the From date".
- The period shows years, months and days (`2 years 6 months 5 days`); Details also shows total days.

## Run locally
`python3 -m http.server 8765`, then open http://localhost:8765 (service workers work on localhost). Test with agent-browser.

## Hosting
Live at https://stephinstanley.github.io/interest-calculator/ (GitHub Pages, `main` branch, root). Repo: github.com/stephinstanley/interest-calculator (public, Stephin's **personal** GitHub account, not the Heartinz org).
- Pushing: this Mac's active gh account is normally the work one (`Stephin-Stanley`), which can't push here. Run `gh auth switch -u stephinstanley`, then `git push`, then `gh auth switch -u Stephin-Stanley` to switch back.
- Commits in this repo use the personal noreply email (set in local git config), so the work email isn't published.
- Pages rebuilds about a minute after a push. Installed phones pick up the new version on their next online launch.

## Installing on a phone
Android Chrome: open the link → menu (⋮) → Install app / Add to Home screen. iPhone Safari: Share → Add to Home Screen.
