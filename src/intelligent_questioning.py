"""
Intelligent Questioning System for Homeopathy
Dynamically generates targeted follow-up questions based on case analysis
Ensures complete totality before prescribing
"""
from typing import Dict, List, Optional, Tuple
import json


class IntelligentQuestioner:
    """
    Generates intelligent follow-up questions based on case analysis
    Identifies gaps in information needed for accurate prescribing
    """
    
    # Essential information categories
    ESSENTIAL_CATEGORIES = {
        'mental_emotional': {
            'weight': 10,
            'min_required': 2,
            'questions': [
                "How would you describe your emotional state? (anxious, irritable, sad, fearful, etc.)",
                "Do you prefer company or solitude when unwell?",
                "What are your main fears or anxieties?",
                "How do you react to stress or bad news?",
                "Do you weep easily? If so, does consolation help or make it worse?",
                "Are you more irritable than usual?",
                "Do you have any recurring dreams or nightmares?",
                "How is your memory and concentration?",
                "Do you tend to be hurried or slow in your actions?",
                "Are you more critical of yourself or others lately?"
            ]
        },
        'thermal_state': {
            'weight': 8,
            'min_required': 1,
            'questions': [
                "Are you generally a hot person or cold person?",
                "Do you prefer warm or cool rooms?",
                "Do you like fresh air or prefer windows closed?",
                "How are your hands and feet - usually warm or cold?",
                "Do you sweat easily? If so, where and when?",
                "Does your condition get worse in hot or cold weather?"
            ]
        },
        'modalities': {
            'weight': 9,
            'min_required': 3,
            'questions': [
                "What makes your symptoms BETTER? (time, position, temperature, pressure, motion, rest, etc.)",
                "What makes your symptoms WORSE? (time, position, temperature, pressure, motion, rest, etc.)",
                "Is there a specific time of day when symptoms are worse?",
                "Does motion/walking make you feel better or worse?",
                "Does lying down help or worsen your symptoms?",
                "Does pressure or rubbing the affected area help?",
                "Are symptoms worse before, during, or after eating?",
                "Does weather affect your symptoms? (cold, damp, heat, storms, etc.)"
            ]
        },
        'food_preferences': {
            'weight': 6,
            'min_required': 2,
            'questions': [
                "What foods do you strongly CRAVE or desire?",
                "What foods do you have an AVERSION to or dislike?",
                "Do you prefer warm or cold drinks?",
                "How is your thirst - excessive, moderate, or little thirst?",
                "Do you crave salt, sweets, sour, spicy, or fatty foods?",
                "Are there foods that definitely disagree with you or make symptoms worse?"
            ]
        },
        'sleep': {
            'weight': 7,
            'min_required': 2,
            'questions': [
                "How is your sleep quality?",
                "What position do you sleep in? (back, side, stomach, curled up, etc.)",
                "Do you feel refreshed after sleep or still tired?",
                "What time do you typically fall asleep and wake up?",
                "Do you have difficulty falling asleep or staying asleep?",
                "Do you wake at a specific time each night?",
                "Do you snore or have breathing issues during sleep?",
                "Do you sweat during sleep? If so, where?"
            ]
        },
        'causation': {
            'weight': 9,
            'min_required': 1,
            'questions': [
                "What do you think caused this condition? (physical, emotional, environmental)",
                "Did this start after any specific event? (grief, anger, fright, injury, exposure, etc.)",
                "Have you had any major emotional shocks or traumas recently?",
                "Did this begin after suppression of something? (skin eruption, discharge, emotions, etc.)",
                "Any recent changes in life circumstances?",
                "Exposure to cold, heat, damp, or weather changes before onset?"
            ]
        },
        'laterality': {
            'weight': 6,
            'min_required': 1,
            'questions': [
                "Are symptoms more on the RIGHT side or LEFT side?",
                "Do symptoms move from one side to the other?",
                "Which side of the body is generally more affected by problems?"
            ]
        },
        'discharges': {
            'weight': 5,
            'min_required': 1,
            'questions': [
                "Is there any discharge? (nasal, vaginal, wound, etc.)",
                "If yes, what color is it? (clear, yellow, green, white, bloody)",
                "What is the consistency? (thin, thick, stringy, watery)",
                "Does it have an odor?",
                "Is it irritating or bland?"
            ]
        },
        'menstrual': {
            'weight': 7,
            'min_required': 2,
            'applicable_to': 'female',
            'questions': [
                "Are your periods regular or irregular?",
                "How is the flow - heavy, moderate, scanty?",
                "What color is the menstrual blood?",
                "Are periods painful? If so, what kind of pain?",
                "Do you have PMS symptoms? What kind?",
                "How do you feel emotionally before, during, and after periods?",
                "Are other symptoms better or worse during menses?"
            ]
        },
        'past_suppression': {
            'weight': 8,
            'min_required': 1,
            'questions': [
                "Have you ever had skin eruptions that were suppressed with creams/ointments?",
                "Have any discharges been stopped with medications?",
                "Have you taken steroids or strong medications in the past?",
                "Were any symptoms suddenly stopped or suppressed?",
                "History of vaccinations and any reactions?"
            ]
        }
    }
    
    # Differential diagnosis questions (remedy-specific)
    DIFFERENTIAL_QUESTIONS = {
        'sulphur_vs_pulsatilla': [
            "Do you feel worse from heat or better from heat?",
            "Do you prefer to be alone or seek company when ill?",
            "Are you generally warm-blooded or chilly?"
        ],
        'arsenicum_vs_phosphorus': [
            "Are you anxious about your health and future?",
            "Do you feel better with company or prefer to be alone?",
            "Do you desire cold drinks or warm drinks?"
        ],
        'nux_vomica_vs_lycopodium': [
            "What time of day are symptoms worst? (morning vs afternoon/evening)",
            "Do you have digestive issues with bloating?",
            "Are you more irritable or lacking in confidence?"
        ],
        'natrum_mur_vs_ignatia': [
            "Do you weep alone or in company?",
            "Does consolation help or make you feel worse?",
            "Are symptoms changeable or consistent?"
        ],
        'bryonia_vs_rhus_tox': [
            "Does motion make symptoms better or worse?",
            "Do you feel better lying still or moving about?",
            "Is there stiffness that improves with continued motion?"
        ]
    }
    
    # Symptom-specific clarification questions
    SYMPTOM_CLARIFICATIONS = {
        'headache': [
            "Describe the exact location of the headache",
            "What does the pain feel like? (throbbing, pressing, bursting, sharp, dull)",
            "Does it extend or radiate anywhere?",
            "What brings it on? (sun, mental exertion, hunger, etc.)",
            "Does pressure or binding the head help?"
        ],
        'cough': [
            "Is the cough dry or with expectoration?",
            "If with expectoration, what color and consistency?",
            "What time of day is cough worse?",
            "What triggers the cough? (lying down, talking, cold air, etc.)",
            "Is there a tickling sensation? Where?"
        ],
        'pain': [
            "Describe the exact character of pain (burning, stitching, cramping, etc.)",
            "Does the pain stay in one place or move around?",
            "Rate pain intensity (1-10)",
            "Does the pain come and go or is it constant?",
            "What position gives relief?"
        ],
        'fever': [
            "Is there a pattern to the fever? (time of day, alternating with chills)",
            "Do you have chills? Before, during, or after fever?",
            "Is there sweating? When and where?",
            "Are you thirsty during fever? For what?",
            "Do you want to be covered or uncovered?"
        ],
        'anxiety': [
            "When is anxiety worst? (time of day, situations)",
            "What are you anxious about specifically?",
            "Physical symptoms with anxiety? (palpitations, trembling, etc.)",
            "Does anticipation of events make you anxious?",
            "How does anxiety affect your daily functioning?"
        ],
        'skin_eruption': [
            "Describe the appearance (color, size, shape, texture)",
            "Is there itching? When is it worse?",
            "Does scratching help or make it worse?",
            "Any discharge? What kind?",
            "Does heat or cold affect it?",
            "Where did it first appear and how has it spread?"
        ],
        'digestive': [
            "Describe the exact nature of digestive discomfort",
            "When does it occur in relation to eating?",
            "What foods make it better or worse?",
            "Is there bloating? When?",
            "Bowel movements - frequency, consistency, color, odor",
            "Any specific cravings or aversions?"
        ],
        'joint_pain': [
            "Which joints are affected? (be specific)",
            "Is there swelling, redness, or heat?",
            "Better or worse with first motion?",
            "Better or worse with continued motion?",
            "Better or worse with rest?",
            "Weather effects? (cold, damp, heat)",
            "Time of day when worst?"
        ]
    }
    
    def __init__(self):
        self.questions_asked = []
        self.information_gaps = []
    
    def analyze_case_completeness(self, case_data: Dict) -> Dict:
        """
        Analyze case data to identify information gaps
        Returns priority questions to ask
        """
        gaps = []
        priority_questions = []
        
        # Check each essential category
        for category, details in self.ESSENTIAL_CATEGORIES.items():
            # Skip gender-specific if not applicable
            if details.get('applicable_to') == 'female':
                # Would need gender info to determine
                pass
            
            # Check if category has sufficient information
            category_data = case_data.get(category, [])
            if isinstance(category_data, list):
                info_count = len([x for x in category_data if x])
            elif isinstance(category_data, str):
                info_count = 1 if category_data else 0
            else:
                info_count = 0
            
            min_required = details.get('min_required', 1)
            
            if info_count < min_required:
                gaps.append({
                    'category': category,
                    'weight': details['weight'],
                    'current_info': info_count,
                    'needed': min_required - info_count,
                    'questions': details['questions'][:min_required - info_count + 2]
                })
        
        # Sort gaps by weight (importance)
        gaps.sort(key=lambda x: x['weight'], reverse=True)
        
        # Generate priority questions
        for gap in gaps[:5]:  # Top 5 most important gaps
            priority_questions.extend(gap['questions'][:2])  # 2 questions per gap
        
        return {
            'completeness_score': self._calculate_completeness(case_data),
            'information_gaps': gaps,
            'priority_questions': priority_questions[:10],  # Max 10 questions
            'ready_for_prescription': len(gaps) <= 2 and self._calculate_completeness(case_data) >= 0.7
        }
    
    def generate_differential_questions(self, top_remedies: List[str]) -> List[str]:
        """
        Generate questions to differentiate between top remedy candidates
        """
        if len(top_remedies) < 2:
            return []
        
        questions = []
        
        # Check for known differentials
        remedy_pairs = [
            f"{top_remedies[0].lower().replace(' ', '_')}_vs_{top_remedies[1].lower().replace(' ', '_')}",
            f"{top_remedies[1].lower().replace(' ', '_')}_vs_{top_remedies[0].lower().replace(' ', '_')}"
        ]
        
        for pair in remedy_pairs:
            if pair in self.DIFFERENTIAL_QUESTIONS:
                questions.extend(self.DIFFERENTIAL_QUESTIONS[pair])
                break
        
        # If no specific differential found, ask general differentiating questions
        if not questions:
            questions = [
                f"Between {top_remedies[0]} and {top_remedies[1]}, we need to clarify:",
                "What is your exact thermal state? (hot/cold blooded)",
                "How do you respond emotionally to stress?",
                "What time of day are symptoms typically worst?",
                "Does motion make you feel better or worse overall?"
            ]
        
        return questions[:5]
    
    def generate_symptom_clarifications(self, case_data: Dict) -> List[str]:
        """
        Generate clarifying questions for specific symptoms mentioned
        """
        questions = []
        
        # Check presenting complaint for key symptom types
        complaint = case_data.get('presenting_complaint', '').lower()
        
        for symptom_type, symptom_questions in self.SYMPTOM_CLARIFICATIONS.items():
            if symptom_type in complaint:
                questions.extend(symptom_questions[:3])
        
        # Check particulars
        for particular in case_data.get('particulars', []):
            desc = particular.get('description', '').lower()
            for symptom_type, symptom_questions in self.SYMPTOM_CLARIFICATIONS.items():
                if symptom_type in desc:
                    questions.extend(symptom_questions[:2])
        
        return list(set(questions))[:8]  # Remove duplicates, max 8
    
    def generate_modality_questions(self, case_data: Dict) -> List[str]:
        """
        Generate specific modality questions if modalities are unclear
        """
        questions = []
        
        # Check if modalities are well documented
        modality_count = 0
        for particular in case_data.get('particulars', []):
            modality_count += len(particular.get('modalities_better', []))
            modality_count += len(particular.get('modalities_worse', []))
        
        if modality_count < 3:
            questions = [
                "What specific things make your symptoms BETTER? (Be as detailed as possible)",
                "What specific things make your symptoms WORSE? (Be as detailed as possible)",
                "Is there a specific time of day when you feel worst?",
                "Does weather affect your symptoms? How?",
                "Does eating affect your symptoms? Better or worse?",
                "Does position (lying, sitting, standing) affect symptoms?",
                "Does motion or rest help more?",
                "Does warmth or cold application help?"
            ]
        
        return questions[:6]
    
    def generate_constitutional_questions(self, case_data: Dict) -> List[str]:
        """
        Generate questions about constitutional state
        """
        questions = [
            "Describe your general energy level (high, moderate, low, exhausted)",
            "How do you handle stress generally?",
            "What is your general body temperature tendency? (always hot/cold/variable)",
            "Describe your personality in a few words",
            "What are your main life concerns or worries?",
            "How is your overall vitality and resilience?",
            "Do you catch colds easily or have strong immunity?",
            "How do you typically react to medications?"
        ]
        
        return questions[:5]
    
    def generate_comprehensive_questions(self, case_data: Dict, 
                                        top_remedies: List[str] = None,
                                        min_confidence: float = 0.8) -> Dict:
        """
        Generate comprehensive set of questions based on case analysis
        """
        # Analyze completeness
        completeness = self.analyze_case_completeness(case_data)
        
        all_questions = {
            'essential_information': [],
            'differential_diagnosis': [],
            'symptom_clarifications': [],
            'modality_details': [],
            'constitutional_assessment': [],
            'priority_order': []
        }
        
        # If case is incomplete, focus on essential information
        if not completeness['ready_for_prescription']:
            all_questions['essential_information'] = completeness['priority_questions']
        
        # If we have top remedies, ask differential questions
        if top_remedies and len(top_remedies) >= 2:
            all_questions['differential_diagnosis'] = self.generate_differential_questions(top_remedies)
        
        # Ask symptom clarifications
        all_questions['symptom_clarifications'] = self.generate_symptom_clarifications(case_data)
        
        # Ask modality questions if needed
        all_questions['modality_details'] = self.generate_modality_questions(case_data)
        
        # Constitutional questions
        all_questions['constitutional_assessment'] = self.generate_constitutional_questions(case_data)
        
        # Create priority order
        priority = []
        
        # Highest priority: essential information gaps
        if all_questions['essential_information']:
            priority.extend([
                {'question': q, 'category': 'essential', 'priority': 'high'}
                for q in all_questions['essential_information'][:5]
            ])
        
        # High priority: differential diagnosis
        if all_questions['differential_diagnosis']:
            priority.extend([
                {'question': q, 'category': 'differential', 'priority': 'high'}
                for q in all_questions['differential_diagnosis'][:3]
            ])
        
        # Medium priority: modalities
        if all_questions['modality_details']:
            priority.extend([
                {'question': q, 'category': 'modality', 'priority': 'medium'}
                for q in all_questions['modality_details'][:4]
            ])
        
        # Medium priority: symptom clarifications
        if all_questions['symptom_clarifications']:
            priority.extend([
                {'question': q, 'category': 'clarification', 'priority': 'medium'}
                for q in all_questions['symptom_clarifications'][:3]
            ])
        
        # Lower priority: constitutional
        if all_questions['constitutional_assessment']:
            priority.extend([
                {'question': q, 'category': 'constitutional', 'priority': 'low'}
                for q in all_questions['constitutional_assessment'][:2]
            ])
        
        all_questions['priority_order'] = priority
        all_questions['completeness_assessment'] = completeness
        
        return all_questions
    
    def _calculate_completeness(self, case_data: Dict) -> float:
        """
        Calculate overall case completeness score (0-1)
        """
        total_weight = 0
        achieved_weight = 0
        
        for category, details in self.ESSENTIAL_CATEGORIES.items():
            weight = details['weight']
            min_required = details.get('min_required', 1)
            total_weight += weight
            
            # Check category data
            category_data = case_data.get(category, [])
            if isinstance(category_data, list):
                info_count = len([x for x in category_data if x])
            elif isinstance(category_data, str):
                info_count = 1 if category_data else 0
            else:
                info_count = 0
            
            if info_count >= min_required:
                achieved_weight += weight
            elif info_count > 0:
                achieved_weight += weight * (info_count / min_required)
        
        return achieved_weight / total_weight if total_weight > 0 else 0.0


def should_ask_more_questions(case_data: Dict, confidence: float, 
                              top_remedies: List[str] = None) -> Tuple[bool, Dict]:
    """
    Determine if more questions should be asked before prescribing
    """
    questioner = IntelligentQuestioner()
    
    # Analyze case
    analysis = questioner.generate_comprehensive_questions(case_data, top_remedies)
    
    # Decision logic
    completeness = analysis['completeness_assessment']['completeness_score']
    ready = analysis['completeness_assessment']['ready_for_prescription']
    
    should_ask = False
    reason = ""
    
    if completeness < 0.6:
        should_ask = True
        reason = "Case information insufficient for safe prescribing"
    elif confidence < 0.7 and top_remedies and len(top_remedies) >= 2:
        should_ask = True
        reason = "Need to differentiate between top remedy candidates"
    elif not ready:
        should_ask = True
        reason = "Essential information categories incomplete"
    
    return should_ask, {
        'should_ask_questions': should_ask,
        'reason': reason,
        'completeness_score': completeness,
        'questions_to_ask': analysis['priority_order'][:10],  # Top 10 priority questions
        'all_questions': analysis,
        'estimated_questions_needed': len(analysis['priority_order'][:10])
    }
