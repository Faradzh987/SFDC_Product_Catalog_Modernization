#!/usr/bin/env python3
"""
NEMA Reference Patcher
Injects the NEMA/Hubbell connector reference button + modal
into salesforce-branch-circuit-mockup.html

Usage:
  python patch_nema.py
  (run from the same folder as salesforce-branch-circuit-mockup.html)
"""

import os, sys, shutil, re
from datetime import datetime

TARGET = "salesforce-branch-circuit-mockup.html"

# ─── CSS to inject before </style> ───────────────────────────────────────────
CSS_PATCH = """
/* ── NEMA Reference Button & Modal ───────────────────────────── */
.nema-ref-btn{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;background:linear-gradient(135deg,#16325c,#0070d2);color:#fff;border:none;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer;font-family:'DM Sans',sans-serif;box-shadow:0 2px 8px rgba(0,112,210,0.3);transition:all 0.15s;letter-spacing:0.01em;}
.nema-ref-btn:hover{background:linear-gradient(135deg,#0058a8,#004a90);transform:translateY(-1px);box-shadow:0 4px 14px rgba(0,112,210,0.4);}
.nf-btn{padding:5px 12px;font-size:11px;font-weight:600;border-radius:5px;border:1px solid #e2e8f0;background:#fff;color:#706e6b;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all 0.15s;}
.nf-btn:hover{background:#eff6ff;color:#0070d2;border-color:#bfdbfe;}
.nf-active{background:#0070d2!important;color:#fff!important;border-color:#0070d2!important;}
.nema-row{cursor:pointer;transition:background 0.1s;}
.nema-row:hover td{background:#eff6ff!important;}
.nema-row.nema-selected td{background:#dcfce7!important;}
.nema-badge{display:inline-flex;align-items:center;font-size:10px;padding:2px 7px;border-radius:10px;font-weight:600;white-space:nowrap;}
.nb-straight{background:#dbeafe;color:#1d4ed8;}
.nb-twistlock{background:#f3e8ff;color:#7c3aed;}
.nb-pinsleeve{background:#fff3e0;color:#c2410c;}
.nb-iec{background:#ccfbf1;color:#0f766e;}
"""

# ─── Button HTML (replaces the sf-form-title that contains Branch Circuit) ───
BUTTON_SNIPPET = """<button class="nema-ref-btn" onclick="openNEMA()" style="margin-left:8px;">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/></svg>
              NEMA / Connector Reference
            </button>"""

# ─── Full modal + JS to inject before </body> ─────────────────────────────────
MODAL_AND_JS = """
<!-- ══════════════════════════════════════════════
     NEMA REFERENCE MODAL  (auto-patched)
══════════════════════════════════════════════ -->
<div id="nema-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:9999;overflow-y:auto;padding:20px 16px;">
  <div style="background:#fff;border-radius:14px;max-width:1000px;margin:0 auto;overflow:hidden;box-shadow:0 24px 80px rgba(0,0,0,0.45);">
    <div style="background:linear-gradient(135deg,#16325c 0%,#0070d2 60%,#0058a8 100%);padding:16px 22px;display:flex;align-items:center;justify-content:space-between;">
      <div>
        <div style="color:#fff;font-size:16px;font-weight:800;letter-spacing:-0.01em;">&#9889; NEMA / Hubbell Connector Reference</div>
        <div style="color:rgba(255,255,255,0.62);font-size:11px;margin-top:3px;">Straight Blade &middot; Twist-Lock &middot; IEC &middot; Pin &amp; Sleeve (IEC 60309) &mdash; click Select to auto-fill circuit fields</div>
      </div>
      <button onclick="closeNEMA()" style="background:rgba(255,255,255,0.15);border:1.5px solid rgba(255,255,255,0.3);border-radius:7px;color:#fff;padding:7px 16px;font-size:12px;font-weight:700;cursor:pointer;font-family:'DM Sans',sans-serif;">&#10005; Close</button>
    </div>
    <div style="background:#f8fafc;border-bottom:2px solid #e2e8f0;padding:10px 18px;display:flex;gap:6px;flex-wrap:wrap;align-items:center;">
      <button onclick="filterNEMA('all')"        id="nf-all"        class="nf-btn nf-active">All</button>
      <button onclick="filterNEMA('straight')"   id="nf-straight"   class="nf-btn">Straight Blade</button>
      <button onclick="filterNEMA('twistlock')"  id="nf-twistlock"  class="nf-btn">Twist-Lock</button>
      <button onclick="filterNEMA('pinsleeve')"  id="nf-pinsleeve"  class="nf-btn">Pin &amp; Sleeve</button>
      <button onclick="filterNEMA('iec')"        id="nf-iec"        class="nf-btn">IEC (C13/C19)</button>
      <div style="display:flex;align-items:center;gap:5px;margin-left:10px;">
        <span style="font-size:10px;font-weight:600;color:#706e6b">Legend:</span>
        <span style="background:#fefce8;border:1px solid #fde047;border-radius:3px;font-size:9px;color:#713f12;padding:1px 6px;font-weight:700;">&#9733; DC Standard</span>
      </div>
      <div style="margin-left:auto;display:flex;align-items:center;gap:6px;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#706e6b" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input id="nema-search" type="text" placeholder="Search voltage, amps, config, use case..."
          oninput="searchNEMA(this.value)"
          style="padding:6px 11px;border:1px solid #e2e8f0;border-radius:7px;font-size:12px;width:260px;font-family:'DM Sans',sans-serif;outline:none;transition:border-color 0.15s;"
          onfocus="this.style.borderColor='#0070d2'" onblur="this.style.borderColor='#e2e8f0'">
      </div>
    </div>
    <div style="overflow-x:auto;max-height:62vh;overflow-y:auto;">
      <table style="width:100%;border-collapse:collapse;font-size:12px;">
        <thead style="position:sticky;top:0;z-index:2;">
          <tr style="background:#f0f4f8;border-bottom:2px solid #e2e8f0;">
            <th style="padding:9px 12px;text-align:left;font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;white-space:nowrap;">Type</th>
            <th style="padding:9px 12px;text-align:left;font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;white-space:nowrap;">Configuration</th>
            <th style="padding:9px 12px;text-align:left;font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;">Voltage</th>
            <th style="padding:9px 12px;text-align:left;font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;">Amperage</th>
            <th style="padding:9px 12px;text-align:left;font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;">Poles / Wires</th>
            <th style="padding:9px 12px;text-align:left;font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;">Grounding</th>
            <th style="padding:9px 12px;text-align:left;font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;">Typical Use</th>
            <th style="padding:9px 12px;text-align:center;font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;white-space:nowrap;">Select</th>
          </tr>
        </thead>
        <tbody id="nema-tbody"></tbody>
      </table>
    </div>
    <div style="padding:10px 18px;background:#f8fafc;border-top:1px solid #e5e7eb;display:flex;align-items:center;justify-content:space-between;">
      <div style="font-size:10px;color:#706e6b;">Source: Hubbell Wiring Device-Kellems &middot; WLCNEMA17 &middot; IEC 60309 &middot; &#9733; = data center standard</div>
      <button onclick="closeNEMA()" style="padding:5px 14px;background:#f0f4f8;color:#706e6b;border:1px solid #e2e8f0;border-radius:5px;font-size:11px;font-weight:600;cursor:pointer;font-family:'DM Sans',sans-serif;">Close</button>
    </div>
  </div>
</div>

<script>
// ── NEMA DATA ──────────────────────────────────────────────────────────────
var NEMA_DATA=[
  // STRAIGHT BLADE
  {type:'straight',config:'NEMA 1-15',voltage:'125V',amps:'15A',poles:'2P / 2W',ground:'No',use:'Non-grounding general purpose',highlight:false},
  {type:'straight',config:'NEMA 5-15',voltage:'125V',amps:'15A',poles:'2P / 3W',ground:'Yes',use:'Standard 120V outlet — most common in US',highlight:true},
  {type:'straight',config:'NEMA 5-20',voltage:'125V',amps:'20A',poles:'2P / 3W',ground:'Yes',use:'20A 120V — IT lab, kitchen, office',highlight:true},
  {type:'straight',config:'NEMA 5-30',voltage:'125V',amps:'30A',poles:'2P / 3W',ground:'Yes',use:'30A 120V — high-draw appliances',highlight:false},
  {type:'straight',config:'NEMA 5-50',voltage:'125V',amps:'50A',poles:'2P / 3W',ground:'Yes',use:'50A 120V — large appliances',highlight:false},
  {type:'straight',config:'NEMA 6-15',voltage:'250V',amps:'15A',poles:'2P / 3W',ground:'Yes',use:'15A 240V — A/C units, power tools',highlight:false},
  {type:'straight',config:'NEMA 6-20',voltage:'250V',amps:'20A',poles:'2P / 3W',ground:'Yes',use:'20A 240V — tools, PDU tail feeds',highlight:true},
  {type:'straight',config:'NEMA 6-30',voltage:'250V',amps:'30A',poles:'2P / 3W',ground:'Yes',use:'30A 240V — welders, HVAC, PDUs',highlight:false},
  {type:'straight',config:'NEMA 6-50',voltage:'250V',amps:'50A',poles:'2P / 3W',ground:'Yes',use:'50A 240V — EV chargers, large equipment',highlight:false},
  {type:'straight',config:'NEMA 6-60',voltage:'250V',amps:'60A',poles:'2P / 3W',ground:'Yes',use:'60A 240V — industrial panel feeds',highlight:false},
  {type:'straight',config:'NEMA 10-30',voltage:'125/250V',amps:'30A',poles:'3P / 3W',ground:'No',use:'Legacy dryer outlet — no ground (old code)',highlight:false},
  {type:'straight',config:'NEMA 14-20',voltage:'125/250V',amps:'20A',poles:'3P / 4W',ground:'Yes',use:'Split-phase 20A — PDU branch circuits',highlight:false},
  {type:'straight',config:'NEMA 14-30',voltage:'125/250V',amps:'30A',poles:'3P / 4W',ground:'Yes',use:'Split-phase 30A — dryers, PDU feeds',highlight:false},
  {type:'straight',config:'NEMA 14-50',voltage:'125/250V',amps:'50A',poles:'3P / 4W',ground:'Yes',use:'Split-phase 50A — EV, RV hookups, PDUs',highlight:true},
  {type:'straight',config:'NEMA 15-20',voltage:'3\u00d8 125/250V',amps:'20A',poles:'3P / 4W',ground:'Yes',use:'3-phase 20A light industrial',highlight:false},
  {type:'straight',config:'NEMA 15-30',voltage:'3\u00d8 250V',amps:'30A',poles:'3P / 4W',ground:'Yes',use:'3-phase 30A — motors, HVAC',highlight:false},
  // TWIST-LOCK
  {type:'twistlock',config:'NEMA L5-15',voltage:'125V',amps:'15A',poles:'2P / 3W',ground:'Yes',use:'Locking 125V 15A — IT equipment',highlight:false},
  {type:'twistlock',config:'NEMA L5-20',voltage:'125V',amps:'20A',poles:'2P / 3W',ground:'Yes',use:'Locking 125V 20A — PDU branch circuits',highlight:true},
  {type:'twistlock',config:'NEMA L5-30',voltage:'125V',amps:'30A',poles:'2P / 3W',ground:'Yes',use:'Locking 125V 30A',highlight:false},
  {type:'twistlock',config:'NEMA L6-15',voltage:'250V',amps:'15A',poles:'2P / 3W',ground:'Yes',use:'Locking 250V 15A',highlight:false},
  {type:'twistlock',config:'NEMA L6-20',voltage:'250V',amps:'20A',poles:'2P / 3W',ground:'Yes',use:'Locking 250V 20A — data center PDU standard',highlight:true},
  {type:'twistlock',config:'NEMA L6-30',voltage:'250V',amps:'30A',poles:'2P / 3W',ground:'Yes',use:'Locking 250V 30A — UPS output, PDU input',highlight:true},
  {type:'twistlock',config:'NEMA L6-50',voltage:'250V',amps:'50A',poles:'2P / 3W',ground:'Yes',use:'Locking 250V 50A',highlight:false},
  {type:'twistlock',config:'NEMA L6-60',voltage:'250V',amps:'60A',poles:'2P / 3W',ground:'Yes',use:'Locking 250V 60A',highlight:false},
  {type:'twistlock',config:'NEMA L14-20',voltage:'125/250V',amps:'20A',poles:'3P / 4W',ground:'Yes',use:'Locking split-phase 20A',highlight:false},
  {type:'twistlock',config:'NEMA L14-30',voltage:'125/250V',amps:'30A',poles:'3P / 4W',ground:'Yes',use:'Locking split-phase 30A — generator feeds',highlight:false},
  {type:'twistlock',config:'NEMA L21-20',voltage:'3\u00d8 120/208V',amps:'20A',poles:'4P / 5W',ground:'Yes',use:'Locking 3\u00d8 208V 20A — most common data center',highlight:true},
  {type:'twistlock',config:'NEMA L21-30',voltage:'3\u00d8 120/208V',amps:'30A',poles:'4P / 5W',ground:'Yes',use:'Locking 3\u00d8 208V 30A — standard PDU input',highlight:true},
  {type:'twistlock',config:'NEMA L22-20',voltage:'3\u00d8 277/480V',amps:'20A',poles:'4P / 5W',ground:'Yes',use:'Locking 3\u00d8 480V 20A — use for 415V circuits',highlight:true},
  {type:'twistlock',config:'NEMA L22-30',voltage:'3\u00d8 277/480V',amps:'30A',poles:'4P / 5W',ground:'Yes',use:'Locking 3\u00d8 480V 30A — 415V PDU standard',highlight:true},
  {type:'twistlock',config:'NEMA L23-20',voltage:'3\u00d8 347/600V',amps:'20A',poles:'4P / 5W',ground:'Yes',use:'Locking 600V 20A — Canadian facilities',highlight:false},
  {type:'twistlock',config:'NEMA L23-30',voltage:'3\u00d8 347/600V',amps:'30A',poles:'4P / 5W',ground:'Yes',use:'Locking 600V 30A',highlight:false},
  // IEC
  {type:'iec',config:'IEC C13',voltage:'250V',amps:'10A (15A rated)',poles:'2P / 3W',ground:'Yes',use:'Server PSU inlet — universal standard',highlight:true},
  {type:'iec',config:'IEC C14 (plug)',voltage:'250V',amps:'10A (15A rated)',poles:'2P / 3W',ground:'Yes',use:'PDU outlet plug for C13 inlet',highlight:true},
  {type:'iec',config:'IEC C15',voltage:'250V',amps:'10A',poles:'2P / 3W',ground:'Yes',use:'High-temp C13 variant — hot equipment',highlight:false},
  {type:'iec',config:'IEC C19',voltage:'250V',amps:'16A (20A rated)',poles:'2P / 3W',ground:'Yes',use:'High-density server PSU, network switches',highlight:true},
  {type:'iec',config:'IEC C20 (plug)',voltage:'250V',amps:'16A (20A rated)',poles:'2P / 3W',ground:'Yes',use:'PDU outlet plug for C19 inlet',highlight:true},
  {type:'iec',config:'IEC C21',voltage:'250V',amps:'16A',poles:'2P / 3W',ground:'Yes',use:'High-temp C19 variant',highlight:false},
  // PIN & SLEEVE
  {type:'pinsleeve',config:'IEC 60309 2P+E 16A 110V',voltage:'100-130V',amps:'16A',poles:'2P+E / 3W',ground:'Yes',use:'Construction site 110V (Yellow)',highlight:false},
  {type:'pinsleeve',config:'IEC 60309 2P+E 16A 230V',voltage:'200-250V',amps:'16A',poles:'2P+E / 3W',ground:'Yes',use:'Single-phase 230V 16A — Blue (EU standard)',highlight:true},
  {type:'pinsleeve',config:'IEC 60309 2P+E 32A 230V',voltage:'200-250V',amps:'32A',poles:'2P+E / 3W',ground:'Yes',use:'Single-phase 230V 32A — Blue',highlight:false},
  {type:'pinsleeve',config:'IEC 60309 3P+E 16A 400V',voltage:'380-415V',amps:'16A',poles:'3P+E / 4W',ground:'Yes',use:'3-phase 400/415V 16A — Red (DC standard)',highlight:true},
  {type:'pinsleeve',config:'IEC 60309 3P+E 32A 400V',voltage:'380-415V',amps:'32A',poles:'3P+E / 4W',ground:'Yes',use:'3-phase 415V 32A — Red — PDU input',highlight:true},
  {type:'pinsleeve',config:'IEC 60309 3P+E 63A 400V',voltage:'380-415V',amps:'63A',poles:'3P+E / 4W',ground:'Yes',use:'3-phase 415V 63A — Red — high-density rows',highlight:true},
  {type:'pinsleeve',config:'IEC 60309 3P+N+E 16A 400V',voltage:'380-415V',amps:'16A',poles:'3P+N+E / 5W',ground:'Yes',use:'3-phase + neutral 415V 16A (Red 5-pin)',highlight:false},
  {type:'pinsleeve',config:'IEC 60309 3P+N+E 32A 400V',voltage:'380-415V',amps:'32A',poles:'3P+N+E / 5W',ground:'Yes',use:'3-phase + neutral 415V 32A (Red 5-pin)',highlight:false},
  {type:'pinsleeve',config:'IEC 60309 3P+N+E 63A 400V',voltage:'380-415V',amps:'63A',poles:'3P+N+E / 5W',ground:'Yes',use:'3-phase + neutral 415V 63A (Red 5-pin)',highlight:false},
  {type:'pinsleeve',config:'IEC 60309 3P+N+E 125A 400V',voltage:'380-415V',amps:'125A',poles:'3P+N+E / 5W',ground:'Yes',use:'3-phase + neutral 415V 125A — main feeds',highlight:false},
];

var _nFilter='all', _nSearch='';
var _nMeta={straight:{label:'Straight Blade',cls:'nb-straight'},twistlock:{label:'Twist-Lock',cls:'nb-twistlock'},iec:{label:'IEC',cls:'nb-iec'},pinsleeve:{label:'Pin & Sleeve',cls:'nb-pinsleeve'}};

function renderNEMATable(){
  var tbody=document.getElementById('nema-tbody');
  if(!tbody)return;
  var q=_nSearch.toLowerCase();
  var rows=NEMA_DATA.filter(function(r){
    return (_nFilter==='all'||r.type===_nFilter)&&
           (!q||r.config.toLowerCase().includes(q)||r.voltage.toLowerCase().includes(q)||
            r.amps.toLowerCase().includes(q)||r.use.toLowerCase().includes(q)||
            r.poles.toLowerCase().includes(q));
  });
  if(!rows.length){tbody.innerHTML='<tr><td colspan="8" style="padding:28px;text-align:center;color:#706e6b;">No configurations match.</td></tr>';return;}
  tbody.innerHTML=rows.map(function(r){
    var m=_nMeta[r.type]||{label:r.type,cls:'nb-straight'};
    var star=r.highlight?'<span style="font-size:9px;background:#fef08a;color:#713f12;padding:1px 5px;border-radius:3px;font-weight:700;margin-left:4px;">\u2605 DC STD</span>':'';
    var bg=r.highlight?'#fefce8':'#fff';
    var cfg=r.config.replace(/'/g,"\\'");
    return '<tr class="nema-row" style="border-bottom:1px solid #f1f5f9;background:'+bg+'" onclick="selectNEMARow(this)">'+
      '<td style="padding:8px 12px"><span class="nema-badge '+m.cls+'">'+m.label+'</span></td>'+
      '<td style="padding:8px 12px;font-weight:700;color:#16325c;font-size:12.5px;">'+r.config+'</td>'+
      '<td style="padding:8px 12px;font-family:monospace;color:#0070d2;font-weight:600;">'+r.voltage+'</td>'+
      '<td style="padding:8px 12px;font-weight:700;color:#e65100;">'+r.amps+'</td>'+
      '<td style="padding:8px 12px;color:#706e6b;font-size:11px;">'+r.poles+'</td>'+
      '<td style="padding:8px 12px"><span style="font-size:10px;padding:2px 8px;border-radius:10px;font-weight:600;background:'+(r.ground==='Yes'?'#dcfce7':'#fee2e2')+';color:'+(r.ground==='Yes'?'#15803d':'#dc2626')+'">'+(r.ground==='Yes'?'\u2713 Yes':'\u2715 No')+'</span></td>'+
      '<td style="padding:8px 12px;color:#374151;font-size:11px;max-width:240px;white-space:normal;line-height:1.4;">'+r.use+star+'</td>'+
      '<td style="padding:8px 12px;text-align:center"><button onclick="event.stopPropagation();applyNEMA(\''+cfg+'\')" '+
        'style="padding:4px 12px;background:#0070d2;color:#fff;border:none;border-radius:5px;font-size:11px;font-weight:700;cursor:pointer;font-family:inherit;transition:all 0.15s;" '+
        'onmouseover="this.style.background=\'#0058a8\'" onmouseout="this.style.background=\'#0070d2\'">Select \u21b5</button></td>'+
    '</tr>';
  }).join('');
}

function filterNEMA(type){
  _nFilter=type;
  document.querySelectorAll('.nf-btn').forEach(function(b){b.classList.remove('nf-active');});
  var el=document.getElementById('nf-'+type);if(el)el.classList.add('nf-active');
  renderNEMATable();
}

function searchNEMA(val){_nSearch=val;renderNEMATable();}

function selectNEMARow(row){
  document.querySelectorAll('.nema-row').forEach(function(r){r.classList.remove('nema-selected');});
  row.classList.add('nema-selected');
}

function applyNEMA(config){
  var row=NEMA_DATA.find(function(r){return r.config===config;});
  if(!row)return;
  // Set termination type dropdown if present
  var tSel=document.getElementById('term-sel');
  if(tSel){
    tSel.value=row.type;
    if(typeof updateTermDetail==='function') updateTermDetail(row.type);
  }
  // Try to match detail dropdown
  var dSel=document.getElementById('term-detail-sel');
  if(dSel){
    var short=config.toLowerCase().replace('nema ','').split(' ')[0];
    for(var i=0;i<dSel.options.length;i++){
      if(dSel.options[i].text.toLowerCase().includes(short)){dSel.selectedIndex=i;break;}
    }
  }
  // Show applied badge if element exists
  var applied=document.getElementById('nema-applied');
  if(applied){applied.style.display='block';applied.innerHTML='\u2713 Applied: <strong>'+config+'</strong> &middot; '+row.voltage+' &middot; '+row.amps;}
  closeNEMA();
  // Toast notification
  var t=document.createElement('div');
  t.style.cssText='position:fixed;bottom:24px;right:24px;background:#2e7d32;color:#fff;padding:11px 20px;border-radius:9px;font-size:12px;font-weight:700;z-index:99999;box-shadow:0 6px 20px rgba(0,0,0,0.25);font-family:"DM Sans",sans-serif;display:flex;align-items:center;gap:8px;';
  t.innerHTML='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>Applied: '+config;
  document.body.appendChild(t);
  setTimeout(function(){if(t.parentNode)t.parentNode.removeChild(t);},2800);
}

function openNEMA(){
  _nFilter='all';_nSearch='';
  document.querySelectorAll('.nf-btn').forEach(function(b){b.classList.remove('nf-active');});
  var a=document.getElementById('nf-all');if(a)a.classList.add('nf-active');
  var s=document.getElementById('nema-search');if(s)s.value='';
  renderNEMATable();
  document.getElementById('nema-modal').style.display='block';
  document.body.style.overflow='hidden';
}
function closeNEMA(){
  document.getElementById('nema-modal').style.display='none';
  document.body.style.overflow='';
}
document.getElementById('nema-modal').addEventListener('click',function(e){if(e.target===this)closeNEMA();});
</script>
"""

# ─── MAIN ────────────────────────────────────────────────────────────────────
def patch():
    if not os.path.exists(TARGET):
        print(f"ERROR: '{TARGET}' not found in current directory.")
        print(f"Current directory: {os.getcwd()}")
        print("Please cd into your project folder first, then run this script.")
        sys.exit(1)

    # Backup
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = f"{TARGET}.backup_{ts}"
    shutil.copy2(TARGET, backup)
    print(f"  Backup created: {backup}")

    with open(TARGET, "r", encoding="utf-8") as f:
        html = f.read()

    original_len = len(html)
    patches_applied = []

    # ── PATCH 1: CSS ──────────────────────────────────────────────────────────
    if "nema-ref-btn" not in html:
        if "</style>" in html:
            html = html.replace("</style>", CSS_PATCH + "\n</style>", 1)
            patches_applied.append("CSS injected before </style>")
        else:
            print("  WARNING: Could not find </style> — CSS not injected.")
    else:
        patches_applied.append("CSS already present — skipped")

    # ── PATCH 2: Button ───────────────────────────────────────────────────────
    if "openNEMA" not in html:
        # Find the sf-form-title div that contains "Branch Circuit"
        # Pattern: look for badge b-blue inside the title that has Branch Circuit
        patterns = [
            # Most likely pattern from the existing file
            (r'(<div class="sf-form-title"><span>[^<]*Branch Circuit[^<]*</span>)(<span class="badge b-blue">Power product</span></div>)',
             r'\1<div style="display:flex;align-items:center;gap:8px;">\2' +
             BUTTON_SNIPPET.strip() +
             r'</div></div>'),
        ]
        patched = False
        for pat, rep in patterns:
            new_html, n = re.subn(pat, rep, html)
            if n > 0:
                html = new_html
                patches_applied.append(f"NEMA button injected ({n} location(s))")
                patched = True
                break
        if not patched:
            # Fallback: inject button after every "badge b-blue">Power product
            fallback = '<span class="badge b-blue">Power product</span>'
            inject  = '<span class="badge b-blue">Power product</span> ' + \
                      '<button class="nema-ref-btn" onclick="openNEMA()" style="margin-left:6px;">' + \
                      '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">' + \
                      '<circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/></svg>' + \
                      ' NEMA / Connector Reference</button>'
            if fallback in html:
                html = html.replace(fallback, inject)
                patches_applied.append("NEMA button injected (fallback method)")
            else:
                print("  WARNING: Could not find Branch Circuit title — button not injected.")
                print("  Manually add: <button class='nema-ref-btn' onclick='openNEMA()'>NEMA / Connector Reference</button>")
                print("  near the ⚡ Branch Circuit form title.")
    else:
        patches_applied.append("Button already present — skipped")

    # ── PATCH 3: Modal + JS ───────────────────────────────────────────────────
    if "nema-modal" not in html:
        if "</body>" in html:
            html = html.replace("</body>", MODAL_AND_JS + "\n</body>", 1)
            patches_applied.append("Modal + JS injected before </body>")
        else:
            html = html + MODAL_AND_JS
            patches_applied.append("Modal + JS appended to end of file")
    else:
        patches_applied.append("Modal already present — skipped")

    # Write output
    with open(TARGET, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n  Done! {TARGET} patched successfully.")
    print(f"  Original size : {original_len:,} bytes")
    print(f"  Patched size  : {len(html):,} bytes")
    print(f"\n  Changes applied:")
    for p in patches_applied:
        print(f"    \u2713 {p}")
    print(f"\n  Original backed up to: {backup}")
    print("  Open salesforce-branch-circuit-mockup.html in your browser to test.")

if __name__ == "__main__":
    print("\nNEMA Reference Patcher")
    print("=" * 46)
    patch()