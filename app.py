"""
Classical Homeopathy Portal - Streamlit Application
Multi-agent workflow with bilingual support (English/Hindi)
"""
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# For Streamlit Cloud, also check st.secrets (only if secrets.toml exists)
try:
    if 'OPENAI_API_KEY' in st.secrets:
        os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
except Exception:
    # No secrets.toml file, use .env instead (local development)
    pass

from src.translations import t, TRANSLATIONS
from src.orchestrator import run_full_case_workflow
from src.embeddings import search as mm_search

# Page config
st.set_page_config(
    page_title="Classical Homeopathy Portal",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'case_data' not in st.session_state:
    st.session_state.case_data = {}
if 'workflow_result' not in st.session_state:
    st.session_state.workflow_result = None

# Sidebar
with st.sidebar:
    st.title("🌿 " + t("title", st.session_state.lang))
    
    st.divider()
    
    st.subheader(t("language", st.session_state.lang))
    lang = st.radio(
        "Select Language",
        ["en", "hi"],
        format_func=lambda x: "🇬🇧 English" if x == "en" else "🇮🇳 हिन्दी",
        key="lang_selector",
        label_visibility="collapsed"
    )
    st.session_state.lang = lang
    
    st.divider()
    
    st.subheader("📋 Navigation")
    
    # Menu items
    menu_items = {
        "📝 New Case": "new_case",
        "📸 Photo Analysis": "photo_analysis",
        "🎥 Video Analysis": "video_analysis",
        "🔍 Materia Medica Search": "mm_search",
        "🧪 Test Cases": "test_cases",
        "📊 Case Statistics": "statistics",
        "ℹ️ About": "about"
    }
    
    page = st.radio(
        "Select Page",
        list(menu_items.keys()),
        key="nav",
        label_visibility="collapsed"
    )
    
    selected_page = menu_items[page]
    
    st.divider()
    
    # Quick stats
    st.caption("📚 Database")
    st.caption("• 73 Remedies")
    st.caption("• 42 Rubrics")
    st.caption("• AI-Powered Analysis")

# Main content
st.title(t("title", lang))
st.caption(t("subtitle", lang))

# PAGE 1: New Case
if selected_page == "new_case":
    st.header(t("case_taking", lang))
    
    with st.form("case_form"):
        # Presenting Complaint
        st.subheader("A. " + t("presenting_complaint", lang))
        presenting_complaint = st.text_area(
            t("presenting_complaint", lang),
            help=t("pc_help", lang),
            height=100,
            key="pc"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            onset = st.text_input(t("onset", lang))
            duration = st.text_input(t("duration", lang))
        with col2:
            course = st.text_input(t("course", lang))
            etiology = st.text_input(t("etiology", lang), help=t("etiology_help", lang))
        
        st.divider()
        
        # Mental/Emotional
        st.subheader("B. " + t("mental_emotional", lang))
        mental_emotional = st.text_area(
            t("mental_help", lang),
            height=80,
            key="mental"
        )
        
        st.divider()
        
        # Generals
        st.subheader("C. " + t("generals", lang))
        
        thermal = st.selectbox(
            t("thermal", lang),
            t("thermal_options", lang)
        )
        
        col1, col2 = st.columns(2)
        with col1:
            cravings = st.text_area(
                t("cravings", lang),
                help=t("cravings_help", lang),
                height=80
            )
            sleep = st.text_area(
                t("sleep", lang),
                help=t("sleep_help", lang),
                height=80
            )
        
        with col2:
            aversions = st.text_area(
                t("aversions", lang),
                help=t("aversions_help", lang),
                height=80
            )
            dreams = st.text_area(
                t("dreams", lang),
                help=t("dreams_help", lang),
                height=80
            )
        
        st.divider()
        
        # History
        st.subheader("D. " + t("past_history", lang) + " / " + t("family_history", lang))
        
        col1, col2 = st.columns(2)
        with col1:
            past_history = st.text_area(
                t("past_history", lang),
                help=t("past_help", lang),
                height=80
            )
        with col2:
            family_history = st.text_area(
                t("family_history", lang),
                help=t("family_help", lang),
                height=80
            )
        
        lifestyle = st.text_area(
            t("lifestyle", lang),
            help=t("lifestyle_help", lang),
            height=80
        )
        
        st.divider()
        
        # Submit buttons
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            submit = st.form_submit_button(
                t("analyze_case", lang),
                type="primary",
                use_container_width=True
            )
        with col2:
            clear = st.form_submit_button(
                t("clear_form", lang),
                use_container_width=True
            )
    
    # Process form submission
    if submit:
        if not presenting_complaint:
            st.error(t("enter_complaint", lang))
        else:
            # Build case data
            case_data = {
                "presenting_complaint": presenting_complaint,
                "onset": onset if onset else None,
                "duration": duration if duration else None,
                "course": course if course else None,
                "etiology": etiology if etiology else None,
                "mental_emotional": [m.strip() for m in mental_emotional.split('\n') if m.strip()],
                "generals": [],
                "particulars": [],
                "cravings": [c.strip() for c in cravings.split('\n') if c.strip()],
                "aversions": [a.strip() for a in aversions.split('\n') if a.strip()],
                "sleep": [s.strip() for s in sleep.split('\n') if s.strip()],
                "dreams": [d.strip() for d in dreams.split('\n') if d.strip()],
                "thermal": thermal if thermal != t("thermal_options", lang)[0] else None,
                "past_history": [p.strip() for p in past_history.split('\n') if p.strip()],
                "family_history": [f.strip() for f in family_history.split('\n') if f.strip()],
                "lifestyle": [l.strip() for l in lifestyle.split('\n') if l.strip()],
                "red_flags": []
            }
            
            st.session_state.case_data = case_data
            
            # Run workflow
            with st.spinner(t("processing", lang)):
                try:
                    result = run_full_case_workflow(case_data)
                    st.session_state.workflow_result = result
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Please check your OpenAI API key in .env file")
    
    # Display results
    if st.session_state.workflow_result:
        st.divider()
        st.header(t("results", lang))
        
        result = st.session_state.workflow_result
        final = result.get("final_result", {})
        
        # Check for emergency
        if final.get("status") == "emergency":
            st.error(t("emergency", lang))
            st.warning(t("emergency_msg", lang))
            for flag in final.get("red_flags", []):
                st.write(f"- {flag}")
            st.stop()
        
        # Show workflow steps
        with st.expander(t("workflow_steps", lang), expanded=False):
            for step in result.get("steps", []):
                agent = step.get("agent")
                step_result = step.get("result", {})
                st.write(f"**{agent}**: {step_result.get('message', 'Complete')}")
        
        # Show prescription
        if final.get("status") == "complete" and final.get("prescription"):
            prescription = final["prescription"]
            
            # Clinical confidence indicator
            clinical_conf = prescription.get("clinical_confidence", 0.5)
            if clinical_conf >= 0.8:
                conf_color = "🟢"
                conf_text = "High Clinical Confidence"
            elif clinical_conf >= 0.6:
                conf_color = "🟡"
                conf_text = "Moderate Clinical Confidence"
            else:
                conf_color = "🟠"
                conf_text = "Lower Confidence - Monitor Closely"
            
            st.success(f"### {t('prescription', lang)} {conf_color} {conf_text}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(t("remedy", lang), prescription.get("remedy", "N/A"))
            with col2:
                st.metric(t("potency", lang), prescription.get("potency", "N/A"))
            with col3:
                st.metric("Confidence", f"{int(clinical_conf * 100)}%")
            
            st.subheader(t("rationale", lang))
            for reason in prescription.get("rationale", []):
                st.write(f"- {reason}")
            
            st.subheader(t("keynotes", lang) + " (Characteristic Symptoms)")
            for keynote in prescription.get("matched_keynotes", []):
                st.write(f"✓ {keynote}")
            
            # Show differential if available
            if prescription.get("differential"):
                with st.expander("🔬 Differential Diagnosis (Other Considered Remedies)"):
                    for diff in prescription.get("differential", []):
                        st.write(f"**{diff.get('remedy', 'Unknown')}** - Score: {diff.get('score', 0)}, Matches: {diff.get('match_count', 0)}")
            
            st.subheader(t("monitoring", lang) + " & Expected Response")
            if prescription.get("expected_response"):
                st.info(f"⏱️ **Timeline**: {prescription.get('expected_response')}")
            for monitor in prescription.get("monitoring", []):
                st.write(f"• {monitor}")
            
            if prescription.get("wellness_advice"):
                st.subheader(t("wellness", lang) + " 🌿")
                for advice in prescription.get("wellness_advice", []):
                    st.write(f"🌟 {advice}")
            
            # Disclaimer
            st.divider()
            st.warning(f"**{t('disclaimer', lang)}**")
            st.caption(final.get("disclaimer", ""))
        
        elif final.get("status") == "needs_more_information":
            st.warning(f"### 📋 {t('case_incomplete', lang) if lang == 'en' else 'केस अधूरा है'}")
            st.info(final.get("message", "More information needed"))
            
            completeness = final.get("completeness_score", 0)
            st.progress(completeness, text=f"Case Completeness: {int(completeness * 100)}%")
            
            st.subheader("🔍 Clarifying Questions Needed:")
            st.write(f"*Please answer these {final.get('estimated_questions', 'several')} questions for accurate prescription:*")
            
            questions = final.get("questions_to_ask", [])
            for idx, q_item in enumerate(questions, 1):
                if isinstance(q_item, dict):
                    question = q_item.get('question', str(q_item))
                    priority = q_item.get('priority', 'medium')
                    category = q_item.get('category', '')
                    
                    # Color code by priority
                    if priority == 'high':
                        st.error(f"**{idx}. {question}** ⭐ *Essential*")
                    elif priority == 'medium':
                        st.warning(f"**{idx}. {question}**")
                    else:
                        st.info(f"**{idx}. {question}**")
                else:
                    st.write(f"**{idx}. {q_item}**")
            
            st.divider()
            st.caption("💡 **Tip**: The more detailed your answers, the more accurate the remedy selection will be.")
        
        elif final.get("status") == "needs_clarification":
            st.info("### 📝 Additional Clarification Needed:")
            st.write(final.get("clarification_reason", "Need more specific information"))
            for idx, q in enumerate(final.get("questions", []), 1):
                st.write(f"**{idx}. {q}**")
        
        elif final.get("status") == "insufficient_evidence":
            st.warning(final.get("message", "Unable to determine remedy"))
            st.caption(final.get("disclaimer", ""))

# PAGE 2: Photo Analysis
elif selected_page == "photo_analysis":
    st.header("📸 Medical Photo Analysis")
    
    st.info("Upload a clear photo of the affected area for AI-powered visual analysis")
    
    # Instructions
    with st.expander("📋 Photo Guidelines", expanded=False):
        st.write("""
        **For Best Results:**
        - Good lighting (natural light preferred)
        - Clear, focused image
        - Show affected area from multiple angles if possible
        - Include size reference (coin, ruler) if relevant
        - Close-up for texture and color details
        
        **What We Analyze:**
        - Color and texture
        - Size and extent
        - Inflammation signs
        - Discharge or secretions
        - Homeopathic remedy indicators
        """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Photo (JPG, PNG, WEBP)",
        type=['jpg', 'jpeg', 'png', 'webp'],
        help="Maximum file size: 20MB"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        
        with col2:
            st.write("**File Details:**")
            st.write(f"- Name: {uploaded_file.name}")
            st.write(f"- Size: {uploaded_file.size / 1024:.1f} KB")
            st.write(f"- Type: {uploaded_file.type}")
        
        # Analyze button
        if st.button("🔬 Analyze Photo", type="primary", use_container_width=True):
            with st.spinner("Analyzing image with AI Vision..."):
                try:
                    from src.image_analysis import analyze_medical_image
                    
                    # Read image data
                    image_data = uploaded_file.read()
                    
                    # Analyze
                    result = analyze_medical_image(image_data, st.session_state.case_data)
                    
                    if result.get("status") == "success":
                        st.success("✅ Analysis Complete!")
                        
                        analysis = result["image_analysis"]
                        
                        # Visual Description
                        st.subheader("👁️ Visual Observations")
                        st.write(analysis.get("visual_description", "N/A"))
                        
                        # Key Features
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Color", analysis.get("color", "N/A"))
                        with col2:
                            st.metric("Texture", analysis.get("texture", "N/A"))
                        with col3:
                            st.metric("Severity", analysis.get("severity", "N/A"))
                        
                        # Specific Features
                        if analysis.get("specific_features"):
                            st.subheader("🔍 Specific Features")
                            for feature in analysis["specific_features"]:
                                st.write(f"• {feature}")
                        
                        # Homeopathic Indicators
                        if analysis.get("homeopathic_indicators"):
                            st.subheader("💊 Homeopathic Indicators")
                            for indicator in analysis["homeopathic_indicators"]:
                                st.write(f"✓ {indicator}")
                        
                        # Suggested Remedies
                        if analysis.get("suggested_remedy_families"):
                            st.subheader("🎯 Suggested Remedy Families")
                            for remedy_info in analysis["suggested_remedy_families"]:
                                if isinstance(remedy_info, dict):
                                    st.write(f"**{remedy_info.get('remedy', 'N/A')}**: {remedy_info.get('reasoning', '')}")
                                else:
                                    st.write(f"• {remedy_info}")
                        
                        # Emergency Check
                        if analysis.get("requires_medical_attention"):
                            st.error("⚠️ **URGENT**: This condition may require immediate medical attention!")
                        
                        # Additional Questions
                        if analysis.get("additional_questions"):
                            st.subheader("❓ Additional Questions to Ask")
                            for q in analysis["additional_questions"]:
                                st.write(f"• {q}")
                        
                        # Save to session
                        if st.button("💾 Add to Current Case"):
                            st.session_state.case_data = result["enhanced_case"]
                            st.success("✅ Visual analysis added to case data!")
                    
                    else:
                        st.error(f"❌ Error: {result.get('message', 'Analysis failed')}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("Please ensure OpenAI API key is configured and image is valid")

# PAGE 3: Video Analysis  
elif selected_page == "video_analysis":
    st.header("🎥 Medical Video Analysis")
    
    st.info("Record or upload a video showing symptoms, movements, or affected areas")
    
    # Recording guides
    with st.expander("📋 Video Recording Guidelines", expanded=False):
        from src.video_analysis import VideoRecordingGuide
        
        guide_type = st.selectbox(
            "Select symptom type for specific guidance:",
            ["General Symptoms", "Skin Conditions", "Joint Pain", "Tremors/Movements", "Respiratory"]
        )
        
        guide_map = {
            "General Symptoms": "general_symptoms",
            "Skin Conditions": "skin_conditions",
            "Joint Pain": "joint_pain",
            "Tremors/Movements": "tremors_movements",
            "Respiratory": "respiratory"
        }
        
        guide = VideoRecordingGuide.get_recording_guide(guide_map[guide_type])
        
        st.write(f"**{guide['title']}**")
        st.write("**Instructions:**")
        for instruction in guide['instructions']:
            st.write(instruction)
        
        st.write("**What to Show:**")
        for item in guide['what_to_show']:
            st.write(f"• {item}")
        
        st.write("**What to Say:**")
        for item in guide['what_to_say']:
            st.write(f"• {item}")
    
    # Video upload
    st.subheader("Upload Video")
    uploaded_video = st.file_uploader(
        "Upload Video (MP4, WEBM, MOV)",
        type=['mp4', 'webm', 'mov'],
        help="Maximum file size: 100MB"
    )
    
    if uploaded_video is not None:
        st.video(uploaded_video)
        
        st.write("**File Details:**")
        st.write(f"- Name: {uploaded_video.name}")
        st.write(f"- Size: {uploaded_video.size / 1024 / 1024:.1f} MB")
        
        col1, col2 = st.columns(2)
        
        with col1:
            analyze_visual = st.checkbox("Analyze Visual Content", value=True)
        with col2:
            analyze_audio = st.checkbox("Transcribe & Analyze Audio", value=True)
        
        if st.button("🔬 Analyze Video", type="primary", use_container_width=True):
            with st.spinner("Analyzing video... This may take a minute..."):
                try:
                    import tempfile
                    from src.video_analysis import analyze_patient_video
                    
                    # Save video to temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                        tmp_file.write(uploaded_video.read())
                        video_path = tmp_file.name
                    
                    # Analyze
                    result = analyze_patient_video(
                        video_path,
                        st.session_state.case_data,
                        include_audio=analyze_audio
                    )
                    
                    if result.get("status") == "success":
                        st.success("✅ Video Analysis Complete!")
                        
                        video_analysis = result.get("video_analysis", {})
                        audio_analysis = result.get("audio_analysis", {})
                        
                        # Visual Analysis
                        if video_analysis and not video_analysis.get("error"):
                            st.subheader("👁️ Visual Analysis")
                            st.write(video_analysis.get("visual_description", "N/A"))
                            
                            if video_analysis.get("movement_observations"):
                                st.write("**Movement Patterns:**")
                                for movement in video_analysis["movement_observations"]:
                                    st.write(f"• {movement}")
                            
                            if video_analysis.get("homeopathic_keynotes"):
                                st.write("**Homeopathic Keynotes:**")
                                for keynote in video_analysis["homeopathic_keynotes"]:
                                    st.write(f"✓ {keynote}")
                        
                        # Audio Analysis
                        if audio_analysis and not audio_analysis.get("error"):
                            st.subheader("🎤 Audio Transcription")
                            with st.expander("View Full Transcription"):
                                st.write(audio_analysis.get("transcription", "N/A"))
                            
                            if audio_analysis.get("symptoms_mentioned"):
                                st.write("**Symptoms Mentioned:**")
                                for symptom in audio_analysis["symptoms_mentioned"]:
                                    st.write(f"• {symptom}")
                        
                        # Suggested Remedies
                        if result.get("video_suggested_remedies"):
                            st.subheader("🎯 Suggested Remedies from Video")
                            for remedy in result["video_suggested_remedies"]:
                                if isinstance(remedy, dict):
                                    st.write(f"**{remedy.get('remedy', 'N/A')}**: {remedy.get('reasoning', '')}")
                        
                        # Emergency Check
                        if result.get("requires_emergency_care"):
                            st.error("⚠️ **URGENT**: Seek immediate medical attention!")
                        
                        # Save to case
                        if st.button("💾 Add to Current Case"):
                            st.session_state.case_data = result["enhanced_case"]
                            st.success("✅ Video analysis added to case data!")
                    
                    else:
                        st.error(f"❌ Error: {result.get('message', 'Analysis failed')}")
                    
                    # Cleanup
                    import os
                    try:
                        os.unlink(video_path)
                    except:
                        pass
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("Please ensure OpenAI API key is configured")

# PAGE 4: Materia Medica Search
elif selected_page == "mm_search":
    st.header(t("mm_search", lang))
    
    search_query = st.text_input(
        t("search_placeholder", lang),
        key="mm_search_input"
    )
    
    if st.button(t("search_mm", lang), type="primary"):
        if search_query:
            with st.spinner("Searching..."):
                try:
                    results = mm_search(search_query, k=5)
                    
                    if results:
                        st.success(f"Found {len(results)} results")
                        
                        for idx, result in enumerate(results):
                            with st.expander(
                                f"{result['title']} (similarity: {result['similarity']:.3f})",
                                expanded=(idx == 0)
                            ):
                                st.text(result['excerpt'])
                    else:
                        st.info(t("no_results", lang))
                
                except Exception as e:
                    import traceback
                    st.error(f"Error: {str(e)}")
                    with st.expander("Debug Info"):
                        st.code(traceback.format_exc())
                    st.info("Please check your OpenAI API key and ensure embeddings index is built")
        else:
            st.warning("Please enter a search query")

# PAGE 5: Test Cases
elif selected_page == "test_cases":
    st.header("🧪 Test Cases for Validation")
    
    st.info("20 comprehensive test cases for validating remedy selection accuracy")
    
    try:
        import json
        with open("test_cases/test_cases_comprehensive.json", "r") as f:
            test_data = json.load(f)
        
        test_cases = test_data["test_cases"]
        
        # Case selector
        case_ids = [f"{tc['case_id']}: {tc['demographics']['age']}yo {tc['demographics']['gender']}" 
                    for tc in test_cases]
        
        selected_case_idx = st.selectbox("Select Test Case:", range(len(case_ids)), 
                                         format_func=lambda x: case_ids[x])
        
        test_case = test_cases[selected_case_idx]
        
        # Display case
        st.subheader(f"Case {test_case['case_id']}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Age", test_case['demographics']['age'])
        with col2:
            st.metric("Gender", test_case['demographics']['gender'])
        with col3:
            st.metric("Difficulty", test_case['difficulty_level'])
        
        st.write(f"**Occupation:** {test_case['demographics']['occupation']}")
        
        # Case details
        with st.expander("📋 Case Details", expanded=True):
            case_data = test_case['case_data']
            st.write(f"**Presenting Complaint:** {case_data['presenting_complaint']}")
            st.write(f"**Duration:** {case_data['duration']}")
            st.write(f"**Etiology:** {case_data.get('etiology', 'N/A')}")
            
            if case_data.get('mental_emotional'):
                st.write("**Mental/Emotional:**")
                for symptom in case_data['mental_emotional']:
                    st.write(f"• {symptom}")
        
        # Expected remedy
        with st.expander("🎯 Expected Remedy (for evaluators)", expanded=False):
            st.write(f"**Remedy:** {test_case['expected_remedy']}")
            st.write(f"**Potency:** {test_case['expected_potency']}")
            st.write("**Key Indicators:**")
            for indicator in test_case['key_indicators']:
                st.write(f"✓ {indicator}")
        
        # Test button
        if st.button("🔬 Run AI Analysis on This Case", type="primary"):
            with st.spinner("Analyzing test case..."):
                try:
                    from src.orchestrator import run_full_case_workflow
                    
                    # Convert test case format to orchestrator format
                    case_data = test_case['case_data'].copy()
                    
                    # Convert lists to strings where needed
                    if isinstance(case_data.get('mental_emotional'), list):
                        case_data['mental_emotional'] = case_data['mental_emotional']
                    if isinstance(case_data.get('generals'), list):
                        case_data['generals'] = case_data['generals']
                    if isinstance(case_data.get('cravings'), list):
                        case_data['cravings'] = ', '.join(case_data['cravings'])
                    if isinstance(case_data.get('aversions'), list):
                        case_data['aversions'] = ', '.join(case_data['aversions'])
                    if isinstance(case_data.get('sleep'), list):
                        case_data['sleep'] = ', '.join(case_data['sleep'])
                    if isinstance(case_data.get('dreams'), list):
                        case_data['dreams'] = ', '.join(case_data['dreams'])
                    if isinstance(case_data.get('past_history'), list):
                        case_data['past_history'] = ', '.join(case_data['past_history'])
                    if isinstance(case_data.get('family_history'), list):
                        case_data['family_history'] = ', '.join(case_data['family_history'])
                    if isinstance(case_data.get('lifestyle'), list):
                        case_data['lifestyle'] = ', '.join(case_data['lifestyle'])
                    
                    # Skip intelligent questioning for test cases (they're already comprehensive)
                    result = run_full_case_workflow(case_data, skip_questioning=True)
                    
                    st.success("✅ Analysis Complete!")
                    
                    final = result.get("final_result", {})
                    
                    if final.get("status") == "complete" and final.get("prescription"):
                        prescription = final["prescription"]
                        
                        # Compare with expected
                        ai_remedy = prescription.get("remedy", "")
                        expected_remedy = test_case['expected_remedy']
                        
                        if ai_remedy.lower() == expected_remedy.lower():
                            st.success(f"✅ **CORRECT!** AI selected: {ai_remedy}")
                        else:
                            st.warning(f"⚠️ **DIFFERENT** - AI selected: {ai_remedy}, Expected: {expected_remedy}")
                        
                        st.write(f"**Potency:** {prescription.get('potency')}")
                        st.write(f"**Confidence:** {prescription.get('clinical_confidence', 0) * 100:.0f}%")
                        
                        st.write("**AI Rationale:**")
                        for reason in prescription.get("rationale", []):
                            st.write(f"• {reason}")
                        
                        st.write("**Matched Keynotes:**")
                        for keynote in prescription.get("matched_keynotes", []):
                            st.write(f"✓ {keynote}")
                    
                    else:
                        st.error("AI could not determine remedy")
                        st.write(final.get("message", ""))
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    except FileNotFoundError:
        st.error("Test cases file not found")
    except Exception as e:
        st.error(f"Error loading test cases: {str(e)}")

# PAGE 6: Statistics
elif selected_page == "statistics":
    st.header("📊 Portal Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Remedies", "73", help="Comprehensive materia medica database")
        st.metric("Polychrests", "20", help="Major constitutional remedies")
    
    with col2:
        st.metric("Repertory Rubrics", "42", help="Weighted symptom mappings")
        st.metric("Test Cases", "20", help="Validation test cases")
    
    with col3:
        st.metric("Embeddings Size", "2.43 MB", help="AI semantic search index")
        st.metric("Languages", "2", help="English & Hindi")
    
    st.divider()
    
    st.subheader("🎯 Remedy Categories")
    
    categories = {
        "Acute Remedies": 25,
        "Chronic/Constitutional": 20,
        "Injury/Trauma": 8,
        "Digestive": 12,
        "Respiratory": 10,
        "Skin Conditions": 12,
        "Mental/Emotional": 15,
        "Nosodes": 3
    }
    
    for category, count in categories.items():
        st.write(f"**{category}:** {count} remedies")
    
    st.divider()
    
    st.subheader("🔬 AI Capabilities")
    st.write("✅ Multi-agent workflow (CaseTaker → Prescription)")
    st.write("✅ OpenAI GPT-4 for differential diagnosis")
    st.write("✅ Semantic embeddings search")
    st.write("✅ Image analysis (Vision API)")
    st.write("✅ Video analysis with audio transcription")
    st.write("✅ Intelligent follow-up questioning")
    st.write("✅ Clinical confidence scoring")
    st.write("✅ Kent's hierarchy of symptoms")
    st.write("✅ Miasmatic analysis")
    st.write("✅ Constitutional assessment")

# PAGE 7: About
elif selected_page == "about":
    st.markdown(t("about_text", lang))
    
    st.divider()
    
    st.subheader("System Status")
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        st.success("✓ OpenAI API Key configured")
    else:
        st.error("✗ OpenAI API Key not found - Please add to .env file")
    
    # Check data files
    if os.path.exists("data/repertory_mapping.csv"):
        st.success("✓ Repertory data loaded")
    else:
        st.error("✗ Repertory data not found")
    
    if os.path.exists("data/materia_medica"):
        mm_files = len([f for f in os.listdir("data/materia_medica") if f.endswith(".md")])
        st.success(f"✓ Materia Medica: {mm_files} remedies")
    else:
        st.error("✗ Materia Medica directory not found")
    
    if os.path.exists("data/mm_index.json"):
        st.success("✓ Embeddings index exists")
    else:
        st.warning("⚠ Embeddings index not built - will be created on first search")

# Footer
st.divider()
st.caption("🌿 Classical Homeopathy Portal | Educational Use Only | Not a substitute for professional medical care")
