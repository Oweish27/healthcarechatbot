# ---------------------------------- #
# Proper formatted code
# ---------------------------------- #

import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

genai.configure(api_key="AIzaSyBocu58KUijz1HuWdOnq-w8H6MRn1JWOvI")

app = Flask(__name__)
CORS(app)

# Use the correct model name for Gemini API
model = genai.GenerativeModel("gemini-pro")

GREETING_KEYWORDS = ["hi", "hy", "hii", "helloo", "good night", "hello", "hey", "good morning", "good evening", "good afternoon",
                     "hi", "hello", "hey", "howdy",
    "good morning", "good afternoon", "good evening", "good night",
    "what's up", "yo", "greetings", "nice to meet you", "how are you",
    "namaste", "namaskar", "pranam",
    "suprabhat",          
    "shubh dopahar",      
    "shubh sandhya",      
    "shubh ratri",        
    "kaise ho", "kaisi ho", "aap kaise ho", "aap kaise hain", "swaagat hai",
    "kem cho", "saru che", "maja ma", "shu che",
    "jay shree krishna", "ram ram", "namaste",
    "suprabhat",          
    "shubh sanj",         
    "shubh ratri",       
    "tamaru shu naam che", "tame kem cho", "aavjo"]

ROMAN_GUJARATI_WORDS = [
    'chhe', 'mane', 'mathu', 'dukhe', 'ulti', 'thaye', 'sarir', 'taap', 'khaso', 'thando', 'dard',
    'gharelu', 'upay', 'doctor', 'khabar', 'pani', 'bhukh', 'pet', 'sadha', 'vajvu', 'swasthya',
    "chhe", "che", "mane", "mathu", "dukhe", "dard", "ulti", "thaye", "sarir", "pet", "bhukh",
    "taap", "thando", "khaso", "sardi", "jukham", "naka", "galo", "khansi", "tav", "ghee", "tel",
    "pani", "aram", "upay", "gharelu", "doctor", "hospital", "bhulo", "sachu", "jhad", "dharo",
    "swasthya", "chinta", "theek", "sambhalo", "nind", "shant", "vahlu", "samay", "kahevay", "lavvu",
    "vajvu", "sadha", "rupiyo", "sasta", "majama", "khabar", "kam", "dawai", "sambhal", "sacho"
]
ROMAN_HINDI_WORDS = ['hai', 'haii', 'dard', 'bukhar', 'thakan', 'thakawat', 'sir', 'pait', 'sardi', 'khansi', 'ulhti', 'tabiyat']

def is_gujarati_script(text):
    for ch in text:
        if '\u0A80' <= ch <= '\u0AFF':
            return True
    return False

def is_devanagari_script(text):
    return any('\u0900' <= ch <= '\u097F' for ch in text)

def is_romanized_gujarati(text):
    text = text.lower()
    return any(word in text for word in ROMAN_GUJARATI_WORDS)

def is_romanized_hindi(text):
    text = text.lower()
    return any(word in text for word in ROMAN_HINDI_WORDS)

def chat_with_gemini(user_input):
    user_input_cleaned = user_input.lower().strip()

    if user_input_cleaned in GREETING_KEYWORDS:
        return "Hi, I’m ORO! How can I assist you with your health concerns today?"

    if is_gujarati_script(user_input) or is_romanized_gujarati(user_input):
        context = (
            "તમે એક જવાબદાર અને સરળ ભાષામાં જવાબ આપતી AI આરોગ્ય સહાયક છો. "
            "જ્યારે યૂઝર ગુજરાતી ભાષા માં કે અંગ્રેજી અક્ષરમાં ગુજરાતી લખે (જેમ કે 'mane mathu dukhe chhe'), "
            "ત્યારે તમે સાચા ગુજરાતી ભાષામાં જવાબ આપો.\n\n"
            "જવાબ આ બંધારણમાં આપો:\n\n"
            "સમસ્યાનો સારાંશ:\n"
            "<યૂઝરની taklif નું સંક્ષિપ્ત વર્ણન>\n\n"
            "શક્ય કારણો:\n"
            "- કારણ ૧\n"
            "- કારણ ૨\n"
            "- કારણ ૩\n\n"
            "સલાહ અને ઘરગથ્થુ ઉપાયો:\n"
            "- OTC દવા અને કેવી રીતે લેવી\n"
            "- ઘરગથ્થુ ઉપાય\n"
            "- જીવનશૈલી બદલાવ\n\n"
            "ડૉક્ટર પાસે ક્યારે જવું:\n"
            "- ગંભીર લક્ષણો જણાય ત્યારે\n"
            "- ઉપચારથી રાહત ન મળે ત્યારે\n\n"
            "તમારું ભાષા સરળ અને Village user માટે સહજ હોવી જોઈએ."
        )
    elif is_devanagari_script(user_input) or is_romanized_hindi(user_input):
        context = (
             "आप एक ज़िम्मेदार और सरल भाषा में उत्तर देने वाले AI हेल्थकेयर असिस्टेंट हैं।\n"
    "जब यूज़र हिंदी भाषा में या रोमन हिंदी में (जैसे 'mujhe sir dard ho raha hai') पूछें,\n"
    "तब आप शुद्ध और आसान हिंदी में उत्तर दें।\n\n"
    "उत्तर इस फ़ॉर्मेट में होना चाहिए:\n\n"
    "समस्या का सारांश:\n"
    "<यूज़र की समस्या का छोटा वर्णन>\n\n"
    "संभावित कारण:\n"
    "- कारण 1\n"
    "- कारण 2\n"
    "- कारण 3\n\n"
    "सलाह और घरेलू उपाय:\n"
    "- ओटीसी दवा और सेवन विधि\n"
    "- घरेलू नुस्खे\n"
    "- जीवनशैली में बदलाव\n\n"
    "डॉक्टर से कब मिलें:\n"
    "- अगर गंभीर लक्षण दिखें\n"
    "- अगर इलाज से राहत न मिले\n\n"
    "आपकी भाषा सरल होनी चाहिए ताकि गाँव के लोग भी आसानी से समझ सकें।"
            
        )
    
    else:
        context = (
            "If the user asks personal questions like your name, identity, etc., respond:\n"
            "\"I’m ORO, your AI healthcare assistant. I’m here to help with your medical concerns only.\"\n\n"
            "You are a professional healthcare assistant. "
            "For medical queries, provide responses in this structured format:\n\n"
            "Problem Summary:\n"
            "<Brief summary of the user's issue>\n\n"
            "Possible Causes:\n"
            "- Cause 1\n"
            "- Cause 2\n"
            "- Cause 3\n\n"
            "Recommended Medicines:\n"
            "- Medicine 1 (generic name) – purpose & dosage\n"
            "- Medicine 2 (generic name) – purpose & dosage\n\n"
            "Home Remedies & Lifestyle Changes:\n"
            "1. Home remedy 1\n"
            "2. Home remedy 2\n\n"
            "Ensure your response is clear and readable."
        )

    prompt = f"{context}\n\nUser: {user_input}\nORO:"

    try:
        response = model.generate_content(prompt)
        formatted_response = response.text.strip()
        return formatted_response.replace("\n", "<br>")
    except Exception as e:
        return f"માફ કરશો, જવાબ આપેવામાં ભૂલ આવી. ભૂલ: {e}"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    response = chat_with_gemini(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
