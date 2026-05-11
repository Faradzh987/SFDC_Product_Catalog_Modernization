filename = 'vendor-management-portal.html'
with open(filename, 'r') as f:
    html = f.read()

# ── 1. PRE-LEASE complexity tier ──────────────────────────────────────────────
html = html.replace(
    '<option value="vendor">Custom scope — vendor specifies</option>',
    '<option value="vendor">Custom scope — vendor specifies</option>\n            <option value="prelease">Pre-lease scope — site not yet operational</option>'
)

# ── 2. WALKTHROUGH checkbox on scope submission ───────────────────────────────
html = html.replace(
    '<div style="margin-top:10px"><button class="btn-p">Submit to Vendor Portal →</button></div>',
    '''<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:10px 12px;margin-bottom:12px">
  <div style="font-size:11px;font-weight:700;color:#16325c;margin-bottom:8px">📋 Additional Tracking</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:12px">
    <label style="display:flex;gap:8px;align-items:center;cursor:pointer">
      <input type="checkbox" id="walkthrough-chk" style="width:14px;height:14px">
      <span>Vendor walkthrough required for this bid</span>
    </label>
    <label style="display:flex;gap:8px;align-items:center;cursor:pointer">
      <input type="checkbox" style="width:14px;height:14px">
      <span>Non-customer / operations request</span>
    </label>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">
    <div class="sf-field" style="margin:0">
      <label>CAS / CSS Number</label>
      <input type="text" placeholder="e.g. CAS-2026-0041 or CSS-1182">
      <div class="hint">Link this scope to a CAS or CSS number</div>
    </div>
    <div class="sf-field" style="margin:0">
      <label>Request Type</label>
      <select>
        <option>Customer-related scope</option>
        <option>Operations / internal request</option>
        <option>Pre-lease / site prep</option>
        <option>PM-driven maintenance</option>
      </select>
    </div>
  </div>
</div>
<div style="margin-top:10px;display:flex;gap:8px">
  <button class="btn-p">Submit to Vendor Portal →</button>
  <button class="btn-s">Save Draft</button>
</div>'''
)

# ── 3. ACTIVE SCOPES — add Walkthrough and CAS columns ───────────────────────
html = html.replace(
    '<thead><tr><th>Scope / Opp</th><th>Market</th><th>Complexity</th><th>Bids Received</th><th>Status</th><th>SLA</th><th>Actions</th></tr></thead>',
    '<thead><tr><th>Scope / Opp</th><th>Market</th><th>Complexity</th><th>CAS/CSS</th><th>Walkthrough</th><th>Bids</th><th>Status</th><th>SLA</th><th>Actions</th></tr></thead>'
)
html = html.replace(
    '<td>CH1</td><td><span class="badge b-orange">Non-Std</span></td><td><strong>3 / 3</strong></td><td><span class="badge b-green">SE Reviewing</span></td><td><span class="badge b-green">✓ In SLA</span></td><td><button class="btn-sm btn-p">View Bids</button></td>',
    '<td>CH1</td><td><span class="badge b-orange">Non-Std</span></td><td style="font-size:11px;color:#706e6b">CAS-2026-0412</td><td><span class="badge b-green">✓ Done</span></td><td><strong>3 / 3</strong></td><td><span class="badge b-green">SE Reviewing</span></td><td><span class="badge b-green">✓ In SLA</span></td><td><button class="btn-sm btn-p">View Bids</button></td>'
)
html = html.replace(
    '<td>SV1</td><td><span class="badge b-green">Standard</span></td><td><strong>2 / 4</strong></td><td><span class="badge b-orange">Awaiting Bids</span></td><td><span class="badge b-orange">⏰ 6h remaining</span></td><td><button class="btn-sm btn-p">View</button></td>',
    '<td>SV1</td><td><span class="badge b-green">Standard</span></td><td style="font-size:11px;color:#706e6b">—</td><td><span class="badge b-gray">Not req.</span></td><td><strong>2 / 4</strong></td><td><span class="badge b-orange">Awaiting Bids</span></td><td><span class="badge b-orange">⏰ 6h remaining</span></td><td><button class="btn-sm btn-p">View</button></td>'
)
html = html.replace(
    '<td>DE1</td><td><span class="badge b-red">Custom</span></td><td><strong>1 / 2</strong></td><td><span class="badge b-orange">Awaiting Bids</span></td><td><span class="badge b-green">✓ 3 days left</span></td><td><button class="btn-sm btn-p">View</button></td>',
    '<td>DE1</td><td><span class="badge b-red">Custom</span></td><td style="font-size:11px;color:#706e6b">CSS-1182</td><td><span class="badge b-orange">⏰ Scheduled</span></td><td><strong>1 / 2</strong></td><td><span class="badge b-orange">Awaiting Bids</span></td><td><span class="badge b-green">✓ 3 days left</span></td><td><button class="btn-sm btn-p">View</button></td>'
)

# ── 4. KPI SCORECARD — add Grade of Work column ───────────────────────────────
html = html.replace(
    '<thead><tr><th>Vendor</th><th>Market(s)</th><th>On-Time Delivery</th><th>Bid Submit Time</th><th>Quote Response SLA</th><th>Drawing Submission</th><th>Delay Reasons</th><th>PM Quality Score</th><th>Overall</th></tr></thead>',
    '<thead><tr><th>Vendor</th><th>Market(s)</th><th>On-Time Delivery</th><th>Bid Submit Time</th><th>Quote Response SLA</th><th>Drawing Submission</th><th>Grade of Work</th><th>Delay Reasons</th><th>PM Quality Score</th><th>Overall</th></tr></thead>'
)

# Add grade of work cells to each vendor row
for vendor, grade, color in [
    ('NTI</strong></td><td>CH1, SV1</td>', 'A', '#15803d'),
    ('Bay Area Structured</strong></td><td>SV1, LA1</td>', 'A+', '#15803d'),
    ('Midwest Cage &amp; Cable</strong></td><td>CH1, DE1</td>', 'B', '#1d4ed8'),
    ('RC Power Solutions</strong> <span class="badge b-red"', 'D', '#dc2626'),
]:
    old_drawing = f'<span class="badge b-green">On time</span></td>\n          <td><span style="font-size:11px;color:#706e6b">'
    if vendor in html:
        # find the drawing submission cell for this vendor and add grade after
        pass

# Simpler approach — add grade col inline
html = html.replace(
    '<td><span class="badge b-green">On time</span></td>\n          <td><span style="font-size:11px;color:#706e6b">Weather delay (1) · Material lead time (1)</span></td>',
    '<td><span class="badge b-green">On time</span></td>\n          <td><div style="width:34px;height:34px;border-radius:50%;background:#dcfce7;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;color:#15803d">A</div></td>\n          <td><span style="font-size:11px;color:#706e6b">Weather delay (1) · Material lead time (1)</span></td>'
)
html = html.replace(
    '<td><span class="badge b-green">On time</span></td>\n          <td><span style="font-size:11px;color:#706e6b">Scope change (1) · Access delay (1)</span></td>',
    '<td><span class="badge b-green">On time</span></td>\n          <td><div style="width:34px;height:34px;border-radius:50%;background:#dcfce7;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;color:#15803d">A+</div></td>\n          <td><span style="font-size:11px;color:#706e6b">Scope change (1) · Access delay (1)</span></td>'
)
html = html.replace(
    '<td><span class="badge b-orange">1 late submission</span></td>\n          <td><span style="font-size:11px;color:#706e6b">Material lead time (1)</span></td>',
    '<td><span class="badge b-orange">1 late submission</span></td>\n          <td><div style="width:34px;height:34px;border-radius:50%;background:#dbeafe;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;color:#1d4ed8">B</div></td>\n          <td><span style="font-size:11px;color:#706e6b">Material lead time (1)</span></td>'
)
html = html.replace(
    '<td><span class="badge b-red">Multiple late</span></td>\n          <td><span style="font-size:11px;color:#c23934">Staffing shortage (2) · No reason given (1)</span></td>',
    '<td><span class="badge b-red">Multiple late</span></td>\n          <td><div style="width:34px;height:34px;border-radius:50%;background:#fee2e2;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;color:#dc2626">D</div></td>\n          <td><span style="font-size:11px;color:#c23934">Staffing shortage (2) · No reason given (1)</span></td>'
)

# ── 5. STANDARD PRICING — add Lead Time + Install Time columns ────────────────
html = html.replace(
    '<thead><tr><th>Item</th><th>Unit</th><th>Your Price</th><th>Lead Time (BD)</th><th>Last Updated</th><th>Status</th></tr></thead>',
    '<thead><tr><th>Item</th><th>Unit</th><th>Your Price</th><th>Lead Time (BD)</th><th>Install Time (hrs)</th><th>Last Updated</th><th>Status</th></tr></thead>'
)

# Add install time inputs to each pricing row
for lt_val, install_val in [('5','4'),('6','6'),('3','2'),('3','2'),('4','8'),('4','6')]:
    html = html.replace(
        f'<input type="number" value="{lt_val}" style="width:60px;padding:4px 6px;border:1px solid #dddbda;border-radius:3px;font-size:12px;font-family:inherit"> <span style="font-size:11px;color:#706e6b">BD</span></td><td style="font-size:11px;color:#706e6b">Apr 1, 2026</td>',
        f'<input type="number" value="{lt_val}" style="width:60px;padding:4px 6px;border:1px solid #dddbda;border-radius:3px;font-size:12px;font-family:inherit"> <span style="font-size:11px;color:#706e6b">BD</span></td><td><input type="number" value="{install_val}" style="width:60px;padding:4px 6px;border:1px solid #dddbda;border-radius:3px;font-size:12px;font-family:inherit"> <span style="font-size:11px;color:#706e6b">hrs</span></td><td style="font-size:11px;color:#706e6b">Apr 1, 2026</td>',
        1
    )

# Jan dates for bottom rows
for lt_val, install_val in [('4','8'),('4','6')]:
    html = html.replace(
        f'<input type="number" value="{lt_val}" style="width:60px;padding:4px 6px;border:1px solid #dddbda;border-radius:3px;font-size:12px;font-family:inherit"> <span style="font-size:11px;color:#706e6b">BD</span></td><td style="font-size:11px;color:#e65100">Jan 15, 2026</td>',
        f'<input type="number" value="{lt_val}" style="width:60px;padding:4px 6px;border:1px solid #dddbda;border-radius:3px;font-size:12px;font-family:inherit"> <span style="font-size:11px;color:#706e6b">BD</span></td><td><input type="number" value="{install_val}" style="width:60px;padding:4px 6px;border:1px solid #dddbda;border-radius:3px;font-size:12px;font-family:inherit"> <span style="font-size:11px;color:#706e6b">hrs</span></td><td style="font-size:11px;color:#e65100">Jan 15, 2026</td>',
        1
    )

# ── 6. DELAY REASON CODES — add PM confirm/override note ─────────────────────
html = html.replace(
    '<div style="font-size:10px;color:#706e6b;margin-bottom:8px">Codes available to vendors and PMs when logging a delay. Richard to provide complete list.</div>',
    '<div style="font-size:10px;color:#706e6b;margin-bottom:8px">Codes available to both vendors and PMs. PMs can confirm or override vendor-entered reasons. Richard to provide complete list.</div><div style="font-size:10px;background:#eff6ff;border-left:3px solid #0070d2;padding:5px 8px;border-radius:3px;color:#1e40af;margin-bottom:8px">ℹ Vendor enters reason → PM receives notification → PM can confirm or override → Final reason logged on scorecard</div>'
)

# ── 7. AWARD REPORTING — add non-customer ops tab note ────────────────────────
html = html.replace(
    '<div class="callout callout-blue">Award reporting replaces manual vendor selection oversight. Procurement reviews during monthly market calls to ensure no single vendor is being over-awarded. Round-robin tracking per market.</div>',
    '<div class="callout callout-blue">Award reporting replaces manual vendor selection oversight. Procurement reviews during monthly market calls to ensure no single vendor is being over-awarded. Round-robin tracking per market. Includes both customer-related and operations/internal requests.</div>'
)

# ── 8. ONBOARDING — add JDE note and work types placeholder ──────────────────
html = html.replace(
    '<div style="font-size:10px;color:#706e6b;margin-bottom:10px">Required from all new vendors before onboarding approval — per Chris / Richard feedback</div>',
    '<div style="font-size:10px;color:#706e6b;margin-bottom:8px">Required from all new vendors before onboarding approval — per Chris / Richard feedback</div><div style="font-size:10px;background:#fff7ed;border-left:3px solid #e65100;padding:5px 8px;border-radius:3px;color:#9a3412;margin-bottom:8px">📎 Background checks and reference documents stored in JDE — not uploaded to this portal directly</div>'
)

# ── 9. WORK TYPES PLACEHOLDER NOTE ───────────────────────────────────────────
html = html.replace(
    'Checkboxes: branch circuits, control circuits, caging, ladder rack, mesh basket, fiber tray, seismic, grounding, overhead conveyance',
    'Checkboxes: branch circuits, control circuits, caging, ladder rack, mesh basket, fiber tray, seismic, grounding, overhead conveyance · ⚠ Full category/subcategory list pending from Richard'
)

# ── 10. ADD OPS REQUEST TAB ───────────────────────────────────────────────────
html = html.replace(
    '<div class="mtab" id="mt-scope" onclick="switchTab(\'scope\')">📐 Scope Submissions</div>',
    '<div class="mtab" id="mt-scope" onclick="switchTab(\'scope\')">📐 Scope Submissions</div>\n  <div class="mtab" id="mt-ops" onclick="switchTab(\'ops\')">🔧 Ops Requests</div>'
)

# Add ops tab pane before closing content div
ops_pane = '''
<div class="tab-pane" id="pane-ops">
  <div class="callout callout-blue">Operations and PMs can submit non-customer vendor requests here — site maintenance, internal builds, pre-lease work. These are tracked separately from customer opportunities but use the same vendor performance system.</div>
  <div class="grid-2">
    <div class="card">
      <div class="card-header"><span class="card-title">🔧 New Ops / Internal Request</span></div>
      <div class="card-body">
        <div class="sec-title">Request Details</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
          <div class="sf-field"><label>Request Type <span class="required">*</span></label>
            <select>
              <option>Operations / site maintenance</option>
              <option>Pre-lease scope</option>
              <option>PM-driven maintenance</option>
              <option>Internal build-out</option>
              <option>Other internal</option>
            </select>
          </div>
          <div class="sf-field"><label>Market <span class="required">*</span></label>
            <select><option>Chicago (CH1)</option><option>Los Angeles (LA1)</option><option>Santa Clara (SV1)</option><option>Denver (DE1)</option></select>
          </div>
          <div class="sf-field"><label>CAS / CSS Number</label>
            <input type="text" placeholder="e.g. CAS-2026-0041">
            <div class="hint">Required if tied to a CAS or CSS number</div>
          </div>
          <div class="sf-field"><label>Requested By <span class="required">*</span></label>
            <input type="text" placeholder="e.g. John Smith — Operations">
          </div>
          <div class="sf-field"><label>Needed By Date</label>
            <input type="date" value="2026-06-15">
          </div>
          <div class="sf-field"><label>Complexity</label>
            <select>
              <option>Standard</option>
              <option>Non-Standard</option>
              <option>Custom Scope</option>
              <option>Pre-Lease</option>
            </select>
          </div>
        </div>
        <div class="sec-title" style="margin-top:4px">Work Types</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:12px;font-size:12px">
          <label style="display:flex;align-items:center;gap:6px;cursor:pointer"><input type="checkbox" style="width:14px;height:14px"> Branch Circuits / Electrical</label>
          <label style="display:flex;align-items:center;gap:6px;cursor:pointer"><input type="checkbox" checked style="width:14px;height:14px"> Caging / Cage Panels</label>
          <label style="display:flex;align-items:center;gap=6px;cursor:pointer"><input type="checkbox" style="width:14px;height:14px"> Ladder Rack</label>
          <label style="display:flex;align-items:center;gap:6px;cursor:pointer"><input type="checkbox" style="width:14px;height:14px"> Mesh Basket</label>
          <label style="display:flex;align-items:center;gap:6px;cursor:pointer"><input type="checkbox" style="width:14px;height:14px"> Overhead Conveyance</label>
          <label style="display:flex;align-items:center;gap:6px;cursor:pointer"><input type="checkbox" style="width:14px;height:14px"> Seismic / Grounding</label>
        </div>
        <div class="sf-field"><label>Description</label>
          <textarea placeholder="Describe the scope of work, location, and any special requirements..."></textarea>
        </div>
        <div class="sf-field"><label>Walkthrough Required?</label>
          <select><option>No</option><option>Yes — schedule before bid</option></select>
        </div>
        <div class="sf-field"><label>Upload Scope / Drawings (optional)</label>
          <div style="border:2px dashed #dddbda;border-radius:4px;padding:12px;text-align:center;cursor:pointer;background:#f9f9f9">
            <div style="font-size:12px;color:#706e6b">📎 Attach scope or drawings</div>
            <div style="font-size:10px;color:#9ca3af;margin-top:2px">PDF, DWG, DXF</div>
          </div>
        </div>
        <button class="btn-p" style="margin-top:4px">Submit Ops Request →</button>
      </div>
    </div>
    <div class="card">
      <div class="card-header"><span class="card-title">📋 Active Ops Requests</span></div>
      <table>
        <thead><tr><th>Request</th><th>Type</th><th>Market</th><th>CAS/CSS</th><th>Walkthrough</th><th>Status</th><th>Actions</th></tr></thead>
        <tbody>
          <tr>
            <td><strong>CH1 — Floor sealing prep</strong><div style="font-size:10px;color:#706e6b">Ops req · John Smith</div></td>
            <td><span class="badge b-gray">Ops</span></td>
            <td>CH1</td>
            <td style="font-size:11px;color:#706e6b">CAS-2026-0039</td>
            <td><span class="badge b-green">✓ Done</span></td>
            <td><span class="badge b-blue">In Progress</span></td>
            <td><button class="btn-sm btn-p">View</button></td>
          </tr>
          <tr>
            <td><strong>DE1 — Pre-lease cage framing</strong><div style="font-size:10px;color:#706e6b">Pre-lease · Ron R.</div></td>
            <td><span class="badge b-purple">Pre-Lease</span></td>
            <td>DE1</td>
            <td style="font-size:11px;color:#706e6b">CSS-1177</td>
            <td><span class="badge b-orange">⏰ Scheduled</span></td>
            <td><span class="badge b-orange">Awaiting Bids</span></td>
            <td><button class="btn-sm btn-p">View</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
'''

html = html.replace('</div>\n\n<!-- ─── VENDOR DETAIL DRAWER', ops_pane + '\n</div>\n\n<!-- ─── VENDOR DETAIL DRAWER')

# ── 11. UPDATE switchTab to include ops ──────────────────────────────────────
html = html.replace(
    "function switchTab(tab){\n  ['directory','kpi','awards','onboard','scope'].forEach(function(t){",
    "function switchTab(tab){\n  ['directory','kpi','awards','onboard','scope','ops'].forEach(function(t){"
)

with open(filename, 'w') as f:
    f.write(html)
print('All 11 updates applied successfully')
