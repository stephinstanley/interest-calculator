# Interest Calculator PWA

Plain HTML/CSS/JS installable web app (no build step) for working out simple interest owed on a personal loan. Used on phones via "Add to Home Screen" instead of an app store.

## Files
- `index.html` — the whole app (markup, styles, script).
- `manifest.json` — install metadata and icons.
- `sw.js` — offline support. Network-first, so fixes reach installed phones on the next online launch. Bump `CACHE` when the `FILES` list changes.
- `icons/icon.svg` — icon source. PNGs made with `qlmanage -t -s 512` and `sips -z` (no ImageMagick on this Mac).

## Screen design (redesigned Sun, 15-Nov-2026)
Mobile first: mobile is the main platform. Everything fits on one phone screen with no scrolling (checked at 360×640, 390×760 and 412 wide, in all three languages). Stephin asked for less scrolling and no person's name.
Context: this is for a **gold finance** business. The interest rate and type (monthly/yearly) are fixed business settings, so they're never asked for on the main screen.
- **Answer panel on top** (ink card): big total, a one-line summary (principal + interest, period, any discount/round-off). Errors show here too. The full bill is behind a **"Show details ⌄ / Hide details ⌃" bar at the bottom of the card** (full width, centred). It must not sit top-left, where it looked like a heading.
- **Rate chip** in the answer panel ("1.5% / month ✎") opens the **Interest setup** bottom sheet (`<dialog>`): rate + Per month | Per year, Save/Cancel. It's saved in localStorage (`interestCfg`), defaults to 1.5% per month, and Clear all doesn't reset it.
- **Input rows** with short left labels: Amount (₹), From, To (+ "Today" link). Nothing else.
- **+ Discount** opens a small panel (× closes and resets it). **Round off to ₹1** is a toggle chip.
- No name field, subtitle, hint text or footer. The calculation note lives inside Details.
- `[hidden]` is forced to `display:none !important`, because component `display` rules would otherwise override it.

## Visual identity: "Ink & Gold" (Sun, 15-Nov-2026; replaced the dark-green theme)
Tokens are on `:root` in `index.html`; use them, don't hard-code colours.
- **Ink** `#1A1814` is for structure, text, the answer card, primary buttons and selected states (an ink pill with gold text).
- **Gold** is only for money and focus. `--gold-hi` `#F2D27E` is the total and interest on ink; `--gold-deep` `#85600F` is links, chips and ₹/% signs on light; `--gold` `#C9972B` is the focus ring and hairlines.
- **Green** `--good` is money saved (discount). **Red** `--bad` is errors. The background is warm ivory `#F7F4EC` with white cards.
- Text contrast passes WCAG AA (4.5:1) everywhere. The icon is a gold ₹ coin on ink (`icons/icon.svg`).


## Calculation
Simple interest, using the saved setup (rate, per month/year, **method**). Default: 1.5% per month, **Exact days**.
Methods (chosen once in Interest setup, saved as `cfg.method`):
- `daily` **Exact days (like banks, e.g. Federal Bank)**: P × yearly rate × days ÷ 365. A monthly rate is ×12 (1.5%/month = 18%/year). This is the default; the father confirmed banks count each day, not 30-day months.
- `m30` **30-day months**: total days ÷ 30 × monthly interest. 12 × 30 = 360, so a real 365-day year counts as 12.17 months, about 1.4% more than daily.
Example, ₹50,000 at 1.5%/month from 29-Dec-2025 to 15-Nov-2026 (321 days): daily ₹7,915.07 · m30 ₹8,025.
A third method, "Months + days" (calendar months + extra days ÷ 30), was added and then removed on Sun, 15-Nov-2026 because it confused Stephin. Saved settings with `mdays` fall back to `daily`.
Details shows interest per month and per day, plus a "How it was worked out" line ("336 days × ₹66.0822 = ₹22,203.62" or "336 ÷ 30 = 11.2 months × ₹2,010 = ₹22,512"). Per-day is shown with up to 4 decimals (`moneyFine`) so it can be checked on a calculator. Interest is **not** rounded per day, like banks. Stephin chose this on Sun, 15-Nov-2026 after 336 × the rounded ₹66.08 came ₹0.74 short. Older saved settings without a valid method get `daily`.
("Once"/full term was removed: gold loans are monthly or yearly.)
Discount panel: ₹ | % | Final amount (what they actually pay; the difference becomes the discount). A box under the input keeps "Total now", "After discount" and the difference (₹ and %) visible while typing.
Round-off is **one on/off button** ("Round off to ₹1", a checkbox-style chip next to + Discount), always to the nearest rupee like banks (50 paise and up rounds up), done last. The ₹10/₹100 options were removed on Sun, 15-Nov-2026: for a small gold finance shop it's only "round or not". It's off by default, and Clear all turns it off. Skipped when Final amount is used.
Details shows: principal, interest, interest per month, period as months + days (total days), before discount / discount (%), before round-off / round-off.
Money shows no paise when whole (₹57,530), otherwise 2 decimals. Calculation is live; there is no Calculate button.
Period years/months are calendar-based. The interest method is a setting (see above).

## Amount in words
Shown as the first line of **Details** ("Total in words") and under the Amount box (to catch typos like 5,00,000 vs 50,000). It was under the big total at first, but that crowded the top (Stephin, Sun, 15-Nov-2026). It uses the Indian system: thousand, lakh, crore, plus paise.
- English is spelled out: "Twelve lakh thirty-four thousand five hundred sixty-seven rupees and fifty paise".
- Tamil and Malayalam use digits plus unit words: "12 ലക്ഷം 34 ആയിരം 567 രൂപ 50 പൈസ".

## Languages
English, Tamil, Malayalam (EN | த | മ at the top right; choice saved in localStorage). All text lives in the `I18N` object in `index.html`, and elements use `data-t`. Month names come from `Intl.DateTimeFormat` (en-IN / ta-IN / ml-IN). Translations were written by Claude, so have a native speaker check them. Keep words short; long labels overflow on narrow phones.

## Dates
Typed on the number pad, the way the pledge receipt shows it (`DD/MM/YYYY`). It replaced the native picker and then the day/month/year dropdowns; Stephin found both annoying.
- Slashes are added automatically (`29122025` → `29/12/2025`), and the caret is kept in place on edits/backspace.
- **No calendar picker.** A custom bottom-sheet calendar (day grid + month/year grid) was built on Sun, 15-Nov-2026 and removed the same day: Stephin found it "confusing" and said to leave pickers out if they're all like that. Don't re-add one without asking.
- A 2-digit year (`291225`) is accepted only when leaving the box, then expanded to `29/12/2025`, so typing "2025" doesn't flash 2020 at "20".
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
