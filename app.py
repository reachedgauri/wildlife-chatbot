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

* { font-family: 'DM Sans', sans-serif !important; }

/* Force dark theme */
html, body, .stApp, .main, [class*="css"] {
    background-color: #060e07 !important;
    color: #d4e8c2 !important;
}

section[data-testid="stSidebar"] > div {
    background: #071209 !important;
    border-right: 1px solid #1a3d1e !important;
}

/* Hero */
.aranya-hero {
    background: linear-gradient(135deg, #0b2a10 0%, #0f3a16 60%, #091f0d 100%);
    border: 1px solid #2d6e35;
    border-radius: 16px;
    padding: 40px 44px;
    margin-bottom: 24px;
}
.aranya-title {
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: 52px !important;
    font-weight: 900 !important;
    color: #6fcf6f !important;
    line-height: 1 !important;
    margin: 0 !important;
}
.aranya-deva {
    font-size: 16px;
    color: #4a9450;
    margin: 4px 0 10px 2px;
    letter-spacing: 2px;
}
.aranya-tag {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4ade80;
    margin-bottom: 18px;
}
.aranya-desc {
    font-size: 15px;
    color: #8fbd8a;
    line-height: 1.75;
    max-width: 600px;
    margin-bottom: 28px;
}
.aranya-stats {
    display: flex;
    gap: 36px;
    flex-wrap: wrap;
    border-top: 1px solid #1e4d24;
    padding-top: 20px;
}
.aranya-stat-num {
    font-family: 'Playfair Display', serif !important;
    font-size: 28px;
    font-weight: 700;
    color: #4ade80;
    display: block;
    line-height: 1;
}
.aranya-stat-label {
    font-size: 10px;
    color: #4a7a4e;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 4px;
    display: block;
}

/* Chat bubbles */
.stChatMessage {
    background: transparent !important;
    padding: 4px 0 !important;
}
[data-testid="stChatMessageContent"] {
    background: #0e2412 !important;
    border: 1px solid #2a5530 !important;
    border-radius: 12px !important;
    padding: 18px 22px !important;
    color: #d4e8c2 !important;
    font-size: 14.5px !important;
    line-height: 1.85 !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3) !important;
}

/* User message different color */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
    background: #132b17 !important;
    border-color: #3a7040 !important;
}

/* Input */
[data-testid="stChatInput"] {
    background: #0e2412 !important;
    border: 1.5px solid #2d6e35 !important;
    border-radius: 12px !important;
    padding: 4px 8px !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #d4e8c2 !important;
    font-size: 14px !important;
}

/* Buttons */
.stButton > button {
    background: #0e2412 !important;
    color: #6fcf6f !important;
    border: 1px solid #2d6e35 !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    padding: 8px 12px !important;
    transition: all 0.15s ease !important;
    text-align: left !important;
}
.stButton > button:hover {
    background: #163620 !important;
    border-color: #4ade80 !important;
    color: #a3f0a3 !important;
}

/* Selects */
[data-baseweb="select"] > div {
    background: #0e2412 !important;
    border: 1px solid #2d6e35 !important;
    border-radius: 8px !important;
    color: #d4e8c2 !important;
}

/* Divider */
hr { border-color: #1a3d1e !important; margin: 12px 0 !important; }

/* Strong / bold in responses */
strong, b { color: #a3f0a3 !important; }
code { background: rgba(74,222,128,0.12) !important; color: #6fcf6f !important; border-radius: 4px !important; padding: 2px 7px !important; font-size: 13px !important; }

/* Caption */
.stCaption { color: #4a7a4e !important; font-size: 12px !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 16px 0;">
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:24px;font-weight:800;color:#6fcf6f;">🌿 Aranya</div>
        <div style="font-size:10px;color:#3d6b42;text-transform:uppercase;letter-spacing:2px;margin-top:3px;">India's Wildlife Law Guide</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    state = st.selectbox("📍 Your State / UT", INDIAN_STATES)
    lang_label = st.selectbox("🌐 Language", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[lang_label]
    st.divider()
    st.markdown("<div style='font-size:12px;color:#4a7a4e;font-weight:600;margin-bottom:8px;'>Quick Actions</div>", unsafe_allow_html=True)
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
    st.markdown("<div style='font-size:11px;color:#2d5530;line-height:1.7;'>Based on Wildlife Protection Act 1972, CITES, and state-specific rules.<br><br>⚠️ Not a substitute for legal counsel.</div>", unsafe_allow_html=True)

# Hero
st.markdown(f"""
<div class="aranya-hero">
    <div class="aranya-title">Aranya</div>
    <div class="aranya-deva">अरण्य</div>
    <div class="aranya-tag">✦ Protect &nbsp;·&nbsp; Report &nbsp;·&nbsp; Know ✦</div>
    <div class="aranya-desc">
        India loses thousands of animals to illegal trade, poaching, and ignorance of the law every year.
        <strong>Aranya</strong> helps you instantly check if an animal case is legal or illegal,
        understand your rights, draft official complaints, and reach the right authorities —
        in your language, for your state.
    </div>
    <div class="aranya-stats">
        <div><span class="aranya-stat-num">36</span><span class="aranya-stat-label">States & UTs</span></div>
        <div><span class="aranya-stat-num">12</span><span class="aranya-stat-label">Languages</span></div>
        <div><span class="aranya-stat-num">500+</span><span class="aranya-stat-label">Species Covered</span></div>
        <div><span class="aranya-stat-num">Free</span><span class="aranya-stat-label">Always</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.caption(f"📍 {state}  ·  🌐 {lang_label}")

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.history = []

if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🌿"):
        st.markdown("""**Namaste! 🙏** I'm Aranya — your guide to India's wildlife laws.

Ask me anything:
- 🔍 **"Is keeping a parrot legal in Maharashtra?"**
- ⚖️ **"What's the penalty for selling peacock feathers?"**
- 📝 **"Draft a complaint about a pet shop selling wild birds"**
- 📞 **"Who do I call to report illegal wildlife trade in Kerala?"**

Select your **state** and **language** in the sidebar for region-specific answers.""")

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
