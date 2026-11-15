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
A box right under the discount input shows "Total now", "After discount" and the difference (₹ and %), so the original total stays visible while typing.
Period shows calendar months + days, plus total days, e.g. "10 months 17 days (321 days)". This is display only; per-month interest still uses days/30.

## Languages
English, Tamil, Malayalam (buttons at the top; choice saved in localStorage). All text lives in the `I18N` object in `index.html`; elements use `data-t` (text) and `data-ph` (placeholder). Month and weekday names come from `Intl.DateTimeFormat` (en-IN / ta-IN / ml-IN). Translations were written by Claude: have a native speaker check them.

## Other features
- Interest per month line (per month: P × r%; per year: P × r% ÷ 12; hidden for Full term).
- Round-off (none / ₹1 / ₹10 / ₹100), done last, after discount. Skipped when the discount type is Final amount and a value is typed. The bill shows "Before round-off" and the ± round-off only when rounding changed the number.
- Clear button resets to defaults (1.5, Per month, today's dates).
- Larger text (18px base, 19px inputs, 56px-tall fields) for easier reading by an older user.

## Dates
Day / Month / Year dropdowns, not native `type=date` (Stephin found the native picker hard, especially picking the year). Month shows number and name (`12 · Dec`) because their records are written like 29/12/2025. The chosen date shows below as `Mon, 29-Dec-2025`; impossible dates (31 Feb) are flagged. Years 1990 to this year + 5.

## Run locally
`python3 -m http.server 8765`, then open http://localhost:8765 (service workers work on localhost). Test with agent-browser.

## Hosting
Live at https://stephinstanley.github.io/interest-calculator/ (GitHub Pages, `main` branch, root). Repo: github.com/stephinstanley/interest-calculator (public, Stephin's **personal** GitHub account, not the Heartinz org).
- Pushing: this Mac's active gh account is normally the work one (`Stephin-Stanley`), which can't push here. Run `gh auth switch -u stephinstanley`, then `git push`, then `gh auth switch -u Stephin-Stanley` to switch back.
- Commits in this repo use the personal noreply email (set in local git config), so the work email isn't published.
- Pages rebuilds about a minute after a push. Installed phones pick up the new version on their next online launch.

## Installing on a phone
Android Chrome: open the link → menu (⋮) → Install app / Add to Home screen. iPhone Safari: Share → Add to Home Screen.
