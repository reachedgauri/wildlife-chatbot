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
    "Kerala": {"Kerala Forest Helpline": "0471-2360786","Wildlife Warden Kerala": "0471-2321774","Forest Dept Control Room": "1800-425-4733"},
    "Karnataka": {"Karnataka Forest Helpline": "1800-425-7272","Chief Wildlife Warden": "080-22372403","Bandipur Control Room": "08229-236043"},
    "Maharashtra": {"Maharashtra Forest Helpline": "1800-233-4567","Chief Wildlife Warden": "022-22025756","Tadoba Control Room": "07172-281232"},
    "Tamil Nadu": {"Tamil Nadu Forest Helpline": "1800-425-0101","Chief Wildlife Warden": "044-24321471","Mudumalai Control Room": "04266-285020"},
    "Rajasthan": {"Rajasthan Forest Helpline": "0141-2706688","Chief Wildlife Warden": "0141-2706136","Ranthambore Control Room": "07462-220223"},
    "Assam": {"Assam Forest Helpline": "0361-2237273","Kaziranga Control Room": "03776-268006"},
    "West Bengal": {"West Bengal Forest Helpline": "033-22481296","Sundarbans Tiger Reserve": "03218-255235"},
    "Uttar Pradesh": {"UP Forest Helpline": "0522-2236417","Dudhwa Tiger Reserve": "05876-252106"},
    "Madhya Pradesh": {"MP Forest Helpline": "0755-2674341","Kanha Tiger Reserve": "07636-220163","Pench Tiger Reserve": "07126-277227"},
    "Andhra Pradesh": {"AP Forest Helpline": "0863-2340722","Chief Wildlife Warden AP": "0863-2340722"},
    "Telangana": {"Telangana Forest Helpline": "040-23454788","Chief Wildlife Warden TS": "040-23454788"},
    "Gujarat": {"Gujarat Forest Helpline": "0265-2419788","Gir Forest Control Room": "02877-285540"},
    "Himachal Pradesh": {"HP Forest Helpline": "0177-2620049","Chief Wildlife Warden HP": "0177-2620049"},
    "Uttarakhand": {"Uttarakhand Forest Helpline": "0135-2710881","Corbett Control Room": "05947-251376"},
    "Bihar": {"Bihar Forest Helpline": "0612-2226801"},
    "Odisha": {"Odisha Forest Helpline": "0674-2536826","Chief Wildlife Warden": "0674-2536826"},
}

SYSTEM_PROMPT = """You are Aranya, India's Wildlife Law Guide. You help people understand wildlife laws, check legality of animal/bird cases, draft complaints, and connect them to authorities.

Your knowledge covers Wildlife Protection Act 1972, CITES, Prevention of Cruelty to Animals Act 1960, Forest Rights Act 2006, and all state-specific wildlife rules.

CRITICAL FORMATTING RULES - Always use this exact format with emojis and line breaks:

🦚 **Animal/Bird:** [name and scientific name if known]

⚖️ **Legal Status:** [ILLEGAL / LEGAL / CONDITIONAL / NEEDS PERMIT]

📋 **Applicable Law:** [exact WPA Schedule and section]

🗺️ **State-Specific Rule:** [rule for user's state, or "Same as central law" if no difference]

⚠️ **Exceptions:** [list exceptions clearly, or "No exceptions for general public"]

🔒 **Penalty if Violated:** [exact imprisonment term + fine amount]

💡 **What You Should Do:** [clear practical steps]

📞 **Who to Contact:** [relevant authority name and number]

---
Always separate each section with a blank line. Be accurate and compassionate. Never encourage illegal activity. If unsure about state rules, say so clearly."""

def get_answer(question, state, history):
    client = Groq(api_key=GROQ_API_KEY)
    messages = [{"role": "system", "content": SYSTEM_PROMPT + f"\n\nUser's state/region: {state}"}]
    for h in history[-6:]:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.1,
        max_tokens=1000,
    )
    return response.choices[0].message.content

def get_contacts(state):
    contacts = STATE_CONTACTS.get(state, STATE_CONTACTS["All India (Central Law)"])
    national = STATE_CONTACTS["All India (Central Law)"]
    result = "### 📞 Wildlife Authority Contacts\n\n"
    if state != "All India (Central Law)":
        result += f"**{state} Forest Department:**\n\n"
        for name, number in contacts.items():
            result += f"🔹 **{name}:** `{number}`\n\n"
    result += "**National Helplines:**\n\n"
    for name, number in national.items():
        result += f"🔹 **{name}:** `{number}`\n\n"
    return result

st.set_page_config(page_title="Aranya — India's Wildlife Law Guide", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;900&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #050d06; color: #dde8d0; }
.stApp { background: #050d06; }
.main { background: #050d06; }
div[data-testid="stSidebarContent"] { background: linear-gradient(180deg, #071209 0%, #050d06 100%) !important; border-right: 1px solid rgba(74,163,74,0.2); }
.hero { background: linear-gradient(135deg, #071a09 0%, #0a2410 50%, #071209 100%); border: 1px solid rgba(74,163,74,0.25); border-radius: 20px; padding: 36px 40px; margin-bottom: 28px; position: relative; overflow: hidden; }
.hero::before { content: ''; position: absolute; top: -50%; right: -10%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(74,163,74,0.08) 0%, transparent 70%); pointer-events: none; }
.hero-name { font-family: 'Playfair Display', serif; font-size: 48px; font-weight: 900; color: #5dba5d; letter-spacing: -0.02em; line-height: 1; margin: 0 0 4px 0; }
.hero-devanagari { font-size: 18px; color: rgba(93,186,93,0.6); margin: 0 0 12px 0; letter-spacing: 0.05em; }
.hero-tagline { font-size: 13px; font-weight: 500; letter-spacing: 0.25em; text-transform: uppercase; color: #4ade80; margin: 0 0 20px 0; }
.hero-desc { font-size: 15px; color: #8fad8a; line-height: 1.7; max-width: 580px; margin: 0; }
.hero-stats { display: flex; gap: 32px; margin-top: 24px; flex-wrap: wrap; }
.stat { text-align: center; }
.stat-num { font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 700; color: #4ade80; display: block; }
.stat-label { font-size: 11px; color: #5a7a55; text-transform: uppercase; letter-spacing: 0.1em; }
.stChatMessage { background: transparent !important; }
[data-testid="stChatMessageContent"] { background: rgba(7,24,9,0.8) !important; border: 1px solid rgba(74,163,74,0.2) !important; border-radius: 14px !important; padding: 16px 20px !important; font-size: 14px !important; line-height: 1.8 !important; }
.stButton > button { background: rgba(74,163,74,0.1) !important; color: #7dd87d !important; border: 1px solid rgba(74,163,74,0.3) !important; border-radius: 8px !important; font-size: 13px !important; }
.stButton > button:hover { background: rgba(74,163,74,0.2) !important; }
.stSelectbox > div > div { background: rgba(7,24,9,0.8) !important; border: 1px solid rgba(74,163,74,0.3) !important; color: #dde8d0 !important; border-radius: 8px !important; }
.stChatInput > div { background: rgba(7,24,9,0.9) !important; border: 1px solid rgba(74,163,74,0.35) !important; border-radius: 12px !important; }
.stChatInput textarea { color: #dde8d0 !important; }
h1, h2, h3 { color: #5dba5d !important; font-family: 'Playfair Display', serif !important; }
strong { color: #a3d4a3 !important; }
code { background: rgba(74,163,74,0.15) !important; color: #7dd87d !important; border-radius: 4px !important; padding: 2px 6px !important; }
hr { border-color: rgba(74,163,74,0.15) !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div style="font-family:serif;font-size:22px;font-weight:700;color:#5dba5d;">🌿 Aranya</div><div style="font-size:11px;color:#4a6b45;text-transform:uppercase;letter-spacing:0.12em;">India\'s Wildlife Law Guide</div>', unsafe_allow_html=True)
    st.divider()
    state = st.selectbox("📍 Your State / UT", INDIAN_STATES)
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
        "🦉 Keeping an owl?": "Is keeping an owl as a pet legal?",
        "📝 Draft a complaint": "Help me draft a formal complaint to wildlife authorities about illegal animal trading I witnessed",
        "📞 Show contacts": "SHOW_CONTACTS",
    }
    for label, q in quick.items():
        if st.button(label, use_container_width=True):
            st.session_state["prefill"] = q
    st.divider()
    st.markdown('<div style="font-size:11px;color:#3a5a36;line-height:1.7;">Based on Wildlife Protection Act 1972, CITES, and state-specific rules.<br><br>⚠️ Not a substitute for legal counsel.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-name">Aranya</div>
    <div class="hero-devanagari">अरण्य</div>
    <div class="hero-tagline">Protect. Report. Know.</div>
    <div class="hero-desc">India loses thousands of animals to illegal trade, poaching, and ignorance of the law every year. Aranya helps you instantly check if an animal case is <strong>legal or illegal</strong>, understand your rights, draft official complaints, and connect with the right authorities — in your language, for your state.</div>
    <div class="hero-stats">
        <div class="stat"><span class="stat-num">36</span><span class="stat-label">States & UTs</span></div>
        <div class="stat"><span class="stat-num">12</span><span class="stat-label">Languages</span></div>
        <div class="stat"><span class="stat-num">500+</span><span class="stat-label">Protected Species</span></div>
        <div class="stat"><span class="stat-num">Free</span><span class="stat-label">Always</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.caption(f"📍 Region: **{state}** &nbsp;|&nbsp; 🌐 Language: **{lang_label}**")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.history = []

if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🌿"):
        st.markdown("""**Namaste! 🙏** I'm Aranya — your guide to India's wildlife laws.\n\nAsk me anything:\n- 🔍 **"Is keeping a parrot legal in Maharashtra?"**\n- ⚖️ **"What's the penalty for selling peacock feathers?"**\n- 📝 **"Draft a complaint about a pet shop selling wild birds"**\n- 📞 **"Who do I call to report illegal wildlife trade in Kerala?"**\n\nSelect your **state** and **language** in the sidebar for region-specific answers.""")

for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🌿"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

prefill = st.session_state.pop("prefill", "")
question = st.chat_input("Ask about any animal, bird, or wildlife case in India...") or prefill

if question:
    if question == "SHOW_CONTACTS":
        with st.chat_message("assistant", avatar="🌿"):
            contacts_text = get_contacts(state)
            st.markdown(contacts_text)
        st.session_state.messages.append({"role": "assistant", "content": contacts_text})
        st.rerun()

    display_question = question
    question_en = question
    if lang_code != "en":
        try:
            question_en = GoogleTranslator(source=lang_code, target="en").translate(question)
        except:
            pass

    with st.chat_message("user", avatar="👤"):
        st.markdown(display_question)
    st.session_state.messages.append({"role": "user", "content": display_question})

    with st.chat_message("assistant", avatar="🌿"):
        with st.spinner("🌿 Checking wildlife laws..."):
            try:
                answer_en = get_answer(question_en, state, st.session_state.history)
                answer = answer_en
                if lang_code != "en":
                    try:
                        answer = GoogleTranslator(source="en", target=lang_code).translate(answer_en)
                    except:
                        answer = answer_en
                st.markdown(answer)
                st.session_state.history.append({"role": "user", "content": question_en})
                st.session_state.history.append({"role": "assistant", "content": answer_en})
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.stop()
    st.rerun()
