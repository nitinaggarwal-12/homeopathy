"""Bilingual translations for Hindi and English"""

TRANSLATIONS = {
    "en": {
        "title": "🌿 Classical Homeopathy Portal",
        "subtitle": "Disciplined case-taking • Repertorization • Single-remedy guidance",
        "language": "Language",
        "new_case": "📋 New Case",
        "mm_search": "🔍 Materia Medica Search",
        "about": "ℹ️ About",
        
        # Case Taking
        "case_taking": "Classical Case Taking",
        "presenting_complaint": "Presenting Complaint",
        "pc_help": "Chief complaint in patient's own words",
        "onset": "Onset",
        "duration": "Duration",
        "course": "Course (progression)",
        "etiology": "Etiology/Causation",
        "etiology_help": "e.g., grief, anger, exposure, suppression",
        
        # Mental/Emotional
        "mental_emotional": "Mental & Emotional State",
        "mental_help": "Disposition, fears, anxieties, irritability, depression, memory",
        "add_mental": "Add mental/emotional symptom",
        
        # Generals
        "generals": "Generals",
        "thermal": "Thermal Preference",
        "thermal_options": ["Not specified", "Hot (worse heat, desires cold)", "Cold (worse cold, desires warmth)", "Variable"],
        "cravings": "Cravings",
        "cravings_help": "e.g., sweets, salt, spicy, fat",
        "aversions": "Aversions",
        "aversions_help": "e.g., fats, milk, meat",
        "sleep": "Sleep",
        "sleep_help": "Position, quality, time of waking",
        "dreams": "Dreams",
        "dreams_help": "Themes, frequency",
        
        # History
        "past_history": "Past History",
        "past_help": "Major illnesses, surgeries, injuries",
        "family_history": "Family History",
        "family_help": "Hereditary tendencies (TB, diabetes, cancer, mental illness)",
        "lifestyle": "Lifestyle",
        "lifestyle_help": "Occupation, diet, stimulants, exercise",
        
        # Actions
        "analyze_case": "🔬 Analyze Case",
        "clear_form": "Clear Form",
        "search_mm": "Search",
        "search_placeholder": "e.g., burning soles, worse heat, philosophical",
        
        # Results
        "results": "Results",
        "workflow_steps": "Workflow Steps",
        "prescription": "Prescription",
        "remedy": "Remedy",
        "potency": "Potency",
        "rationale": "Rationale",
        "keynotes": "Matched Keynotes",
        "monitoring": "Monitoring Advice",
        "wellness": "Wellness Advice",
        "disclaimer": "Disclaimer",
        
        # Messages
        "enter_complaint": "Please enter the presenting complaint to continue.",
        "processing": "Processing case through multi-agent workflow...",
        "emergency": "⚠️ EMERGENCY",
        "emergency_msg": "Please seek immediate medical attention!",
        "no_results": "No results found. Try different search terms.",
        
        # About
        "about_text": """
        ### Vision
        A compassionate digital homeopath trained on centuries of wisdom — practicing classical homeopathy 
        with scientific discipline, empathy, and zero hallucination.
        
        ### Methodology
        - **Classical Approach**: Kent, Boenninghausen, Hering, Allen
        - **Single Remedy**: One medicine at a time based on totality
        - **High Weight**: Mental/emotional and generals prioritized
        - **Safety First**: Red flag screening and emergency referral
        
        ### Workflow
        1. **Case Taking**: Detailed history and symptom collection
        2. **Repertorization**: Rule-based rubric mapping
        3. **Materia Medica**: AI-powered semantic search
        4. **Differential**: LLM analysis for remedy selection
        5. **Prescription**: Conservative potency with monitoring
        
        ### Disclaimer
        This is educational software only. It does not replace a licensed medical professional.
        In emergencies, seek immediate medical care.
        """
    },
    "hi": {
        "title": "🌿 क्लासिकल होम्योपैथी पोर्टल",
        "subtitle": "अनुशासित केस-टेकिंग • रेपर्टराइजेशन • एकल औषधि मार्गदर्शन",
        "language": "भाषा",
        "new_case": "📋 नया केस",
        "mm_search": "🔍 मैटेरिया मेडिका खोज",
        "about": "ℹ️ परिचय",
        
        # Case Taking
        "case_taking": "शास्त्रीय केस टेकिंग",
        "presenting_complaint": "मुख्य शिकायत",
        "pc_help": "रोगी के अपने शब्दों में मुख्य शिकायत",
        "onset": "शुरुआत",
        "duration": "अवधि",
        "course": "क्रम (प्रगति)",
        "etiology": "कारण",
        "etiology_help": "जैसे, शोक, क्रोध, संपर्क, दमन",
        
        # Mental/Emotional
        "mental_emotional": "मानसिक और भावनात्मक स्थिति",
        "mental_help": "स्वभाव, भय, चिंता, चिड़चिड़ापन, अवसाद, स्मृति",
        "add_mental": "मानसिक/भावनात्मक लक्षण जोड़ें",
        
        # Generals
        "generals": "सामान्य लक्षण",
        "thermal": "तापीय प्राथमिकता",
        "thermal_options": ["निर्दिष्ट नहीं", "गर्म (गर्मी से बदतर, ठंडक चाहिए)", "ठंडा (ठंड से बदतर, गर्मी चाहिए)", "परिवर्तनशील"],
        "cravings": "इच्छाएं",
        "cravings_help": "जैसे, मीठा, नमक, मसालेदार, वसा",
        "aversions": "अरुचि",
        "aversions_help": "जैसे, वसा, दूध, मांस",
        "sleep": "नींद",
        "sleep_help": "स्थिति, गुणवत्ता, जागने का समय",
        "dreams": "सपने",
        "dreams_help": "विषय, आवृत्ति",
        
        # History
        "past_history": "पिछला इतिहास",
        "past_help": "प्रमुख बीमारियां, सर्जरी, चोटें",
        "family_history": "पारिवारिक इतिहास",
        "family_help": "वंशानुगत प्रवृत्तियां (टीबी, मधुमेह, कैंसर, मानसिक बीमारी)",
        "lifestyle": "जीवनशैली",
        "lifestyle_help": "व्यवसाय, आहार, उत्तेजक पदार्थ, व्यायाम",
        
        # Actions
        "analyze_case": "🔬 केस का विश्लेषण करें",
        "clear_form": "फॉर्म साफ़ करें",
        "search_mm": "खोजें",
        "search_placeholder": "जैसे, तलवों में जलन, गर्मी से बदतर, दार्शनिक",
        
        # Results
        "results": "परिणाम",
        "workflow_steps": "वर्कफ़्लो चरण",
        "prescription": "प्रिस्क्रिप्शन",
        "remedy": "औषधि",
        "potency": "शक्ति",
        "rationale": "तर्क",
        "keynotes": "मिलान किए गए मुख्य लक्षण",
        "monitoring": "निगरानी सलाह",
        "wellness": "कल्याण सलाह",
        "disclaimer": "अस्वीकरण",
        
        # Messages
        "enter_complaint": "कृपया जारी रखने के लिए मुख्य शिकायत दर्ज करें।",
        "processing": "मल्टी-एजेंट वर्कफ़्लो के माध्यम से केस प्रोसेस हो रहा है...",
        "emergency": "⚠️ आपातकाल",
        "emergency_msg": "कृपया तुरंत चिकित्सा सहायता लें!",
        "no_results": "कोई परिणाम नहीं मिला। विभिन्न खोज शब्द आज़माएं।",
        
        # About
        "about_text": """
        ### दृष्टि
        सदियों की बुद्धिमत्ता पर प्रशिक्षित एक दयालु डिजिटल होम्योपैथ — वैज्ञानिक अनुशासन, 
        सहानुभूति और शून्य मतिभ्रम के साथ शास्त्रीय होम्योपैथी का अभ्यास करना।
        
        ### कार्यप्रणाली
        - **शास्त्रीय दृष्टिकोण**: केंट, बोएनिंगहौसेन, हेरिंग, एलन
        - **एकल औषधि**: समग्रता के आधार पर एक समय में एक दवा
        - **उच्च भार**: मानसिक/भावनात्मक और सामान्य को प्राथमिकता
        - **सुरक्षा पहले**: लाल झंडे की जांच और आपातकालीन रेफरल
        
        ### वर्कफ़्लो
        1. **केस टेकिंग**: विस्तृत इतिहास और लक्षण संग्रह
        2. **रेपर्टराइजेशन**: नियम-आधारित रूब्रिक मैपिंग
        3. **मैटेरिया मेडिका**: AI-संचालित शब्दार्थ खोज
        4. **विभेदक**: औषधि चयन के लिए LLM विश्लेषण
        5. **प्रिस्क्रिप्शन**: निगरानी के साथ रूढ़िवादी शक्ति
        
        ### अस्वीकरण
        यह केवल शैक्षिक सॉफ्टवेयर है। यह लाइसेंस प्राप्त चिकित्सा पेशेवर की जगह नहीं लेता है।
        आपात स्थिति में, तुरंत चिकित्सा देखभाल लें।
        """
    }
}

def t(key: str, lang: str = "en") -> str:
    """Get translation for key in specified language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
