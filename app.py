
import streamlit as st
import pandas as pd
import numpy as np

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
    "NORMATIVA DIPORTISTICA E AMBIENTALE": 2
}

st.title("Simulatore Esame Nautica")

if 'started' not in st.session_state:
    if st.button('Inizia Esame'):
        st.session_state.started = True
        st.session_state.questions = []
        for tema, num in test_structure.items():
            subset = df[df['TEMA'] == tema].sample(num)
            for _, riga in subset.iterrows():
                st.session_state.questions.append({
                    'tema': tema,
                    'domanda': riga['DOMANDA'],
                    'risposte': [riga['RISPOSTA 1'], riga['RISPOSTA 2'], riga['RISPOSTA 3']],
                    'corretta': '1' if riga['V/F'] == 'V' else '2' if riga['V/F.1'] == 'V' else '3'
                })
        st.session_state.current_question = 0
        st.session_state.correct_answers = 0

if 'started' in st.session_state:
    q = st.session_state.questions[st.session_state.current_question]
    st.subheader(f"{q['tema']}: {q['domanda']}")

    risposta = st.radio("Seleziona la risposta:", ['1', '2', '3'], format_func=lambda x: q['risposte'][int(x)-1])

    if st.button('Conferma risposta'):
        if risposta == q['corretta']:
            st.success("Corretto!")
            st.session_state.correct_answers += 1
        else:
            st.error(f"Errato! La risposta corretta era la {q['corretta']}.")

        if st.session_state.current_question + 1 < len(st.session_state.questions):
            st.session_state.current_question += 1
        else:
            st.subheader(f"Esame terminato! Hai risposto correttamente a {st.session_state.correct_answers} domande su {len(st.session_state.questions)}.")
            if st.button('Ricomincia Esame'):
                del st.session_state['started']
