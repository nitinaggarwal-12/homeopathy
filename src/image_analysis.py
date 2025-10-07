"""
Medical Image Analysis for Homeopathy
Analyzes photos of affected body parts to aid in remedy selection
"""
import os
import base64
from typing import Dict, List, Optional
from io import BytesIO
from PIL import Image
import json

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class MedicalImageAnalyzer:
    """
    Analyzes medical images using OpenAI Vision API
    Focuses on homeopathically relevant features
    """
    
    ANALYSIS_PROMPT = """You are an expert homeopathic physician analyzing a medical image.

Analyze this image and provide detailed observations relevant to homeopathic remedy selection:

1. **Visual Characteristics**:
   - Color (red, blue, purple, yellow, pale, etc.)
   - Texture (smooth, rough, scaly, cracked, moist, dry)
   - Size and extent of affected area
   - Shape and borders (well-defined, irregular, spreading)
   - Any discharge or secretions (color, consistency)
   - Swelling or inflammation present

2. **Specific Features**:
   - Vesicles, pustules, or blisters
   - Crusts or scabs
   - Ulceration or erosion
   - Bleeding or bruising
   - Warmth or redness
   - Any patterns or distribution

3. **Homeopathic Indicators**:
   - Burning appearance
   - Itching appearance (scratch marks)
   - Suppuration signs
   - Dryness or moisture
   - Symmetry or one-sided
   - Location on body (if visible)

4. **Possible Conditions** (differential):
   - What conditions could this represent?
   - Severity assessment

5. **Homeopathic Remedy Considerations**:
   - Based on visual appearance, which remedy families might be indicated?
   - Key visual keynotes that match specific remedies

Return your analysis in JSON format with these sections:
{
  "visual_description": "detailed description",
  "color": "predominant color",
  "texture": "texture description",
  "moisture": "dry/moist/weeping",
  "inflammation": "none/mild/moderate/severe",
  "specific_features": ["list of features"],
  "possible_conditions": ["list"],
  "homeopathic_indicators": ["list of remedy-relevant features"],
  "suggested_remedy_families": ["list with reasoning"],
  "severity": "mild/moderate/severe",
  "requires_medical_attention": true/false,
  "additional_questions": ["questions to ask patient"]
}

Be thorough and clinically accurate. Focus on features relevant to homeopathic prescribing."""
    
    def __init__(self):
        self.client = None
        if OpenAI:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.client = OpenAI(api_key=api_key)
    
    def analyze_image(self, image_data: bytes, image_format: str = "jpeg") -> Dict:
        """
        Analyze medical image and return homeopathically relevant observations
        """
        if not self.client:
            return {
                "error": "OpenAI client not initialized. Check API key.",
                "visual_description": "Image analysis unavailable"
            }
        
        try:
            # Convert image to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Call OpenAI Vision API
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Vision-capable model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self.ANALYSIS_PROMPT
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{image_format};base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            # Parse response
            content = response.choices[0].message.content
            
            # Try to extract JSON
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
            analysis["raw_response"] = content
            
            return analysis
            
        except Exception as e:
            return {
                "error": f"Image analysis failed: {str(e)}",
                "visual_description": "Unable to analyze image"
            }
    
    def integrate_with_case(self, image_analysis: Dict, case_data: Dict) -> Dict:
        """
        Integrate image analysis findings with verbal symptoms
        """
        if image_analysis.get("error"):
            return {
                "status": "error",
                "message": image_analysis.get("error")
            }
        
        # Extract key visual indicators
        visual_symptoms = []
        
        # Color
        color = image_analysis.get("color", "")
        if color:
            visual_symptoms.append(f"Visual: {color} coloration")
        
        # Texture
        texture = image_analysis.get("texture", "")
        if texture:
            visual_symptoms.append(f"Visual: {texture} texture")
        
        # Moisture
        moisture = image_analysis.get("moisture", "")
        if moisture:
            visual_symptoms.append(f"Visual: {moisture} appearance")
        
        # Inflammation
        inflammation = image_analysis.get("inflammation", "")
        if inflammation and inflammation != "none":
            visual_symptoms.append(f"Visual: {inflammation} inflammation")
        
        # Specific features
        for feature in image_analysis.get("specific_features", []):
            visual_symptoms.append(f"Visual: {feature}")
        
        # Add to case data
        enhanced_case = case_data.copy()
        
        # Add visual symptoms to particulars
        if "particulars" not in enhanced_case:
            enhanced_case["particulars"] = []
        
        enhanced_case["particulars"].append({
            "section": "Visual Analysis",
            "description": image_analysis.get("visual_description", ""),
            "modalities_better": [],
            "modalities_worse": [],
            "concomitants": visual_symptoms
        })
        
        # Add to generals if systemic features noted
        if "generals" not in enhanced_case:
            enhanced_case["generals"] = []
        
        enhanced_case["generals"].extend(visual_symptoms)
        
        return {
            "status": "success",
            "enhanced_case": enhanced_case,
            "image_analysis": image_analysis,
            "visual_symptoms_added": visual_symptoms,
            "remedy_considerations": image_analysis.get("suggested_remedy_families", []),
            "requires_medical_attention": image_analysis.get("requires_medical_attention", False),
            "additional_questions": image_analysis.get("additional_questions", [])
        }


class ImagePreprocessor:
    """
    Preprocess images for optimal analysis
    """
    
    @staticmethod
    def validate_image(image_data: bytes) -> Dict:
        """Validate uploaded image"""
        try:
            img = Image.open(BytesIO(image_data))
            
            # Check format
            if img.format not in ['JPEG', 'PNG', 'WEBP']:
                return {
                    "valid": False,
                    "error": "Unsupported format. Please upload JPEG, PNG, or WEBP"
                }
            
            # Check size
            width, height = img.size
            if width < 200 or height < 200:
                return {
                    "valid": False,
                    "error": "Image too small. Minimum 200x200 pixels required"
                }
            
            if width > 4096 or height > 4096:
                return {
                    "valid": False,
                    "error": "Image too large. Maximum 4096x4096 pixels"
                }
            
            # Check file size (max 20MB)
            if len(image_data) > 20 * 1024 * 1024:
                return {
                    "valid": False,
                    "error": "File too large. Maximum 20MB"
                }
            
            return {
                "valid": True,
                "format": img.format,
                "size": (width, height),
                "file_size": len(image_data)
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": f"Invalid image file: {str(e)}"
            }
    
    @staticmethod
    def optimize_image(image_data: bytes, max_size: int = 2048) -> bytes:
        """Optimize image for API upload"""
        try:
            img = Image.open(BytesIO(image_data))
            
            # Resize if too large
            width, height = img.size
            if width > max_size or height > max_size:
                ratio = min(max_size / width, max_size / height)
                new_size = (int(width * ratio), int(height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert to RGB if needed
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            
            # Save optimized
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            return output.getvalue()
            
        except Exception:
            return image_data  # Return original if optimization fails


def analyze_medical_image(image_data: bytes, case_data: Dict) -> Dict:
    """
    Main function to analyze medical image and integrate with case
    """
    # Validate image
    preprocessor = ImagePreprocessor()
    validation = preprocessor.validate_image(image_data)
    
    if not validation.get("valid"):
        return {
            "status": "error",
            "message": validation.get("error")
        }
    
    # Optimize image
    optimized_image = preprocessor.optimize_image(image_data)
    
    # Analyze image
    analyzer = MedicalImageAnalyzer()
    analysis = analyzer.analyze_image(optimized_image, "jpeg")
    
    # Integrate with case
    result = analyzer.integrate_with_case(analysis, case_data)
    
    return result


# Remedy-specific visual indicators
VISUAL_REMEDY_INDICATORS = {
    "Sulphur": [
        "Red, burning, itching eruptions",
        "Dirty, unwashed appearance",
        "Worse from warmth, bathing",
        "Dry, scaly skin"
    ],
    "Graphites": [
        "Thick, honey-like discharge",
        "Cracks in skin, especially bends",
        "Moist, sticky eruptions",
        "Behind ears, corners of mouth"
    ],
    "Arsenicum album": [
        "Dry, scaly, burning eruptions",
        "Anxious appearance",
        "Worse from cold",
        "Restless"
    ],
    "Petroleum": [
        "Deep cracks, fissures",
        "Worse in winter",
        "Dry, rough, cracked",
        "Hands and fingers affected"
    ],
    "Rhus toxicodendron": [
        "Vesicular eruptions",
        "Intense itching",
        "Worse at night, rest",
        "Better from motion, heat"
    ],
    "Apis mellifica": [
        "Swelling, edema",
        "Red, shiny, puffy",
        "Stinging pains",
        "Worse from heat"
    ],
    "Arnica": [
        "Bruising, ecchymosis",
        "Black and blue discoloration",
        "Trauma, injury",
        "Sore, tender"
    ],
    "Belladonna": [
        "Bright red, hot",
        "Throbbing, pulsating",
        "Sudden onset",
        "Radiating heat"
    ],
    "Lachesis": [
        "Bluish, purple discoloration",
        "Left-sided",
        "Cannot bear tight clothing",
        "Worse after sleep"
    ],
    "Hepar sulphuris": [
        "Suppuration, pus formation",
        "Extremely sensitive to touch",
        "Splinter-like pains",
        "Worse from cold"
    ]
}
