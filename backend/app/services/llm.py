import os
import json
import google.generativeai as genai

from ..config import get_settings


def generate_substitution(drink_name: str, nutrition: dict | None = None) -> dict:
    """
    Generate a diabetes-friendly substitution using Gemini API.
    Returns dict with: name, notes, sugar_delta, caffeine_delta
    """
    settings = get_settings()
    api_key = settings.gemini_api_key
    
    if not api_key:
        # Fallback if no API key
        return {
            "name": f"Unsweetened {drink_name}",
            "notes": f"Lower sugar alternative for {drink_name}. Consider using sugar-free sweeteners or unsweetened bases.",
            "sugar_delta": -20.0 if nutrition else None,
            "caffeine_delta": None,
        }
    
    try:
        genai.configure(api_key=api_key)
        
        # Try to get available models first
        try:
            models_list = genai.list_models()
            available_models = []
            for m in models_list:
                if hasattr(m, 'supported_generation_methods') and 'generateContent' in m.supported_generation_methods:
                    model_name = m.name if hasattr(m, 'name') else str(m)
                    available_models.append(model_name)
            print(f"📋 Available Gemini models: {available_models[:5]}")  # Show first 5
        except Exception as list_error:
            print(f"⚠️ Could not list models: {list_error}")
            available_models = []
        
        # Try model names - use newer Gemini 2.0/2.5 models that are actually available
        model_names_to_try = [
            'models/gemini-2.0-flash',      # Stable 2.0 version (fast)
            'models/gemini-2.5-flash',      # Newer, faster
            'models/gemini-2.5-pro',        # Newer, more capable
            'models/gemini-2.0-flash-exp',  # Experimental 2.0
            'models/gemini-1.5-pro',       # Fallback to older if available
            'models/gemini-1.5-flash',     # Fallback to older if available
        ]
        
        model = None
        last_error = None
        for model_name in model_names_to_try:
            try:
                # Try to create the model - this will fail if model doesn't exist
                model = genai.GenerativeModel(model_name)
                print(f"✅ Successfully initialized model: {model_name}")
                break
            except Exception as model_error:
                last_error = model_error
                print(f"⚠️ Model '{model_name}' failed: {str(model_error)[:100]}")
                continue
        
        if model is None:
            error_msg = f"No working Gemini model found. Last error: {last_error}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
        
        # Build nutrition context
        nutrition_context = ""
        if nutrition:
            sugar = nutrition.get("sugar_grams")
            caffeine = nutrition.get("caffeine_mg")
            if sugar is not None:
                nutrition_context += f"\n- Current sugar content: {sugar}g per serving"
            if caffeine is not None:
                nutrition_context += f"\n- Current caffeine content: {caffeine}mg per serving"
        
        prompt = f"""You are a nutrition assistant helping people with diabetes find healthier drink alternatives.

Original drink: {drink_name}
{nutrition_context}

Please suggest a diabetes-friendly substitute that:
1. Has significantly lower sugar content (aim for <10g sugar or sugar-free)
2. Maintains a similar flavor profile when possible
3. Uses natural sweeteners (stevia, monk fruit) or unsweetened bases
4. Is realistic and available at cafes or easy to make at home

Respond in JSON format with these exact fields:
{{
    "name": "Substitute drink name",
    "notes": "Brief explanation of why this is a good substitute and how to order/make it",
    "sugar_delta": estimated_sugar_reduction_in_grams (negative number),
    "caffeine_delta": estimated_caffeine_change_in_mg (can be 0 if similar)
}}

Example response:
{{
    "name": "Mango Green Tea with Stevia",
    "notes": "Same fruity flavor profile with 80% less sugar. Ask for green tea base with sugar-free mango syrup and stevia instead of regular syrup.",
    "sugar_delta": -30.0,
    "caffeine_delta": -20.0
}}

Now provide the substitution for "{drink_name}":"""

        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Try to extract JSON from response (sometimes Gemini wraps it in markdown)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(response_text)
        
        # Validate and return
        return {
            "name": result.get("name", f"Unsweetened {drink_name}"),
            "notes": result.get("notes", "Diabetes-friendly alternative"),
            "sugar_delta": float(result.get("sugar_delta", -20.0)) if result.get("sugar_delta") is not None else None,
            "caffeine_delta": float(result.get("caffeine_delta", 0.0)) if result.get("caffeine_delta") is not None else None,
        }
    
    except json.JSONDecodeError as e:
        print(f"⚠️ Failed to parse Gemini JSON response: {e}")
        # Fallback response
        return {
            "name": f"Unsweetened {drink_name}",
            "notes": f"Lower sugar alternative for {drink_name}. Consider using sugar-free sweeteners or unsweetened bases.",
            "sugar_delta": -20.0 if nutrition else None,
            "caffeine_delta": None,
        }
    except Exception as e:
        print(f"⚠️ Gemini API error: {e}")
        print(f"   API Key present: {bool(api_key)}")
        print(f"   Error type: {type(e).__name__}")
        # Fallback response
        return {
            "name": f"Unsweetened {drink_name}",
            "notes": f"Lower sugar alternative for {drink_name}. Consider using sugar-free sweeteners or unsweetened bases.",
            "sugar_delta": -20.0 if nutrition else None,
            "caffeine_delta": None,
        }
