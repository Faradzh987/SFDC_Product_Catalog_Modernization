import re

filename = 'salesforce-branch-circuit-mockup.html'
with open(filename, 'r') as f:
    html = f.read()

new_style = '''<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --sf-blue: #0070d2;
  --sf-navy: #032D60;
  --sf-dark: #16325c;
  --sf-green: #2e7d32;
  --sf-red: #c23934;
  --sf-orange: #e65100;
  --sf-gray: #706e6b;
  --sf-border: #e5e7eb;
  --sf-bg: #f8fafc;
  --sf-white: #ffffff;
  --sf-card-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --sf-card-shadow-hover: 0 4px 12px rgba(0,112,210,0.12), 0 2px 4px rgba(0,0,0,0.06);
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'DM Sans',sans-serif;background:var(--sf-bg);color:var(--sf-dark);font-size:13px;line-height:1.5}
h1{font-size:15px;font-weight:600;color:var(--sf-dark);margin-bottom:2px}
.subtitle{font-size:11px;color:var(--sf-gray);margin-bottom:12px}

/* TOP NAV */
.toggle-row{display:flex;align-items:center;gap:10px;margin-bottom:12px;padding:10px 16px;background:var(--sf-white);border:1px solid var(--sf-border);border-radius:var(--radius-md);width:fit-content;box-shadow:var(--sf-card-shadow)}
.toggle-lbl{font-size:12px;font-weight:500;color:var(--sf-gray)}
.toggle-lbl.active{color:var(--sf-dark);font-weight:600}
.toggle-track{position:relative;width:40px;height:22px;border-radius:11px;cursor:pointer;transition:background 0.2s;display:inline-block}
.toggle-track input{position:absolute;opacity:0;width:100%;height:100%;cursor:pointer;margin:0;z-index:1}
.toggle-knob{position:absolute;top:3px;left:3px;width:16px;height:16px;background:#fff;border-radius:50%;transition:transform 0.2s;pointer-events:none;box-shadow:0 1px 3px rgba(0,0,0,0.2)}

/* CALLOUTS */
.callout{padding:8px 14px;border-radius:var(--radius-sm);font-size:11px;margin-bottom:12px;border-left:3px solid;line-height:1.6;display:flex;align-items:flex-start;gap:8px}
.callout-red{background:#fef2f2;border-color:var(--sf-red);color:#991b1b}
.callout-green{background:#f0fdf4;border-color:var(--sf-green);color:#166534}
.callout-blue{background:#eff6ff;border-color:var(--sf-blue);color:#1e40af}
.callout-orange{background:#fff7ed;border-color:var(--sf-orange);color:#9a3412}

/* SF CHROME */
.sf-wrap{border-radius:var(--radius-lg);overflow:hidden;border:1px solid var(--sf-border);margin-bottom:14px;box-shadow:var(--sf-card-shadow)}
.sf-topbar{background:linear-gradient(135deg,#0070d2 0%,#005fb2 100%);padding:8px 14px;display:flex;align-items:center;gap:10px}
.sf-topbar-title{color:#fff;font-size:12px;font-weight:600;letter-spacing:0.01em}
.sf-topbar-pill{background:rgba(255,255,255,0.2);color:rgba(255,255,255,0.9);font-size:10px;padding:2px 8px;border-radius:20px;font-weight:500;border:1px solid rgba(255,255,255,0.15)}
.sf-subbar{background:#f8fafc;border-bottom:1px solid var(--sf-border);padding:6px 14px;display:flex;align-items:center;justify-content:space-between}
.sf-subbar-title{font-size:14px;font-weight:600;color:var(--sf-dark)}
.sf-meta{font-size:10px;color:var(--sf-gray);padding:4px 14px;background:#fff;border-bottom:1px solid #f0f0f0}
.sf-table-wrap{overflow-x:auto;background:#fff}

/* TABLES */
table{width:100%;border-collapse:collapse;font-size:12px}
thead tr{background:#f8fafc;border-bottom:2px solid var(--sf-border)}
th{padding:8px 12px;text-align:left;font-size:10px;font-weight:600;color:var(--sf-gray);white-space:nowrap;text-transform:uppercase;letter-spacing:0.05em}
td{padding:7px 12px;border-bottom:1px solid #f1f5f9;color:var(--sf-dark);white-space:nowrap}
tr:last-child td{border-bottom:none}
tr:hover td{background:#f8fafc}
.link{color:var(--sf-blue);cursor:pointer;text-decoration:none;font-weight:500}
.link:hover{text-decoration:underline}

/* BADGES */
.badge{display:inline-flex;align-items:center;font-size:10px;padding:2px 8px;border-radius:20px;font-weight:600;white-space:nowrap;gap:3px}
.b-green{background:#dcfce7;color:#15803d}
.b-blue{background:#dbeafe;color:#1d4ed8}
.b-red{background:#fee2e2;color:#dc2626}
.b-purple{background:#f3e8ff;color:#7c3aed}
.b-orange{background:#ffedd5;color:#c2410c}
.b-gray{background:#f1f5f9;color:#475569}
.b-teal{background:#ccfbf1;color:#0f766e}

/* STEP LABELS */
.step-wrap{margin-bottom:14px}
.step-label{display:flex;align-items:center;gap:10px;margin-bottom:8px;padding:10px 16px;background:var(--sf-white);border:1px solid var(--sf-border);border-radius:var(--radius-md);box-shadow:var(--sf-card-shadow)}
.step-num{background:var(--sf-blue);color:#fff;font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;white-space:nowrap}
.step-title{font-size:13px;font-weight:600;color:var(--sf-dark)}
.step-sub{font-size:11px;color:var(--sf-gray);margin-left:2px}

/* FORM FIELDS */
.step1-card{background:#fff;border:1px solid var(--sf-border);border-radius:var(--radius-md);padding:14px;margin-bottom:8px;box-shadow:var(--sf-card-shadow)}
.sf-field{margin-bottom:10px}
.sf-field label{display:block;font-size:10px;font-weight:600;color:var(--sf-gray);text-transform:uppercase;letter-spacing:0.05em;margin-bottom:3px}
.sf-field select,.sf-field input,.sf-field textarea{width:100%;padding:6px 10px;border:1px solid var(--sf-border);border-radius:var(--radius-sm);font-size:12px;color:var(--sf-dark);background:#fff;font-family:'DM Sans',sans-serif;transition:border-color 0.15s,box-shadow 0.15s}
.sf-field select:focus,.sf-field input:focus,.sf-field textarea:focus{outline:none;border-color:var(--sf-blue);box-shadow:0 0 0 3px rgba(0,112,210,0.1)}
.sf-field textarea{resize:vertical;min-height:60px}
.hint{font-size:10px;color:var(--sf-gray);margin-top:2px}
.required{color:var(--sf-red)}
.info-btn{font-size:10px;color:var(--sf-blue);cursor:pointer;text-decoration:underline;font-weight:400;text-transform:none;letter-spacing:0;margin-left:4px}

/* CATEGORY TABS */
.cat-tabs{display:flex;gap:0;background:#f8fafc;border-bottom:2px solid var(--sf-blue);margin:0}
.ctab{padding:9px 18px;font-size:12px;font-weight:600;cursor:pointer;color:var(--sf-gray);border:1px solid var(--sf-border);border-bottom:none;background:#f8fafc;margin-right:3px;border-radius:var(--radius-sm) var(--radius-sm) 0 0;transition:all 0.15s}
.ctab.active{background:var(--sf-blue);color:#fff;border-color:var(--sf-blue)}
.ctab:hover:not(.active){background:#eff6ff;color:var(--sf-blue);border-color:#bfdbfe}

/* PRODUCT TABS */
.product-tabs{display:flex;gap:2px;padding:8px 14px 0;background:#fff;border-bottom:1px solid var(--sf-border);flex-wrap:wrap}
.ptab{padding:6px 12px;font-size:11px;font-weight:600;cursor:pointer;border-radius:var(--radius-sm) var(--radius-sm) 0 0;border:1px solid transparent;border-bottom:none;color:var(--sf-gray);background:transparent;margin-bottom:-1px;transition:all 0.15s}
.ptab.active{background:#fff;border-color:var(--sf-border);color:var(--sf-blue);border-bottom-color:#fff}
.ptab:hover:not(.active){background:#f8fafc;color:var(--sf-blue)}

/* FORM CARDS */
.sf-form-card{background:#fff;border:1px solid var(--sf-border);border-top:none;border-radius:0 0 var(--radius-md) var(--radius-md);padding:16px;margin-bottom:14px}
.sf-form-title{font-size:13px;font-weight:600;color:var(--sf-dark);margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid #f1f5f9;display:flex;align-items:center;justify-content:space-between}
.sf-cols{display:grid;grid-template-columns:1fr 1fr;gap:0 20px}
.sf-col-title{font-size:10px;font-weight:700;color:var(--sf-gray);text-transform:uppercase;letter-spacing:0.06em;padding:5px 0;border-bottom:1px solid #f1f5f9;margin-bottom:8px}
.sf-btn-row{display:flex;gap:8px;margin-top:12px}

/* BUTTONS */
.btn-p,.sf-btn-p{padding:6px 16px;background:var(--sf-blue);color:#fff;border:none;border-radius:var(--radius-sm);font-size:12px;font-weight:600;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all 0.15s;box-shadow:0 1px 2px rgba(0,112,210,0.2)}
.btn-p:hover,.sf-btn-p:hover{background:#005fb2;transform:translateY(-1px);box-shadow:0 3px 8px rgba(0,112,210,0.3)}
.btn-s,.sf-btn-s{padding:6px 14px;background:#fff;color:var(--sf-blue);border:1px solid var(--sf-blue);border-radius:var(--radius-sm);font-size:12px;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all 0.15s;font-weight:500}
.btn-s:hover,.sf-btn-s:hover{background:#eff6ff}
.btn-g{padding:6px 14px;background:var(--sf-green);color:#fff;border:none;border-radius:var(--radius-sm);font-size:12px;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all 0.15s;font-weight:600}
.btn-g:hover{background:#1b5e20;transform:translateY(-1px)}

/* PRODUCT LANDING CARDS */
.product-pane{display:none}
.product-pane.active{display:block}

/* VENDOR CARDS */
.vendor-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px}
.vendor-card{background:#fff;border:2px solid var(--sf-border);border-radius:var(--radius-md);padding:14px;cursor:pointer;transition:all 0.2s;box-shadow:var(--sf-card-shadow)}
.vendor-card:hover{border-color:var(--sf-blue);box-shadow:var(--sf-card-shadow-hover);transform:translateY(-1px)}
.vendor-card.selected{border-color:var(--sf-green);background:#f0fdf4;box-shadow:0 2px 8px rgba(46,125,50,0.15)}
.vendor-name{font-size:13px;font-weight:700;color:var(--sf-dark);margin-bottom:8px}
.vendor-detail{font-size:11px;color:var(--sf-gray);margin-bottom:4px;display:flex;justify-content:space-between}
.vendor-detail span:last-child{font-weight:600;color:var(--sf-dark)}
.vendor-badge{display:inline-block;font-size:10px;padding:2px 8px;border-radius:20px;font-weight:600;margin-top:6px}
.vb-best{background:#dcfce7;color:#15803d}
.vb-fast{background:#dbeafe;color:#1d4ed8}
.vb-cheap{background:#ffedd5;color:#c2410c}

/* UPDATE BOX */
.update-box{background:#f0fdf4;border:1px solid #86efac;border-radius:var(--radius-md);padding:14px;margin-bottom:14px}
.update-title{font-size:12px;font-weight:700;color:var(--sf-green);margin-bottom:10px;display:flex;align-items:center;gap:6px}
.update-fields{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.update-field{background:#fff;border:1px solid #86efac;border-radius:var(--radius-sm);padding:8px 10px;text-align:center}
.update-val{font-size:18px;font-weight:700;color:var(--sf-green)}
.update-lbl{font-size:10px;color:var(--sf-gray);margin-top:2px}

/* TOPO HINT */
.topo-hint{margin-top:6px;font-size:11px;padding:8px 10px;border-radius:var(--radius-sm);display:none;line-height:1.5;border-left:3px solid}
.warn-flag{margin-top:4px;font-size:11px;padding:5px 8px;border-radius:var(--radius-sm);background:#fee2e2;border-left:3px solid var(--sf-red);color:var(--sf-red);display:none}
.market-pill{display:inline-flex;align-items:center;gap:3px;background:#dbeafe;border:1px solid #bfdbfe;border-radius:20px;font-size:10px;color:#1d4ed8;padding:1px 7px;margin-left:6px;font-weight:500}

/* SUPPLEMENTALS */
.supp-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}
.supp-card{background:#fff;border:1px solid var(--sf-border);border-radius:var(--radius-md);padding:14px;box-shadow:var(--sf-card-shadow)}
.supp-title{font-size:12px;font-weight:700;color:var(--sf-dark);margin-bottom:5px;display:flex;align-items:center;gap:5px}
.supp-sub{font-size:11px;color:var(--sf-gray);margin-bottom:10px;line-height:1.5}
.supp-item{display:flex;align-items:center;justify-content:space-between;padding:5px 0;border-bottom:1px solid #f1f5f9;font-size:12px}
.supp-item:last-child{border-bottom:none}

/* IMPACT CARDS */
.impact{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px}
.impact-card{background:#fff;border-radius:var(--radius-md);padding:12px 16px;border:1px solid var(--sf-border);box-shadow:var(--sf-card-shadow);transition:box-shadow 0.2s}
.impact-card:hover{box-shadow:var(--sf-card-shadow-hover)}
.impact-num{font-size:28px;font-weight:700;line-height:1}
.impact-lbl{font-size:11px;color:var(--sf-gray);margin-top:3px}

/* LEAD TIME BOX */
#lt-result{margin-top:10px;background:#eff6ff;border:1px solid #bfdbfe;border-radius:var(--radius-md);padding:12px 14px;font-size:12px;color:var(--sf-dark);line-height:1.8}
#lt-circuit-box{background:#f8fafc;border:1px solid var(--sf-border);border-radius:var(--radius-md);padding:12px 14px;margin-bottom:14px}

/* QUOTE BASKET */
#basket-items{max-height:400px;overflow-y:auto}

/* CAGE RESULT */
#cage-result{background:#eff6ff;border:1px solid #bfdbfe;border-radius:var(--radius-sm);padding:10px;font-size:12px;color:var(--sf-dark)}

/* SECTION TITLES */
.sec-title{font-size:10px;font-weight:700;color:var(--sf-gray);padding:8px 0;border-bottom:1px solid #f1f5f9;margin-bottom:10px;text-transform:uppercase;letter-spacing:0.06em;display:flex;align-items:center;gap:6px}

/* SCROLLBAR */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:#f1f5f9}
::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:#94a3b8}
</style>'''

# Replace entire style block
html = re.sub(r'<style>.*?</style>', new_style, html, count=1, flags=re.DOTALL)

# Also tighten the body padding
html = html.replace('background:#f3f3f3;padding:24px;color:#16325c', 
                    'background:var(--sf-bg);padding:16px 20px;color:var(--sf-dark)')

# Fix toggle track colors to use CSS vars
html = html.replace("id=\"tt\" style=\"background:#c23934\"", "id=\"tt\" style=\"background:#c23934\"")

with open(filename, 'w') as f:
    f.write(html)
print('✓ Redesigned salesforce-branch-circuit-mockup.html')
