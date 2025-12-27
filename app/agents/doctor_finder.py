import os
import requests
from dotenv import load_dotenv

load_dotenv()


def determine_specialization(symptoms: str, severity: str = None) -> str:
    """
    Maps symptoms to doctor type.
    
    Returns the recommended specialist based on symptom keywords.
    """
    symptoms_lower = symptoms.lower()
    
    if any(word in symptoms_lower for word in ['chest pain', 'heart', 'cardiac']):
        return "Cardiologist"
    elif any(word in symptoms_lower for word in ['skin', 'rash', 'acne', 'itching']):
        return "Dermatologist"
    elif any(word in symptoms_lower for word in ['ear', 'nose', 'throat', 'sore throat']):
        return "ENT Specialist"
    elif any(word in symptoms_lower for word in ['bone', 'joint', 'fracture', 'sprain']):
        return "Orthopedic"
    elif any(word in symptoms_lower for word in ['eye', 'vision', 'blurry']):
        return "Ophthalmologist"
    else:
        return "General Physician"


def get_mappls_token():
    """
    Generates OAuth2 access token for Mappls API.
    
    Returns: Access token string or None if failed
    """
    client_id = os.environ.get("MAPPLS_CLIENT_ID")
    client_secret = os.environ.get("MAPPLS_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print(" Mappls credentials not found")
        return None
    
    token_url = "https://outpost.mappls.com/api/security/oauth/token"
    
    params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    try:
        response = requests.post(token_url, data=params, timeout=10)
        
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f" Token generation failed: {response.status_code}")
            return None
    except Exception as e:
        print(f" Token error: {e}")
        return None


def find_nearby_doctors(specialization: str, latitude: float, longitude: float, radius: int = 5000):
    """
    Finds nearby hospitals/clinics using Mappls Places API.
    
    Process:
    1. Get OAuth2 token
    2. Search for hospitals near the location
    3. Return top 5 closest results
    
    Note: Shows all nearby hospitals. Most hospitals have multiple 
          departments, so user can call to verify specialty availability.
    """
    
    # Step 1: Authentication
    access_token = get_mappls_token()
    
    if not access_token:
        return {
            "success": False,
            "error": "Authentication failed",
            "doctors": []
        }
    
    # Step 2: Search for nearby hospitals
    url = "https://atlas.mappls.com/api/places/nearby/json"
    
    params = {
        "keywords": "hospital",  # Search for hospitals
        "refLocation": f"{latitude},{longitude}",  # User location
        "radius": radius  # Search radius in meters
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        print(f" Finding hospitals for {specialization}...")
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"   API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            doctors = []
            
            # Extract hospital information
            if "suggestedLocations" in data:
                for place in data["suggestedLocations"][:5]:  # Top 5 closest
                    distance_value = place.get("distance", "N/A")
                    distance_str = f"{distance_value}m" if isinstance(distance_value, (int, float)) else str(distance_value)
                    
                    doctors.append({
                        "name": place.get("placeName", "Unknown Hospital"),
                        "address": place.get("placeAddress", "Address not available"),
                        "distance": distance_str,
                        "specialization": specialization  # What user needs
                    })
            
            return {
                "success": True,
                "doctors": doctors,
                "count": len(doctors),
                "recommended_specialization": specialization
            }
        
        elif response.status_code == 204:
            # No results found
            return {
                "success": False,
                "error": "No hospitals found in this area",
                "doctors": []
            }
        
        else:
            return {
                "success": False,
                "error": f"API error: {response.status_code}",
                "doctors": []
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "doctors": []
        }


# Test code
if __name__ == "__main__":
    print("="*60)
    print("DOCTOR FINDER TEST")
    print("="*60)
    
    # Test case
    symptom = "chest pain and breathing difficulty"
    
    print(f"\nSymptom: '{symptom}'")
    
    # Step 1: Determine specialization
    spec = determine_specialization(symptom)
    print(f"Recommended: {spec}\n")
    
    # Step 2: Find nearby hospitals
    result = find_nearby_doctors(
        specialization=spec,
        latitude=30.7333,  # Chandigarh
        longitude=76.7794,
        radius=5000  # 5km
    )
    
    # Display results
    if result["success"]:
        print(f" Found {result['count']} hospitals nearby\n")
        
        for i, doc in enumerate(result["doctors"], 1):
            print(f"{i}. {doc['name']}")
            print(f"    {doc['address']}")
            print(f"    {doc['distance']}m away")
            print(f"    Ask for: {doc['specialization']}\n")
    else:
        print(f"✗ Error: {result['error']}")
    
    print("="*60)