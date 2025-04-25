import streamlit as st
import pandas as pd
import numpy as np
import time
import streamlit.components.v1 as components

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

#st.title("Simulatore Esame - Patente D")

import streamlit as st

# Titolo con immagine cliccabile e testo accanto
st.markdown(
    """
    <h1 style='text-align: center;'>
        <a href="https://www.patentenautica.org" target="_blank" style="text-decoration: none;">
            <img src="https://patentenautica.org/wp-content/uploads/2025/04/ChatGPT-Image-24-apr-2025-10_20_53-1-300x300.png" 
                 alt="Patente Nautica" width="70" style="vertical-align: middle;">
            <span style="font-size: 24px; color: #002e60; vertical-align: middle; margin-left: 10px;">PatenteNautica.org</span>
        </a>
        <br>
        Simulatore Esame - Patente D
    </h1>
    """, 
    unsafe_allow_html=True
)


DURATA_ESAME = 30 * 60  # 30 minuti

if 'started' not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    if st.button('Clicca due volte e Inizia!'):
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
                    'tema': tema,
                    'domanda': riga['DOMANDA'],
                    'risposte': [riga['RISPOSTA 1'], riga['RISPOSTA 2'], riga['RISPOSTA 3']],
                    'corretta': '1' if riga['V/F'] == 'V' else '2' if riga['V/F.1'] == 'V' else '3',
                    'immagine': riga['IMMAGINE'] if pd.notna(riga['IMMAGINE']) else None
                })
        st.query_params["started"] = "1"
        st.stop()
if st.session_state.started:
    tempo_rimasto = DURATA_ESAME - (time.time() - st.session_state.start_time)
    if tempo_rimasto > 0 and st.session_state.current_question < len(st.session_state.questions):
        minuti, secondi = divmod(int(tempo_rimasto), 60)
        #st.sidebar.write(f"⏳ Tempo rimanente - si aggiorna all'arrivo di una nuova domanda: {minuti:02d}:{secondi:02d}")
        minuti, secondi = divmod(int(tempo_rimasto), 60)
        st.sidebar.markdown(
            f"""
            <div style='text-align: center; color: #e53935;'>
            <span style='font-size: 18px;'>⏳ Tempo rimanente</span><br>
            <span style='font-size: 12px;'>si aggiorna all'arrivo di una nuova domanda</span><br>
            <span style='font-size: 32px; font-weight: bold;'>{minuti:02d}:{secondi:02d}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
       
        # ✅ Barra di progresso
        progress = st.session_state.current_question / len(st.session_state.questions)
        st.progress(progress)
        q = st.session_state.questions[st.session_state.current_question]
        
        st.subheader(f"{q['tema']}: {q['domanda']}")

# Mostra immagine sotto la domanda
        if q['immagine']:
           st.image(q['immagine'], caption="Figura di riferimento", use_container_width=True)

        #if q['immagine']:
            #st.image(q['immagine'])

        #st.subheader(f"{q['tema']}: {q['domanda']}")
        risposta = st.radio("Seleziona la risposta:", ['1', '2', '3'],
                            format_func=lambda x: q['risposte'][int(x)-1], key=f"risposta_{st.session_state.current_question}")

        if st.button("Conferma risposta / Avanti", key=f"conferma_{st.session_state.current_question}"):
            if risposta == q['corretta']:
                st.success("Corretto!")
                st.session_state.correct_answers += 1
            else:
                st.error(f"Errato! La risposta corretta era la {q['corretta']}: {q['risposte'][int(q['corretta'])-1]}")
                st.session_state.incorrect.append({
                    'domanda': q['domanda'],
                    'risposta_corretta': q['risposte'][int(q['corretta'])-1]
                })
            st.session_state.current_question += 1

    elif tempo_rimasto <= 0 or st.session_state.current_question >= len(st.session_state.questions):
        st.warning("⏰ Esame terminato!")

        # 🎯 Valutazione finale con emoji
        punteggio = st.session_state.correct_answers
        totale = len(st.session_state.questions)
        st.subheader(f"Hai risposto correttamente a {punteggio} domande su {totale}.")

        # Emoji e messaggio finale
        if punteggio >= 13:
            st.success("🎉 Complimenti, ottimo risultato!")
        elif punteggio >= 10:
            st.info("💪 Buon lavoro, ma puoi migliorare ancora.")
        else:
            st.warning("📘 Allenati ancora un po', riprova!")

        if st.session_state.incorrect:
            st.write("### Domande sbagliate:")
            for err in st.session_state.incorrect:
                st.write("**Domanda:**", err['domanda'])
                st.write("**Risposta corretta:**", err['risposta_corretta'])

        if st.button('Ricomincia Esame'):
            st.session_state.clear()
            st.rerun()

import streamlit.components.v1 as components

