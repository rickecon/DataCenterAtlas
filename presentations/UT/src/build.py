import base64, csv, json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
OUT  = HERE.parent / 'ut_legislator_briefing.html'

geo = (HERE/'ut_counties.json').read_text()

rates = {}
with open(REPO/'data/UT/avg_proptax_rate_by_cnty_ut_2025.csv') as f:
    for row in csv.DictReader(f):
        rates[row['cnty_name']] = round(float(row['rate_cnty_avg']), 8)

# sanity: every geojson county has a rate
names = {f['properties']['name'] for f in json.loads(geo)['features']}
missing = names ^ set(rates)
assert not missing, f'name mismatch: {missing}'

logo = (HERE/'ai_logo.svg').read_text().strip()
logo = re.sub(r'\swidth="171"', ' width="171"', logo)
logo = logo.replace('style="display:inline-block"', 'aria-label="Abundance Institute" role="img"')
brand = f'<div class="brand" title="Abundance Institute">{logo}</div>'

fig3 = (REPO/'images/all/fig3_MWtoFMV.html').read_bytes()
fig3_src = 'data:text/html;base64,' + base64.b64encode(fig3).decode()

html = (HERE/'tpl_head.html').read_text() \
     + (HERE/'tpl_body.html').read_text() \
     + (HERE/'tpl_script.html').read_text()

n_brand = html.count('__BRAND__')
html = html.replace('__BRAND__', brand)
html = html.replace('__FIG3_SRC__', fig3_src)
html = html.replace('__GEO__', geo)
html = html.replace('__RATES__', json.dumps(rates, separators=(',',':')))

assert '__' not in html.replace('__', '', 0) or not re.search(r'__[A-Z0-9_]+__', html), 'unreplaced token'

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html)
print(f'brand blocks: {n_brand}  counties: {len(rates)}')
print(f'mean rate: {sum(rates.values())/len(rates)*100:.3f}%   min {min(rates.values())*100:.3f}%  max {max(rates.values())*100:.3f}%')
print(f'wrote {OUT}  ({OUT.stat().st_size/1e6:.2f} MB)')
