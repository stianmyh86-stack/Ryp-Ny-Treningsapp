import streamlit as st
import pandas as pd

# --- KONFIGURASJON AV PROGRAMMER ---
# Data hentet fra PDF side 14-15 (Grunnprogram) og side 16 (Ekstrem Muskelvekst)

PROGRAMS = {
    "Grunnprogrammet": {
        "info": "Passer for alle i starten. Fokus på teknikk, kondisjon og muskelvekst.",
        "exercises": ["Knebøy", "Markløft m/strake", "Skråbenk", "Nedtrekk", "Roing", "Arnoldpress", "Biceps curl", "Tricepspress"],
        "phases": {
            1: {"reps": "15", "sets": 2, "mult": [0.65, 0.70, 0.75]},
            2: {"reps": "10", "sets": 2, "mult": [0.80, 0.85, 0.90]}, # Uke 2
            3: {"reps": "10", "sets": 2, "mult": [0.95, 1.00, 1.05]}, # Uke 3
            4: {"reps": "5", "sets": 2, "mult": [1.00, 1.05, 1.10], "drop": True}, # Uke 4
            5: {"reps": "5", "sets": 2, "mult": [1.15, 1.20, 1.25], "drop": True}, # Uke 5
            6: {"reps": "5", "sets": 2, "mult": [1.30, 1.35, 1.40], "drop": True}, # Uke 6
        }
    },
    "Ekstrem Muskelvekst": {
        "info": "For deg som vil prioritere maksimal muskelmasse. Høyere volum, færre isolasjonsøvelser, raskere progresjon.",
        "exercises": ["Knebøy", "Dips", "Roing", "Arnoldpress"], # Basert på tabell side 16
        "phases": {
            1: {"reps": "15", "sets": 2, "mult": [0.70, 0.75, 0.80]},
            2: {"reps": "10", "sets": 3, "mult": [0.85, 0.90, 0.95]},
            3: {"reps": "10", "sets": 3, "mult": [1.00, 1.05, 1.10]},
            4: {"reps": "5", "sets": "4 + 1 (dropp)", "mult": [1.05, 1.10, 1.15]},
            5: {"reps": "5", "sets": "4 + 1 (dropp)", "mult": [1.20, 1.25, 1.30]},
            6: {"reps": "5", "sets": "4 + 1 (dropp)", "mult": [1.35, 1.40, 1.45]},
        }
    }
}

# --- HOVEDAPP ---
def main():
    st.title("Tech Nutrition - Release YOUR Potential")
    st.write("Generer ditt treningsprogram basert på dine 10RM.")

    # 1. Velg Program
    st.sidebar.header("Innstillinger")
    prog_choice = st.sidebar.selectbox("Velg Program", list(PROGRAMS.keys()))
    current_prog = PROGRAMS[prog_choice]
    
    st.info(f"**Valgt program:** {prog_choice}\n\n{current_prog['info']}")

    # 2. Input av 10RM
    st.sidebar.subheader("Dine 10RM (Maks vekt for 10 reps)")
    rm_values = {}
    for ex in current_prog["exercises"]:
        # Standardverdier for å gjøre det enklere å teste
        default_val = 60.0 if ex in ["Knebøy", "Markløft m/strake"] else 40.0
        if ex in ["Biceps curl", "Tricepspress", "Arnoldpress"]: default_val = 15.0
        
        rm_values[ex] = st.sidebar.number_input(f"{ex} (kg)", value=default_val, step=2.5)

    # 3. Velg Uke
    week = st.slider("Velg uke i programmet (1-6)", 1, 6)
    
    # 4. Hent data for valgt uke
    phase_data = current_prog["phases"][week]
    reps = phase_data["reps"]
    sets = phase_data["sets"]
    multipliers = phase_data["mult"]
    
    # Vis info om fasen
    st.header(f"Uke {week} - {reps} Reps Fasen")
    
    if "dropp" in str(sets) or phase_data.get("drop"):
        st.warning("🔥 **Droppsett:** På siste settet reduserer du vekten (ca 20-30%) og tar så mange reps du klarer.")
    
    if prog_choice == "Ekstrem Muskelvekst" and week >= 4:
        st.success("💪 **Ekstrem-modus:** 4 tunge sett + 1 droppsett for maksimal stimulans!")

    # 5. Bygg tabellen
    table_data = []
    for ex in current_prog["exercises"]:
        rm = rm_values[ex]
        
        # Beregn vekter og rund av til nærmeste 2.5kg (eller 1kg for små øvelser)
        weights = []
        for m in multipliers:
            raw_w = rm * m
            # Avrunding
            step = 2.5 if raw_w > 20 else 1.0
            rounded_w = round(raw_w / step) * step
            weights.append(f"{rounded_w} kg")
        
        # Sjekk om sett skal vises som tall eller tekst (for 4+1)
        sets_display = sets
        
        # Grunnprogrammet har spesifikke droppsett-regler i uke 4-6 (merket med +1 i PDF)
        if prog_choice == "Grunnprogrammet" and week >= 4:
            # I grunnprogrammet er det ofte bare siste øvelse på muskelgruppe som har droppsett
            # For enkelhets skyld i appen markerer vi de tunge.
            pass 

        table_data.append([
            ex, 
            sets_display, 
            reps, 
            weights[0], # Mandag
            weights[1], # Onsdag
            weights[2]  # Fredag
        ])

    # Lag DataFrame for visning
    df = pd.DataFrame(table_data, columns=["Øvelse", "Sett", "Reps", "Mandag", "Onsdag", "Fredag"])
    
    # Vis tabell
    st.table(df)
    
    st.write("---")
    st.caption("Basert på 'Release YOUR Potential' konseptet. Husk oppvarming før tunge løft!")

if __name__ == "__main__":
    main()
