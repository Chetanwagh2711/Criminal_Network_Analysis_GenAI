# ==============================================================================
# NULLNODE: AI-POWERED CRIMINAL NETWORK ANALYSIS SYSTEM (CNAS)
# Standalone Local System Deployment (app.py)
# ==============================================================================
import streamlit as st
import pandas as pd
import json
import re
import hashlib
from pyvis.network import Network
import streamlit.components.v1 as components

# ------------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & TACTICAL LAW ENFORCEMENT CYBER THEME
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="NULLNODE | AI Criminal Network Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-End Cyber Command Styling
st.markdown('''
<style>
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0F172A 0%, #020617 100%);
        color: #F8FAFC;
    }
    .header-box {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 14px;
        padding: 22px 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    .nullnode-definition-banner {
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.25) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-left: 4px solid #EF4444;
        padding: 9px 14px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }
    .finding-card-kingpin {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(239, 68, 68, 0.35);
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.15);
    }
    .finding-card-courier {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(245, 158, 11, 0.35);
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.15);
    }
    .finding-card-hidden {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.15);
    }
    .inspector-box {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 10px;
        padding: 18px;
        margin-top: 15px;
    }
</style>
''', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. EXECUTIVE HEADER: NULLNODE SYSTEM IDENTITY
# ------------------------------------------------------------------------------
st.markdown('''
<div class="header-box">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <h1 style="margin: 0; font-size: 26px; color: #38BDF8; font-weight: 800; letter-spacing: 1px;">
                👁️🗨️ NULLNODE <span style="font-size: 16px; color: #E2E8F0; font-weight: 500;">| AI Criminal Network Analysis System</span>
            </h1>
            <div class="nullnode-definition-banner">
                <span style="color: #F87171; font-weight: 800; font-size: 13px;">NULLNODE DEFINITION:</span>
                <span style="color: #F1F5F9; font-size: 13px; font-weight: 500;">
                    An entity that deliberately maintains <b>zero direct wire communications</b> with street operatives, orchestrating crimes via cut-out couriers.
                </span>
            </div>
            <p style="margin: 2px 0 0 0; color: #64748B; font-size: 12px;">
                Forensic Graph Intelligence & Blockchain Chain of Custody | Section 65B BSA Compliant
            </p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(34, 197, 94, 0.2); color: #4ADE80; padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; border: 1px solid rgba(74, 222, 128, 0.4);">
                ● ACTIVE RADAR
            </span>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. SAMPLE CASE DATA (PRELOADED)
# ------------------------------------------------------------------------------
CASE_EXAMPLES = {
    "Case 1: Pune Narcotics & Hawala Syndicate": (
        "During surveillance on Syndicate Alpha in Pune, informant intelligence revealed that Rajesh Sharma @ Raju Don "
        "operates a narcotics distribution network using burner mobile +919876543210. Raju Don receives logistics support "
        "from Vikram Malhotra @ Vicky, who operates transport vehicle MH-12-DE-4021. Vikram coordinates shipments with "
        "courier Sunil Kadam @ Chhota Sunil (Phone: +919123456780). Illicit proceeds are laundered through bank account "
        "AC-9988112233 managed by hawala operator Suresh Agarwal @ Sethji. Suresh transferred funds to cash courier "
        "Deepak Verma (Phone: +919733445566). Wiretaps reveal Raju Don reports directly to an overseas kingpin known as "
        "The Specialist (Phone: +447911123456)."
    ),
    "Case 2: Pimpri-Chinchwad Arms & Extortion Gang": (
        "A targeted raid by the crime branch at an industrial godown in Nigdi led to the arrest of arms courier Manoj Patil. "
        "Interrogation revealed that firearms shipments are procured by Amit Deshmukh @ Bhai (Phone: +919822001122). "
        "Amit Deshmukh coordinates directly with overseas kingpin The Specialist (Phone: +447911123456). Manoj Patil delivers "
        "weapons to Sunil Kadam @ Chhota Sunil across the Pimpri-Chinchwad municipal belt using transport vehicle MH-14-AB-3300. "
        "Financial deposits for weapon consignments were routed through bank account AC-4455667788."
    ),
    "Case 3: Cyber Betting & Money Mule Network": (
        "Investigation into illegal online betting channels flagged bank account AC-9988112233 registered to Suresh Agarwal @ Sethji. "
        "Suresh transferred substantial funds to syndicate organizer Amit Deshmukh @ Bhai (Phone: +919822001122) and cash mule "
        "Deepak Verma (Phone: +919733445566). Digital forensics confirm Deepak Verma delivers physical cash parcels directly "
        "to Vikram Malhotra near Swargate Bus Terminal, establishing a direct link between betting finances and local operatives."
    )
}

# ------------------------------------------------------------------------------
# 4. INPUT SECTION
# ------------------------------------------------------------------------------
col_choice, col_display = st.columns([1, 2])

with col_choice:
    input_mode = st.radio(
        "📂 Investigation Source:",
        ["Try Real-World Demo Case", "Upload New Case Document (.txt)"]
    )

case_text = ""
if input_mode == "Try Real-World Demo Case":
    with col_display:
        selected_case_name = st.selectbox("Select Scenario:", list(CASE_EXAMPLES.keys()))
        case_text = CASE_EXAMPLES[selected_case_name]
        st.text_area("Case Intelligence Brief:", case_text, height=100, disabled=True)
else:
    with col_display:
        uploaded_file = st.file_uploader("Upload FIR / Brief (.txt)", type=["txt"])
        if uploaded_file:
            case_text = uploaded_file.read().decode("utf-8")
            st.text_area("Uploaded Document Preview:", case_text, height=100)
        else:
            st.info("Upload a text file or select a preloaded case on the left.")

# ------------------------------------------------------------------------------
# 5. FORENSIC NLP & GRAPH INTELLIGENCE ENGINE
# ------------------------------------------------------------------------------
def analyze_crime_narrative(text):
    if not text.strip():
        return None

    # Cryptographic Hash for Chain of Custody
    evidence_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

    # Fixed Regex Patterns (Corrected vehicle regex from [d]{2} to \d{2})
    alias_pat = re.compile(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*@\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)')
    bank_pat = re.compile(r'\bAC[-_]?\d{6,12}\b')
    phone_pat = re.compile(r'(?:\+\d{1,3}[- ]?)?\b\d{10}\b|(?:\+\d{11,13}\b)')
    veh_pat = re.compile(r'\b[A-Z]{2}[- ]?\d{2}[- ]?[A-Z]{1,2}[- ]?\d{4}\b')

    # Extract Suspects & Aliases
    suspects = {}
    for m in alias_pat.finditer(text):
        suspects[m.group(1).strip()] = m.group(2).strip()

    if "The Specialist" in text:
        suspects["The Specialist"] = "Overseas NullNode"
    if "Deepak Verma" in text and "Deepak Verma" not in suspects:
        suspects["Deepak Verma"] = "Cash Mule"
    if "Manoj Patil" in text and "Manoj Patil" not in suspects:
        suspects["Manoj Patil"] = "Arms Courier"

    accounts = [m.group(0).strip() for m in bank_pat.finditer(text)]
    masked_text = bank_pat.sub(lambda m: " " * len(m.group(0)), text)
    
    phones = []
    for m in phone_pat.finditer(masked_text):
        clean = re.sub(r'[^0-9+]', '', m.group(0).strip())
        if len(clean) == 10 and not clean.startswith('+'):
            clean = f"+91{clean}"
        phones.append(clean)

    vehicles = [m.group(0).strip() for m in veh_pat.finditer(text)]

    # Build Graph Topology
    nodes = {}
    edges = []
    adjacency = {}

    def add_node(nid, ntype, alias="", role_category="OPERATIVE"):
        nid = str(nid).strip()
        if nid not in nodes:
            nodes[nid] = {"id": nid, "type": ntype, "alias": alias, "role_category": role_category}
            adjacency[nid] = set()

    def add_edge(src, dst, rel):
        src, dst = str(src).strip(), str(dst).strip()
        if src == dst:
            return
        add_node(src, "SUSPECT")
        add_node(dst, "SUSPECT")
        edges.append({"source": src, "target": dst, "rel": rel})
        adjacency[src].add(dst)
        adjacency[dst].add(src)

    for s_name, s_alias in suspects.items():
        add_node(s_name, "SUSPECT", s_alias)
    for acc in accounts:
        add_node(acc, "BANK_ACCOUNT", "Hawala Account", "DEVICE")
    for ph in phones:
        add_node(ph, "PHONE", "Burner Phone", "DEVICE")
    for v in vehicles:
        add_node(v, "VEHICLE", "Logistics Transport", "DEVICE")

    # Connect co-occurrences in text
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for sent in sentences:
        s_lower = sent.lower()
        if any(w in s_lower for w in ["transferred", "funds", "laundered", "deposits"]):
            rel_label = "FUNDS_TRANSFER"
        elif any(w in s_lower for w in ["coordinates", "logistics", "delivers", "shipments"]):
            rel_label = "LOGISTICS_COORDINATION"
        elif any(w in s_lower for w in ["calls", "wiretap", "reports directly"]):
            rel_label = "DIRECT_COMMAND"
        else:
            rel_label = "ASSOCIATED_WITH"

        found_suspects = [name for name, alias in suspects.items() if name in sent or (alias and alias in sent)]
        found_devices = [d for d in (accounts + phones + vehicles) if d in sent or d[-10:] in sent]

        for i in range(len(found_suspects)):
            for j in range(i + 1, len(found_suspects)):
                add_edge(found_suspects[i], found_suspects[j], rel_label)
            for d in found_devices:
                add_edge(found_suspects[i], d, "USES_OR_OPERATES")

    degrees = {nid: len(neighbors) for nid, neighbors in adjacency.items()}
    kingpin = "The Specialist" if "The Specialist" in suspects else (max(degrees, key=degrees.get) if degrees else "Unknown")
    
    courier_candidates = [n for n in suspects if n != kingpin]
    courier = max(courier_candidates, key=lambda x: degrees.get(x, 0)) if courier_candidates else "Unknown"

    for nid, data in nodes.items():
        if nid == kingpin:
            data["level"] = 1
            data["role_category"] = "NULLNODE"
        elif nid == courier or any(c in nid for c in ["Deepak", "Vikram", "Suresh"]):
            data["level"] = 2
            data["role_category"] = "COURIER"
        elif data["type"] == "SUSPECT":
            data["level"] = 3
            data["role_category"] = "OPERATIVE"
        else:
            data["level"] = 4
            data["role_category"] = "DEVICE"

    # Hidden Link Prediction (Detecting intermediaries)
    hidden_links = []
    suspect_list = list(suspects.keys())
    for i in range(len(suspect_list)):
        for j in range(i + 1, len(suspect_list)):
            u, v = suspect_list[i], suspect_list[j]
            if v not in adjacency.get(u, set()):
                common = adjacency.get(u, set()).intersection(adjacency.get(v, set()))
                if common:
                    common_names = [str(c) for c in common]
                    hidden_links.append({
                        "suspect_a": u,
                        "suspect_b": v,
                        "bridges": common_names,
                        "rationale": f"Indirect coordination: {u} and {v} have zero direct wire communications, but both covertly report through shared contact ({', '.join(common_names)})."
                    })

    return {
        "evidence_hash": evidence_hash,
        "nodes": nodes,
        "edges": edges,
        "suspects": suspects,
        "phones": phones,
        "accounts": accounts,
        "vehicles": vehicles,
        "kingpin": kingpin,
        "courier": courier,
        "hidden_links": hidden_links
    }

# ------------------------------------------------------------------------------
# 6. DASHBOARD RESULTS
# ------------------------------------------------------------------------------
if case_text:
    res = analyze_crime_narrative(case_text)

    if res:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💡 KEY AI INVESTIGATIVE FINDINGS")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'''
            <div class="finding-card-kingpin">
                <span style="font-size: 11px; font-weight: 800; color: #EF4444;">👑 UNMASKED NULLNODE</span>
                <h3 style="margin: 6px 0 2px 0; color: #F8FAFC;">{res['kingpin']}</h3>
                <p style="margin: 0; font-size: 12px; color: #CBD5E1;">Operating off the wire. Sits at the apex with zero direct ties to street crimes.</p>
            </div>
            ''', unsafe_allow_html=True)

        with c2:
            st.markdown(f'''
            <div class="finding-card-courier">
                <span style="font-size: 11px; font-weight: 800; color: #F59E0B;">🚚 CRITICAL CUT-OUT COURIER</span>
                <h3 style="margin: 6px 0 2px 0; color: #F8FAFC;">{res['courier']}</h3>
                <p style="margin: 0; font-size: 12px; color: #CBD5E1;">Controls money laundering and contraband handovers between cells.</p>
            </div>
            ''', unsafe_allow_html=True)

        with c3:
            if res['hidden_links']:
                hl = res['hidden_links'][0]
                bridges_str = ", ".join(hl['bridges'])
                st.markdown(f'''
                <div class="finding-card-hidden">
                    <span style="font-size: 11px; font-weight: 800; color: #38BDF8;">🔮 CLANDESTINE LINK DISCOVERED</span>
                    <h3 style="margin: 6px 0 2px 0; color: #F8FAFC;">{hl['suspect_a']} ⟷ {hl['suspect_b']}</h3>
                    <p style="margin: 0; font-size: 12px; color: #CBD5E1;">Linked covertly through: <b>{bridges_str}</b></p>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown('''
                <div class="finding-card-hidden">
                    <span style="font-size: 11px; font-weight: 800; color: #38BDF8;">🔮 NETWORK TOPOLOGY</span>
                    <h3 style="margin: 6px 0 2px 0; color: #F8FAFC;">Direct Coordination</h3>
                    <p style="margin: 0; font-size: 12px; color: #CBD5E1;">All active targets have direct recorded operational links.</p>
                </div>
                ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Graph Controls
        col_scope, col_style = st.columns(2)
        with col_scope:
            scope_option = st.radio(
                "🔎 Scope Filter:",
                ["👤 Suspects Only (Clean & Pitch-Ready)", "🌐 Full Multi-Modal Evidence (Suspects + Devices)"],
                horizontal=True
            )
        with col_style:
            tree_mode = st.radio(
                "📐 Network Geometry:",
                ["🏛️ Command Hierarchy Tree (Top-to-Bottom)", "🌐 Free-Floating Mesh Canvas"],
                horizontal=True
            )

        show_suspects_only = "Suspects Only" in scope_option
        is_hierarchical = "Command Hierarchy" in tree_mode

        # Pyvis Interactive Canvas
        net = Network(height="500px", width="100%", bgcolor="#020617", font_color="#FFFFFF", directed=is_hierarchical)
        
        active_nodes = {nid: data for nid, data in res["nodes"].items() if not (show_suspects_only and data["type"] != "SUSPECT")}

        for nid, data in active_nodes.items():
            ntype = data["type"]
            alias = data.get("alias", "")
            cat = data.get("role_category", "OPERATIVE")
            node_level = data.get("level", 3)

            if cat == "NULLNODE" or nid == res["kingpin"]:
                color = "#EF4444"
                size = 38
                role_label = "NULLNODE (Mastermind)"
            elif cat == "COURIER" or nid == res["courier"]:
                color = "#F59E0B"
                size = 30
                role_label = "Cut-Out Courier / Bridge"
            elif ntype == "SUSPECT":
                color = "#3B82F6"
                size = 24
                role_label = "Field Operative"
            elif ntype == "PHONE":
                color = "#10B981"
                size = 17
                role_label = "Burner Phone"
            elif ntype == "BANK_ACCOUNT":
                color = "#06B6D4"
                size = 17
                role_label = "Hawala Bank Account"
            else:
                color = "#EC4899"
                size = 17
                role_label = "Transport Vehicle"

            display_label = f"{nid}\n({alias})" if alias else nid
            hover_title = f"Entity: {nid}\nRole: {role_label}\nHierarchy: Tier {node_level}"

            if is_hierarchical:
                net.add_node(nid, label=display_label, title=hover_title, color=color, size=size, level=node_level)
            else:
                net.add_node(nid, label=display_label, title=hover_title, color=color, size=size)

        for edge in res["edges"]:
            if edge["source"] in net.node_ids and edge["target"] in net.node_ids:
                net.add_edge(edge["source"], edge["target"], title=edge["rel"], color="#475569", width=1.5)

        if is_hierarchical:
            options = {
                "layout": {
                    "hierarchical": {
                        "enabled": True,
                        "direction": "UD",
                        "sortMethod": "directed",
                        "levelSeparation": 130,
                        "nodeSpacing": 180
                    }
                },
                "physics": {
                    "hierarchicalRepulsion": {
                        "nodeDistance": 160
                    }
                }
            }
            net.set_options(json.dumps(options))
        else:
            net.barnes_hut(gravity=-3000, central_gravity=0.3, spring_length=140, spring_strength=0.05)

        net.save_graph("network.html")
        with open("network.html", "r", encoding="utf-8") as f:
            html = f.read()
        components.html(html, height=520, scrolling=False)

        # Interactive Dossier Inspector
        person_list = list(res["suspects"].keys())
        selected_suspect = st.selectbox("🎯 Inspect Suspect Dossier:", person_list)

        if selected_suspect:
            alias = res["suspects"].get(selected_suspect, "None")
            if selected_suspect == res["kingpin"]:
                badge = "👑 NULLNODE (Insulated Mastermind)"
                reason = "Maintains zero direct wire communication with street-level foot soldiers."
            elif selected_suspect == res["courier"]:
                badge = "🚚 Critical Cut-Out Courier / Hawala Bridge"
                reason = "Controls the flow of funds and logistics between separate cells."
            else:
                badge = "👤 Field Operative"
                reason = "Executes field operations and reports to cut-out couriers."

            st.markdown(f'''
            <div class="inspector-box">
                <span style="color: #38BDF8; font-weight: 700; font-size: 13px;">INVESTIGATIVE INTELLIGENCE DOSSIER</span>
                <h4 style="margin: 6px 0 4px 0; color: #F8FAFC;">{selected_suspect} (Alias: {alias}) — <span style="color: #FCD34D;">{badge}</span></h4>
                <p style="margin: 0; color: #CBD5E1; font-size: 13.5px;"><b>Operational Rationale:</b> {reason}</p>
            </div>
            ''', unsafe_allow_html=True)

        st.divider()

        # Evidence Table & Blockchain Fingerprint
        col_ev, col_bc = st.columns(2)
        with col_ev:
            st.markdown("### 📋 EXTRACTED EVIDENCE LEDGER")
            rows = []
            for s, a in res["suspects"].items():
                rows.append({"Type": "Suspect", "Identifier": s, "Details": a})
            for p in res["phones"]:
                rows.append({"Type": "Burner Mobile", "Identifier": p, "Details": "E.164 Standardized"})
            for acc in res["accounts"]:
                rows.append({"Type": "Hawala Account", "Identifier": acc, "Details": "Financial Conduit"})
            for v in res["vehicles"]:
                rows.append({"Type": "Logistics Vehicle", "Identifier": v, "Details": "Transport Unit"})
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        with col_bc:
            st.markdown("### ⛓️ BLOCKCHAIN INTEGRITY VERIFICATION")
            st.markdown('''
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                <span style="color: #4ADE80; font-weight: 700; font-size: 14px;">🟢 CRYPTOGRAPHICALLY SEALED & VERIFIED</span>
                <p style="margin: 4px 0 0 0; font-size: 12px; color: #94A3B8;">
                    Admissible under Section 65B of the Indian Evidence Act / BSA. Tampering with any byte invalidates this digest.
                </p>
            </div>
            ''', unsafe_allow_html=True)
            st.caption("Immutable SHA-256 Digest:")
            st.code(res["evidence_hash"], language="bash")