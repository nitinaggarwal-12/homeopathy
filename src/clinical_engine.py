"""
Advanced Clinical Homeopathy Engine
Based on classical methodology with modern AI enhancement
"""
import os
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import json

class ClinicalScoringEngine:
    """
    Advanced scoring system based on Boenninghausen's methodology
    with Kent's hierarchy of symptoms
    """
    
    # Kent's Hierarchy Weights
    MENTAL_EMOTIONAL_WEIGHT = 10  # Highest priority
    GENERAL_SYMPTOMS_WEIGHT = 7   # Physical generals
    PARTICULAR_SYMPTOMS_WEIGHT = 3 # Local symptoms
    MODALITY_WEIGHT = 5            # Better/worse factors
    CAUSATION_WEIGHT = 8           # Etiology/causation
    CONCOMITANT_WEIGHT = 4         # Accompanying symptoms
    
    # Miasmatic influences
    MIASMS = {
        'psora': ['itching', 'suppression', 'functional', 'deficiency'],
        'sycosis': ['overgrowth', 'warts', 'tumors', 'excess'],
        'syphilis': ['destruction', 'ulceration', 'deformity', 'night aggravation'],
        'tubercular': ['weakness', 'emaciation', 'restlessness', 'changing symptoms']
    }
    
    def __init__(self):
        self.remedy_scores = defaultdict(float)
        self.remedy_evidence = defaultdict(list)
        self.constitutional_markers = {}
        self.miasmatic_indicators = defaultdict(int)
    
    def calculate_totality_score(self, case_data: Dict, remedy_data: Dict) -> float:
        """
        Calculate comprehensive totality score based on:
        1. Kent's hierarchy of symptoms
        2. Boenninghausen's characteristic symptoms
        3. Constitutional match
        4. Miasmatic layer
        """
        total_score = 0.0
        
        # 1. Mental/Emotional Symptoms (Highest Weight)
        mental_score = self._score_mental_symptoms(
            case_data.get('mental_emotional', []),
            remedy_data
        )
        total_score += mental_score * self.MENTAL_EMOTIONAL_WEIGHT
        
        # 2. General Symptoms
        general_score = self._score_generals(case_data, remedy_data)
        total_score += general_score * self.GENERAL_SYMPTOMS_WEIGHT
        
        # 3. Causation/Etiology
        causation_score = self._score_causation(
            case_data.get('etiology', ''),
            remedy_data
        )
        total_score += causation_score * self.CAUSATION_WEIGHT
        
        # 4. Modalities
        modality_score = self._score_modalities(case_data, remedy_data)
        total_score += modality_score * self.MODALITY_WEIGHT
        
        # 5. Particulars (Lower weight)
        particular_score = self._score_particulars(
            case_data.get('particulars', []),
            remedy_data
        )
        total_score += particular_score * self.PARTICULAR_SYMPTOMS_WEIGHT
        
        # 6. Constitutional Match
        constitutional_score = self._score_constitution(case_data, remedy_data)
        total_score += constitutional_score * 6
        
        # 7. Miasmatic Layer
        miasmatic_score = self._assess_miasm(case_data, remedy_data)
        total_score += miasmatic_score * 4
        
        return total_score
    
    def _score_mental_symptoms(self, mental_symptoms: List[str], remedy_data: Dict) -> float:
        """Score mental/emotional symptoms - highest priority"""
        if not mental_symptoms:
            return 0.0
        
        remedy_text = str(remedy_data).lower()
        matches = 0
        total = len(mental_symptoms)
        
        for symptom in mental_symptoms:
            symptom_lower = symptom.lower()
            # Check for keyword matches
            keywords = symptom_lower.split()
            if any(keyword in remedy_text for keyword in keywords if len(keyword) > 3):
                matches += 1
        
        return matches / total if total > 0 else 0.0
    
    def _score_generals(self, case_data: Dict, remedy_data: Dict) -> float:
        """Score general symptoms (thermal, cravings, aversions, sleep)"""
        score = 0.0
        count = 0
        
        remedy_text = str(remedy_data).lower()
        
        # Thermal state
        thermal = case_data.get('thermal', '').lower()
        if thermal and thermal in remedy_text:
            score += 1.0
            count += 1
        
        # Cravings
        for craving in case_data.get('cravings', []):
            if craving.lower() in remedy_text:
                score += 1.0
            count += 1
        
        # Aversions
        for aversion in case_data.get('aversions', []):
            if aversion.lower() in remedy_text:
                score += 1.0
            count += 1
        
        # Sleep
        for sleep_symptom in case_data.get('sleep', []):
            if sleep_symptom.lower() in remedy_text:
                score += 0.5
            count += 1
        
        return score / count if count > 0 else 0.0
    
    def _score_causation(self, etiology: str, remedy_data: Dict) -> float:
        """Score causation/etiology - very important"""
        if not etiology:
            return 0.0
        
        remedy_text = str(remedy_data).lower()
        etiology_lower = etiology.lower()
        
        # Strong causation indicators
        causation_keywords = {
            'grief': ['grief', 'loss', 'disappointment', 'bereavement'],
            'anger': ['anger', 'indignation', 'rage', 'suppressed anger'],
            'fright': ['fright', 'shock', 'fear', 'trauma'],
            'cold': ['cold', 'exposure', 'draft', 'chill'],
            'injury': ['injury', 'trauma', 'accident', 'fall']
        }
        
        for cause_type, keywords in causation_keywords.items():
            if any(kw in etiology_lower for kw in keywords):
                if any(kw in remedy_text for kw in keywords):
                    return 1.0
        
        return 0.0
    
    def _score_modalities(self, case_data: Dict, remedy_data: Dict) -> float:
        """Score modalities (better/worse conditions)"""
        # This would need more sophisticated parsing
        # For now, basic implementation
        return 0.5
    
    def _score_particulars(self, particulars: List, remedy_data: Dict) -> float:
        """Score particular/local symptoms"""
        if not particulars:
            return 0.0
        
        remedy_text = str(remedy_data).lower()
        matches = 0
        
        for particular in particulars:
            desc = particular.get('description', '').lower()
            if desc and desc in remedy_text:
                matches += 1
        
        return matches / len(particulars) if particulars else 0.0
    
    def _score_constitution(self, case_data: Dict, remedy_data: Dict) -> float:
        """Assess constitutional match"""
        # Basic implementation - would need more data
        return 0.5
    
    def _assess_miasm(self, case_data: Dict, remedy_data: Dict) -> float:
        """Assess miasmatic layer"""
        # Basic miasmatic assessment
        case_text = str(case_data).lower()
        
        for miasm, indicators in self.MIASMS.items():
            for indicator in indicators:
                if indicator in case_text:
                    self.miasmatic_indicators[miasm] += 1
        
        return 0.5


class DifferentialAnalyzer:
    """
    Advanced differential diagnosis system
    Compares top remedies using characteristic symptoms
    """
    
    def __init__(self):
        self.comparison_matrix = {}
    
    def compare_remedies(self, case_data: Dict, top_remedies: List[Dict], 
                        mm_context: List[Dict]) -> Dict:
        """
        Perform detailed differential analysis
        Returns the most indicated remedy with confidence score
        """
        if len(top_remedies) < 2:
            if top_remedies:
                return {
                    'selected_remedy': top_remedies[0]['name'],
                    'confidence': 0.7,
                    'differential': [],
                    'reasoning': 'Single clear indication'
                }
            return {'selected_remedy': None, 'confidence': 0.0}
        
        # Compare top 3 remedies
        comparisons = []
        for remedy in top_remedies[:3]:
            remedy_name = remedy['name']
            
            # Find MM context for this remedy
            remedy_mm = next((mm for mm in mm_context if mm['remedy'] == remedy_name), None)
            
            if remedy_mm:
                characteristic_matches = self._find_characteristic_symptoms(
                    case_data, remedy_mm
                )
                
                comparisons.append({
                    'remedy': remedy_name,
                    'score': remedy['score'],
                    'characteristic_matches': characteristic_matches,
                    'match_count': len(characteristic_matches)
                })
        
        # Sort by characteristic matches (quality over quantity)
        comparisons.sort(key=lambda x: (x['match_count'], x['score']), reverse=True)
        
        if comparisons:
            best = comparisons[0]
            confidence = self._calculate_confidence(best, comparisons)
            
            return {
                'selected_remedy': best['remedy'],
                'confidence': confidence,
                'characteristic_matches': best['characteristic_matches'],
                'differential': comparisons[1:],
                'reasoning': f"Selected based on {best['match_count']} characteristic symptoms"
            }
        
        return {'selected_remedy': None, 'confidence': 0.0}
    
    def _find_characteristic_symptoms(self, case_data: Dict, remedy_mm: Dict) -> List[str]:
        """
        Identify characteristic (pathognomonic) symptoms
        These are the symptoms that strongly indicate a specific remedy
        """
        characteristics = []
        
        # Check mental/emotional characteristics
        for mental in case_data.get('mental_emotional', []):
            if mental.lower() in str(remedy_mm).lower():
                characteristics.append(f"Mental: {mental}")
        
        # Check generals
        thermal = case_data.get('thermal')
        if thermal and thermal.lower() in str(remedy_mm).lower():
            characteristics.append(f"General: {thermal}")
        
        # Check causation
        etiology = case_data.get('etiology')
        if etiology and etiology.lower() in str(remedy_mm).lower():
            characteristics.append(f"Causation: {etiology}")
        
        return characteristics
    
    def _calculate_confidence(self, best: Dict, all_comparisons: List[Dict]) -> float:
        """
        Calculate confidence score based on:
        - Number of characteristic matches
        - Gap between top remedies
        - Absolute score
        """
        if not all_comparisons:
            return 0.5
        
        # Base confidence on characteristic matches
        match_confidence = min(best['match_count'] / 5.0, 1.0)  # 5+ matches = full confidence
        
        # Adjust based on gap to second remedy
        if len(all_comparisons) > 1:
            gap = best['match_count'] - all_comparisons[1]['match_count']
            gap_confidence = min(gap / 3.0, 0.3)  # Max 0.3 boost from gap
        else:
            gap_confidence = 0.3
        
        total_confidence = min(match_confidence + gap_confidence, 1.0)
        
        return round(total_confidence, 2)


class PotencySelector:
    """
    Intelligent potency selection based on:
    - Vitality of patient
    - Acuteness vs chronicity
    - Mental vs physical symptoms
    - Sensitivity
    """
    
    POTENCY_GUIDELINES = {
        'acute_high_vitality': '200C',
        'acute_moderate': '30C',
        'acute_low_vitality': '6C',
        'chronic_clear_mental': '200C',
        'chronic_mixed': '30C',
        'chronic_physical': '30C',
        'sensitive': '6C',
        'elderly': '30C',
        'children': '30C'
    }
    
    def select_potency(self, case_data: Dict, remedy_confidence: float) -> Tuple[str, str]:
        """
        Select appropriate potency and repetition
        Returns: (potency, repetition_guidance)
        """
        # Assess case characteristics
        is_acute = self._is_acute(case_data)
        has_strong_mental = len(case_data.get('mental_emotional', [])) >= 3
        vitality = self._assess_vitality(case_data)
        
        # Select potency
        if is_acute:
            if vitality == 'high':
                potency = '200C'
                repetition = "Single dose, observe 12-24 hours"
            elif vitality == 'moderate':
                potency = '30C'
                repetition = "Single dose, may repeat after 6-12 hours if needed"
            else:
                potency = '6C'
                repetition = "May repeat every 2-4 hours in acute phase"
        else:  # Chronic
            if has_strong_mental and remedy_confidence > 0.8:
                potency = '200C'
                repetition = "Single dose, wait 7-14 days, observe carefully"
            else:
                potency = '30C'
                repetition = "Single dose, wait 5-7 days, observe response"
        
        return potency, repetition
    
    def _is_acute(self, case_data: Dict) -> bool:
        """Determine if case is acute or chronic"""
        duration = case_data.get('duration', '').lower()
        onset = case_data.get('onset', '').lower()
        
        acute_indicators = ['sudden', 'hours', 'days', 'yesterday', 'today', 'acute']
        return any(indicator in duration + onset for indicator in acute_indicators)
    
    def _assess_vitality(self, case_data: Dict) -> str:
        """Assess patient vitality"""
        # Simple assessment - would need more data in practice
        generals = ' '.join(case_data.get('generals', [])).lower()
        lifestyle = ' '.join(case_data.get('lifestyle', [])).lower()
        
        low_vitality_indicators = ['weak', 'exhausted', 'elderly', 'debilitated', 'chronic']
        
        if any(indicator in generals + lifestyle for indicator in low_vitality_indicators):
            return 'low'
        
        return 'moderate'  # Default to moderate


class FollowUpAnalyzer:
    """
    Analyze follow-up responses and guide next steps
    Based on Hahnemann's observations and Kent's guidelines
    """
    
    RESPONSE_PATTERNS = {
        'ideal': {
            'description': 'Improvement in order: Mental → General → Particular',
            'action': 'Wait and observe, do not repeat'
        },
        'aggravation_then_improvement': {
            'description': 'Initial aggravation followed by improvement',
            'action': 'Good sign, wait and observe'
        },
        'no_response': {
            'description': 'No change after appropriate time',
            'action': 'Consider different remedy or potency'
        },
        'partial_response': {
            'description': 'Some improvement but incomplete',
            'action': 'Wait longer or consider complementary remedy'
        },
        'new_symptoms': {
            'description': 'New symptoms appearing',
            'action': 'Assess if proving or uncovering deeper layer'
        }
    }
    
    def analyze_response(self, initial_case: Dict, follow_up: Dict) -> Dict:
        """Analyze patient response to remedy"""
        # This would need actual follow-up data structure
        # Placeholder for future implementation
        return {
            'pattern': 'ideal',
            'recommendation': 'Continue observation',
            'next_steps': []
        }


def get_clinical_recommendation(case_data: Dict, repertory_result: Dict, 
                                mm_context: List[Dict]) -> Dict:
    """
    Main function to get clinical recommendation using advanced engines
    """
    # Initialize engines
    scorer = ClinicalScoringEngine()
    differentiator = DifferentialAnalyzer()
    potency_selector = PotencySelector()
    
    # Get top candidates from repertory
    top_candidates = repertory_result.get('candidates', [])[:5]
    
    if not top_candidates:
        return {
            'status': 'insufficient_data',
            'message': 'Unable to find matching remedies. Please provide more detailed symptoms.'
        }
    
    # Perform differential analysis
    differential = differentiator.compare_remedies(case_data, top_candidates, mm_context)
    
    if not differential.get('selected_remedy'):
        return {
            'status': 'unclear',
            'message': 'Multiple remedies indicated. Need more differentiating symptoms.',
            'candidates': top_candidates[:3]
        }
    
    # Select potency
    potency, repetition = potency_selector.select_potency(
        case_data, 
        differential.get('confidence', 0.5)
    )
    
    return {
        'status': 'success',
        'remedy': differential['selected_remedy'],
        'potency': potency,
        'confidence': differential['confidence'],
        'repetition': repetition,
        'characteristic_symptoms': differential.get('characteristic_matches', []),
        'differential_diagnosis': differential.get('differential', []),
        'reasoning': differential.get('reasoning', ''),
        'clinical_notes': _generate_clinical_notes(case_data, differential)
    }


def _generate_clinical_notes(case_data: Dict, differential: Dict) -> List[str]:
    """Generate clinical notes for the prescription"""
    notes = []
    
    # Confidence assessment
    confidence = differential.get('confidence', 0)
    if confidence >= 0.8:
        notes.append("High confidence prescription based on clear characteristic symptoms")
    elif confidence >= 0.6:
        notes.append("Moderate confidence - observe response carefully")
    else:
        notes.append("Low confidence - consider this as trial prescription, reassess after 5-7 days")
    
    # Monitoring guidance
    notes.append("Monitor in this order: 1) Mental/emotional state, 2) Energy/sleep/appetite, 3) Chief complaint")
    notes.append("Good response: Improvement should follow Hering's Law (inside out, top to bottom, reverse order of appearance)")
    
    # Red flags
    if case_data.get('red_flags'):
        notes.append("⚠️ Red flags present - ensure appropriate medical supervision")
    
    return notes
