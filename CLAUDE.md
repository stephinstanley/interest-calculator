# Interest Calculator PWA

Plain HTML/CSS/JS installable web app (no build step) for working out simple interest owed on a personal loan. Used on phones via "Add to Home Screen" instead of an app store.

## Files
- `index.html` — the whole app (markup, styles, script).
- `manifest.json` — install metadata and icons.
- `sw.js` — offline support. Network-first, so fixes reach installed phones on the next online launch. Bump `CACHE` when the `FILES` list changes.
- `icons/icon.svg` — icon source. PNGs made with `qlmanage -t -s 512` and `sips -z` (no ImageMagick on this Mac).

## Calculation
Simple interest = Principal × Rate/100 × Period. Annual rate: days/365. Monthly rate: days/30.

## Run locally
`python3 -m http.server 8765`, then open http://localhost:8765 (service workers work on localhost). Test with agent-browser.

## Installing on a phone
Needs HTTPS hosting (not chosen yet). Android Chrome: menu → Install app. iPhone Safari: Share → Add to Home Screen.
