"""
Comprehensive Clinical Guidance System
Detailed instructions for dosage, diet, lifestyle, and healing timeline
"""
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class DosingProtocol:
    """
    Detailed dosing protocols based on condition severity and patient vitality
    """
    
    PROTOCOLS = {
        'acute_severe': {
            'potency': '200C',
            'frequency': 'Single dose, may repeat after 12 hours if no improvement',
            'duration': '1-3 days for acute relief',
            'follow_up': 'Reassess after 24 hours'
        },
        'acute_moderate': {
            'potency': '30C',
            'frequency': 'Single dose, may repeat after 6-8 hours if needed',
            'duration': '2-5 days for resolution',
            'follow_up': 'Reassess after 48 hours'
        },
        'acute_mild': {
            'potency': '30C or 6C',
            'frequency': 'Single dose, may repeat after 4-6 hours',
            'duration': '3-7 days',
            'follow_up': 'Reassess after 3 days'
        },
        'chronic_deep': {
            'potency': '200C or 1M',
            'frequency': 'Single dose, wait 14-30 days',
            'duration': '3-6 months for deep healing',
            'follow_up': 'Monthly follow-up for first 3 months'
        },
        'chronic_moderate': {
            'potency': '30C or 200C',
            'frequency': 'Single dose, wait 7-14 days',
            'duration': '2-4 months',
            'follow_up': 'Follow-up every 2-3 weeks'
        },
        'chronic_mild': {
            'potency': '30C',
            'frequency': 'Single dose, wait 5-7 days',
            'duration': '1-2 months',
            'follow_up': 'Follow-up every 2 weeks'
        }
    }
    
    @staticmethod
    def get_detailed_dosing(case_type: str, remedy: str, potency: str) -> Dict:
        """Get comprehensive dosing instructions"""
        protocol = DosingProtocol.PROTOCOLS.get(case_type, DosingProtocol.PROTOCOLS['chronic_moderate'])
        
        return {
            'remedy': remedy,
            'potency': potency,
            'form': 'Pills/Globules (sugar pills) or Liquid dilution',
            'how_to_take': [
                f"Take {potency} potency - typically 3-4 pills or 3-5 drops in water",
                "Take on empty stomach (30 minutes before or after food/drink)",
                "Let pills dissolve under tongue (do not swallow whole)",
                "If liquid: Add drops to 1/4 glass of water, stir and sip slowly",
                "Avoid touching pills with hands - use cap to dispense",
                "Store away from strong odors, heat, and direct sunlight"
            ],
            'frequency': protocol['frequency'],
            'duration': protocol['duration'],
            'when_to_repeat': [
                "ONLY repeat if symptoms return after initial improvement",
                "Do NOT repeat if improvement is continuing",
                "Do NOT repeat if new symptoms appear (consult practitioner)",
                "In acute cases: May repeat more frequently if no response after appropriate time",
                "In chronic cases: Wait full period before considering repetition"
            ],
            'signs_remedy_working': [
                "Mental/emotional improvement first (feel calmer, more hopeful)",
                "Energy and sleep improve",
                "Appetite normalizes",
                "Chief complaint begins to reduce",
                "Old symptoms may temporarily return (good sign - healing in reverse order)"
            ],
            'when_to_stop': [
                "When symptoms are 80-90% better (let body complete healing)",
                "If completely symptom-free",
                "If new unusual symptoms appear",
                "If aggravation lasts more than 24-48 hours without improvement"
            ],
            'follow_up': protocol['follow_up']
        }


class DietaryGuidance:
    """
    Comprehensive dietary recommendations for healing
    """
    
    # General homeopathic diet principles
    GENERAL_DIET = {
        'recommended': [
            "Fresh, organic vegetables (cooked and raw)",
            "Whole grains (rice, quinoa, oats, millet)",
            "Fresh fruits (seasonal and local when possible)",
            "Legumes and lentils (well-cooked)",
            "Nuts and seeds (in moderation)",
            "Herbal teas (chamomile, ginger, tulsi)",
            "Pure water (room temperature or warm)",
            "Light, easily digestible meals",
            "Eat at regular times",
            "Chew food thoroughly"
        ],
        'avoid': [
            "Strong coffee (interferes with remedies)",
            "Mint and menthol (antidotes many remedies)",
            "Camphor, eucalyptus (antidotes remedies)",
            "Excessive spices and chilies",
            "Processed and junk food",
            "Excessive sugar and artificial sweeteners",
            "Alcohol and tobacco",
            "Very cold or iced drinks",
            "Eating late at night",
            "Overeating"
        ],
        'timing': [
            "Breakfast: 7-9 AM (light and nourishing)",
            "Lunch: 12-2 PM (largest meal of the day)",
            "Dinner: 6-8 PM (light and early)",
            "Avoid snacking between meals",
            "Last meal 2-3 hours before sleep"
        ]
    }
    
    # Condition-specific dietary modifications
    CONDITION_SPECIFIC = {
        'digestive': {
            'add': ['Ginger tea', 'Fennel seeds', 'Buttermilk', 'Cooked vegetables', 'Rice porridge'],
            'avoid': ['Raw vegetables', 'Heavy fried foods', 'Dairy products', 'Beans and cabbage'],
            'note': 'Eat small, frequent meals. Fast one day per week if possible.'
        },
        'respiratory': {
            'add': ['Warm water', 'Ginger-honey tea', 'Turmeric milk', 'Steam inhalation', 'Soups'],
            'avoid': ['Cold drinks', 'Ice cream', 'Dairy products', 'Bananas', 'Citrus fruits'],
            'note': 'Keep throat and chest warm. Avoid cold and damp.'
        },
        'skin': {
            'add': ['Green leafy vegetables', 'Cucumber', 'Coconut water', 'Bitter gourd', 'Turmeric'],
            'avoid': ['Spicy food', 'Sour foods', 'Fermented foods', 'Eggs', 'Seafood'],
            'note': 'Drink plenty of water. Avoid scratching affected areas.'
        },
        'mental_emotional': {
            'add': ['Almonds', 'Walnuts', 'Brahmi tea', 'Ashwagandha', 'Warm milk', 'Dates'],
            'avoid': ['Caffeine', 'Alcohol', 'Stimulants', 'Heavy meals at night'],
            'note': 'Regular meal times important. Avoid skipping meals.'
        },
        'joint_pain': {
            'add': ['Turmeric', 'Ginger', 'Garlic', 'Fenugreek', 'Warm water', 'Ghee'],
            'avoid': ['Cold water', 'Yogurt', 'Sour foods', 'Tomatoes', 'Potatoes'],
            'note': 'Keep joints warm. Gentle movement important.'
        },
        'fever': {
            'add': ['Plenty of water', 'Coconut water', 'Fruit juices', 'Light soups', 'Rice water'],
            'avoid': ['Heavy meals', 'Meat', 'Dairy', 'Oily food'],
            'note': 'Light fasting beneficial. Let fever run its course naturally.'
        }
    }
    
    @staticmethod
    def get_dietary_plan(condition_type: str, remedy: str) -> Dict:
        """Get comprehensive dietary guidance"""
        specific = DietaryGuidance.CONDITION_SPECIFIC.get(condition_type, {})
        
        return {
            'general_principles': DietaryGuidance.GENERAL_DIET,
            'specific_for_condition': specific,
            'remedy_specific_notes': DietaryGuidance._get_remedy_specific_diet(remedy),
            'hydration': [
                "Drink 8-10 glasses of pure water daily",
                "Prefer room temperature or warm water",
                "Avoid drinking water immediately before/after meals",
                "Sip water throughout the day, don't gulp"
            ]
        }
    
    @staticmethod
    def _get_remedy_specific_diet(remedy: str) -> List[str]:
        """Remedy-specific dietary considerations"""
        remedy_diets = {
            'Sulphur': ['Avoid excessive sweets despite craving', 'Light, cooling foods beneficial'],
            'Nux vomica': ['Avoid coffee, alcohol, spices', 'Simple, bland diet essential'],
            'Pulsatilla': ['Avoid fatty foods', 'Light, fresh foods preferred'],
            'Lycopodium': ['Avoid beans, cabbage, onions', 'Eat small frequent meals'],
            'Arsenicum album': ['Warm food and drinks', 'Avoid cold and raw foods'],
            'Phosphorus': ['Avoid very cold drinks despite craving', 'Light, easily digestible food'],
            'Natrum muriaticum': ['Reduce salt intake despite craving', 'Avoid bread and starchy foods']
        }
        return remedy_diets.get(remedy, ['Follow general dietary guidelines'])


class LifestyleGuidance:
    """
    Comprehensive lifestyle modifications for healing
    """
    
    GENERAL_LIFESTYLE = {
        'sleep': [
            "Sleep by 10 PM, wake by 6 AM (align with natural rhythms)",
            "7-8 hours of quality sleep essential",
            "Keep bedroom dark, quiet, and well-ventilated",
            "Avoid screens 1 hour before bed",
            "Sleep on right side for better digestion",
            "Keep head towards east or south (traditional wisdom)"
        ],
        'exercise': [
            "Morning walk in fresh air (30-45 minutes)",
            "Yoga or gentle stretching daily",
            "Pranayama (breathing exercises) - 10-15 minutes",
            "Avoid strenuous exercise during acute illness",
            "Regular, moderate exercise better than intense sporadic activity",
            "Exercise before breakfast or 2 hours after meals"
        ],
        'stress_management': [
            "Meditation: 10-20 minutes daily (morning best)",
            "Deep breathing: 5 minutes, 3 times daily",
            "Avoid excessive worry and anxiety",
            "Maintain positive mental attitude",
            "Practice gratitude daily",
            "Limit news and negative media",
            "Spend time in nature",
            "Maintain social connections"
        ],
        'daily_routine': [
            "Wake up early (before sunrise ideal)",
            "Drink warm water upon waking",
            "Empty bowels daily (morning)",
            "Oil pulling or tongue scraping",
            "Bath or shower daily",
            "Regular meal times",
            "Short rest after lunch (10-15 minutes)",
            "Early dinner (before 8 PM)",
            "Relaxing evening routine"
        ],
        'environmental': [
            "Fresh air and sunlight daily",
            "Keep living space clean and clutter-free",
            "Avoid excessive air conditioning",
            "Maintain comfortable room temperature",
            "Use natural cleaning products",
            "Minimize electromagnetic exposure (phones, WiFi at night)",
            "Indoor plants for air purification"
        ]
    }
    
    CONDITION_SPECIFIC = {
        'respiratory': [
            "Steam inhalation twice daily",
            "Keep chest and throat covered",
            "Avoid cold and damp environments",
            "Practice pranayama (breathing exercises)",
            "Avoid dust, smoke, strong perfumes"
        ],
        'digestive': [
            "Eat slowly and mindfully",
            "Walk 100 steps after meals",
            "Avoid lying down immediately after eating",
            "Practice abdominal breathing",
            "Gentle abdominal massage with warm oil"
        ],
        'skin': [
            "Avoid hot water baths",
            "Use mild, natural soaps",
            "Cotton clothing preferred",
            "Avoid synthetic fabrics",
            "Sunlight exposure (moderate)",
            "Keep skin moisturized naturally"
        ],
        'mental_emotional': [
            "Regular meditation essential",
            "Journaling thoughts and feelings",
            "Creative expression (art, music, writing)",
            "Avoid isolation - maintain connections",
            "Counseling or therapy if needed",
            "Spiritual practices beneficial"
        ],
        'joint_pain': [
            "Keep joints warm",
            "Gentle movement throughout day",
            "Avoid prolonged sitting or standing",
            "Warm oil massage to affected areas",
            "Avoid cold and damp",
            "Proper posture important"
        ]
    }
    
    @staticmethod
    def get_lifestyle_plan(condition_type: str, case_data: Dict) -> Dict:
        """Get comprehensive lifestyle guidance"""
        specific = LifestyleGuidance.CONDITION_SPECIFIC.get(condition_type, [])
        
        return {
            'general': LifestyleGuidance.GENERAL_LIFESTYLE,
            'specific_for_condition': specific,
            'things_to_avoid': LifestyleGuidance._get_avoidance_list(condition_type),
            'positive_habits': LifestyleGuidance._get_positive_habits(case_data)
        }
    
    @staticmethod
    def _get_avoidance_list(condition_type: str) -> List[str]:
        """Things to strictly avoid"""
        return [
            "Suppressing natural urges (urination, bowel movement, sneezing, etc.)",
            "Excessive mental or physical strain",
            "Irregular sleep patterns",
            "Excessive worry and negative thinking",
            "Toxic relationships and environments",
            "Substance abuse (alcohol, tobacco, drugs)"
        ]
    
    @staticmethod
    def _get_positive_habits(case_data: Dict) -> List[str]:
        """Positive habits to cultivate"""
        return [
            "Maintain optimistic outlook",
            "Practice self-care daily",
            "Express emotions healthily",
            "Cultivate meaningful relationships",
            "Engage in purposeful activities",
            "Practice forgiveness (self and others)",
            "Live in alignment with values",
            "Contribute to community/society"
        ]


class HealingTimeline:
    """
    Expected healing timeline and progress markers
    """
    
    @staticmethod
    def get_timeline(condition_type: str, chronicity: str, vitality: str) -> Dict:
        """
        Generate expected healing timeline
        """
        # Base timelines
        timelines = {
            'acute': {
                'high_vitality': {
                    'initial_response': '2-6 hours',
                    'significant_improvement': '24-48 hours',
                    'resolution': '3-7 days',
                    'complete_healing': '1-2 weeks'
                },
                'moderate_vitality': {
                    'initial_response': '6-12 hours',
                    'significant_improvement': '2-3 days',
                    'resolution': '5-10 days',
                    'complete_healing': '2-3 weeks'
                },
                'low_vitality': {
                    'initial_response': '12-24 hours',
                    'significant_improvement': '3-5 days',
                    'resolution': '1-2 weeks',
                    'complete_healing': '3-4 weeks'
                }
            },
            'chronic': {
                'high_vitality': {
                    'initial_response': '3-7 days',
                    'significant_improvement': '2-4 weeks',
                    'major_improvement': '2-3 months',
                    'complete_healing': '6-12 months'
                },
                'moderate_vitality': {
                    'initial_response': '1-2 weeks',
                    'significant_improvement': '4-6 weeks',
                    'major_improvement': '3-6 months',
                    'complete_healing': '12-18 months'
                },
                'low_vitality': {
                    'initial_response': '2-3 weeks',
                    'significant_improvement': '6-8 weeks',
                    'major_improvement': '6-12 months',
                    'complete_healing': '18-24 months'
                }
            }
        }
        
        timeline = timelines.get(condition_type, timelines['chronic']).get(vitality, timelines['chronic']['moderate_vitality'])
        
        return {
            'timeline': timeline,
            'progress_markers': HealingTimeline._get_progress_markers(),
            'herings_law': HealingTimeline._get_herings_law_explanation(),
            'what_to_expect': HealingTimeline._get_expectations(condition_type)
        }
    
    @staticmethod
    def _get_progress_markers() -> List[str]:
        """Signs of healing progress"""
        return [
            "✓ Improved mental state (calmer, more hopeful, better mood)",
            "✓ Better sleep quality and energy levels",
            "✓ Improved appetite and digestion",
            "✓ Gradual reduction in chief complaint",
            "✓ Old symptoms may temporarily return (healing in reverse)",
            "✓ Symptoms move from inside to outside (e.g., internal to skin)",
            "✓ Symptoms move from above downward",
            "✓ Symptoms disappear in reverse order of appearance"
        ]
    
    @staticmethod
    def _get_herings_law_explanation() -> Dict:
        """Hering's Law of Cure"""
        return {
            'principle': "Healing occurs in specific patterns (Hering's Law of Cure)",
            'directions': [
                "From within outward (internal organs heal before external symptoms)",
                "From above downward (head symptoms clear before lower body)",
                "From more important to less important organs",
                "In reverse order of symptom appearance (recent symptoms go first)"
            ],
            'example': "A person with asthma and eczema: asthma improves first (internal), then eczema may temporarily worsen (external) before healing completely."
        }
    
    @staticmethod
    def _get_expectations(condition_type: str) -> List[str]:
        """What to expect during healing"""
        return [
            "Initial aggravation possible (symptoms briefly worsen before improving - good sign)",
            "Healing may not be linear - ups and downs are normal",
            "Old suppressed symptoms may resurface temporarily",
            "Discharge or elimination may increase (body detoxifying)",
            "Energy may fluctuate initially",
            "Patience essential - deep healing takes time",
            "Each person heals at their own pace",
            "Trust the process and your body's wisdom"
        ]


def generate_comprehensive_guidance(case_data: Dict, remedy: str, potency: str, 
                                    condition_type: str, confidence: float) -> Dict:
    """
    Generate complete clinical guidance package
    """
    # Determine case characteristics
    is_acute = 'acute' if any(word in str(case_data.get('duration', '')).lower() 
                               for word in ['sudden', 'hours', 'days', 'acute']) else 'chronic'
    vitality = 'moderate'  # Default, would need more sophisticated assessment
    
    # Determine case type for dosing
    if is_acute == 'acute':
        if confidence >= 0.8:
            case_type = 'acute_severe'
        elif confidence >= 0.6:
            case_type = 'acute_moderate'
        else:
            case_type = 'acute_mild'
    else:
        if confidence >= 0.8:
            case_type = 'chronic_deep'
        elif confidence >= 0.6:
            case_type = 'chronic_moderate'
        else:
            case_type = 'chronic_mild'
    
    # Generate all guidance components
    dosing = DosingProtocol.get_detailed_dosing(case_type, remedy, potency)
    diet = DietaryGuidance.get_dietary_plan(condition_type, remedy)
    lifestyle = LifestyleGuidance.get_lifestyle_plan(condition_type, case_data)
    timeline = HealingTimeline.get_timeline(is_acute, 'moderate', vitality)
    
    return {
        'dosing_protocol': dosing,
        'dietary_guidance': diet,
        'lifestyle_modifications': lifestyle,
        'healing_timeline': timeline,
        'important_notes': [
            "🔴 This is a holistic healing process - all aspects work together",
            "🔴 Homeopathy + Diet + Lifestyle = Complete Healing",
            "🔴 Be patient and consistent - healing takes time",
            "🔴 Keep a symptom diary to track progress",
            "🔴 Consult your homeopath for follow-up and adjustments",
            "🔴 In case of emergency or severe symptoms, seek immediate medical care"
        ]
    }
