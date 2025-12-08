import streamlit as st
from datetime import datetime

# Configurare pagină
st.set_page_config(
    page_title="CardioReport RO - Protocol Coronarografie",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titlu și Header
st.title("🫀 CardioReport RO")
st.markdown("**Generator de Rapoarte pentru Cardiologie Intervențională** (Stil CardioReport France)")
st.markdown("---")

# --- SIDEBAR: Date Generale ---
with st.sidebar:
    st.header("1. Date Pacient & Procedură")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        nume_pacient = st.text_input("Nume Pacient", placeholder="ex. Popescu Ion")
    with col_s2:
        varsta = st.number_input("Vârstă", min_value=18, max_value=120, value=60)
    
    fo = st.text_input("Nr. Foaie Observație (FO)")
    data_proc = st.date_input("Data Procedurii", datetime.today())
    operator = st.text_input("Operator Principal", value="Dr. ")
    
    st.subheader("Factori de Risc")
    risc = st.multiselect(
        "Selectați factorii:",
        ["HTA", "Diabet Zaharat", "Dyslipidemie", "Fumat", "Obezitate", "Heredocolaterale", "Insuf. Renală", "Fost fumător"]
    )
    
    st.subheader("Indicație")
    indicatie = st.selectbox(
        "Motivul procedurii:",
        ["Angină Stabilă", "Angină Instabilă", "NSTEMI", "STEMI", "Pre-operator", "Control (Stent/Bypass)", "Insuficiență Cardiacă", "Test de ischemie pozitiv"]
    )

# --- TAB-uri PRINCIPALE ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 Abord & Tehnică", 
    "🫀 Anatomie & Leziuni", 
    "🎈 Angioplastie (PCI)", 
    "📝 Concluzii & Rx",
    "📄 Raport Final"
])

# --- TAB 1: Detalii Tehnice ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.info("Cale de Abord")
        abord = st.radio("Artera puncționată:", ["Radială Dreaptă", "Radială Stângă", "Femurală Dreaptă", "Femurală Stângă", "Brahială"])
        teaca = st.selectbox("Mărime Teacă (Sheath):", ["4F", "5F", "6F", "7F", "8F"], index=2)
    
    with col2:
        st.info("Detalii Tehnice")
        contrast = st.number_input("Volum Contrast (ml):", value=80, step=10)
        scopie = st.number_input("Timp Scopie (min):", value=5.0, step=0.5)
        dap = st.number_input("DAP (Gy.cm2):", value=40.0, step=1.0)
        catetere_dg = st.text_area("Catetere Diagnostic:", "JL 3.5, JR 4.0", height=70)

    st.markdown("### Hemodinamică")
    c1, c2 = st.columns(2)
    ao_pressure = c1.text_input("TA Aortă (mmHg):", "120/80")
    lvedp = c2.text_input("LVEDP (mmHg):", "10")

# --- TAB 2: Anatomie Coronariană ---
with tab2:
    st.write("Descrieți anatomia și leziunile identificate.")
    dominanta = st.radio("Dominanță Coronariană:", ["Dreaptă (85%)", "Stângă", "Echilibrată"], horizontal=True)
    
    # Funcție helper pentru segmente
    def segment_analysis(vessel_name):
        with st.expander(f"Detalii {vessel_name}", expanded=False):
            status = st.selectbox(f"Status {vessel_name}:", ["Normal", "Ateromatoză difuză fără stenoze semnificative", "Stenoze semnificative", "Ocluzie cronică (CTO)", "Ocluzie acută"], key=f"status_{vessel_name}")
            descriere = st.text_area(f"Descriere detaliată {vessel_name}:", placeholder=f"Ex: Stenoză 70% segment mediu, calcificată...", key=f"desc_{vessel_name}")
            flux = st.selectbox(f"Flux TIMI {vessel_name}:", ["TIMI 3", "TIMI 2", "TIMI 1", "TIMI 0"], key=f"timi_{vessel_name}")
        return status, descriere, flux

    st.markdown("### Trunchi Comun (TC)")
    tc_status, tc_desc, tc_flow = segment_analysis("Trunchi Comun")

    st.markdown("### Arteră Interventriculară Anterioară (IVA)")
    iva_status, iva_desc, iva_flow = segment_analysis("IVA")

    st.markdown("### Arteră Circumflexă (Cx)")
    cx_status, cx_desc, cx_flow = segment_analysis("Cx")

    st.markdown("### Arteră Coronară Dreaptă (CD)")
    cd_status, cd_desc, cd_flow = segment_analysis("CD")

# --- TAB 3: Angioplastie (PCI) ---
with tab3:
    pci_done = st.checkbox("S-a efectuat Angioplastie (PCI)?")
    
    pci_details = ""
    stent_data = []
    
    if pci_done:
        st.subheader("Detalii Intervenție")
        vessel_treated = st.multiselect("Vas tratat:", ["TC", "IVA", "Cx", "CD", "Ram Diagonal", "Ram Marginal"])
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            cateter_guide = st.text_input("Cateter Ghid (Guiding):", "EBU 3.5 6F")
            ghid_metalic = st.text_input("Ghid Metalic (Wire):", "Sion Blue")
        with col_p2:
            tehnica = st.text_input("Tehnică:", "Direct Stenting / Predilatare + Stent / DEB")
        
        st.markdown("#### Materiale Implantate (Stenturi/Baloane)")
        num_stents = st.number_input("Număr stenturi:", 0, 5, 1)
        
        for i in range(num_stents):
            c_s1, c_s2, c_s3 = st.columns(3)
            s_type = c_s1.selectbox(f"Tip Stent #{i+1}", ["DES (Activ)", "BMS (Metal)", "DEB (Balon Activ)", "POBA"], key=f"s_type_{i}")
            s_dim = c_s2.text_input(f"Dimensiuni (D x L) #{i+1}", "ex. 3.0 x 18", key=f"s_dim_{i}")
            s_loc = c_s3.text_input(f"Segment #{i+1}", "ex. IVA mediu", key=f"s_loc_{i}")
            stent_data.append(f"- {s_type}: {s_dim} mm pe {s_loc}")

        rezultat_final = st.selectbox("Rezultat Angiografic:", ["Succes (Stenoză reziduală < 10%, TIMI 3)", "Flux lent (Slow flow)", "Disecție", "Eșec"], index=0)
        pci_details = st.text_area("Alte detalii PCI (Complicații, tromboaspirație, etc.):")

# --- TAB 4: Concluzii ---
with tab4:
    st.header("Concluzii și Recomandări")
    
    concluzie_predefinita = "Coronare angiografic normale."
    if pci_done:
        concluzie_predefinita = f"Angioplastie cu {num_stents} stenturi pe {', '.join(vessel_treated) if vessel_treated else 'vas'} cu rezultat bun."
    elif iva_status == "Stenoze semnificative" or cd_status == "Stenoze semnificative":
        concluzie_predefinita = "Boală coronariană semnificativă. Se recomandă..."
        
    concluzie_finala = st.text_area("Concluzie Finală:", value=concluzie_predefinita, height=100)
    
    recomandari = st.multiselect("Recomandări:", 
                                 ["Tratament Medical Optimal", 
                                  "DAPT (Aspirină + Clopidogrel)", 
                                  "DAPT (Aspirină + Ticagrelor)", 
                                  "Revascularizare Chirurgicală (CABG)", 
                                  "FFR / iFR pentru evaluare funcțională",
                                  "Ecocardiografie",
                                  "Oprire fumat"],
                                 default=["Tratament Medical Optimal"])
    
    tratament_med = st.text_area("Plan tratament la externare:", "Aspirină 75mg 1-0-0\nAtorvastatină 80mg 0-0-1\n...")

# --- TAB 5: Generare Raport ---
with tab5:
    st.success("Raportul este gata de generare.")
    
    # Construim textul
    current_date = data_proc.strftime("%d/%m/%Y")
    factori_risc_str = ", ".join(risc) if risc else "Negativi"
    
    report_text = f"""
# PROTOCOL DE CORONAROGRAFIE { "ȘI ANGIOPLASTIE" if pci_done else ""}
**Unitatea:** Laborator Cateterism Cardiac
**Data:** {current_date}
**Operator:** {operator}

---
### 1. DATE PACIENT
**Nume:** {nume_pacient} | **Vârstă:** {varsta} ani | **FO:** {fo}
**Factori de Risc:** {factori_risc_str}
**Indicație:** {indicatie}

### 2. DETALII PROCEDURALE
**Abord:** {abord} ({teaca})
**Hemodinamică:** TA: {ao_pressure}, LVEDP: {lvedp} mmHg
**Radioscopie:** {scopie} min | **DAP:** {dap} Gy.cm2 | **Contrast:** {contrast} ml
**Catetere diagnostic:** {catetere_dg}

---
### 3. DESCRIERE ANGIOGRAFICĂ
**Dominanță:** {dominanta}

* **Trunchi Comun (TC):** {tc_status}. {f"({tc_desc})" if tc_desc else ""}
* **Arteră Interventriculară Anterioară (IVA):** {iva_status}. {f"({iva_desc})" if iva_desc else ""} [Flux {iva_flow}]
* **Arteră Circumflexă (Cx):** {cx_status}. {f"({cx_desc})" if cx_desc else ""} [Flux {cx_flow}]
* **Arteră Coronară Dreaptă (CD):** {cd_status}. {f"({cd_desc})" if cd_desc else ""} [Flux {cd_flow}]

"""

    if pci_done:
        stents_formatted = "\n".join(stent_data)
        report_text += f"""
---
### 4. ANGIOPLASTIE CORONARIANĂ (PCI)
**Vas tratat:** {", ".join(vessel_treated)}
**Materiale:**
{stents_formatted}
**Ghid:** {cateter_guide}, {ghid_metalic}
**Detalii:** {pci_details}
**Rezultat:** {rezultat_final}
"""

    report_text += f"""
---
### 5. CONCLUZII
**{concluzie_finala}**

### 6. RECOMANDĂRI
{", ".join(recomandari)}

**Tratament:**
{tratament_med}

---
*Generat cu CardioReport RO*
"""

    # Afișare
    st.text_area("Previzualizare Raport (Copy-Paste în Word/EHR):", report_text, height=600)
    
    st.download_button(
        label="📥 Descarcă Raport (.txt)",
        data=report_text,
        file_name=f"Raport_Coro_{nume_pacient.replace(' ', '_')}.txt",
        mime="text/plain"
    )
