#!/usr/bin/env python3
"""
fix_nema_branch.py
Removes NEMA button from everywhere, adds it ONLY to Branch Circuit section.
"""
import os, sys, shutil, re
from datetime import datetime

TARGET = "salesforce-branch-circuit-mockup.html"

NEMA_BUTTON = (
    ' <button class="nema-ref-btn" onclick="openNEMA()" style="margin-left:8px;">'
    '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">'
    '<circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/></svg>'
    ' NEMA / Connector Reference</button>'
)

def fix():
    if not os.path.exists(TARGET):
        print(f"ERROR: '{TARGET}' not found in {os.getcwd()}")
        sys.exit(1)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = f"{TARGET}.backup_{ts}"
    shutil.copy2(TARGET, backup)
    print(f"  Backup: {backup}")

    with open(TARGET, "r", encoding="utf-8") as f:
        html = f.read()

    # ── STEP 1: Strip ALL existing NEMA buttons ───────────────────────────────
    html = re.sub(
        r'\s*<button[^>]+onclick=["\']openNEMA\(\)["\'][^>]*>.*?</button>',
        '', html, flags=re.DOTALL
    )
    # Clean up any empty flex wrappers left behind
    html = re.sub(
        r'<div style="display:flex;[^"]*align-items:center[^"]*">\s*'
        r'(<span class="badge[^>]*>[^<]*</span>)\s*</div>',
        r'\1', html
    )
    print("  ✓ Removed NEMA button from all locations")

    # ── STEP 2: Inject ONLY into Branch Circuit form title ────────────────────
    # The Branch Circuit section title contains "Branch Circuit" and has
    # "Power product" badge. Find it and append the button after the badge.

    # Pattern: find the exact sf-form-title containing "Branch Circuit"
    pattern = re.compile(
        r'(<div class="sf-form-title">)'          # opening div
        r'(.*?Branch Circuit.*?)'                  # content with Branch Circuit
        r'(</div>)',                               # closing div
        re.DOTALL
    )

    matches = list(pattern.finditer(html))

    if matches:
        # Use the first match
        m = matches[0]
        new_title = m.group(1) + m.group(2).rstrip() + NEMA_BUTTON + '\n' + m.group(3)
        html = html[:m.start()] + new_title + html[m.end():]
        print(f"  ✓ NEMA button injected into Branch Circuit form title")
    else:
        # Fallback: inject after "Power product · attaches to space" badge
        fallback = 'Power product · attaches to space'
        fallback2 = 'Power product</span>'
        target_str = None
        if fallback in html:
            target_str = fallback
        elif fallback2 in html:
            target_str = fallback2

        if target_str:
            # Find last occurrence of this badge (the one in the Branch Circuit view)
            pos = html.rfind(target_str)
            insert_at = pos + len(target_str)
            html = html[:insert_at] + NEMA_BUTTON + html[insert_at:]
            print("  ✓ NEMA button injected (fallback: Power product badge)")
        else:
            print("  ⚠ Could not find Branch Circuit title.")
            print("    Manually add: <button class='nema-ref-btn' onclick='openNEMA()'>")
            print("    NEMA / Connector Reference</button>")
            print("    next to the Branch Circuit form title.")

    with open(TARGET, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n  Done! Reload the page — NEMA button should appear ONLY in Branch Circuit.")
    print(f"  Backup: {backup}")

if __name__ == "__main__":
    print("\nNEMA Fix — Branch Circuit Only")
    print("=" * 40)
    fix()
