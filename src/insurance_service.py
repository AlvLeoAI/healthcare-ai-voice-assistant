import json
from typing import Dict, Optional, List
from pathlib import Path

class InsuranceService:
    """Handles insurance verification logic"""
    
    def __init__(self, data_path: Optional[str] = None):
        """
    Initialize insurance service
    
    Args:
        data_path: Optional custom path to insurance_providers.json
                  If None, uses data/insurance_providers.json relative to project root
        """
        if data_path is None:
        # Get project root directory
            base_dir = Path(__file__).parent.parent
            self.data_path = base_dir / "data" / "insurance_providers.json"
        else:
            self.data_path = Path(data_path)
    
        self.providers_data = self._load_data()
    
    def _load_data(self) -> dict:
        """Load insurance data from JSON file"""
        with open(self.data_path, 'r') as f:
            return json.load(f)
    
    def verify_insurance(self, provider_name: str, plan_type: Optional[str] = None) -> Dict:
        """
        Verify if insurance provider is accepted
        
        Args:
            provider_name: Name of insurance provider
            plan_type: Optional plan type (PPO, HMO, etc.)
            
        Returns:
            Dictionary with verification results
        """
        # Normalize provider name for matching
        provider_name_lower = provider_name.lower()
        
        # Check accepted providers
        for provider in self.providers_data.get("accepted_providers", []):
            if provider_name_lower in provider["name"].lower():
                return self._build_accepted_response(provider, plan_type)
        
        # Check not accepted list
        for not_accepted in self.providers_data.get("not_accepted", []):
            if provider_name_lower in not_accepted.lower():
                return {
                    "accepted": False,
                    "provider_name": provider_name,
                    "message": f"Unfortunately, we do not accept {provider_name} at this time. Please contact our billing department for alternative options."
                }
        
        # Provider not found in either list
        return {
            "accepted": None,
            "provider_name": provider_name,
            "message": f"I'll need to verify {provider_name} with our billing department. Can I have someone call you back to confirm coverage?"
        }
    
    def _build_accepted_response(self, provider: Dict, plan_type: Optional[str]) -> Dict:
        """Build response for accepted provider"""
        response = {
            "accepted": True,
            "provider_name": provider["name"],
            "provider_id": provider["id"]
        }
        
        # Check if specific plan type is accepted
        if plan_type:
            plan_type_upper = plan_type.upper()
            if plan_type_upper in provider["plans_accepted"]:
                response["plan_accepted"] = True
                response["message"] = f"Great news! We accept {provider['name']} {plan_type} plans."
            else:
                response["plan_accepted"] = False
                response["message"] = f"We accept {provider['name']}, but we need to verify if we accept {plan_type} plans specifically. Accepted plans are: {', '.join(provider['plans_accepted'])}."
        else:
            response["message"] = f"Yes, we accept {provider['name']}. We accept these plan types: {', '.join(provider['plans_accepted'])}."
        
        # Add additional info
        if provider.get("requires_referral"):
            response["message"] += " Please note that a referral is required."
        
        if provider.get("copay_info"):
            response["copay_info"] = provider["copay_info"]
        
        return response
    
    def get_accepted_providers(self) -> List[str]:
        """Get list of all accepted provider names"""
        return [p["name"] for p in self.providers_data.get("accepted_providers", [])]
    
    def get_provider_details(self, provider_id: str) -> Optional[Dict]:
        """Get detailed information about a specific provider"""
        for provider in self.providers_data.get("accepted_providers", []):
            if provider["id"] == provider_id:
                return provider
        return None
    
    def format_accepted_providers_list(self) -> str:
        """Format list of accepted providers for conversation"""
        providers = self.get_accepted_providers()
        if len(providers) <= 2:
            return " and ".join(providers)
        return ", ".join(providers[:-1]) + f", and {providers[-1]}"
