#!/usr/bin/env python3
"""
catalog_chain.py — Fast catalog chain via direct MCP HTTP

Usage:
  python3 scrapers/catalog_chain.py <curatedOfferId>
  python3 scrapers/catalog_chain.py <id1> <id2> ...

  Single ID  → returns a single JSON object (backward compatible).
  Multiple IDs → returns a JSON array, one object per ID, fetched in parallel.

Stages (per ID):
  1. Initialize MCP HTTP session
  2. get_curated_offer → offerId (collection ID) + prePurchaseKeyMap component IDs
  3. get_offer_collection_definition (parallel with step 4)
  4. get_offer_definition_by_id × N for all prePurchaseKeyMap components (parallel)
  5. get_offer_definition_by_id × M for remaining collection members (parallel)

Output: flat JSON to stdout, timing to stderr.
  geometry field: "collection" when prePurchaseKeyMap.componentIds is non-empty, else "standalone".
"""

import sys
import json
import time
import ast
import concurrent.futures
import requests

BASE = "https://catalog-mcp.ecomm.int.test-gdcorp.tools/mcp/"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}

KNOWN_COMPONENTS = {
    "575a7d2a-d1ef-40f2-a7e5-dbcc09c20391": {"name": "M365 / Office 365", "tags": ["partneremail", "m365"]},
    "927a9d45-7c5b-4652-ad68-d5cd9be75028": {"name": "Titan Email", "tags": ["titanemail"]},
    "2468b30f-f448-4b21-a506-9c4103666f0d": {"name": "Professional Email", "tags": ["partneremail", "professional-email"]},
    "28e5b730-4e70-46b0-8672-6e18a17f81a1": {"name": "SSL Certificate", "tags": ["sslcert"]},
    "d29f7b62-9766-43bc-b230-353579eaad9c": {"name": "VPS4 Hosting", "tags": ["vps4", "virtualPrivateServerHostingV4"]},
    "05730877-89bd-49c0-8fff-c9880b743bf0": {"name": "cPanel Business Hosting", "tags": ["diablo"]},
    "d9e7bde4-7b28-49b3-b2fd-5dc528ab8062": {"name": "WAM / Websites & Marketing", "tags": ["wam", "wsb"]},
    "862a92dc-879f-4148-b43d-5c98898754c4": {"name": "WAM International", "tags": ["wsb", "wam"]},
    "edf13c43-7d39-4f90-aa81-b40666d51f75": {"name": "NewDomain", "tags": ["new-domain-offer"]},
    "2c5e3bb2-e6dc-4b13-855e-36b148cc98fd": {"name": "Duda", "tags": ["duda"]},
    "89973c51-aacd-49a7-bcf8-876ff0e425b8": {"name": "Smart Line", "tags": []},
    "566f8074-1510-4219-91e5-ff1f7c1dcf37": {"name": "WordPressOffer", "tags": ["wpaas"]},
    "72a57662-22d2-46c9-adb1-2da4663a6fed": {"name": "Norton", "tags": ["norton"]},
}


def _parse_mcp_response(text):
    """Parse MCP response, handling the known 'structured_content must be a dict' wrapper bug."""
    for line in text.split('\n'):
        if not line.startswith('data: '):
            continue
        d = json.loads(line[6:])
        content = d.get('result', {}).get('content', [])
        for item in content:
            raw = item.get('text', '')
            # Happy path: text is clean JSON
            try:
                inner = json.loads(raw)
                return inner[0] if isinstance(inner, list) else inner
            except (json.JSONDecodeError, ValueError):
                pass
            # Known MCP wrapper bug: data is a Python literal embedded in error string
            # "Error calling tool '...': structured_content must be a dict or None. Got list: [{...}]"
            marker = "Got list: "
            idx = raw.find(marker)
            if idx != -1:
                literal = raw[idx + len(marker):]
                # Strip trailing MCP wrapper message: "]. Tools should wrap non-dict values..."
                # Find the last ']' which closes the outer list
                last_bracket = literal.rfind(']')
                if last_bracket != -1:
                    literal = literal[:last_bracket + 1]
                try:
                    parsed = ast.literal_eval(literal)
                    return parsed[0] if isinstance(parsed, list) else parsed
                except (ValueError, SyntaxError):
                    pass
    return None


def mcp_tool_call(session_id, name, arguments, call_id):
    r = requests.post(BASE,
        headers={**HEADERS, "mcp-session-id": session_id},
        data=json.dumps({"jsonrpc": "2.0", "id": call_id, "method": "tools/call",
                          "params": {"name": name, "arguments": arguments}}),
        timeout=30)
    r.raise_for_status()
    return _parse_mcp_response(r.text)


def init_session():
    r = requests.post(BASE, headers=HEADERS, data=json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "catalog-chain", "version": "1.0"}}
    }), timeout=15)
    r.raise_for_status()
    session_id = r.headers.get("mcp-session-id")
    # send initialized notification (fire-and-forget)
    requests.post(BASE,
        headers={**HEADERS, "mcp-session-id": session_id},
        data=json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}),
        timeout=10)
    return session_id


def run_chain(curated_offer_id):
    t0 = time.time()
    timings = {}

    # Stage 1: init + get_curated_offer (sequential dependency)
    session_id = init_session()
    timings['init'] = time.time() - t0
    print(f"[{timings['init']:.2f}s] session initialized", file=sys.stderr)

    t1 = time.time()
    curated = mcp_tool_call(session_id, "get_curated_offer",
        {"datasource": "catalog-curated-offers", "curatedOfferId": curated_offer_id}, 2)
    if not curated or curated.get('code') == 'NOT_FOUND' or 'offerId' not in curated:
        return {"curatedOfferId": curated_offer_id, "error": "not_found"}
    timings['curated_offer'] = time.time() - t1

    collection_id = curated['offerId']
    prepurchase_offers = curated.get('prePurchaseKeyMap', {}).get('offers', [])
    prepurchase_component_ids = [o['offerId'] for o in prepurchase_offers]
    prepurchase_component_plans = {o['offerId']: o.get('plan') for o in prepurchase_offers}
    print(f"[{time.time()-t0:.2f}s] curated_offer ({timings['curated_offer']:.2f}s) "
          f"| offerId={collection_id[:8]}... | prePurchase components={len(prepurchase_component_ids)}",
          file=sys.stderr)

    # Stage 2+3: collection def + prePurchase component defs in parallel
    # Known components are resolved from the cache; only unknown ones make API calls.
    cached_prepurchase = [oid for oid in prepurchase_component_ids if oid in KNOWN_COMPONENTS]
    unknown_prepurchase = [oid for oid in prepurchase_component_ids if oid not in KNOWN_COMPONENTS]
    t2 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        coll_fut = ex.submit(mcp_tool_call, session_id, "get_offer_collection_definition",
                             {"datasource": "catalog-offers", "offerCollectionId": collection_id}, 10)
        comp_futs = {
            oid: ex.submit(mcp_tool_call, session_id, "get_offer_definition_by_id",
                           {"datasource": "catalog-offers", "offerId": oid}, 20 + i)
            for i, oid in enumerate(unknown_prepurchase)
        }
        collection = coll_fut.result()
        prepurchase_components = {
            **{oid: KNOWN_COMPONENTS[oid] for oid in cached_prepurchase},
            **{oid: f.result() for oid, f in comp_futs.items()},
        }
    timings['collection_and_components'] = time.time() - t2

    if not collection:
        raise RuntimeError(f"get_offer_collection_definition returned None for: {collection_id}")

    all_member_ids = [o['offerId'] for o in collection.get('offers', [])]
    remaining_ids = [oid for oid in all_member_ids if oid not in prepurchase_component_ids]
    print(f"[{time.time()-t0:.2f}s] collection_def + {len(prepurchase_component_ids)} prePurchase "
          f"({len(cached_prepurchase)} cached, {len(unknown_prepurchase)} fetched) "
          f"({timings['collection_and_components']:.2f}s) | {len(remaining_ids)} remaining members",
          file=sys.stderr)

    # Stage 4: remaining collection members in parallel
    # Known components resolved from cache; only unknown ones make API calls.
    cached_remaining = [oid for oid in remaining_ids if oid in KNOWN_COMPONENTS]
    unknown_remaining = [oid for oid in remaining_ids if oid not in KNOWN_COMPONENTS]
    t3 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        extra_futs = {
            oid: ex.submit(mcp_tool_call, session_id, "get_offer_definition_by_id",
                           {"datasource": "catalog-offers", "offerId": oid}, 50 + i)
            for i, oid in enumerate(unknown_remaining)
        }
        extra_offers = {
            **{oid: KNOWN_COMPONENTS[oid] for oid in cached_remaining},
            **{oid: f.result() for oid, f in extra_futs.items()},
        }
    timings['remaining_members'] = time.time() - t3
    print(f"[{time.time()-t0:.2f}s] {len(remaining_ids)} remaining members "
          f"({len(cached_remaining)} cached, {len(unknown_remaining)} fetched) "
          f"({timings['remaining_members']:.2f}s)", file=sys.stderr)

    timings['total'] = time.time() - t0

    # Assemble flat output
    def offer_summary(oid, plan=None):
        d = prepurchase_components.get(oid) or extra_offers.get(oid)
        if not d:
            return {"offerId": oid, "name": None, "plan": plan, "plans": None, "tags": None, "error": "fetch_failed"}
        return {
            "offerId": oid,
            "name": d.get('name'),
            "plan": plan,
            "plans": d.get('plans'),
            "tags": d.get('tags', []),
        }

    geometry = "collection" if prepurchase_component_ids else "standalone"

    result = {
        "curatedOfferId": curated_offer_id,
        "geometry": geometry,
        "plan": curated.get('plan'),
        "active": curated.get('active'),
        "revisionNumber": curated.get('revisionNumber'),
        "configKeyValues": curated.get('configKeyValues'),
        "discountCodes": curated.get('discountCodes', []),
        "quantityByOfferKey": curated.get('prePurchaseKeyMap', {}).get('quantityByOfferKey'),
        "offerCollectionId": collection_id,
        "collection": {
            "name": collection.get('name'),
            "status": collection.get('status'),
            "revisionNumber": collection.get('revisionNumber'),
            "schema": collection.get('schema'),
            "offers": all_member_ids,
        },
        "prePurchaseKeyMap": {
            "componentIds": prepurchase_component_ids,
            "components": [offer_summary(oid, plan=prepurchase_component_plans.get(oid)) for oid in prepurchase_component_ids],
        },
        "collectionMembers": [offer_summary(oid) for oid in all_member_ids],
        "timings": timings,
    }

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scrapers/catalog_chain.py <curatedOfferId> [<id2> ...]", file=sys.stderr)
        sys.exit(1)

    ids = sys.argv[1:]

    if len(ids) == 1:
        # Single-ID path — backward-compatible: output a single JSON object
        try:
            result = run_chain(ids[0])
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Multi-ID path — run each ID in parallel, output a JSON array
        def _run_safe(cid):
            try:
                return run_chain(cid)
            except Exception as e:
                print(f"ERROR [{cid}]: {e}", file=sys.stderr)
                return {"curatedOfferId": cid, "error": str(e)}

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(ids)) as ex:
            ordered_futures = [ex.submit(_run_safe, cid) for cid in ids]
            results = [f.result() for f in ordered_futures]

        print(json.dumps(results, indent=2))
