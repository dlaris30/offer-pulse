#!/usr/bin/env python3
"""
pricing-xml-checker — structural checker and comparator for GoDaddy pricing promo XML.

Checks generated XML against hard structural rules and diffs it field-by-field
against a source-of-truth expected XML. Produces scored comparison reports.

This tool measures output quality. It does not generate XML or update its own rules.
Failure reports are reviewed by a human and used to improve the generation skill.

Commands:
  python checker.py derive                         Scan golden-set/, update derived_rules.json
  python checker.py check <xml>                    Check structural rules on a single XML
  python checker.py compare <generated> <expected> Full field-by-field comparison
  python checker.py report                         Aggregate all saved comparison reports
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

SCRIPT_DIR   = Path(__file__).parent
GOLDEN_DIR   = SCRIPT_DIR / "golden-set"
DERIVED_FILE = GOLDEN_DIR / "derived_rules.json"
REPORTS_DIR  = SCRIPT_DIR / "reports"

XSI_NIL = "{http://www.w3.org/2001/XMLSchema-instance}nil"

# ─────────────────────────────────────────────────────────────────────────────
# XML PARSING
# ─────────────────────────────────────────────────────────────────────────────

def _text(root, tag, default=""):
    el = root.find(tag)
    return (el.text or "").strip() if el is not None else default

def _is_nil(root, tag):
    el = root.find(tag)
    return el is None or el.get(XSI_NIL) == "true"

def parse_promo(path: Path) -> dict:
    """Parse a ProductPromo XML into a structured dict."""
    # Strip the XML declaration — source files declare utf-16 but are stored as utf-8
    content = path.read_text(encoding="utf-8", errors="replace")
    if content.startswith("<?xml"):
        content = content[content.index("?>") + 2:].lstrip()
    root = ET.fromstring(content)

    awards = []
    for aw in root.findall(".//ProductAwardV2"):
        pfids = [int(p.text) for p in aw.findall(".//PfIds/int") if p.text]

        currencies = {}
        for c in aw.findall(".//AwardCurrencies/ProductAwardCurrency"):
            curr = (c.findtext("Currency") or "").strip()
            amt  = (c.findtext("DiscountAmount") or "").strip()
            if curr and amt:
                try:
                    currencies[curr] = float(amt)
                except ValueError:
                    pass

        aq_el  = aw.find("AwardQuantity")
        aq_nil = aq_el is not None and aq_el.get(XSI_NIL) == "true"

        awards.append({
            "award_id":       (aw.findtext("AwardId") or "").strip(),
            "amount_type":    (aw.findtext("AwardAmountType") or "").strip(),
            "award_type":     (aw.findtext("AwardType") or "").strip(),
            "award_quantity": None if aq_nil else (aw.findtext("AwardQuantity") or "").strip() or None,
            "percent_off":    (aw.findtext("PercentOff") or "").strip() or None,
            "pfids":          pfids,
            "currencies":     currencies,
        })

    cond_el         = root.find("Conditions")
    conditions_empty = cond_el is not None and len(list(cond_el)) == 0

    pl_ids = [el.text for el in root.findall(".//PrivateLabels/PrivateLabelV2/PrivateLabelID") if el.text]

    return {
        "promo_code":        _text(root, "PromoCode"),
        "name":              _text(root, "Name"),
        "description":       _text(root, "Description"),
        "start_date":        _text(root, "StartDate"),
        "expiration_date":   _text(root, "ExpirationDate"),
        "rank":              _text(root, "Rank"),
        "rank_value":        _text(root, "RankValue"),
        "use_limit":         None if _is_nil(root, "UseLimit") else _text(root, "UseLimit") or None,
        "number_of_uses":    None if _is_nil(root, "NumberOfUses") else _text(root, "NumberOfUses") or None,
        "award_applies_to":  _text(root, "AwardAppliesTo"),
        "restriction":       _text(root, "Restriction"),
        "usage_type":        _text(root, "UsageType"),
        "conditions_empty":  conditions_empty,
        "private_label_ids": pl_ids,
        "awards":            awards,
        "has_pfid_list":     root.find("PFIDList") is not None,
    }


# ─────────────────────────────────────────────────────────────────────────────
# HARD RULES  (zero exceptions in corpus — always enforced as FAIL)
# ─────────────────────────────────────────────────────────────────────────────

def check_hard_rules(promo: dict) -> list:
    results = []

    def rule(id_, desc, passed, detail=""):
        results.append({
            "id":          id_,
            "tier":        "hard",
            "description": desc,
            "status":      "PASS" if passed else "FAIL",
            "detail":      detail,
        })

    # S1 — Conditions empty
    rule("S1", "Conditions block is empty",
         promo["conditions_empty"],
         "" if promo["conditions_empty"] else "Has child elements — remove all conditions")

    # S2 — PrivateLabels PL1
    pl = promo["private_label_ids"]
    rule("S2", "PrivateLabels present with exactly PL1",
         pl == ["1"],
         "" if pl == ["1"] else f"Found: {pl}")

    # S3 — AwardAppliesTo
    AAT = "HighestPriceFirstMayOverlapConditions"
    rule("S3", "AwardAppliesTo present and correct",
         promo["award_applies_to"] == AAT,
         "" if promo["award_applies_to"] == AAT else f"Found: '{promo['award_applies_to']}'")

    # S4 — No PFIDList
    rule("S4", "No PFIDList block",
         not promo["has_pfid_list"],
         "PFIDList present — remove it" if promo["has_pfid_list"] else "")

    # S5 — Name == Description
    rule("S5", "Name equals Description",
         promo["name"] == promo["description"],
         "" if promo["name"] == promo["description"]
         else f"Name:  '{promo['name']}'\nDesc:  '{promo['description']}'")

    # C1/C2 — AwardAmountType consistency
    for i, aw in enumerate(promo["awards"], 1):
        amt = aw["amount_type"]
        aq  = aw["award_quantity"]
        ul  = promo["use_limit"]
        if amt == "Unlimited":
            rule(f"C1.{i}", f"Award {i} (Unlimited) → AwardQuantity nil",
                 aq is None,
                 "" if aq is None else f"AwardQuantity={aq}")
        elif amt == "Units":
            # AwardQuantity must be set; UseLimit is an optional per-shopper constraint
            rule(f"C2.{i}", f"Award {i} (Units) → AwardQuantity is set",
                 aq is not None,
                 "AwardQuantity must be a number when AwardAmountType=Units" if aq is None else "")
            # When UseLimit is set, it must equal AwardQuantity
            if ul is not None and aq is not None:
                rule(f"C2u.{i}", f"Award {i}: UseLimit matches AwardQuantity",
                     ul == aq,
                     f"UseLimit={ul} but AwardQuantity={aq}" if ul != aq else "")

    # C3/C4 — AwardType consistency
    for i, aw in enumerate(promo["awards"], 1):
        has_curr = bool(aw["currencies"])
        if aw["award_type"] == "PercentOff":
            rule(f"C3.{i}", f"Award {i} (PercentOff) → no AwardCurrencies",
                 not has_curr,
                 "AwardCurrencies present — should be absent for PercentOff" if has_curr else "")
        elif aw["award_type"] == "SetAmount":
            rule(f"C4.{i}", f"Award {i} (SetAmount) → AwardCurrencies non-empty",
                 has_curr,
                 "AwardCurrencies missing or empty" if not has_curr else "")

    # C5 — All DiscountAmount positive
    for i, aw in enumerate(promo["awards"], 1):
        for curr, amt in aw["currencies"].items():
            if amt <= 0:
                rule(f"C5.{i}.{curr}", f"Award {i} {curr}: DiscountAmount > 0",
                     False, f"DiscountAmount={amt}")

    # C6 — No duplicate PFIDs across awards
    seen, dups = set(), set()
    for aw in promo["awards"]:
        for pfid in aw["pfids"]:
            (dups if pfid in seen else seen).add(pfid)
    rule("C6", "No duplicate PFIDs across awards",
         not dups,
         f"Duplicate PFIDs: {sorted(dups)}" if dups else "")

    return results


# ─────────────────────────────────────────────────────────────────────────────
# DERIVE — learn patterns from corpus
# ─────────────────────────────────────────────────────────────────────────────

def cmd_derive():
    xml_files = sorted(GOLDEN_DIR.glob("*.xml"))
    if not xml_files:
        sys.exit("No XML files found in golden-set/")

    promos = []
    for f in xml_files:
        try:
            promos.append((f.stem, parse_promo(f)))
        except Exception as e:
            print(f"  [warn] Could not parse {f.name}: {e}", file=sys.stderr)

    n = len(promos)
    print(f"Deriving rules from {n} examples...")

    rules = {}

    def count(predicate):
        c = sum(1 for _, p in promos if predicate(p))
        return c, n, round(c / n, 3)

    # Universal structural rules
    for id_, desc, fn in [
        ("R1", "Conditions block is always empty",                     lambda p: p["conditions_empty"]),
        ("R2", "PrivateLabels always contains exactly PL1",            lambda p: p["private_label_ids"] == ["1"]),
        ("R3", "AwardAppliesTo always HighestPriceFirstMayOverlapConditions",
                                                                       lambda p: p["award_applies_to"] == "HighestPriceFirstMayOverlapConditions"),
        ("R4", "Name always equals Description",                       lambda p: p["name"] == p["description"]),
        ("R5", "No PFIDList block present",                            lambda p: not p["has_pfid_list"]),
    ]:
        sup, tot, conf = count(fn)
        rules[id_] = {"description": desc, "support": f"{sup}/{tot}", "confidence": conf}
        flag = "✅" if conf == 1.0 else ("⚠️" if conf >= 0.8 else "❌")
        print(f"  {flag} {id_}: {desc} — {sup}/{tot}")

    # Award-level patterns
    amt_types  = Counter(aw["amount_type"] for _, p in promos for aw in p["awards"])
    award_types = Counter(aw["award_type"]  for _, p in promos for aw in p["awards"])
    total_awards = sum(amt_types.values())

    rules["P_amt_type"] = {
        "description": "AwardAmountType distribution",
        "data": dict(amt_types),
        "total_awards": total_awards,
        "note": "Unlimited is the default; Units only for use-limit promos (goes with UseLimit=1)",
    }
    rules["P_award_type"] = {
        "description": "AwardType distribution",
        "data": dict(award_types),
        "total_awards": total_awards,
        "note": "SetAmount is the default; PercentOff used for fee waivers (no AwardCurrencies)",
    }
    print(f"  📊 AwardAmountType: {dict(amt_types)}")
    print(f"  📊 AwardType:       {dict(award_types)}")

    # Currency patterns
    currency_freq = Counter()
    for _, p in promos:
        for aw in p["awards"]:
            currency_freq.update(aw["currencies"].keys())

    usd_only_count = sum(
        1 for _, p in promos
        if all(set(aw["currencies"]) == {"USD"} for aw in p["awards"] if aw["currencies"])
        and any(aw["currencies"] for aw in p["awards"])
    )
    no_usd_count = sum(
        1 for _, p in promos
        if not any("USD" in aw["currencies"] for aw in p["awards"])
    )
    has_inr_count = sum(
        1 for _, p in promos
        if any("INR" in aw["currencies"] for aw in p["awards"])
    )

    rules["P_currencies"] = {
        "description": "Currency patterns across corpus",
        "frequency": {c: f"{v}/{n}" for c, v in currency_freq.most_common()},
        "usd_only_promos":  f"{usd_only_count}/{n}",
        "no_usd_promos":    f"{no_usd_count}/{n}",
        "has_inr_promos":   f"{has_inr_count}/{n}",
        "note": (
            "USD-only = US-market-only scope. "
            "No USD = ROW-only scope. "
            f"INR present in {has_inr_count}/{n} promos — global or IN-scope."
        ),
    }

    top_curr = currency_freq.most_common(10)
    print(f"  📊 Top currencies: {', '.join(f'{c}({v})' for c, v in top_curr)}")
    print(f"  📊 USD-only: {usd_only_count}/{n}  |  No-USD: {no_usd_count}/{n}  |  Has INR: {has_inr_count}/{n}")

    # Restriction patterns
    restrictions = Counter(p["restriction"] for _, p in promos)
    rules["P_restrictions"] = {
        "description": "Restriction field distribution",
        "data": dict(restrictions),
        "note": "NoRestriction is the default. Others indicate eligibility constraints.",
    }
    print(f"  📊 Restriction:     {dict(restrictions)}")

    output = {
        "corpus_size":  n,
        "derived_at":   datetime.now().strftime("%Y-%m-%d"),
        "corpus_files": [f.stem for f in xml_files],
        "rules":        rules,
    }
    DERIVED_FILE.write_text(json.dumps(output, indent=2))
    print(f"\nWrote {DERIVED_FILE}")
    print("Rule confidence: 1.0 = hard rule (enforce as FAIL), <1.0 = pattern (report as WARN)")


# ─────────────────────────────────────────────────────────────────────────────
# CHECK — lint a single XML
# ─────────────────────────────────────────────────────────────────────────────

def cmd_check(xml_path: str):
    path = Path(xml_path)
    if not path.exists():
        sys.exit(f"File not found: {xml_path}")

    promo = parse_promo(path)
    results = check_hard_rules(promo)

    # Load derived rules for pattern notes
    derived = {}
    if DERIVED_FILE.exists():
        derived = json.loads(DERIVED_FILE.read_text()).get("rules", {})

    print(f"\n{'─'*60}")
    print(f"LINT: {path.name}")
    print(f"{'─'*60}")

    fails = [r for r in results if r["status"] == "FAIL"]
    passes = [r for r in results if r["status"] == "PASS"]

    for r in results:
        icon = "✅" if r["status"] == "PASS" else "❌"
        print(f"  {icon} [{r['id']}] {r['description']}")
        if r["detail"]:
            for line in r["detail"].splitlines():
                print(f"       {line}")

    print(f"\n{'─'*60}")
    print(f"Tier 1+2: {len(passes)}/{len(results)} pass  |  {len(fails)} fail")

    if derived:
        corpus_n = json.loads(DERIVED_FILE.read_text()).get("corpus_size", "?")
        print(f"Derived rules from corpus of {corpus_n} examples.")

    if fails:
        print(f"\n⚠️  {len(fails)} issue(s) must be fixed before submission:")
        for r in fails:
            print(f"   • [{r['id']}] {r['description']}")
            if r["detail"]:
                print(f"     → {r['detail'].splitlines()[0]}")

    print()
    return len(fails)


# ─────────────────────────────────────────────────────────────────────────────
# COMPARE — diff generated vs expected
# ─────────────────────────────────────────────────────────────────────────────

def compare_promos(gen: dict, exp: dict) -> list:
    diffs = []

    def diff(field, gen_val, exp_val, tolerance=None):
        if tolerance and isinstance(gen_val, str) and isinstance(exp_val, str):
            # Date tolerance: allow ±1 day
            try:
                gd = datetime.fromisoformat(gen_val.replace("T00:00:00", ""))
                ed = datetime.fromisoformat(exp_val.replace("T00:00:00", ""))
                days_off = abs((gd - ed).days)
                if days_off == 0:
                    status = "MATCH"
                elif days_off == 1:
                    status = "WARN"
                else:
                    status = "MISMATCH"
                diffs.append({"field": field, "status": status,
                               "generated": gen_val, "expected": exp_val,
                               "note": f"Off by {days_off} day(s)"})
                return
            except Exception:
                pass
        status = "MATCH" if gen_val == exp_val else "MISMATCH"
        diffs.append({"field": field, "status": status,
                      "generated": str(gen_val), "expected": str(exp_val)})

    # Scalar fields
    diff("PromoCode",       gen["promo_code"],       exp["promo_code"])
    diff("StartDate",       gen["start_date"],        exp["start_date"],        tolerance="date")
    diff("ExpirationDate",  gen["expiration_date"],   exp["expiration_date"],   tolerance="date")
    diff("Name",            gen["name"],              exp["name"])
    diff("Description",     gen["description"],       exp["description"])
    diff("Rank",            gen["rank"],              exp["rank"])
    diff("Restriction",     gen["restriction"],       exp["restriction"])
    diff("UsageType",       gen["usage_type"],        exp["usage_type"])
    diff("NumberOfUses",    gen["number_of_uses"],    exp["number_of_uses"])

    # Structural
    diff("Conditions empty",      gen["conditions_empty"],    exp["conditions_empty"])
    diff("PrivateLabels PL1",     gen["private_label_ids"],   exp["private_label_ids"])
    diff("AwardAppliesTo",        gen["award_applies_to"],    exp["award_applies_to"])
    diff("PFIDList absent",       not gen["has_pfid_list"],   not exp["has_pfid_list"])

    # PFID sets
    gen_pfids = set(pfid for aw in gen["awards"] for pfid in aw["pfids"])
    exp_pfids = set(pfid for aw in exp["awards"] for pfid in aw["pfids"])
    missing = sorted(exp_pfids - gen_pfids)
    extra   = sorted(gen_pfids - exp_pfids)
    pfid_status = "MATCH" if not missing and not extra else "MISMATCH"
    note = []
    if missing: note.append(f"Missing {len(missing)} PFIDs: {missing[:5]}{'...' if len(missing) > 5 else ''}")
    if extra:   note.append(f"Extra {len(extra)} PFIDs: {extra[:5]}{'...' if len(extra) > 5 else ''}")
    diffs.append({"field": "PFID set", "status": pfid_status,
                  "generated": f"{len(gen_pfids)} PFIDs", "expected": f"{len(exp_pfids)} PFIDs",
                  "note": " | ".join(note) if note else ""})

    # Currency sets (union across all awards)
    gen_curr = set(c for aw in gen["awards"] for c in aw["currencies"])
    exp_curr = set(c for aw in exp["awards"] for c in aw["currencies"])
    missing_c = sorted(exp_curr - gen_curr)
    extra_c   = sorted(gen_curr - exp_curr)
    curr_status = "MATCH" if not missing_c and not extra_c else "MISMATCH"
    note = []
    if missing_c: note.append(f"Missing currencies: {missing_c}")
    if extra_c:   note.append(f"Extra currencies: {extra_c}")
    diffs.append({"field": "Currency set", "status": curr_status,
                  "generated": f"{sorted(gen_curr)}", "expected": f"{sorted(exp_curr)}",
                  "note": " | ".join(note) if note else ""})

    # USD amounts (per PFID)
    gen_usd = {}
    for aw in gen["awards"]:
        amt = aw["currencies"].get("USD")
        if amt is not None:
            for pfid in aw["pfids"]:
                gen_usd[pfid] = amt

    exp_usd = {}
    for aw in exp["awards"]:
        amt = aw["currencies"].get("USD")
        if amt is not None:
            for pfid in aw["pfids"]:
                exp_usd[pfid] = amt

    price_mismatches = []
    for pfid in sorted(set(gen_usd) & set(exp_usd)):
        if abs(gen_usd[pfid] - exp_usd[pfid]) > 0.01:
            price_mismatches.append(f"PFID {pfid}: gen=${gen_usd[pfid]:.2f} exp=${exp_usd[pfid]:.2f}")

    price_status = "MATCH" if not price_mismatches else "MISMATCH"
    diffs.append({"field": "USD amounts", "status": price_status,
                  "generated": "", "expected": "",
                  "note": "; ".join(price_mismatches) if price_mismatches else f"All {len(set(gen_usd) & set(exp_usd))} checked OK"})

    # Award count
    diff("Award row count", len(gen["awards"]), len(exp["awards"]))

    return diffs


def cmd_compare(gen_path: str, exp_path: str, save_report: bool = True):
    gp = Path(gen_path)
    ep = Path(exp_path)
    for p in [gp, ep]:
        if not p.exists():
            sys.exit(f"File not found: {p}")

    gen = parse_promo(gp)
    exp = parse_promo(ep)

    # Run structural lint first
    hard_results = check_hard_rules(gen)
    hard_fails = [r for r in hard_results if r["status"] == "FAIL"]

    diffs = compare_promos(gen, exp)

    print(f"\n{'═'*60}")
    print(f"COMPARE: {gp.name}  →  {ep.name}")
    print(f"{'═'*60}")

    # Structural results
    print(f"\n── Structural (hard rules) ─────────────────────────────")
    for r in hard_results:
        icon = "✅" if r["status"] == "PASS" else "❌"
        print(f"  {icon} [{r['id']}] {r['description']}")
        if r["detail"]:
            print(f"       {r['detail'].splitlines()[0]}")

    # Comparison results
    print(f"\n── Field comparison ────────────────────────────────────")
    icons = {"MATCH": "✅", "WARN": "⚠️", "MISMATCH": "❌"}
    for d in diffs:
        icon = icons.get(d["status"], "?")
        line = f"  {icon} {d['field']}"
        if d["status"] != "MATCH":
            if d["generated"] or d["expected"]:
                line += f"\n       gen: {d['generated']}\n       exp: {d['expected']}"
            if d.get("note"):
                line += f"\n       note: {d['note']}"
        elif d.get("note"):
            line += f"  ({d['note']})"
        print(line)

    mismatches = [d for d in diffs if d["status"] == "MISMATCH"]
    warns      = [d for d in diffs if d["status"] == "WARN"]

    print(f"\n{'─'*60}")
    print(f"Hard rules: {len(hard_results) - len(hard_fails)}/{len(hard_results)} pass  |  {len(hard_fails)} fail")
    print(f"Comparison: {len(diffs) - len(mismatches) - len(warns)}/{len(diffs)} match  |  {len(mismatches)} mismatch  |  {len(warns)} warn")
    print()

    # Save report
    if save_report:
        REPORTS_DIR.mkdir(exist_ok=True)
        report = {
            "timestamp":   datetime.now().isoformat(),
            "generated":   gp.name,
            "expected":    ep.name,
            "hard_fails":  hard_fails,
            "diffs":       diffs,
            "summary": {
                "hard_fail_count":  len(hard_fails),
                "mismatch_count":   len(mismatches),
                "warn_count":       len(warns),
            },
        }
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = REPORTS_DIR / f"compare_{gp.stem}_{ts}.json"
        report_path.write_text(json.dumps(report, indent=2))
        print(f"Report saved: {report_path}")

    return len(hard_fails) + len(mismatches)


# ─────────────────────────────────────────────────────────────────────────────
# REPORT — aggregate all comparison results
# ─────────────────────────────────────────────────────────────────────────────

def cmd_report():
    if not REPORTS_DIR.exists() or not list(REPORTS_DIR.glob("*.json")):
        print("No comparison reports found. Run `compare` first.")
        return

    report_files = sorted(REPORTS_DIR.glob("*.json"))
    print(f"\n{'═'*60}")
    print(f"AGGREGATE REPORT  ({len(report_files)} runs)")
    print(f"{'═'*60}\n")

    hard_fail_counts  = Counter()
    mismatch_counts   = Counter()
    total_hard_fails  = 0
    total_mismatches  = 0

    for f in report_files:
        data = json.loads(f.read_text())
        total_hard_fails += data["summary"]["hard_fail_count"]
        total_mismatches += data["summary"]["mismatch_count"]
        for r in data.get("hard_fails", []):
            hard_fail_counts[r["id"]] += 1
        for d in data.get("diffs", []):
            if d["status"] == "MISMATCH":
                mismatch_counts[d["field"]] += 1

    print(f"Total runs:              {len(report_files)}")
    print(f"Total hard rule fails:   {total_hard_fails}")
    print(f"Total field mismatches:  {total_mismatches}")

    if hard_fail_counts:
        print(f"\n── Most common hard rule failures ──────────────────────")
        for rule_id, count in hard_fail_counts.most_common():
            pct = round(100 * count / len(report_files))
            print(f"  {rule_id:8s}  {count:3d}/{len(report_files)} runs  ({pct}%)")

    if mismatch_counts:
        print(f"\n── Most common field mismatches ────────────────────────")
        for field, count in mismatch_counts.most_common():
            pct = round(100 * count / len(report_files))
            print(f"  {field:30s}  {count:3d}/{len(report_files)} runs  ({pct}%)")

    print()


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="pricing-xml-checker — structural checker and comparator for GoDaddy pricing promo XML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("derive", help="Scan golden-set/, update derived_rules.json")

    p_check = sub.add_parser("check", help="Check structural rules on a single XML")
    p_check.add_argument("xml", help="Path to generated XML file")

    p_compare = sub.add_parser("compare", help="Diff generated XML against expected XML")
    p_compare.add_argument("generated", help="Path to generated XML")
    p_compare.add_argument("expected",  help="Path to expected (source of truth) XML")
    p_compare.add_argument("--no-save", action="store_true", help="Don't save report to disk")

    sub.add_parser("report", help="Aggregate all stored comparison results")

    args = parser.parse_args()

    if args.command == "derive":
        cmd_derive()
    elif args.command == "check":
        sys.exit(min(cmd_check(args.xml), 1))
    elif args.command == "compare":
        sys.exit(min(cmd_compare(args.generated, args.expected, save_report=not args.no_save), 1))
    elif args.command == "report":
        cmd_report()


if __name__ == "__main__":
    main()
