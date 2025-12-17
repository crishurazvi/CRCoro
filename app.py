import streamlit as st
from datetime import datetime

# ==========================================
# 1. SETUP & CSS MAGIC (THE CORE OF MODERN UI)
# ==========================================
st.set_page_config(
    page_title="CardioReport Pro | Intervențional",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed" # Ascundem sidebar-ul nativ pentru un look full-screen
)

# --- CSS AVANSAT ---
st.markdown("""
    <style>
    /* IMPORT FONT CLINIC */
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
        background-color: #f4f6f9; /* Gri clinic deschis */
        color: #1e293b;
    }

    /* ELIMINARE PADDING STUPID STREAMLIT */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95% !important;
    }

    /* CARDURI CUSTOM (Containere) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid #e2e8f0;
        padding: 20px;
        margin-bottom: 1rem;
    }

    /* INPUTURI MODERNE */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        height: 45px;
        color: #334155;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }

    /* TABS REINVENTATE */
    .stTabs [data-baseweb="tab-list"] {
        background-color: white;
        padding: 10px;
        border-radius: 12px;
        gap: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
        padding: 8px 16px;
        border: none;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #eff6ff;
        color: #2563eb; /* Albastru puternic */
    }

    /* LIVE PREVIEW PAPER EFFECT */
    .paper-preview {
        background-color: white;
        padding: 40px;
        min-height: 800px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        font-family: 'Times New Roman', serif;
        font-size: 14px;
        line-height: 1.6;
        color: #000;
    }
    
    /* CAPTION STYLING */
    .section-header {
        color: #64748b;
        font-size: 0.85rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 10px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- STATE ---
if 'pci_events' not in st.session_state:
    st.session_state.pci_events = []

# ==========================================
# 2. LOGICĂ DE GENERARE RAPORT (Backend)
# ==========================================
def get_report_text(data, lesions, pci_list):
    # Această funcție construiește textul brut pentru afișare
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    lines = []
    lines.append(f"SPITALUL CLINIC DE URGENȚĂ | LABORATOR DE CATETERISM")
    lines.append(f"RAPORT DE PROCEDURĂ INTERVENȚIONALĂ")
    lines.append("-" * 60)
    lines.append(f"PACIENT: {data['nume'].upper()} | Vârstă: {data['varsta']} ani | FO: {data['fo']}")
    lines.append(f"CNP: {data.get('cnp', '-')}")
    lines.append(f"DATA: {data['data'].strftime('%d/%m/%Y')} | OPERATOR: {data['op1']}")
    lines.append(f"OPERATOR SECUNDAR: {data['op2']}")
    lines.append("-" * 60)
    
    lines.append("\n1. DATE CLINICE & INDICAȚIE")
    lines.append(f"   Diagnostic: {data['indicatie']}")
    lines.append(f"   Factori de Risc: {', '.join(data['risc']) if data['risc'] else 'Fără factori majori'}")
    
    lines.append("\n2. DATE TEHNICE")
    lines.append(f"   Abord: {data['abord']} ({data['teaca']})")
    lines.append(f"   Contrast: {data['contrast']} ml (Visipaque)")
    lines.append(f"   Fluoroscopie: {data['scopie']} min | Doză (DAP): {data['dap']} Gy.cm2")
    lines.append(f"   Hemodinamica: Ao {data['ao']}, LVEDP {data['lvedp']} mmHg")
    
    lines.append(f"\n3. DESCRIERE ANGIOGRAFICĂ ({data['dominanta']})")
    if not lesions:
        lines.append("   Coronare epicardice permeabile, fără leziuni semnificative angiografic.")
    else:
        for k, v in lesions.items():
            lines.append(f"   • {k}: {v}")
            
    if pci_list:
        lines.append("\n4. ANGIOPLASTIE (PCI)")
        for item in pci_list:
            lines.append(f"   [{item['time']}] {item['artera']}: {item['text']}")
    
    lines.append("\n5. CONCLUZII")
    lines.append(f"   {data['concluzii']}")
    
    lines.append("\n6. RECOMANDĂRI")
    lines.append(f"   {data['recomandari']}")
    lines.append(f"   Tratament: {data['rx']}")
    
    return "\n".join(lines)

# ==========================================
# 3. LAYOUT PRINCIPAL (Split View)
# ==========================================

# HEADER ZONA SUPERIOARĂ
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("### 🩺 CardioReport **Pro**")
    st.caption("Sistem avansat de raportare angiografică")
with col_h2:
    st.markdown(f"🗓️ **{datetime.now().strftime('%d %b %Y')}**")

st.divider()

# SPLIT SCREEN
main_col_left, main_col_right = st.columns([1.3, 1]) 

# >>>>>>>>>>>> ZONA DE EDITOR (STÂNGA) <<<<<<<<<<<<
with main_col_left:
    
    # Navigare prin Tabs
    tab_pat, tab_anat, tab_pci, tab_concl = st.tabs([
        "👤 Pacient & Tehnic", 
        "🫀 Anatomie", 
        "💉 Angioplastie", 
        "📝 Finalizare"
    ])

    # --- TAB 1: PACIENT & TEHNIC ---
    with tab_pat:
        with st.container(border=True):
            st.markdown('<p class="section-header">Date Demografice</p>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            nume = c1.text_input("Nume Pacient", placeholder="ex. POPESCU ION")
            cnp = c2.text_input("CNP", placeholder="Optional")
            
            c3, c4, c5 = st.columns(3)
            varsta = c3.number_input("Vârstă", 18, 100, 60)
            fo = c4.text_input("Nr. FO", placeholder="12345/2024")
            data_proc = c5.date_input("Data", datetime.today())

            st.markdown('<p class="section-header">Echipa & Risc</p>', unsafe_allow_html=True)
            op1 = st.selectbox("Operator Principal", ["Dr. CRISAN", "Dr. OLARIU", "Dr. ZUS", "Rezident"])
            op2 = st.text_input("Operator Secundar", placeholder="Asistent / Rezident")
            
            risc = st.multiselect("Factori Risc", ["HTA", "DZ", "Fumat", "Dislipidemie", "Obezitate"], ["HTA"])
            indicatie = st.selectbox("Indicație", ["Angina Stabila", "Sdr. Coronarian Acut", "STEMI", "NSTEMI", "Control"])

        with st.container(border=True):
            st.markdown('<p class="section-header">Parametri Procedurali</p>', unsafe_allow_html=True)
            tc1, tc2, tc3 = st.columns(3)
            abord = tc1.selectbox("Abord", ["Radial Dr.", "Radial Stg.", "Femural Dr."], index=0)
            teaca = tc2.selectbox("Teaca", ["5F", "6F", "7F"], index=1)
            contrast = tc3.number_input("Contrast (ml)", 50, 500, 100, 10)
            
            tc4, tc5, tc6 = st.columns(3)
            scopie = tc4.number_input("Scopie (min)", 0.0, 100.0, 4.5)
            dap = tc5.number_input("DAP (Gy)", 0.0, 500.0, 35.0)
            ao = tc6.text_input("TA Ao", "130/80")
            lvedp = st.text_input("LVEDP", "8") # Hidden logic simplificata

    # --- TAB 2: ANATOMIE ---
    lesion_dict = {} # Stocăm leziunile aici local pentru a fi regenerate
    with tab_anat:
        st.info("Bifați segmentele afectate și descrieți leziunea.")
        
        dominanta = st.radio("Dominanță Coronariană", ["Dreaptă (RCA)", "Stângă (LCX)", "Codominanță"], horizontal=True)
        
        # Grid vizual pentru vase
        col_v1, col_v2 = st.columns(2)
        
        with col_v1:
            with st.container(border=True):
                st.markdown("**Stânga (LAD & LCX)**")
                # Trunchi
                if st.checkbox("Trunchi Comun (LM)"):
                    lesion_dict["Trunchi Comun"] = st.text_input("Detalii LM", "Stenoză distală 40%")
                # LAD
                if st.checkbox("Descendentă Anterioară (LAD)"):
                    lesion_dict["LAD"] = st.text_input("Detalii LAD", "Stenoză medie 80% tip B2")
                # LCX
                if st.checkbox("Circumflexă (LCX)"):
                    lesion_dict["LCX"] = st.text_input("Detalii LCX", "Neregulată difuz")
                    
        with col_v2:
            with st.container(border=True):
                st.markdown("**Dreapta (RCA)**")
                if st.checkbox("Coronara Dreaptă (RCA)"):
                    lesion_dict["RCA"] = st.text_input("Detalii RCA", "Ocluzie cronică (CTO) medie")
                if st.checkbox("Ramuri Secundare (Diag/Marg)"):
                    lesion_dict["Ramuri"] = st.text_input("Detalii Ramuri", "D1 stenoză ostială 90%")

    # --- TAB 3: ANGIOPLASTIE ---
    with tab_pci:
        st.markdown('<p class="section-header">Protocol Intervențional</p>', unsafe_allow_html=True)
        
        c_pci1, c_pci2 = st.columns([2, 1])
        with c_pci1:
            pci_art = st.selectbox("Artera", ["LAD", "LCX", "RCA", "LM", "D1", "OM1"])
            pci_desc = st.text_area("Descriere pas", height=100, placeholder="ex. Predilatare balon 2.5x15mm...")
        with c_pci2:
            st.write("")
            st.write("")
            if st.button("➕ Adaugă Pas", type="primary", use_container_width=True):
                if pci_desc:
                    st.session_state.pci_events.append({
                        "artera": pci_art,
                        "text": pci_desc,
                        "time": datetime.now().strftime("%H:%M")
                    })
            
            if st.button("Șterge Tot", type="secondary", use_container_width=True):
                st.session_state.pci_events = []
                st.rerun()

        # Timeline vizual
        if st.session_state.pci_events:
            st.markdown("---")
            for idx, ev in enumerate(st.session_state.pci_events):
                st.markdown(f"**{idx+1}. {ev['artera']}**: {ev['text']}")

    # --- TAB 4: FINALIZARE ---
    with tab_concl:
        with st.container(border=True):
            st.markdown('<p class="section-header">Sinteză</p>', unsafe_allow_html=True)
            
            # Auto-sugestie
            sugestie = "Coronare angiografic normale."
            if lesion_dict: sugestie = "Boală coronariană semnificativă."
            if st.session_state.pci_events: sugestie += " Revascularizare percutană cu succes."
            
            concluzii = st.text_area("Concluzii Raport", value=sugestie, height=100)
            recomandari = st.text_area("Recomandări", value="Tratament Medical Optimal. Control la 1 an.", height=70)
            rx = st.text_input("Rețetă Externare", "Aspirina 75mg + Clopidogrel 75mg + Atorvastatin 80mg")

# >>>>>>>>>>>> ZONA DE LIVE PREVIEW (DREAPTA) <<<<<<<<<<<<
with main_col_right:
    st.markdown("###### 📄 Previzualizare Raport")
    
    # Colectăm toate datele într-un dicționar
    data_pack = {
        "nume": nume if nume else "____________________",
        "cnp": cnp,
        "varsta": varsta,
        "fo": fo if fo else "___",
        "data": data_proc,
        "op1": op1,
        "op2": op2,
        "indicatie": indicatie,
        "risc": risc,
        "abord": abord,
        "teaca": teaca,
        "contrast": contrast,
        "scopie": scopie,
        "dap": dap,
        "ao": ao,
        "lvedp": lvedp,
        "dominanta": dominanta,
        "concluzii": concluzii if 'concluzii' in locals() else "...",
        "recomandari": recomandari if 'recomandari' in locals() else "...",
        "rx": rx if 'rx' in locals() else "..."
    }
    
    # Generăm textul
    full_report = get_report_text(data_pack, lesion_dict, st.session_state.pci_events)
    
    # Afișare stilizată "Foaie A4"
    st.markdown(f"""
    <div class="paper-preview">
        <div style="text-align:center; margin-bottom:20px;">
            <h2 style="margin:0; font-size:18px;">SPITALUL CLINIC DE URGENȚĂ</h2>
            <h4 style="margin:0; font-size:14px; color:#555;">LABORATOR DE ANGIOGRAFIE</h4>
        </div>
        <hr style="border-top: 1px solid #000;">
        <div style="font-family: monospace; white-space: pre-wrap;">{full_report}</div>
        <div style="margin-top:50px; text-align:right;">
            <p>Semnătura Parafa,</p>
            <p><strong>{op1}</strong></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="🖨️ Descarcă Raport Oficial (.txt)",
        data=full_report,
        file_name=f"Raport_{nume}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        type="primary",
        use_container_width=True
    )
