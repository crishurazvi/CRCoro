import streamlit as st
from datetime import datetime

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(
    page_title="CardioReport RO - Protocol Coronarografie",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STILIZARE CSS (Pt. a maximiza spațiul și a curăța interfața) ---
st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    h1 {font-size: 2rem !important;}
    h3 {font-size: 1.4rem !important;}
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE (Memorie temporară) ---
if 'lista_operatori' not in st.session_state:
    st.session_state.lista_operatori = ["Dr. Popescu", "Dr. Ionescu", "Dr. Georgescu"]
if 'protocoale_pci' not in st.session_state:
    st.session_state.protocoale_pci = []

# --- SIDEBAR: DATE GENERALE ---
with st.sidebar:
    st.title("🫀 CardioReport RO")
    st.markdown("---")
    st.header("1. Date Pacient")
    
    # Adăugare Operator Dinamic
    col_op1, col_op2 = st.columns([3, 1])
    with col_op1:
        operator_selectat = st.selectbox("Operator Principal", st.session_state.lista_operatori, index=0)
    with col_op2:
        # Buton mic pentru a simula adăugarea (în realitate ar trebui bază de date)
        nou_op = st.text_input("Nou", label_visibility="collapsed", placeholder="+")
        if nou_op and nou_op not in st.session_state.lista_operatori:
            st.session_state.lista_operatori.append(nou_op)
            st.rerun()

    operator_secundar = st.text_input("Operator Secundar", placeholder="ex. Rezident / Asistent")
    
    st.markdown("---")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        nume_pacient = st.text_input("Nume Pacient", placeholder="Nume Prenume")
        fo = st.text_input("Nr. Foaie (FO)")
    with col_p2:
        varsta = st.number_input("Vârstă", 18, 110, 60)
        id_procedura = st.text_input("ID Procedură", placeholder="ex. 2024-1023")

    data_proc = st.date_input("Data Procedurii", datetime.today())
    
    st.subheader("Factori de Risc")
    risc = st.multiselect("Factori:", 
        ["HTA", "Diabet Zaharat", "Dyslipidemie", "Fumat", "Obezitate", "Heredocolaterale", "Insuf. Renală", "Fost fumător"],
        default=[])
    
    st.subheader("Indicație")
    indicatie = st.selectbox("Motiv:", 
        ["Angină Stabilă", "Angină Instabilă", "NSTEMI", "STEMI", "Pre-operator", "Control (Stent/Bypass)", "Insuficiență Cardiacă", "Test de ischemie pozitiv"])

# --- TAB-uri ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📍 1. Abord & Tehnică", 
    "🫀 2. Anatomie & Leziuni", 
    "🎈 3. Angioplastie (PCI)", 
    "📄 4. Raport Final"
])

# ==========================================
# TAB 1: ABORD & HEMODINAMICĂ
# ==========================================
with tab1:
    col_teh1, col_teh2 = st.columns(2)
    
    with col_teh1:
        st.info("Cale de Abord & Materiale")
        c1, c2 = st.columns(2)
        abord = c1.selectbox("Artera puncționată:", ["Radială Dreaptă", "Radială Stângă", "Femurală Dreaptă", "Femurală Stângă", "Brahială"])
        teaca = c2.selectbox("Teacă (Sheath):", ["4F", "5F", "6F", "7F", "8F"], index=2)
        
        catetere_dg = st.text_area("Catetere Diagnostic:", "JL 3.5, JR 4.0", height=68)
        
        st.markdown("##### Hemostază")
        hemostaza = st.selectbox("Metodă închidere:", ["Compresie Manuală", "TR Band (Pneumatic)", "AngioSeal", "Perclose ProGlide", "Femostop"])
        staza_detalii = st.text_input("Detalii hemostază (opțional):", placeholder="ex. scos teaca la 4h")

    with col_teh2:
        st.info("Hemodinamică & Radioscopie")
        h1, h2 = st.columns(2)
        ao = h1.text_input("TA Aortă (mmHg):", "120/80")
        lvedp = h2.text_input("LVEDP (mmHg):", "10")
        
        st.markdown("---")
        r1, r2, r3 = st.columns(3)
        contrast = r1.number_input("Contrast (ml):", value=80, step=10)
        scopie = r2.number_input("Scopie (min):", value=5.0, step=0.5)
        dap = r3.number_input("DAP (Gy.cm2):", value=40.0, step=1.0)

# ==========================================
# TAB 2: ANATOMIE (SISTEMATIZATĂ)
# ==========================================
with tab2:
    st.write("Selectați segmentele cu leziuni pentru a le edita detaliile.")
    
    dominanta = st.radio("Dominanță Coronariană:", ["Dreaptă (RCA)", "Stângă (LCA)", "Echilibrată"], horizontal=True)
    st.markdown("---")

    # Dictionar pentru stocarea datelor despre leziuni
    lesion_data = {}

    def render_vessel_section(vessel_name, segments, key_prefix):
        """Genereaza UI pentru un vas si segmentele sale"""
        with st.expander(f"📌 {vessel_name}", expanded=False):
            # Flux general
            flux_global = st.selectbox(f"Flux TIMI general ({vessel_name}):", ["TIMI 3", "TIMI 2", "TIMI 1", "TIMI 0"], key=f"flow_{key_prefix}")
            
            st.markdown(f"**Leziuni Segmentare ({vessel_name})**")
            
            # Iterăm prin segmente
            for seg in segments:
                is_diseased = st.checkbox(f"{seg}", key=f"chk_{key_prefix}_{seg}")
                if is_diseased:
                    c1, c2, c3 = st.columns([1, 2, 1])
                    stenosis = c1.slider(f"% Stenoză ({seg})", 10, 100, 70, 5, key=f"st_{key_prefix}_{seg}")
                    desc = c2.text_input(f"Descriere ({seg})", placeholder="ex. excentrică, calcificată", key=f"desc_{key_prefix}_{seg}")
                    lesion_type = c3.selectbox("Tip", ["A", "B1", "B2", "C"], key=f"type_{key_prefix}_{seg}")
                    
                    # Salvăm datele dacă există leziune
                    lesion_data[f"{vessel_name} - {seg}"] = {
                        "stenosis": stenosis,
                        "desc": desc,
                        "type": lesion_type
                    }
            return flux_global

    # 1. TRUNCHI COMUN
    tc_flow = render_vessel_section("Trunchi Comun (LM)", ["Ostium", "Corp", "Bifurcație distală"], "LM")

    # 2. IVA (LAD)
    c1, c2 = st.columns(2)
    with c1:
        iva_flow = render_vessel_section("Artera Interventriculară Ant. (IVA/LAD)", 
                                         ["Ostium", "Proximal", "Mediu", "Distal", "Diagonală 1 (D1)", "Diagonală 2 (D2)"], "LAD")
    with c2:
    # 3. CIRCUMFLEXA (LCX)
        cx_flow = render_vessel_section("Artera Circumflexă (Cx/LCX)", 
                                        ["Ostium", "Proximal", "Mediu", "Distal", "Marginală 1 (OM1)", "Marginală 2 (OM2)", "Intermediara"], "LCX")

    # 4. CORONARA DREAPTA (RCA)
    rca_flow = render_vessel_section("Coronara Dreaptă (CD/RCA)", 
                                     ["Ostium", "Proximal", "Mediu", "Distal", "IVP (PDA)", "Postero-Laterală (PL)"], "RCA")

    # 5. ALTELE
    byp_flow = render_vessel_section("Bypass-uri / Altele", ["LIMA la IVA", "RIMA", "Venous Graft la CD", "Venous Graft la Cx"], "BYP")

# ==========================================
# TAB 3: ANGIOPLASTIE (PROTOCOL DINAMIC)
# ==========================================
with tab3:
    st.info("Adăugați protocolul pentru fiecare arteră tratată, pe rând.")
    
    col_pci1, col_pci2 = st.columns([1, 2])
    
    with col_pci1:
        pci_artera = st.selectbox("1. Alege Artera tratată:", ["-", "TC (LM)", "IVA (LAD)", "Cx (LCX)", "CD (RCA)", "Diagonală", "Marginală", "Bypass"])
        pci_text = st.text_area("2. Scrie Protocolul (Manual):", height=200, placeholder="Ex: Ghidare cu EBU 3.5. Trecut ghid Sion Blue. Predilatare balon 2.5x15. Implantare stent DES 3.0x28mm la 12atm. Postdilatare NC 3.25x12 la 18atm. Rezultat final bun, flux TIMI 3.")
        
        if st.button("➕ Adaugă Protocol Artera"):
            if pci_artera != "-" and pci_text:
                st.session_state.protocoale_pci.append({"artera": pci_artera, "text": pci_text})
                st.success(f"Protocol pentru {pci_artera} adăugat!")
            else:
                st.error("Selectează artera și scrie textul.")
        
        if st.button("🗑️ Șterge tot (Reset PCI)"):
            st.session_state.protocoale_pci = []
            st.rerun()

    with col_pci2:
        st.subheader("Protocoale introduse:")
        if not st.session_state.protocoale_pci:
            st.write("Nu s-au introdus date de angioplastie.")
        else:
            for idx, item in enumerate(st.session_state.protocoale_pci):
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px; color: black;">
                    <strong>{idx+1}. Artera: {item['artera']}</strong><br>
                    {item['text']}
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# TAB 4: RAPORT FINAL (PLAIN TEXT)
# ==========================================
with tab4:
    st.header("Raport Final")
    
    # Concluzii (Editabile)
    st.subheader("Concluzii & Recomandări")
    
    # Generare sugestie concluzie
    sugestie_concluzie = "Coronare angiografic normale."
    if lesion_data:
        sugestie_concluzie = "Boală coronariană semnificativă " + ("uni/bi/tri-vasculară.")
    if st.session_state.protocoale_pci:
        sugestie_concluzie = f"Angioplastie coronariană cu succes la nivelul {', '.join([p['artera'] for p in st.session_state.protocoale_pci])}."

    concluzie_finala = st.text_area("Concluzii:", value=sugestie_concluzie, height=80)
    
    # Recomandari
    recomandari_list = st.multiselect("Recomandări:", 
        ["Tratament Medical Optimal", "DAPT (Aspirină+Clopidogrel)", "DAPT (Aspirină+Ticagrelor)", "Revascularizare Chirurgicală (CABG)", "Control la 1 an", "Ecocardiografie", "Oprire fumat"],
        default=["Tratament Medical Optimal"])
    
    tratament_text = st.text_area("Tratament la externare:", "Aspirina 75mg 1-0-0\nAtorvastatina 80mg 0-0-1", height=80)

    st.markdown("---")
    
    # GENERATOR TEXT (FĂRĂ MARKDOWN)
    def generate_plain_text():
        lines = []
        lines.append(f"PROTOCOL DE CORONAROGRAFIE {'SI ANGIOPLASTIE' if st.session_state.protocoale_pci else ''}")
        lines.append(f"Unitatea: Laborator Cateterism Cardiac")
        lines.append(f"Data: {data_proc.strftime('%d/%m/%Y')} | ID Procedura: {id_procedura}")
        lines.append(f"Operator: {operator_selectat} | Secundar: {operator_secundar}")
        lines.append("-" * 40)
        
        lines.append("1. DATE PACIENT")
        lines.append(f"Nume: {nume_pacient} | Varsta: {varsta} ani | FO: {fo}")
        lines.append(f"Factori de Risc: {', '.join(risc) if risc else 'Negativi'}")
        lines.append(f"Indicatie: {indicatie}")
        lines.append("")
        
        lines.append("2. DETALII PROCEDURALE")
        lines.append(f"Abord: {abord} ({teaca})")
        lines.append(f"Hemostaza: {hemostaza} {f'({staza_detalii})' if staza_detalii else ''}")
        lines.append(f"Hemodinamica: TA Ao: {ao} mmHg, LVEDP: {lvedp} mmHg")
        lines.append(f"Parametri: Scopie {scopie} min | DAP {dap} Gy.cm2 | Contrast {contrast} ml")
        lines.append(f"Catetere: {catetere_dg}")
        lines.append("-" * 40)
        
        lines.append("3. DESCRIERE ANGIOGRAFICA")
        lines.append(f"Dominanta: {dominanta}")
        lines.append(f"FLUX TIMI: TC[{tc_flow}] IVA[{iva_flow}] Cx[{cx_flow}] CD[{rca_flow}]")
        lines.append("")
        
        if not lesion_data:
            lines.append("Fara leziuni semnificative angiografic pe segmentele analizate.")
        else:
            lines.append("LEZIUNI IDENTIFICATE:")
            # Grupare dupa vas pentru claritate in text
            sorted_lesions = sorted(lesion_data.items()) 
            for key, data in sorted_lesions:
                # key format: "Vas - Segment"
                lines.append(f" - {key}: Stenoza {data['stenosis']}%, Tip {data['type']}. {data['desc']}")
        
        if st.session_state.protocoale_pci:
            lines.append("-" * 40)
            lines.append("4. PROTOCOL ANGIOPLASTIE (PCI)")
            for item in st.session_state.protocoale_pci:
                lines.append(f"VAS TRATAT: {item['artera']}")
                lines.append(f"Protocol: {item['text']}")
                lines.append("")
        
        lines.append("-" * 40)
        lines.append("5. CONCLUZII")
        lines.append(concluzie_finala)
        lines.append("")
        lines.append("6. RECOMANDARI")
        lines.append(", ".join(recomandari_list))
        lines.append("Tratament medicamentos:")
        lines.append(tratament_text)
        
        return "\n".join(lines)

    raport_final = generate_plain_text()
    
    st.text_area("Previzualizare Raport (Gata de printat):", value=raport_final, height=600)
    
    # Buton de download (Streamlit nu are "Copy to clipboard" nativ fara componente extra, dar text area permite Ctrl+A, Ctrl+C usor)
    st.download_button("💾 Descarcă Raport (.txt)", data=raport_final, file_name=f"Raport_{nume_pacient}_{id_procedura}.txt")
