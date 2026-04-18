import streamlit as st
from groq import Groq
from deep_translator import GoogleTranslator

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

INDIAN_STATES = [
    "All India (Central Law)","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar",
    "Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand",
    "Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya",
    "Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu",
    "Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
    "Andaman & Nicobar","Chandigarh","Delhi (NCT)","Jammu & Kashmir",
    "Ladakh","Lakshadweep","Puducherry"
]

LANGUAGES = {
    "English":"en","हिंदी (Hindi)":"hi","தமிழ் (Tamil)":"ta",
    "తెలుగు (Telugu)":"te","ಕನ್ನಡ (Kannada)":"kn","മലയാളം (Malayalam)":"ml",
    "मराठी (Marathi)":"mr","বাংলা (Bengali)":"bn","ગુજરાતી (Gujarati)":"gu",
    "ਪੰਜਾਬੀ (Punjabi)":"pa","ଓଡ଼ିଆ (Odia)":"or","অসমীয়া (Assamese)":"as",
}

STATE_CONTACTS = {
    "All India (Central Law)": {
        "Wildlife Crime Control Bureau (WCCB)": "011-23370217",
        "Wildlife SOS Emergency": "9871963535",
        "WWF India": "011-41504814",
        "Project Tiger Directorate": "011-23073017",
        "Ministry of Environment": "011-24695271",
    },
    "Kerala": {
        "Kerala Forest Helpline": "0471-2360786",
        "Wildlife Warden Kerala": "0471-2321774",
        "Wildlife SOS Kerala": "9871963535",
        "Forest Dept Control Room": "1800-425-4733",
    },
    "Karnataka": {
        "Karnataka Forest Helpline": "1800-425-7272",
        "Chief Wildlife Warden": "080-22372403",
        "Bandipur Control Room": "08229-236043",
        "Nagarhole Control Room": "08274-252041",
    },
    "Maharashtra": {
        "Maharashtra Forest Helpline": "1800-233-4567",
        "Chief Wildlife Warden": "022-22025756",
        "Tadoba Control Room": "07172-281232",
    },
    "Tamil Nadu": {
        "Tamil Nadu Forest Helpline": "1800-425-0101",
        "Chief Wildlife Warden": "044-24321471",
        "Mudumalai Control Room": "04266-285020",
    },
    "Rajasthan": {
        "Rajasthan Forest Helpline": "0141-2706688",
        "Chief Wildlife Warden": "0141-2706136",
        "Ranthambore Control Room": "07462-220223",
    },
    "Assam": {
        "Assam Forest Helpline": "0361-2237273",
        "Kaziranga Control Room": "03776-268006",
        "Wildlife Crime Cell Assam": "0361-2237271",
    },
    "West Bengal": {
        "West Bengal Forest Helpline": "033-22481296",
        "Sundarbans Tiger Reserve": "03218-255235",
        "Chief Wildlife Warden WB": "033-22485190",
    },
    "Uttar Pradesh": {
        "UP Forest Helpline": "0522-2236417",
        "Dudhwa Tiger Reserve": "05876-252106",
        "Chief Wildlife Warden UP": "0522-2236417",
    },
    "Madhya Pradesh": {
        "MP Forest Helpline": "0755-2674341",
        "Kanha Tiger Reserve": "07636-220163",
        "Pench Tiger Reserve": "07126-277227",
        "Chief Wildlife Warden MP": "0755-2674244",
    },
}

SYSTEM_PROMPT = """You are an expert Indian wildlife law advisor. You help users understand if animal/bird cases are legal or illegal, draft complaints, and provide guidance.

Your knowledge covers:
- Wildlife Protection Act 1972 (WPA) - all schedules and amendments
- Schedule I (Tiger, Lion, Elephant, Rhino, Peacock, King Cobra, Python, Sea Turtle) - 3-7 years imprisonment
- Schedule II (Mongoose, Monitor Lizard, Blackbuck, Wild Boar) - 1-3 years
- Schedule IV (Parrots, Owls, Flamingo) - up to 3 years
- Schedule V Vermin (Crow, Rat, Fruit Bat) - legal to kill
- CITES Appendix I and II listings
- State-specific rules for all Indian states
- Prevention of Cruelty to Animals Act 1960
- Forest Rights Act 2006

For legal/illegal queries, always structure your answer as:
🦚 **Animal/Bird:** [name]
⚖️ **Legal Status:** LEGAL / ILLEGAL / CONDITIONAL
📋 **Law:** [exact WPA Schedule/section]
🗺️ **State Rule:** [specific rule for user's state if any]
⚠️ **Exceptions:** [if any exist]
🔒 **Penalty:** [imprisonment + fine]
💡 **What to do:** [practical advice]

For complaint drafting, write a formal complaint letter to the Forest Department.
For contact numbers, provide the relevant authority contacts.
Be accurate, helpful, and clear. Never encourage illegal activity."""

def get_answer(question, state, history):
    client = Groq(api_key=GROQ_API_KEY)
    messages = [{"role": "system", "content": SYSTEM_PROMPT + f"\n\nUser's state: {state}"}]
    for h in history[-6:]:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.1,
        max_tokens=1000,
    )
    return response.choices[0].message.content

def get_contacts(state):
    contacts = STATE_CONTACTS.get(state, STATE_CONTACTS["All India (Central Law)"])
    national = STATE_CONTACTS["All India (Central Law)"]
    result = f"### 📞 Wildlife Authority Contacts\n\n"
    if state != "All India (Central Law)":
        result += f"**{state} Forest Department:**\n"
        for name, number in contacts.items():
            result += f"- {name}: `{number}`\n"
        result += "\n"
    result += "**National Helplines:**\n"
    for name, number in national.items():
        result += f"- {name}: `{number}`\n"
    return result

# ── UI ──────────────────────────────────────────────────
st.set_page_config(page_title="Wildlife Law Advisor — India", page_icon="🦚", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #0a0f0a; color: #e2e8f0; }
.stApp { background: #0a0f0a; }
.main { background: #0a0f0a; }
div[data-testid="stSidebarContent"] { background: #0d1a0e !important; border-right: 1px solid #1a3a1e; }
.stChatMessage { background: transparent !important; }
[data-testid="stChatMessageContent"] { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 12px !important; }
.stButton > button { background: linear-gradient(135deg,#166534,#15803d) !important; color: white !important; border: none !important; border-radius: 8px !important; }
.stSelectbox > div > div { background: rgba(255,255,255,0.05) !important; border: 1px solid #1a5c2a !important; color: #e2e8f0 !important; }
.stTextInput > div > div > input { background: rgba(255,255,255,0.05) !important; border: 1px solid #1a5c2a !important; color: #e2e8f0 !important; }
h1, h2, h3 { color: #4ade80 !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🦚 Wildlife Law Advisor")
    st.caption("India • WPA 1972 • Free for all users")
    st.divider()
    state = st.selectbox("📍 Your State", INDIAN_STATES)
    lang_label = st.selectbox("🌐 Language", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[lang_label]
    st.divider()
    st.markdown("**Quick Actions:**")
    quick = {
        "🦜 Can I keep a parrot?": "Can I keep a parrot at home?",
        "🦚 Peacock feather trade?": "Is trading peacock feathers legal?",
        "🐍 Snake charming legal?": "Is snake charming legal in India?",
        "🐢 Selling turtle eggs?": "Is selling turtle eggs legal?",
        "🐘 Private elephant?": "Can I privately own an elephant?",
        "📝 Draft a complaint": "Help me draft a complaint to wildlife authorities about illegal animal trading I witnessed",
        "📞 Show contacts": "SHOW_CONTACTS",
    }
    for label, q in quick.items():
        if st.button(label, use_container_width=True):
            st.session_state["prefill"] = q
    st.divider()
    st.caption("⚠️ Not a substitute for legal advice")

# Main
st.markdown("# 🦚 Wildlife Law Advisor — India")
st.caption(f"Region: **{state}** | Language: **{lang_label}**")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.history = []

# Show welcome
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("""**Namaste! 🙏** I can help you with:
- ✅ Is keeping/trading/hunting this animal **legal or illegal**?
- 📝 **Draft a complaint** to wildlife authorities
- 📞 **Contact numbers** of wildlife departments
- 🗺️ **State-specific rules** for all Indian states
- 🌐 Answers in **12 Indian languages**

Ask me anything about any animal or bird case in India!""")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prefill = st.session_state.pop("prefill", "")
question = st.chat_input("Ask about any animal, bird, or wildlife case...") or prefill

if question:
    # Handle contacts shortcut
    if question == "SHOW_CONTACTS":
        with st.chat_message("assistant"):
            contacts_text = get_contacts(state)
            st.markdown(contacts_text)
        st.session_state.messages.append({"role": "assistant", "content": contacts_text})
        st.rerun()

    # Translate to English if needed
    display_question = question
    if lang_code != "en":
        try:
            question_en = GoogleTranslator(source=lang_code, target="en").translate(question)
        except:
            question_en = question
    else:
        question_en = question

    with st.chat_message("user"):
        st.markdown(display_question)
    st.session_state.messages.append({"role": "user", "content": display_question})

    with st.chat_message("assistant"):
        with st.spinner("Checking wildlife laws..."):
            try:
                answer_en = get_answer(question_en, state, st.session_state.history)
                if lang_code != "en":
                    try:
                        answer = GoogleTranslator(source="en", target=lang_code).translate(answer_en)
                    except:
                        answer = answer_en
                else:
                    answer = answer_en
                st.markdown(answer)
                st.session_state.history.append({"role": "user", "content": question_en})
                st.session_state.history.append({"role": "assistant", "content": answer_en})
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.stop()
    st.rerun()
