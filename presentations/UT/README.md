# Utah legislative briefing deck

`ut_legislator_briefing.html` — a self-contained, click-through interactive deck
(7 slides) built for a one-on-one presentation over video conference.

## Presenting

Open the file in Chrome and press **F** for fullscreen, then share that tab/window
in Google Meet.

| Key | Action |
| :-- | :-- |
| `→` / `Space` | Next slide |
| `←` | Previous slide |
| `1`–`7` | Jump to slide |
| `O` | Slide overview grid |
| `F` | Toggle fullscreen |

The current slide is written to the URL hash (`#s3`), so you can reload or deep-link
into any slide.

**Needs an internet connection for Slide 4 only** — it embeds the live
DataCenterAtlas. Everything else (both maps, Figure 3, the widget) is embedded in
the file and works offline. If the embed misbehaves live, the **Open in new tab**
button on that slide is the fallback.

## Slides

1. **Utah, Data Centers, and Energy** — four claims; click any card header to expand its
   supporting bullets. Several bullets link out to source articles.
2. **Average effective property tax rates by county, 2025** — choropleth in 5 blue bands;
   hover a county for its rate to 3 decimals, click a legend band to isolate it.
3. **Where Utah's data centers actually are** — 48 facilities across 7 markets, sized by
   count, joined to each host county's average effective rate.
4. **Utah revenue and jobs model** — the live DataCenterAtlas, embedded. Click Utah on its map.
5. **How we calculate a data center's value** — the live Figure 3 from the Econosseur post,
   with the real-property/personal-property point called out.
6. **Two Abundance Institute articles** — "Introducing DataCenterAtlas.org" (June 9, 2026) and
   "Which Localities Can Capture the Benefits of the Data Center Infrastructure Boom?"
   (Aug. 11, 2026), each with the article's own summary bullets.
7. **Two Kem C. Gardner Policy Institute studies** — the Aug. 19 tax policy explainer and the
   Aug. 10 property tax brief, with the residential-exemption caveat on the latter's Figure 1.

## Data sources

| Slide | Source |
| :-- | :-- |
| 2 | `data/UT/avg_proptax_rate_by_cnty_ut_2025.csv` (Utah State Tax Commission, 2025 Tax Area Rates) |
| 2, 3 | County boundaries: US Census cartographic boundary files, FIPS state 49 |
| 3 | Data Center Map, "Utah Data Centers," retrieved 20 Aug 2026 |
| 5 | `images/all/fig3_MWtoFMV.html`, embedded verbatim as a data URI |
| 6 | Econosseur (Richard W. Evans); bullets taken verbatim from each article's summary |
| 7 | Kem C. Gardner Policy Institute Public Finance Briefs, Aug. 2026 |

## Published copy

An unlisted copy is served from the RickEconSite Astro repo, which passes `public/`
through verbatim and auto-deploys to www.rickecon.com on every push to `main`:

```
RickEconSite/public/slides/ut-data-centers-energy/index.html
  -> https://www.rickecon.com/slides/ut-data-centers-energy/
```

It is not linked from anywhere on the site and carries a `noindex, nofollow` robots
meta tag, so it is reachable by URL only. After rebuilding, re-copy it:

```
cp presentations/UT/ut_legislator_briefing.html \
   ../../websites/RickEconSite/public/slides/ut-data-centers-energy/index.html
```

## Rebuilding

The deck is generated, not hand-edited. Edit the pieces in `src/`, then:

```
python3 presentations/UT/src/build.py
```

`build.py` reads the county rates straight from `data/UT/`, asserts that every county
in the boundary file has a matching rate, inlines the Abundance Institute logo, and
base64-embeds Figure 3. Re-run it whenever the underlying CSV changes.

- `src/tpl_head.html` — design tokens and CSS
- `src/tpl_body.html` — slide markup
- `src/tpl_script.html` — map rendering, interactions, navigation
- `src/ut_counties.json` — Utah county boundaries (29 features, ~17 KB)
