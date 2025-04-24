
import streamlit as st
import pandas as pd
import numpy as np
import time

# Carica il dataset
df = pd.read_csv('Updated_Questions_Dataset.csv')

# Struttura dell'esame
test_structure = {
    "TEORIA DELLO SCAFO": 1,
    "MOTORI": 2,
    "SICUREZZA DELLA NAVIGAZIONE": 3,
    "MANOVRA E CONDOTTA": 3,
    "COLREG": 2,
    "METEOROLOGIA": 1,
    "NAVIGAZIONE": 1,
    "NORMATIVA DIPORTISTICA E AMBIENTALE": 3
}

st.title("Simulatore Esame Nautica")

DURATA_ESAME = 30 * 60  # 30 minuti

if 'started' not in st.session_state:
    if st.button('Inizia Esame'):
        st.session_state.started = True
        st.session_state.start_time = time.time()
        st.session_state.questions = []
        for tema, num in test_structure.items():
            subset = df[df['TEMA'] == tema].sample(num)
            for _, riga in subset.iterrows():
                st.session_state.questions.append({
                    'tema': tema,
                    'domanda': riga['DOMANDA'],
                    'risposte': [riga['RISPOSTA 1'], riga['RISPOSTA 2'], riga['RISPOSTA 3']],
                    'corretta': '1' if riga['V/F'] == 'V' else '2' if riga['V/F.1'] == 'V' else '3',
                    'immagine': riga['IMMAGINE'] if pd.notna(riga['IMMAGINE']) else None,
                    'risposta_data': None
                })
        st.session_state.current_question = 0
        st.session_state.correct_answers = 0

if 'started' in st.session_state:
    tempo_rimasto = DURATA_ESAME - (time.time() - st.session_state.start_time)
    if tempo_rimasto > 0:
        minuti, secondi = divmod(int(tempo_rimasto), 60)
        st.sidebar.write(f"⏳ Tempo rimanente: {minuti:02d}:{secondi:02d}")

        q = st.session_state.questions[st.session_state.current_question]

        # Mostra immagine se presente
        if q['immagine']:
            st.image(q['immagine'])

        st.subheader(f"{q['tema']}: {q['domanda']}")

        risposta = st.radio("Seleziona la risposta:", ['1', '2', '3'], index=0,
                            format_func=lambda x: q['risposte'][int(x)-1], key=f"risposta_{st.session_state.current_question}")

        if st.button('Conferma risposta'):
            q['risposta_data'] = risposta
            if risposta == q['corretta']:
                st.success("Corretto!")
                st.session_state.correct_answers += 1
            else:
                st.error(f"Errato! La risposta corretta era la {q['corretta']}.")

        if q['risposta_data']:
            if st.session_state.current_question + 1 < len(st.session_state.questions):
                if st.button("Avanti"):
                    st.session_state.current_question += 1
            else:
                st.success(f"Esame terminato! Risposte corrette: {st.session_state.correct_answers} su {len(st.session_state.questions)}.")
                if st.button('Ricomincia Esame'):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
    else:
        st.warning("⏰ Tempo scaduto!")
        st.subheader(f"Risposte corrette: {st.session_state.correct_answers} su {len(st.session_state.questions)}")
        if st.button('Ricomincia Esame'):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
