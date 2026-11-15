# Interest Calculator PWA

Plain HTML/CSS/JS installable web app (no build step) for working out simple interest owed on a personal loan. Used on phones via "Add to Home Screen" instead of an app store.

## Files
- `index.html` — the whole app (markup, styles, script).
- `manifest.json` — install metadata and icons.
- `sw.js` — offline support. Network-first, so fixes reach installed phones on the next online launch. Bump `CACHE` when the `FILES` list changes.
- `icons/icon.svg` — icon source. PNGs made with `qlmanage -t -s 512` and `sips -z` (no ImageMagick on this Mac).

## Calculation
Simple interest = Principal × Rate/100 × Period. Defaults: rate 1.5, Per month (the family's usual rate: ₹1.5 per ₹100 per month). Rate periods: Full term (Period = 1, dates don't change it), Per month (days/30), Per year (days/365).
Optional discount, as ₹ amount, %, or **Final amount** (what they actually pay; the difference from the total becomes the discount), taken off the total (principal + interest). The bill always shows the discount as both % and ₹.
Calculation is live (on every input/change); there is no Calculate button.

## Dates
Day / Month / Year dropdowns, not native `type=date` (Stephin found the native picker hard, especially picking the year). Month shows number and name (`12 · Dec`) because their records are written like 29/12/2025. The chosen date shows below as `Mon, 29-Dec-2025`; impossible dates (31 Feb) are flagged. Years 1990 to this year + 5.

## Run locally
`python3 -m http.server 8765`, then open http://localhost:8765 (service workers work on localhost). Test with agent-browser.

## Installing on a phone
Needs HTTPS hosting (not chosen yet). Android Chrome: menu → Install app. iPhone Safari: Share → Add to Home Screen.
