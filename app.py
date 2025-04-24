import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

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

# Titolo con stile personalizzato
st.markdown("<h1 style='text-align: center; color: navy;'>🧭 Simulatore Esame Nautico</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Simulazione interattiva con tempo reale, immagini e riepilogo dettagliato</p>", unsafe_allow_html=True)

DURATA_ESAME = 30 * 60  # 30 minuti

# Inizializza lo stato
if 'started' not in st.session_state:
    st.session_state.started = False

# Inizia esame
if not st.session_state.started:
    if st.button('🟢 Inizia Esame'):
        st.session_state.started = True
        st.session_state.start_time = time.time()
        st.session_state.questions = []
        st.session_state.current_question = 0
        st.session_state.correct_answers = 0
        st.session_state.incorrect = []
        for tema, num in test_structure.items():
            subset = df[df['TEMA'] == tema].sample(num)
            for _, riga in subset.iterrows():
                st.session_state.questions.append({
                    'tema': riga['TEMA'],
                    'domanda': riga['DOMANDA'],
                    'risposte': [riga['RISPOSTA 1'], riga['RISPOSTA 2'], riga['RISPOSTA 3']],
                    'corretta': '1' if riga['V/F'] == 'V' else '2' if riga['V/F.1'] == 'V' else '3',
                    'immagine': riga['IMMAGINE'] if pd.notna(riga['IMMAGINE']) else None
                })
        st.rerun()

if st.session_state.started:
    # Timer visivo
    tempo_rimasto = DURATA_ESAME - (time.time() - st.session_state.start_time)
    if tempo_rimasto > 0 and st.session_state.current_question < len(st.session_state.questions):
        minuti, secondi = divmod(int(tempo_rimasto), 60)
        st.sidebar.markdown(f"<h4 style='color:red;'>⏱️ {minuti:02d}:{secondi:02d}</h4>", unsafe_allow_html=True)
        st.progress(st.session_state.current_question / len(st.session_state.questions))

        q = st.session_state.questions[st.session_state.current_question]

        # Layout con immagine e testo
        col1, col2 = st.columns([1, 2])
        if q['immagine']:
            col1.image(q['immagine'], use_column_width=True)
        col2.subheader(f"{q['tema']}: {q['domanda']}")

        risposta = st.radio("Seleziona la risposta:", ['1', '2', '3'],
                            format_func=lambda x: q['risposte'][int(x)-1],
                            key=f"risposta_{st.session_state.current_question}")

        if st.button("Conferma risposta", key=f"conferma_{st.session_state.current_question}"):
            if risposta == q['corretta']:
                st.success("✅ Corretto!")
                st.session_state.correct_answers += 1
            else:
                st.error(f"❌ Errato! Risposta corretta: {q['risposte'][int(q['corretta'])-1]}")
                st.session_state.incorrect.append({
                    'domanda': q['domanda'],
                    'risposta_corretta': q['risposte'][int(q['corretta'])-1]
                })
            st.session_state.current_question += 1
            st.rerun()

    # Esame concluso
    elif tempo_rimasto <= 0 or st.session_state.current_question >= len(st.session_state.questions):
        st.balloons()
        st.subheader(f"📝 Hai risposto correttamente a {st.session_state.correct_answers} su {len(st.session_state.questions)} domande.")

        # Grafico riepilogativo
        fig, ax = plt.subplots()
        labels = ['Corrette', 'Sbagliate']
        sizes = [st.session_state.correct_answers, len(st.session_state.questions) - st.session_state.correct_answers]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

        # Domande sbagliate
        if st.session_state.incorrect:
            st.write("### ❌ Domande sbagliate:")
            for err in st.session_state.incorrect:
                st.write("**Domanda:**", err['domanda'])
                st.write("**Risposta corretta:**", err['risposta_corretta'])
                st.markdown("---")

        if st.button("🔁 Ricomincia Esame"):
            st.session_state.clear()
            st.rerun()
