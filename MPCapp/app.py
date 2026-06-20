import json

import streamlit as st
from core.presenter import NPCPresenter

st.set_page_config(page_title="NPC Dialogue Sandbox", layout="wide")

if "presenter" not in st.session_state:
    st.session_state.presenter = NPCPresenter()
    st.session_state.last_analysis = None

p = st.session_state.presenter

st.title("Dynamic NPC Dialogue Sandbox")

with st.sidebar:
    st.header("NPC Configuration")
    name = st.text_input("Name", p.name)
    desc = st.text_area("Description", p.description, height=100)
    if name != p.name:
        p.name = name
    if desc != p.description:
        p.description = desc

    st.divider()
    st.subheader("Mood Controls")
    for trait in ["friendliness", "suspicion", "energy"]:
        current = p.moods[trait]
        new_val = st.slider(trait.capitalize(), 0.0, 1.0, current, 0.05)
        diff = round(new_val - current, 2)
        if diff != 0:
            p.adjust_mood(trait, diff)

    st.divider()
    st.subheader("World Context")
    p.update_world_state(
        "location",
        st.text_input("Location", p.world_state["location"]),
    )
    p.update_world_state(
        "time_of_day",
        st.selectbox(
            "Time of Day",
            ["Day", "Night", "Dawn", "Dusk"],
            index=["Day", "Night", "Dawn", "Dusk"].index(p.world_state["time_of_day"]),
        ),
    )
    p.update_world_state(
        "player_held_item",
        st.text_input("Player Holding", p.world_state["player_held_item"]),
    )

    st.divider()
    if st.button("Export NPC Config (JSON)"):
        config = p.export_config()
        st.download_button(
            "Download JSON",
            data=json.dumps(config, indent=2),
            file_name=f"{p.name.lower().replace(' ', '_')}_config.json",
            mime="application/json",
        )

    if st.button("Reset NPC", type="primary"):
        st.session_state.presenter = NPCPresenter()
        st.session_state.last_analysis = None
        st.rerun()

col_chat, col_status = st.columns([3, 1])

with col_chat:
    st.subheader("Dialogue")
    chat_container = st.container(height=400)
    with chat_container:
        for msg in p.chat_history:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**{p.name}:** {msg['content']}")

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Your message",
            placeholder="Say something to the NPC...",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Send", use_container_width=True)
        if submitted and user_input:
            reply, analysis = p.handle_player_input(user_input)
            st.session_state.last_analysis = analysis
            st.rerun()

with col_status:
    st.subheader("NPC Status")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("Friendliness", f'{p.moods["friendliness"]:.0%}')
        st.metric("Energy", f'{p.moods["energy"]:.0%}')
    with col_m2:
        st.metric("Suspicion", f'{p.moods["suspicion"]:.0%}')

    if st.session_state.last_analysis:
        a = st.session_state.last_analysis
        st.divider()
        st.subheader("Sentiment Analysis")
        st.caption(f"Sentiment: **{a['sentiment'].capitalize()}**")
        st.caption(f"Score: {a['score']:.2f}")
        st.caption(f"Aggression: {a['aggression']:.2f}")

    st.divider()
    llm_status = "Connected" if p.has_llm else "Mock Mode (set OPENAI_API_KEY)"
    st.caption(f"LLM: {llm_status}")
