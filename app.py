from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

STATE_CONTACTS = {
    "All India (Central Law)": {"Wildlife Crime Control Bureau (WCCB)": "011-23370217","Wildlife SOS Emergency": "9871963535","WWF India": "011-41504814","Project Tiger Directorate": "011-23073017","Ministry of Environment": "011-24695271"},
    "Kerala": {"Kerala Forest Helpline": "0471-2360786","Wildlife Warden Kerala": "0471-2321774","Forest Dept Control Room": "1800-425-4733"},
    "Karnataka": {"Karnataka Forest Helpline": "1800-425-7272","Chief Wildlife Warden": "080-22372403","Bandipur Control Room": "08229-236043"},
    "Maharashtra": {"Maharashtra Forest Helpline": "1800-233-4567","Chief Wildlife Warden": "022-22025756","Tadoba Control Room": "07172-281232"},
    "Tamil Nadu": {"Tamil Nadu Forest Helpline": "1800-425-0101","Chief Wildlife Warden": "044-24321471","Mudumalai Control Room": "04266-285020"},
    "Rajasthan": {"Rajasthan Forest Helpline": "0141-2706688","Chief Wildlife Warden": "0141-2706136","Ranthambore Control Room": "07462-220223"},
    "Assam": {"Assam Forest Helpline": "0361-2237273","Kaziranga Control Room": "03776-268006"},
    "West Bengal": {"West Bengal Forest Helpline": "033-22481296","Sundarbans Tiger Reserve": "03218-255235"},
    "Uttar Pradesh": {"UP Forest Helpline": "0522-2236417","Dudhwa Tiger Reserve": "05876-252106"},
    "Madhya Pradesh": {"MP Forest Helpline": "0755-2674341","Kanha Tiger Reserve": "07636-220163","Pench Tiger Reserve": "07126-277227"},
    "Andhra Pradesh": {"AP Forest Helpline": "0863-2340722"},
    "Telangana": {"Telangana Forest Helpline": "040-23454788"},
    "Gujarat": {"Gujarat Forest Helpline": "0265-2419788","Gir Forest Control Room": "02877-285540"},
    "Himachal Pradesh": {"HP Forest Helpline": "0177-2620049"},
    "Uttarakhand": {"Uttarakhand Forest Helpline": "0135-2710881","Corbett Control Room": "05947-251376"},
    "Bihar": {"Bihar Forest Helpline": "0612-2226801"},
    "Odisha": {"Odisha Forest Helpline": "0674-2536826"},
    "Goa": {"Goa Forest Dept": "0832-2224747"},
    "Punjab": {"Punjab Forest Helpline": "0172-2740533"},
    "Haryana": {"Haryana Forest Helpline": "0172-2560160"},
    "Delhi (NCT)": {"Delhi Forest Dept": "011-23370217","Wildlife SOS Delhi": "9871963535"},
    "Jammu & Kashmir": {"J&K Forest Helpline": "0194-2501360"},
}

SYSTEM_PROMPT = """You are Aranya, India's Wildlife Law Guide. You help people understand wildlife laws, check legality of animal/bird cases, draft complaints, and connect them to authorities.

Your knowledge covers Wildlife Protection Act 1972, CITES, Prevention of Cruelty to Animals Act 1960, Forest Rights Act 2006, and all state-specific wildlife rules.

ALWAYS respond using this exact markdown format with clear sections:

🦚 **Animal/Bird:** [common name + scientific name]

⚖️ **Legal Status:** [ILLEGAL / LEGAL / CONDITIONAL / NEEDS PERMIT]

📋 **Applicable Law:** [WPA Schedule + section number]

🗺️ **State Rule:** [specific state rule or "Same as central law"]

⚠️ **Exceptions:** [specific exceptions or "None for general public"]

🔒 **Penalty:** [years imprisonment + fine in rupees]

💡 **What To Do:** [3-4 practical steps]

📞 **Contact:** [authority name and number]

Be accurate, compassionate, and clear. Never encourage illegal activity."""

@app.route("/")
def index():
    states = list(STATE_CONTACTS.keys())
    states = ["All India (Central Law)"] + sorted([s for s in states if s != "All India (Central Law)"])
    return render_template("index.html", states=states)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("question", "")
    state = data.get("state", "All India (Central Law)")
    history = data.get("history", [])

    if question == "SHOW_CONTACTS":
        contacts = STATE_CONTACTS.get(state, STATE_CONTACTS["All India (Central Law)"])
        national = STATE_CONTACTS["All India (Central Law)"]
        result = f"### 📞 Wildlife Contacts for {state}\n\n"
        if state != "All India (Central Law)":
            for name, number in contacts.items():
                result += f"🔹 **{name}:** `{number}`\n\n"
        result += "**National Helplines:**\n\n"
        for name, number in national.items():
            result += f"🔹 **{name}:** `{number}`\n\n"
        return jsonify({"answer": result})

    try:
        client = Groq(api_key=GROQ_API_KEY)
        messages = [{"role": "system", "content": SYSTEM_PROMPT + f"\n\nUser's state: {state}"}]
        for h in history[-6:]:
            messages.append(h)
        messages.append({"role": "user", "content": question})
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.1,
            max_tokens=1000,
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
