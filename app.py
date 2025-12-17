import streamlit as st
from datetime import datetime

# ==========================================
# 1. CONFIGURARE & TEMĂ UI
# ==========================================
st.set_page_config(
    page_title="CardioReport RO | Protocol Coronarografie",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONALIZAT PENTRU ASPECT ULTRA-MODERN ---
st.markdown("""
    <style>
    /* Import Font Modern */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Modificare Header & Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    
    /* Input-uri stilizate */
    .stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > div {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    
    /* Tabs stilizate */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 0 20px;
        font-weight: 600;
        color: #555;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #007bff; /* Albastru Medical */
        color: white;
    }

    /* Titluri */
    h1, h2, h3 {
        color: #2c3e50;
    }
    
    /* Card-uri Custom */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'lista_operatori' not in st.session_state:
    st.session_state.lista_operatori = ["Dr. CRISAN", "Dr. OLARIU", "Dr. ZUS"]
if 'protocoale_pci' not in st.session_state:
    st.session_state.protocoale_pci = []

# ==========================================
# 2. SIDEBAR - DATE GENERALE
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/heart-with-pulse.png", width=60)
    st.title("CardioReport RO")
    st.caption("v2.0 • Laborator Cateterism")
    st.markdown("---")
    
    with st.container(border=True):
        st.markdown("**🧑‍⚕️ Echipa Medicală**")
        col_op1, col_op2 = st.columns([4, 1])
        with col_op1:
            operator_selectat = st.selectbox("Operator Principal", st.session_state.lista_operatori, index=0)
        with col_op2:
            nou_op = st.text_input("Add", label_visibility="collapsed", placeholder="+")
            if nou_op and nou_op not in st.session_state.lista_operatori:
                st.session_state.lista_operatori.append(nou_op)
                st.rerun()
        operator_secundar = st.text_input("Operator Secundar", placeholder="Opțional")

    with st.container(border=True):
        st.markdown("**👤 Identificare Pacient**")
        nume_pacient = st.text_input("Nume & Prenume", placeholder="EX: POPESCU ION")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            fo = st.text_input("Foaie (FO)", placeholder="12345")
        with col_p2:
            varsta = st.number_input("Vârstă", 18, 110, 60)
        id_procedura = st.text_input("ID Procedură", value=f"PROC-{datetime.now().strftime('%Y%m%d')}")
        data_proc = st.date_input("Data", datetime.today())

    with st.expander("⚠️ Factori de Risc & Indicație", expanded=False):
        risc = st.multiselect("Factori Risc",
                ["HTA", "Diabet Zaharat", "Dyslipidemie", "Fumat", "Obezitate", "AHC", "IRC"],
            default=[])
        indicatie = st.selectbox("Indicație Clinică", 
            ["Angină Stabilă", "Angină Instabilă", "NSTEMI", "STEMI", "Ischemie Silențioasă", "Control Post-PCI", "Pre-operator Valvular"])

# ==========================================
# 3. ZONA PRINCIPALĂ (TABS)
# ==========================================

# Header Principal
st.markdown(f"### 📋 Protocol Procedură: **{nume_pacient if nume_pacient else 'Pacient Nou'}**")

tab1, tab2, tab3, tab4 = st.tabs([
    "🛠️ 1. Abord & Tehnică", 
    "🫀 2. Anatomie & Leziuni", 
    "💉 3. Angioplastie (PCI)", 
    "📄 4. Raport Final"
])

# --- TAB 1: ABORD & HEMODINAMICĂ ---
with tab1:
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        with st.container(border=True):
            st.markdown("#### 📍 Abord Vascular")
            c1, c2 = st.columns(2)
            abord = c1.selectbox("Loc Puncție", ["Radial Drept", "Radial Stâng", "Femural Drept", "Femural Stâng", "Brahial"])
            teaca = c2.selectbox("Teacă (Sheath)", ["4F", "5F", "6F", "7F", "8F"], index=2)
            
            st.markdown("#### 🩹 Hemostază")
            hemostaza = st.selectbox("Metodă", ["Compresie Manuală", "TR Band (Pneumatic)", "AngioSeal", "Perclose ProGlide", "Femostop"], index=1)
            
            st.markdown("#### 🔧 Materiale Diagnostic")
            catetere_dg = st.text_area("Catetere Utilizate", "JL 3.5, JR 4.0", help="Editați dacă s-au folosit curbe atipice")

    with col_t2:
        with st.container(border=True):
            st.markdown("#### 📊 Parametri Procedurali")
            
            sub_c1, sub_c2 = st.columns(2)
            ao = sub_c1.text_input("TA Aortă (mmHg)", "120/80")
            lvedp = sub_c2.text_input("LVEDP (mmHg)", "10")
            
            st.divider()
            
            r1, r2, r3 = st.columns(3)
            contrast = r1.number_input("Contrast (ml)", value=80, step=10)
            scopie = r2.number_input("Scopie (min)", value=5.0, step=0.5)
            dap = r3.number_input("DAP (Gy.cm2)", value=40.0, step=1.0)
            
            st.info(f"💡 **Total Iradiere:** {dap} Gy.cm2 | **Volum Contrast:** {contrast} ml", icon="☢️")

# --- TAB 2: ANATOMIE (SISTEMATIZATĂ) ---
with tab2:
    st.markdown("##### Configurație Coronariană")
    dominanta = st.radio("Dominanță:", ["Dreaptă", "Stângă", "Echilibrată"], horizontal=True)
    st.divider()

    lesion_data = {}

    def vessel_card(title, segments, key_prefix, color="#f0f2f6"):
        with st.container(border=True):
            col_head, col_flow = st.columns([3, 1])
            col_head.markdown(f"### {title}")
            flux_val = col_flow.selectbox(f"Flux {key_prefix}", ["TIMI 3", "TIMI 2", "TIMI 1", "TIMI 0"], label_visibility="collapsed")
            
            # Segmente Expandabile
            with st.expander(f"🔽 Detalii Leziuni {title}", expanded=False):
                for seg in segments:
                    is_active = st.checkbox(f"Leziune: {seg}", key=f"chk_{key_prefix}_{seg}")
                    if is_active:
                        c1, c2, c3 = st.columns([2, 3, 2])
                        sten = c1.slider(f"% Stenoză ({seg})", 30, 99, 70, 5, key=f"sld_{key_prefix}_{seg}")
                        desc = c2.text_input(f"Morphologie ({seg})", placeholder="ex. calcificată, excentrică", key=f"txt_{key_prefix}_{seg}")
                        type_l = c3.selectbox("Tip ACC/AHA", ["A", "B1", "B2", "C"], key=f"typ_{key_prefix}_{seg}")
                        
                        lesion_data[f"{title} - {seg}"] = {"stenosis": sten, "desc": desc, "type": type_l}
            return flux_val

    col_left, col_right = st.columns(2)
    
    with col_left:
        lm_flow = vessel_card("Trunchi Comun (LM)", ["Ostium", "Corp", "Distal"], "LM")
        iva_flow = vessel_card("Artera Descendentă Ant. (LAD)", ["Ostium", "Proximal", "Mediu", "Distal", "D1", "D2"], "LAD")
        cx_flow = vessel_card("Artera Circumflexă (LCX)", ["Ostium", "Proximal", "Distal", "OM1", "OM2"], "LCX")
        
    with col_right:
        rca_flow = vessel_card("Coronara Dreaptă (RCA)", ["Ostium", "Proximal", "Mediu", "Distal", "IVP", "PL"], "RCA")
        byp_flow = vessel_card("Grefe / Bypass", ["LIMA", "RIMA", "SVG-RCA", "SVG-Cx"], "BYP")

# --- TAB 3: ANGIOPLASTIE (PCI) ---
with tab3:
    col_input, col_display = st.columns([1, 1.5])
    
    with col_input:
        with st.container(border=True):
            st.markdown("#### ➕ Adăugare Protocol")
            pci_artera = st.selectbox("Artera Tratată", ["TC (LM)", "IVA (LAD)", "Cx (LCX)", "CD (RCA)", "Diagonală", "Marginală", "Bypass"])
            pci_text = st.text_area("Descriere Procedură", height=150, placeholder="Ex: Ghidare EBU 3.5 6F. Predilatare NC 2.5x15. Stent DES 3.0x28 la 14atm. Postdilatare...")
            
            if st.button("Adaugă în Raport", type="primary", use_container_width=True):
                if pci_text:
                    st.session_state.protocoale_pci.append({"artera": pci_artera, "text": pci_text, "time": datetime.now().strftime("%H:%M")})
                    st.success("Adăugat!")
                else:
                    st.warning("Scrieți protocolul înainte de a adăuga.")

            if st.button("Reset Tot", type="secondary", use_container_width=True):
                st.session_state.protocoale_pci = []
                st.rerun()

    with col_display:
        st.markdown("#### 📜 Jurnal Procedură")
        if not st.session_state.protocoale_pci:
            st.info("Nicio intervenție înregistrată încă.")
        else:
            for i, item in enumerate(st.session_state.protocoale_pci):
                st.markdown(f"""
                <div style="background-color: #f1f3f4; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #007bff;">
                    <small style="color: #666;">{item['time']} • <strong>{item['artera']}</strong></small><br>
                    <span style="font-size: 15px;">{item['text']}</span>
                </div>
                """, unsafe_allow_html=True)

# --- TAB 4: RAPORT FINAL ---
with tab4:
    st.markdown("### Generare Raport Final")
    
    # Logică Concluzii Auto
    default_concluzie = "Coronare angiografic normale."
    if lesion_data:
        default_concluzie = "Boală coronariană semnificativă."
    if st.session_state.protocoale_pci:
        vessels = list(set([x['artera'] for x in st.session_state.protocoale_pci]))
        default_concluzie = f"Angioplastie coronariană cu implant de stent la nivelul: {', '.join(vessels)}."

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        concluzie_finala = st.text_area("Concluzii", value=default_concluzie, height=100)
    with col_c2:
        recomandari_list = st.multiselect("Recomandări Standard", 
            ["Tratament Medical Optimal", "DAPT 12 luni", "DAPT 6 luni", "DAPT 1 lună", "CABG", "Control la 1 an", "Ecocardiografie"],
            default=["Tratament Medical Optimal"])
        rx_text = st.text_input("Tratament la externare", "Aspirina 75mg, Clopidogrel 75mg, Statina")

    # GENERATOR TEXT
    def build_report():
        lines = [
            f"CLINICA DE CARDIOLOGIE - LABORATOR CATETERISM",
            f"PROTOCOL PROCEDURAL: {'ANGIOPLASTIE' if st.session_state.protocoale_pci else 'CORONAROGRAFIE'}",
            f"--------------------------------------------------",
            f"Data: {data_proc.strftime('%d/%m/%Y')} | ID: {id_procedura}",
            f"Pacient: {nume_pacient} ({varsta} ani) | FO: {fo}",
            f"Echipa: {operator_selectat} / {operator_secundar}",
            f"Indicatie: {indicatie} | Risc: {', '.join(risc)}",
            f"",
            f"DETALII TEHNICE:",
            f"- Abord: {abord} ({teaca})",
            f"- Contrast: {contrast} ml | Iradiere: {dap} Gy.cm2",
            f"- Hemodinamica: TA {ao} mmHg | LVEDP {lvedp} mmHg",
            f"",
            f"DESCRIERE ANGIOGRAFICĂ (Dominanță {dominanta}):"
        ]
        
        if not lesion_data:
            lines.append("- Fără leziuni semnificative angiografic.")
        else:
            for k, v in lesion_data.items():
                lines.append(f"- {k}: Stenoză {v['stenosis']}%, {v['desc']} (Tip {v['type']})")
        
        if st.session_state.protocoale_pci:
            lines.append(f"\nPROCEDURA INTERVENȚIONALĂ (PCI):")
            for p in st.session_state.protocoale_pci:
                lines.append(f"> {p['artera']}: {p['text']}")
        
        lines.append(f"\nCONCLUZII: {concluzie_finala}")
        lines.append(f"RECOMANDĂRI: {', '.join(recomandari_list)}")
        lines.append(f"Rx la externare: {rx_text}")
        
        return "\n".join(lines)

    raport_text = build_report()
    
    st.text_area("Previzualizare", value=raport_text, height=400, help="Acest text poate fi copiat direct în fișa pacientului.")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    with col_btn1:
        st.download_button("💾 Descarcă TXT", data=raport_text, file_name=f"{nume_pacient}_Raport.txt", mime="text/plain", use_container_width=True)
