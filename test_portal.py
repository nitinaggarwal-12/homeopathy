#!/usr/bin/env python3
"""
Quick test script to verify all portal features are working
"""

import os
import sys
import json

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing imports...")
    try:
        from src import orchestrator
        from src import clinical_engine
        from src import intelligent_questioning
        from src import image_analysis
        from src import video_analysis
        from src import clinical_guidance
        from src import embeddings
        from src import repertory
        from src import safety
        from src import translations
        from src import schema
        print("✅ All modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_files():
    """Test that all data files exist"""
    print("\n🔍 Testing data files...")
    
    required_files = [
        "data/repertory_mapping.csv",
        "data/mm_index.json",
        "test_cases/test_cases_comprehensive.json",
        ".env"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_exist = False
    
    # Check materia medica files
    mm_dir = "data/materia_medica"
    if os.path.exists(mm_dir):
        mm_files = [f for f in os.listdir(mm_dir) if f.endswith('.md')]
        print(f"✅ {len(mm_files)} remedy files in {mm_dir}")
        if len(mm_files) < 70:
            print(f"⚠️  Warning: Expected ~73 remedy files, found {len(mm_files)}")
    else:
        print(f"❌ Missing: {mm_dir}")
        all_exist = False
    
    return all_exist

def test_test_cases():
    """Test that test cases are valid"""
    print("\n🔍 Testing test cases...")
    try:
        with open("test_cases/test_cases_comprehensive.json", "r") as f:
            data = json.load(f)
        
        test_cases = data.get("test_cases", [])
        print(f"✅ Loaded {len(test_cases)} test cases")
        
        if len(test_cases) != 20:
            print(f"⚠️  Warning: Expected 20 test cases, found {len(test_cases)}")
        
        # Count demographics
        male = sum(1 for tc in test_cases if tc['demographics']['gender'] == 'Male')
        female = sum(1 for tc in test_cases if tc['demographics']['gender'] == 'Female')
        children = sum(1 for tc in test_cases if tc['demographics']['age'] < 13)
        
        print(f"   📊 Demographics: {male} Male, {female} Female, {children} Children")
        
        # Count difficulty
        easy = sum(1 for tc in test_cases if tc['difficulty_level'] == 'Easy')
        moderate = sum(1 for tc in test_cases if tc['difficulty_level'] == 'Moderate')
        difficult = sum(1 for tc in test_cases if tc['difficulty_level'] == 'Difficult')
        
        print(f"   📊 Difficulty: {easy} Easy, {moderate} Moderate, {difficult} Difficult")
        
        return True
    except Exception as e:
        print(f"❌ Error loading test cases: {e}")
        return False

def test_embeddings():
    """Test embeddings index"""
    print("\n🔍 Testing embeddings index...")
    try:
        with open("data/mm_index.json", "r") as f:
            index = json.load(f)
        
        remedies = index.get("remedies", [])
        print(f"✅ Embeddings index loaded: {len(remedies)} remedies")
        
        if len(remedies) < 70:
            print(f"⚠️  Warning: Expected ~73 remedies, found {len(remedies)}")
        
        # Check index size
        import os
        size_mb = os.path.getsize("data/mm_index.json") / (1024 * 1024)
        print(f"   📊 Index size: {size_mb:.2f} MB")
        
        return True
    except Exception as e:
        print(f"❌ Error loading embeddings: {e}")
        return False

def test_repertory():
    """Test repertory mapping"""
    print("\n🔍 Testing repertory mapping...")
    try:
        import pandas as pd
        df = pd.read_csv("data/repertory_mapping.csv")
        
        print(f"✅ Repertory loaded: {len(df)} rubrics")
        
        if len(df) < 40:
            print(f"⚠️  Warning: Expected ~42 rubrics, found {len(df)}")
        
        # Check columns
        required_cols = ['rubric', 'keywords', 'remedies', 'weight']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            print(f"❌ Missing columns: {missing}")
            return False
        
        print(f"   📊 All required columns present")
        return True
    except Exception as e:
        print(f"❌ Error loading repertory: {e}")
        return False

def test_openai_key():
    """Test OpenAI API key"""
    print("\n🔍 Testing OpenAI API key...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your-api-key-here":
            print(f"✅ OpenAI API key configured")
            print(f"   📊 Key starts with: {api_key[:7]}...")
            return True
        else:
            print("❌ OpenAI API key not configured")
            return False
    except Exception as e:
        print(f"❌ Error checking API key: {e}")
        return False

def test_intelligent_questioning():
    """Test intelligent questioning module"""
    print("\n🔍 Testing intelligent questioning...")
    try:
        from src.intelligent_questioning import should_ask_more_questions
        
        # Test with minimal case
        minimal_case = {
            "presenting_complaint": "headache",
            "mental_emotional": [],
            "generals": []
        }
        
        should_ask, analysis = should_ask_more_questions(
            minimal_case,
            confidence=0.5,
            top_remedies=["Belladonna", "Bryonia"]
        )
        
        print(f"✅ Intelligent questioning working")
        print(f"   📊 Should ask: {should_ask}")
        print(f"   📊 Completeness: {analysis['completeness_score']:.0%}")
        print(f"   📊 Questions to ask: {len(analysis['questions_to_ask'])}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing intelligent questioning: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    print("🧪 HOMEOPATHY PORTAL - FEATURE TEST")
    print("=" * 70)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Data Files", test_data_files()))
    results.append(("Test Cases", test_test_cases()))
    results.append(("Embeddings", test_embeddings()))
    results.append(("Repertory", test_repertory()))
    results.append(("OpenAI Key", test_openai_key()))
    results.append(("Intelligent Questioning", test_intelligent_questioning()))
    
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Portal is ready!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
