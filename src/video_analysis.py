"""
Video Analysis for Homeopathy
Records and analyzes patient videos showing symptoms, affected areas, movements, etc.
Includes audio transcription for verbal symptom description
"""
import os
import base64
from typing import Dict, List, Optional, Tuple
import json
import tempfile
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class VideoAnalyzer:
    """
    Analyzes patient videos for homeopathic assessment
    Extracts visual symptoms, movements, and audio descriptions
    """
    
    VIDEO_ANALYSIS_PROMPT = """You are an expert homeopathic physician analyzing a patient video.

Analyze this video comprehensively for homeopathic remedy selection:

1. **Visual Observations**:
   - Appearance of affected area (color, texture, size, shape)
   - Any visible symptoms (rash, swelling, tremor, etc.)
   - Patient's general appearance and demeanor
   - Facial expressions (pain, anxiety, distress)
   - Body language and posture
   - Gait or movement patterns (if shown)
   - Any visible discharge or secretions

2. **Movement Analysis**:
   - Tremors, twitching, or involuntary movements
   - Range of motion limitations
   - Gait abnormalities (limping, shuffling, etc.)
   - Coordination issues
   - Speed and quality of movements
   - Asymmetry (left vs right side)

3. **Behavioral Observations**:
   - Restlessness or stillness
   - Anxiety or calmness
   - Pain behaviors (guarding, wincing, etc.)
   - Energy level (lethargic, agitated, normal)
   - Interaction style

4. **Specific Homeopathic Indicators**:
   - Better/worse with motion
   - Position preferences
   - Thermal state (appears hot/cold)
   - Laterality (left/right sided symptoms)
   - Aggravation patterns visible

5. **Severity Assessment**:
   - Mild, moderate, or severe presentation
   - Functional impact visible
   - Acute vs chronic appearance

6. **Remedy Considerations**:
   - Which remedy families match the visual presentation?
   - Key visual keynotes observed
   - Movement patterns suggesting specific remedies

Return analysis in JSON format:
{
  "visual_description": "detailed description",
  "affected_areas": ["list of visible affected areas"],
  "movement_observations": ["list of movement patterns"],
  "behavioral_signs": ["list of behavioral indicators"],
  "pain_indicators": ["visible signs of pain/discomfort"],
  "homeopathic_keynotes": ["remedy-relevant observations"],
  "laterality": "left/right/bilateral/none",
  "thermal_state": "appears hot/cold/neutral",
  "energy_level": "low/moderate/high/restless",
  "suggested_remedies": [{"remedy": "name", "reasoning": "why indicated"}],
  "severity": "mild/moderate/severe",
  "functional_impact": "description",
  "requires_emergency_care": true/false,
  "additional_questions": ["questions to clarify findings"]
}

Be thorough and clinically observant."""

    AUDIO_TRANSCRIPTION_PROMPT = """Transcribe this audio and extract homeopathically relevant information:

1. Transcribe exactly what the patient says
2. Note tone of voice (anxious, calm, weak, strong)
3. Note speech patterns (rapid, slow, hesitant, clear)
4. Extract key symptoms mentioned
5. Note emotional state from voice
6. Identify any modalities mentioned (better/worse conditions)

Return in JSON:
{
  "transcription": "full text",
  "tone_of_voice": "description",
  "speech_pattern": "description",
  "symptoms_mentioned": ["list"],
  "modalities_mentioned": ["list"],
  "emotional_state": "description",
  "key_phrases": ["important phrases"]
}"""
    
    def __init__(self):
        self.client = None
        if OpenAI:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.client = OpenAI(api_key=api_key)
    
    def analyze_video(self, video_path: str) -> Dict:
        """
        Analyze video file for homeopathic indicators
        """
        if not self.client:
            return {
                "error": "OpenAI client not initialized",
                "visual_description": "Video analysis unavailable"
            }
        
        try:
            # Read video file
            with open(video_path, 'rb') as video_file:
                video_data = video_file.read()
            
            # Encode video to base64
            base64_video = base64.b64encode(video_data).decode('utf-8')
            
            # Analyze video using GPT-4 Vision
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self.VIDEO_ANALYSIS_PROMPT
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:video/mp4;base64,{base64_video}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            
            # Parse JSON response
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
            elif "{" in content:
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                json_str = content[json_start:json_end]
            else:
                json_str = content
            
            analysis = json.loads(json_str)
            return analysis
            
        except Exception as e:
            return {
                "error": f"Video analysis failed: {str(e)}",
                "visual_description": "Unable to analyze video"
            }
    
    def transcribe_audio(self, audio_path: str) -> Dict:
        """
        Transcribe audio from video and analyze speech patterns
        """
        if not self.client:
            return {"error": "OpenAI client not initialized"}
        
        try:
            # Transcribe using Whisper API
            with open(audio_path, 'rb') as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            # Analyze transcription for homeopathic relevance
            analysis_response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": self.AUDIO_TRANSCRIPTION_PROMPT
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this patient's verbal description:\n\n{transcription}"
                    }
                ],
                temperature=0.3
            )
            
            content = analysis_response.choices[0].message.content
            
            # Parse JSON
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
            elif "{" in content:
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                json_str = content[json_start:json_end]
            else:
                json_str = content
            
            audio_analysis = json.loads(json_str)
            audio_analysis["raw_transcription"] = transcription
            
            return audio_analysis
            
        except Exception as e:
            return {
                "error": f"Audio transcription failed: {str(e)}",
                "transcription": ""
            }
    
    def analyze_video_comprehensive(self, video_path: str, extract_audio: bool = True) -> Dict:
        """
        Comprehensive video analysis including visual and audio
        """
        results = {
            "video_analysis": {},
            "audio_analysis": {},
            "integrated_findings": {}
        }
        
        # Analyze video visually
        results["video_analysis"] = self.analyze_video(video_path)
        
        # Extract and analyze audio if requested
        if extract_audio:
            # Note: In production, you'd extract audio from video first
            # For now, assuming audio extraction is handled separately
            audio_path = video_path.replace('.mp4', '.mp3').replace('.webm', '.mp3')
            if os.path.exists(audio_path):
                results["audio_analysis"] = self.transcribe_audio(audio_path)
        
        # Integrate findings
        results["integrated_findings"] = self._integrate_video_audio(
            results["video_analysis"],
            results["audio_analysis"]
        )
        
        return results
    
    def _integrate_video_audio(self, video_analysis: Dict, audio_analysis: Dict) -> Dict:
        """
        Integrate visual and audio findings for comprehensive assessment
        """
        integrated = {
            "comprehensive_symptoms": [],
            "visual_and_verbal_match": [],
            "discrepancies": [],
            "confidence": "high"
        }
        
        # Combine symptoms from both sources
        visual_symptoms = video_analysis.get("homeopathic_keynotes", [])
        verbal_symptoms = audio_analysis.get("symptoms_mentioned", [])
        
        integrated["comprehensive_symptoms"] = list(set(visual_symptoms + verbal_symptoms))
        
        # Check for matches between what patient says and what is visible
        for verbal in verbal_symptoms:
            if any(verbal.lower() in visual.lower() for visual in visual_symptoms):
                integrated["visual_and_verbal_match"].append(verbal)
        
        # Note any discrepancies
        if len(verbal_symptoms) > 0 and len(visual_symptoms) > 0:
            if len(integrated["visual_and_verbal_match"]) < len(verbal_symptoms) * 0.5:
                integrated["discrepancies"].append(
                    "Some verbal symptoms not visually confirmed - may need further investigation"
                )
        
        # Assess confidence
        if len(integrated["visual_and_verbal_match"]) >= 3:
            integrated["confidence"] = "high"
        elif len(integrated["comprehensive_symptoms"]) >= 5:
            integrated["confidence"] = "moderate"
        else:
            integrated["confidence"] = "low - more information needed"
        
        return integrated


class VideoRecordingGuide:
    """
    Provides guidance for patients on how to record effective videos
    """
    
    RECORDING_INSTRUCTIONS = {
        "skin_conditions": {
            "title": "Recording Skin Conditions",
            "instructions": [
                "1. Ensure good lighting (natural light is best)",
                "2. Hold camera steady or use a stand",
                "3. Show affected area from multiple angles",
                "4. Include close-up views of texture, color",
                "5. Show the extent/size (compare to coin or ruler if possible)",
                "6. Demonstrate any movement that affects it",
                "7. Duration: 30-60 seconds"
            ],
            "what_to_show": [
                "Color and texture",
                "Size and borders",
                "Any discharge or crusting",
                "Surrounding skin",
                "Multiple affected areas if present"
            ],
            "what_to_say": [
                "Describe sensations (itching, burning, pain)",
                "When it started",
                "What makes it better or worse",
                "Any other symptoms"
            ]
        },
        "joint_pain": {
            "title": "Recording Joint Pain/Stiffness",
            "instructions": [
                "1. Show the affected joint at rest",
                "2. Demonstrate range of motion slowly",
                "3. Show any swelling or deformity",
                "4. Demonstrate what movements cause pain",
                "5. Show how you walk or move (if applicable)",
                "6. Duration: 45-90 seconds"
            ],
            "what_to_show": [
                "Joint appearance (swelling, redness)",
                "Range of motion",
                "Gait or movement patterns",
                "Comparison with unaffected side"
            ],
            "what_to_say": [
                "Pain level (1-10)",
                "When pain is worse (morning, evening, motion, rest)",
                "How long you've had it",
                "What activities are difficult"
            ]
        },
        "tremors_movements": {
            "title": "Recording Tremors or Abnormal Movements",
            "instructions": [
                "1. Record in good lighting",
                "2. Show movement at rest",
                "3. Show movement during activity",
                "4. Include face if facial movements present",
                "5. Record for at least 60 seconds",
                "6. Show both sides of body for comparison"
            ],
            "what_to_show": [
                "Tremor frequency and amplitude",
                "When tremor occurs (rest, action, both)",
                "Which body parts affected",
                "Severity and impact on function"
            ],
            "what_to_say": [
                "When tremors started",
                "What triggers or worsens them",
                "What helps reduce them",
                "Impact on daily activities"
            ]
        },
        "respiratory": {
            "title": "Recording Breathing Difficulties",
            "instructions": [
                "1. Record in quiet environment",
                "2. Show chest movement while breathing",
                "3. Record any coughing episodes",
                "4. Show face (color, distress)",
                "5. Demonstrate breathing at rest and after activity",
                "6. Duration: 60-90 seconds"
            ],
            "what_to_show": [
                "Breathing rate and effort",
                "Chest movement",
                "Use of accessory muscles",
                "Any wheezing (audible)",
                "Coughing pattern"
            ],
            "what_to_say": [
                "Describe breathing difficulty",
                "When it's worse (time, position, activity)",
                "Any triggers (cold, allergens)",
                "Associated symptoms"
            ]
        },
        "general_symptoms": {
            "title": "Recording General Symptoms",
            "instructions": [
                "1. Find quiet, well-lit space",
                "2. Sit or stand comfortably",
                "3. Look at camera and speak clearly",
                "4. Describe symptoms in detail",
                "5. Show any visible symptoms",
                "6. Duration: 2-3 minutes"
            ],
            "what_to_show": [
                "Your general appearance",
                "Energy level",
                "Any visible symptoms",
                "Facial expressions"
            ],
            "what_to_say": [
                "Main complaint in your own words",
                "When and how it started",
                "What makes it better or worse",
                "How it affects your daily life",
                "Your emotional state",
                "Sleep, appetite, energy",
                "Any other symptoms"
            ]
        }
    }
    
    @staticmethod
    def get_recording_guide(symptom_type: str) -> Dict:
        """Get recording instructions for specific symptom type"""
        return VideoRecordingGuide.RECORDING_INSTRUCTIONS.get(
            symptom_type,
            VideoRecordingGuide.RECORDING_INSTRUCTIONS["general_symptoms"]
        )
    
    @staticmethod
    def get_all_guides() -> Dict:
        """Get all recording guides"""
        return VideoRecordingGuide.RECORDING_INSTRUCTIONS


class VideoIntegrator:
    """
    Integrates video analysis with case data
    """
    
    @staticmethod
    def integrate_video_with_case(video_analysis: Dict, audio_analysis: Dict, 
                                   case_data: Dict) -> Dict:
        """
        Integrate video findings into case data structure
        """
        enhanced_case = case_data.copy()
        
        # Add visual symptoms to particulars
        if "particulars" not in enhanced_case:
            enhanced_case["particulars"] = []
        
        # Add video observations
        if video_analysis and not video_analysis.get("error"):
            enhanced_case["particulars"].append({
                "section": "Video Analysis - Visual",
                "description": video_analysis.get("visual_description", ""),
                "modalities_better": [],
                "modalities_worse": [],
                "concomitants": video_analysis.get("homeopathic_keynotes", [])
            })
            
            # Add movement observations
            if video_analysis.get("movement_observations"):
                enhanced_case["particulars"].append({
                    "section": "Video Analysis - Movement",
                    "description": "Movement patterns observed",
                    "modalities_better": [],
                    "modalities_worse": [],
                    "concomitants": video_analysis.get("movement_observations", [])
                })
        
        # Add audio transcription to mental/emotional if relevant
        if audio_analysis and not audio_analysis.get("error"):
            transcription = audio_analysis.get("transcription", "")
            if transcription:
                # Add verbal symptoms
                verbal_symptoms = audio_analysis.get("symptoms_mentioned", [])
                if "mental_emotional" not in enhanced_case:
                    enhanced_case["mental_emotional"] = []
                
                # Add emotional state from voice
                emotional_state = audio_analysis.get("emotional_state", "")
                if emotional_state:
                    enhanced_case["mental_emotional"].append(f"Voice analysis: {emotional_state}")
                
                # Add modalities mentioned
                modalities = audio_analysis.get("modalities_mentioned", [])
                for mod in modalities:
                    if "better" in mod.lower():
                        # Add to appropriate section
                        pass
                    elif "worse" in mod.lower():
                        # Add to appropriate section
                        pass
        
        # Add suggested remedies from video
        video_remedies = []
        if video_analysis and video_analysis.get("suggested_remedies"):
            video_remedies = video_analysis["suggested_remedies"]
        
        return {
            "status": "success",
            "enhanced_case": enhanced_case,
            "video_analysis": video_analysis,
            "audio_analysis": audio_analysis,
            "video_suggested_remedies": video_remedies,
            "requires_emergency_care": video_analysis.get("requires_emergency_care", False),
            "additional_questions": video_analysis.get("additional_questions", []) + 
                                   audio_analysis.get("key_phrases", [])
        }


def analyze_patient_video(video_path: str, case_data: Dict, 
                         include_audio: bool = True) -> Dict:
    """
    Main function to analyze patient video and integrate with case
    """
    analyzer = VideoAnalyzer()
    
    # Comprehensive analysis
    if include_audio:
        results = analyzer.analyze_video_comprehensive(video_path, extract_audio=True)
    else:
        results = {
            "video_analysis": analyzer.analyze_video(video_path),
            "audio_analysis": {},
            "integrated_findings": {}
        }
    
    # Integrate with case data
    integrator = VideoIntegrator()
    final_result = integrator.integrate_video_with_case(
        results["video_analysis"],
        results["audio_analysis"],
        case_data
    )
    
    final_result["video_results"] = results
    
    return final_result
