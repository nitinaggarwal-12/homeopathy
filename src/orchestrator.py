"""
Multi-agent orchestrator for classical homeopathy workflow:
CaseTaker → Repertory → MateriaMedica → Differential → Prescription → Wellness
"""
import os
import json
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

from .repertory import repertorize
from .safety import has_red_flags
from .embeddings import search as mm_search
from .clinical_engine import get_clinical_recommendation
from .intelligent_questioning import should_ask_more_questions, IntelligentQuestioner

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_HIGH_REASONING = os.getenv("OPENAI_HIGH_REASONING", "gpt-4o")
REPERTORY_PATH = os.getenv("REPERTORY_PATH", "data/repertory_mapping.csv")


def load_prompt(filename: str) -> str:
    """Load prompt from prompts/ directory"""
    path = os.path.join("prompts", filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def _client():
    if OpenAI is None:
        raise RuntimeError("openai package not installed")
    return OpenAI(api_key=OPENAI_API_KEY)


def call_llm(system_prompt: str, user_message: str, model: str = None, temperature: float = 0.3) -> str:
    """Call OpenAI Chat Completions API"""
    client = _client()
    model = model or OPENAI_MODEL
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content


def agent_case_taker(case_data: Dict) -> Dict:
    """
    CaseTakerAgent: Validates and structures case data
    Returns structured case with any missing critical fields flagged
    """
    # Check for red flags first
    flags = has_red_flags(case_data)
    if flags:
        return {
            "status": "emergency",
            "red_flags": flags,
            "message": "URGENT: Please seek immediate medical attention for these symptoms."
        }
    
    # Validate minimum required fields
    missing = []
    if not case_data.get("presenting_complaint"):
        missing.append("presenting_complaint")
    
    if missing:
        return {
            "status": "incomplete",
            "missing_fields": missing,
            "message": "Please provide the presenting complaint to continue."
        }
    
    return {
        "status": "complete",
        "case": case_data,
        "message": "Case data validated successfully."
    }


def agent_repertory(case_data: Dict) -> Dict:
    """
    RepertoryAgent: Converts symptoms into rubrics and proposes candidate remedies
    """
    rep_result = repertorize(case_data, REPERTORY_PATH)
    
    return {
        "status": "complete",
        "repertory": rep_result,
        "top_candidates": rep_result.get("candidates", [])[:5],
        "message": f"Found {len(rep_result.get('candidates', []))} candidate remedies."
    }


def agent_materia_medica(candidates: List[Dict], case_summary: str) -> Dict:
    """
    MateriaMedicaAgent: Cross-checks candidates with MM using embeddings
    """
    # Search MM for each top candidate
    mm_context = []
    
    for candidate in candidates[:3]:  # Top 3 only
        remedy_name = candidate.get("name", "")
        search_query = f"{remedy_name} {case_summary}"
        results = mm_search(search_query, k=2)
        
        if results:
            mm_context.append({
                "remedy": remedy_name,
                "score": candidate.get("score", 0),
                "mm_excerpts": [r.get("excerpt", "") for r in results]
            })
    
    return {
        "status": "complete",
        "mm_context": mm_context,
        "message": f"Retrieved Materia Medica context for {len(mm_context)} remedies."
    }


def agent_differential(case_data: Dict, repertory_result: Dict, mm_context: List[Dict]) -> Dict:
    """
    DifferentialAgent: Uses advanced clinical engine + LLM for analysis
    """
    # First, use clinical engine for rule-based analysis
    clinical_result = get_clinical_recommendation(case_data, repertory_result, mm_context)
    
    if clinical_result.get('status') == 'success':
        # We have a clear clinical recommendation
        # Now enhance with LLM for wellness advice and detailed rationale
        system_prompt = load_prompt("system.txt")
        dosage_policy = load_prompt("dosage_policy.txt")
        
        user_message = f"""
# Clinical Analysis Complete

Selected Remedy: {clinical_result['remedy']}
Potency: {clinical_result['potency']}
Confidence: {clinical_result['confidence']}
Characteristic Symptoms: {', '.join(clinical_result.get('characteristic_symptoms', []))}

# Case Summary
Presenting Complaint: {case_data.get('presenting_complaint', 'N/A')}
Mental/Emotional: {', '.join(case_data.get('mental_emotional', []))}
Generals: {', '.join(case_data.get('generals', []))}
Thermal: {case_data.get('thermal', 'N/A')}
Past History: {', '.join(case_data.get('past_history', []))}
Family History: {', '.join(case_data.get('family_history', []))}
Lifestyle: {', '.join(case_data.get('lifestyle', []))}

Please provide:
1. Detailed rationale for why {clinical_result['remedy']} is indicated
2. Key monitoring points specific to this remedy
3. Wellness advice (diet, lifestyle, mental health) tailored to this case
4. Expected timeline for response

Return as JSON with fields: rationale (list), monitoring (list), wellness_advice (list), expected_response (string)
"""
        
        try:
            response = call_llm(system_prompt, user_message, model=OPENAI_HIGH_REASONING, temperature=0.3)
            
            # Parse JSON
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "{" in response:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
            else:
                json_str = response
            
            llm_enhancement = json.loads(json_str)
            
            # Combine clinical + LLM results
            return {
                "status": "complete",
                "remedy": clinical_result['remedy'],
                "potency": clinical_result['potency'],
                "confidence": clinical_result['confidence'],
                "rationale": llm_enhancement.get('rationale', [clinical_result.get('reasoning', '')]),
                "matched_keynotes": clinical_result.get('characteristic_symptoms', []),
                "monitoring": llm_enhancement.get('monitoring', clinical_result.get('clinical_notes', [])),
                "needs_clarification": False,
                "clarification_questions": [],
                "wellness_advice": llm_enhancement.get('wellness_advice', []),
                "expected_response": llm_enhancement.get('expected_response', clinical_result.get('repetition', '')),
                "differential": clinical_result.get('differential_diagnosis', []),
                "clinical_confidence": clinical_result['confidence']
            }
            
        except Exception as e:
            # If LLM fails, return clinical result alone
            return {
                "status": "complete",
                "remedy": clinical_result['remedy'],
                "potency": clinical_result['potency'],
                "confidence": clinical_result['confidence'],
                "rationale": [clinical_result.get('reasoning', '')],
                "matched_keynotes": clinical_result.get('characteristic_symptoms', []),
                "monitoring": clinical_result.get('clinical_notes', []),
                "needs_clarification": False,
                "clarification_questions": [],
                "wellness_advice": ["Maintain regular sleep schedule", "Eat fresh, wholesome foods", "Practice stress management"],
                "expected_response": clinical_result.get('repetition', '')
            }
    
    else:
        # Clinical engine couldn't decide - use LLM for analysis
        system_prompt = load_prompt("system.txt")
        dosage_policy = load_prompt("dosage_policy.txt")
        
        user_message = f"""
# Case Summary
Presenting Complaint: {case_data.get('presenting_complaint', 'N/A')}
Mental/Emotional: {', '.join(case_data.get('mental_emotional', []))}
Generals: {', '.join(case_data.get('generals', []))}
Thermal: {case_data.get('thermal', 'N/A')}
Cravings: {', '.join(case_data.get('cravings', []))}
Aversions: {', '.join(case_data.get('aversions', []))}
Sleep: {', '.join(case_data.get('sleep', []))}
Past History: {', '.join(case_data.get('past_history', []))}
Family History: {', '.join(case_data.get('family_history', []))}

# Top Candidates
{json.dumps(repertory_result.get('candidates', [])[:5], indent=2)}

# Materia Medica Context
{json.dumps(mm_context, indent=2)}

Based on classical homeopathy principles, analyze and recommend ONE remedy if ≥3 characteristic keynotes match.
If insufficient evidence, request clarification.
"""
        
        try:
            response = call_llm(system_prompt, user_message, model=OPENAI_HIGH_REASONING, temperature=0.2)
            
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "{" in response:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
            else:
                json_str = response
            
            result = json.loads(json_str)
            result["status"] = "complete"
            result["clinical_confidence"] = 0.5  # Lower confidence when clinical engine couldn't decide
            return result
            
        except json.JSONDecodeError:
            return {
                "status": "complete",
                "remedy": None,
                "potency": None,
                "rationale": ["Unable to determine clear remedy. More symptoms needed."],
                "matched_keynotes": [],
                "monitoring": [],
                "needs_clarification": True,
                "clarification_questions": ["Please provide more detailed mental/emotional symptoms", "Describe modalities (what makes symptoms better or worse)"],
                "wellness_advice": []
            }


def agent_prescription(differential_result: Dict) -> Dict:
    """
    PrescriptionAgent: Formats final prescription with disclaimer
    """
    disclaimer = load_prompt("disclaimer.txt")
    
    if differential_result.get("needs_clarification"):
        return {
            "status": "needs_clarification",
            "questions": differential_result.get("clarification_questions", []),
            "message": "Additional information needed for accurate prescription."
        }
    
    remedy = differential_result.get("remedy")
    if not remedy:
        return {
            "status": "insufficient_evidence",
            "message": "Unable to determine a clear remedy. Please consult a qualified homeopath.",
            "disclaimer": disclaimer
        }
    
    return {
        "status": "complete",
        "prescription": {
            "remedy": remedy,
            "potency": differential_result.get("potency"),
            "rationale": differential_result.get("rationale", []),
            "matched_keynotes": differential_result.get("matched_keynotes", []),
            "monitoring": differential_result.get("monitoring", []),
            "wellness_advice": differential_result.get("wellness_advice", [])
        },
        "disclaimer": disclaimer,
        "message": f"Prescription: {remedy} {differential_result.get('potency', '')}"
    }


def run_full_case_workflow(case_data: Dict, skip_questioning: bool = False) -> Dict:
    """
    Orchestrates the complete workflow:
    CaseTaker → Repertory → MateriaMedica → Differential → Prescription
    """
    workflow_result = {
        "steps": [],
        "final_result": None
    }
    
    # Step 1: Case Taking
    case_result = agent_case_taker(case_data)
    workflow_result["steps"].append({"agent": "CaseTaker", "result": case_result})
    
    if case_result["status"] == "emergency":
        workflow_result["final_result"] = case_result
        return workflow_result
    
    if case_result["status"] == "incomplete":
        workflow_result["final_result"] = case_result
        return workflow_result
    
    # Step 2: Repertorization
    repertory_result = agent_repertory(case_data)
    workflow_result["steps"].append({"agent": "Repertory", "result": repertory_result})
    
    if not repertory_result.get("top_candidates"):
        workflow_result["final_result"] = {
            "status": "no_candidates",
            "message": "No matching remedies found. Please provide more detailed symptoms."
        }
        return workflow_result
    
    # Step 3: Materia Medica Search
    case_summary = f"{case_data.get('presenting_complaint', '')} {' '.join(case_data.get('mental_emotional', []))} {' '.join(case_data.get('generals', []))}"
    mm_result = agent_materia_medica(repertory_result["top_candidates"], case_summary)
    workflow_result["steps"].append({"agent": "MateriaMedica", "result": mm_result})
    
    # Step 4: Check if more questions needed before differential (unless skipped for test cases)
    top_remedy_names = [r['name'] for r in repertory_result["top_candidates"][:3]]
    
    if not skip_questioning:
        should_ask, question_analysis = should_ask_more_questions(
            case_data, 
            confidence=0.5,  # Initial confidence before differential
            top_remedies=top_remedy_names
        )
        
        if should_ask and question_analysis['completeness_score'] < 0.6:
            # Case too incomplete - ask questions first
            workflow_result["final_result"] = {
                "status": "needs_more_information",
                "message": question_analysis['reason'],
                "completeness_score": question_analysis['completeness_score'],
                "questions_to_ask": question_analysis['questions_to_ask'],
                "estimated_questions": question_analysis['estimated_questions_needed']
            }
            workflow_result["steps"].append({
                "agent": "IntelligentQuestioner",
                "result": {
                    "status": "questions_required",
                    "message": f"Need {question_analysis['estimated_questions_needed']} clarifying questions"
                }
            })
            return workflow_result
    
    # Step 5: Differential Analysis
    differential_result = agent_differential(case_data, repertory_result["repertory"], mm_result["mm_context"])
    workflow_result["steps"].append({"agent": "Differential", "result": differential_result})
    
    # Step 6: Check if questions needed after differential (skip for test cases)
    if not skip_questioning and differential_result.get("remedy"):
        confidence = differential_result.get("clinical_confidence", differential_result.get("confidence", 0.5))
        should_ask_post, post_question_analysis = should_ask_more_questions(
            case_data,
            confidence=confidence,
            top_remedies=top_remedy_names
        )
        
        if should_ask_post and confidence < 0.7:
            # Add clarifying questions to result
            differential_result["needs_clarification"] = True
            differential_result["clarification_questions"] = [
                q['question'] for q in post_question_analysis['questions_to_ask'][:5]
            ]
            differential_result["clarification_reason"] = post_question_analysis['reason']
    
    # Step 7: Prescription
    prescription_result = agent_prescription(differential_result)
    workflow_result["steps"].append({"agent": "Prescription", "result": prescription_result})
    
    workflow_result["final_result"] = prescription_result
    
    return workflow_result
