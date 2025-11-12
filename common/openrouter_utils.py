"""Utility functions for OpenRouter API interactions."""

import requests
from typing import Dict, List


def get_free_models() -> Dict[str, str]:
    """
    Fetch free models from OpenRouter API that support reasoning and tools.
    
    Returns:
        Dict[str, str]: Dictionary with model names as keys and model IDs as values.
                       Example: {"NVIDIA: Nemotron Nano 12B 2 VL (free)": "nvidia/nemotron-nano-12b-v2-vl:free"}
    """
    api_url = "https://openrouter.ai/api/v1/models?&supported_parameters=tools&max_price=0"
    
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        free_models = {}
        
        for model in data.get("data", []):
            pricing = model.get("pricing", {})
            
            # Check if all pricing fields are "0" (free model)
            is_free = all(
                pricing.get(field) == "0" 
                for field in ["prompt", "completion", "request", "image", "web_search", "internal_reasoning"]
            )
            
            if is_free:
                name = model.get("name", "")
                model_id = model.get("id", "")
                if name and model_id:
                    free_models[name] = model_id
        
        return free_models
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching models from OpenRouter API: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}


def get_free_models_list() -> List[Dict[str, str]]:
    """
    Fetch free models from OpenRouter API that support reasoning and tools.
    
    Returns:
        List[Dict[str, str]]: List of dictionaries with 'name' and 'id' keys.
                              Example: [{"name": "NVIDIA: Nemotron Nano 12B 2 VL (free)", 
                                        "id": "nvidia/nemotron-nano-12b-v2-vl:free"}]
    """
    api_url = "https://openrouter.ai/api/v1/models?&supported_parameters=tools&max_price=0"
    
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        free_models = []
        
        for model in data.get("data", []):
            pricing = model.get("pricing", {})
            
            # Check if all pricing fields are "0" (free model)
            is_free = all(
                pricing.get(field) == "0" 
                for field in ["prompt", "completion", "request", "image", "web_search", "internal_reasoning"]
            )
            
            if is_free:
                name = model.get("name", "")
                model_id = model.get("id", "")
                if name and model_id:
                    free_models.append({"name": name, "id": model_id})
        
        return free_models
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching models from OpenRouter API: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

