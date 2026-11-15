# Interest Calculator PWA

Plain HTML/CSS/JS installable web app (no build step) for working out simple interest owed on a personal loan. Used on phones via "Add to Home Screen" instead of an app store.

## Files
- `index.html` — the whole app (markup, styles, script).
- `manifest.json` — install metadata and icons.
- `sw.js` — offline support. Network-first, so fixes reach installed phones on the next online launch. Bump `CACHE` when the `FILES` list changes.
- `icons/icon.svg` — icon source. PNGs made with `qlmanage -t -s 512` and `sips -z` (no ImageMagick on this Mac).

## Screen design (redesigned Sun, 15-Nov-2026)
Goal: everything fits on one phone screen with no scrolling (checked at 390×760). Stephin asked for less scrolling and no person's name.
- **Answer panel on top** (dark green): big total, a one-line summary (principal + interest, period, any discount/round-off). The full bill is behind a "Details" toggle. Errors show here too.
- **Input rows** with short left labels: Amount (₹), Interest (rate % + Month | Year | Once switch), From, To (+ "Today" link).
- **Discount** and **Round-off** are "+" buttons that open small panels; × closes and resets them.
- No name field, subtitle, hint text or footer. The calculation note lives inside Details.
- `[hidden]` is forced to `display:none !important`, because component `display` rules would otherwise override it.

## Calculation
Simple interest = Principal × Rate/100 × Period. Defaults: 1.5, Month (the family's usual rate: ₹1.5 per ₹100 per month). Month = days/30, Year = days/365, Once = rate charged one time (Period = 1, dates don't change it).
Discount panel: ₹ | % | Final amount (what they actually pay; the difference becomes the discount). A box under the input keeps "Total now", "After discount" and the difference (₹ and %) visible while typing.
Round-off panel: ₹1 | ₹10 | ₹100 (default ₹10), done last. Skipped when Final amount is used.
Details shows: principal, interest, interest per month (hidden for Once), period as months + days (total days), before discount / discount (%), before round-off / round-off.
Money shows no paise when whole (₹57,530), otherwise 2 decimals. Calculation is live; there is no Calculate button.
Period months are calendar months (display only); per-month interest still uses days/30. Still waiting on the father: does he count by calendar months?

## Languages
English, Tamil, Malayalam (EN | த | മ at the top right; choice saved in localStorage). All text lives in the `I18N` object in `index.html`, and elements use `data-t`. Month names come from `Intl.DateTimeFormat` (en-IN / ta-IN / ml-IN). Translations were written by Claude, so have a native speaker check them. Keep words short: the Malayalam "Once" is ഒരിക്കൽ because ഒറ്റത്തവണ overflowed.

## Dates
Day / Month / Year dropdowns, not native `type=date` (Stephin found the native picker hard, especially picking the year). Month shows number and name (`12 · Dec`) because their records are written like 29/12/2025. An impossible date (31 Feb) turns the day box red and shows an error. Years 1990 to next year.

## Run locally
`python3 -m http.server 8765`, then open http://localhost:8765 (service workers work on localhost). Test with agent-browser.

## Hosting
Live at https://stephinstanley.github.io/interest-calculator/ (GitHub Pages, `main` branch, root). Repo: github.com/stephinstanley/interest-calculator (public, Stephin's **personal** GitHub account, not the Heartinz org).
- Pushing: this Mac's active gh account is normally the work one (`Stephin-Stanley`), which can't push here. Run `gh auth switch -u stephinstanley`, then `git push`, then `gh auth switch -u Stephin-Stanley` to switch back.
- Commits in this repo use the personal noreply email (set in local git config), so the work email isn't published.
- Pages rebuilds about a minute after a push. Installed phones pick up the new version on their next online launch.

## Installing on a phone
Android Chrome: open the link → menu (⋮) → Install app / Add to Home screen. iPhone Safari: Share → Add to Home Screen.
