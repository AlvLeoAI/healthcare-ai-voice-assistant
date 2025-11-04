import os
import json
from openai import OpenAI
from typing import List, Dict, Optional
import logging
from pathlib import Path

from .appointment_service import AppointmentService
from .insurance_service import InsuranceService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversationEngine:
    """Manages conversation flow with LLM and function calling"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.appointment_service = AppointmentService()
        self.insurance_service = InsuranceService()
        self.conversation_history: List[Dict] = []
        self.system_prompt = self._load_system_prompt()
        
         # Load clinic info with absolute path
        base_dir = Path(__file__).parent.parent
        clinic_info_path = base_dir / "data" / "clinic_info.json"
        with open(clinic_info_path, 'r') as f:
            self.clinic_info = json.load(f)
    
    def _load_system_prompt(self) -> str:
        """Load system prompt"""
        return """You are an AI receptionist for Riverside Medical Center, a family practice clinic in Austin, Texas.

**YOUR ROLE:**
- Help patients schedule appointments
- Verify insurance information  
- Answer basic questions about the clinic
- You are professional, empathetic, and efficient

**CONVERSATION RULES:**
- Ask ONE question at a time
- Keep responses under 2 sentences when possible
- Confirm information before finalizing
- If you don't understand, politely ask for clarification
- Never provide medical advice

**CRITICAL SCHEDULING RULES:**
- IMPORTANT: The current year is 2025. When users mention dates like "November 3rd" without a year, use 2025
- When calling check_available_slots or book_appointment, always use format YYYY-MM-DD where YYYY is 2025
- ONLY use dates and times returned by the check_available_slots function
- When a user mentions ANY date, you MUST call check_available_slots FIRST before responding
- NEVER assume a date is closed, unavailable, or has no slots without calling the function first
- If check_available_slots returns empty slots, say "no available slots" - do not invent reasons why

**CAPABILITIES:**
- Schedule appointments (Mon-Fri, 9 AM - 5 PM)
- Check insurance acceptance (we accept major providers)
- Provide clinic info (location, hours, doctors)

**LIMITATIONS:**
- Cannot prescribe or diagnose
- Cannot access medical records
- For emergencies, direct to 911
- For complex issues, offer to transfer to staff

**CONVERSATION FLOW:**
- Greet caller warmly
- Identify their need (appointment, insurance, or information)
- Collect required information step by step
- Process request and confirm
- Close politely

**TONE:** Professional yet warm, patient and clear

**IMPORTANT:** Use function calls to check appointments, verify insurance, and get clinic information. Always confirm details before finalizing bookings."""
    
    def get_response(self, user_message: str) -> str:
        """
        Get AI response for user message
        
        Args:
            user_message: User's message
            
        Returns:
            AI assistant's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare messages for API
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history
        
        try:
            # Call OpenAI API with function calling
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                functions=self._get_function_definitions(),
                function_call="auto",
                temperature=0.7,
                max_tokens=200
            )
            
            message = response.choices[0].message
            
            # Handle function calling
            if message.function_call:
                function_response = self._handle_function_call(message.function_call)
                
                # Add function call and response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": message.function_call.name,
                        "arguments": message.function_call.arguments
                    }
                })
                
                self.conversation_history.append({
                    "role": "function",
                    "name": message.function_call.name,
                    "content": json.dumps(function_response)
                })
                
                # Get final response from model
                second_response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": self.system_prompt}
                    ] + self.conversation_history,
                    temperature=0.7,
                    max_tokens=200
                )
                
                assistant_message = second_response.choices[0].message.content
            else:
                assistant_message = message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            logger.info(f"Assistant: {assistant_message}")
            return assistant_message
            
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            return "I apologize, I'm having trouble processing that. Could you please repeat?"
    
    def _handle_function_call(self, function_call) -> Dict:
        """Execute function based on LLM's function call"""
        function_name = function_call.name
        arguments = json.loads(function_call.arguments)
        
        logger.info(f"Calling function: {function_name} with args: {arguments}")
        
        if function_name == "check_available_slots":
            date = arguments.get("date")
            doctor_id = arguments.get("doctor_id")
            slots = self.appointment_service.get_available_slots(date, doctor_id)
            return {"available_slots": slots, "date": date}
        
        elif function_name == "book_appointment":
            result = self.appointment_service.book_appointment(
                patient_name=arguments["patient_name"],
                date=arguments["date"],
                time=arguments["time"],
                doctor_id=arguments["doctor_id"],
                appointment_type=arguments.get("appointment_type", "follow_up"),
                patient_phone=arguments.get("patient_phone"),
                reason=arguments.get("reason")
            )
            return result
        
        elif function_name == "verify_insurance":
            provider_name = arguments["provider_name"]
            plan_type = arguments.get("plan_type")
            result = self.insurance_service.verify_insurance(provider_name, plan_type)
            return result
        
        elif function_name == "get_clinic_info":
            info_type = arguments.get("info_type", "general")
            return self._get_clinic_info(info_type)
        
        elif function_name == "get_next_available_dates":
            dates = self.appointment_service.get_next_available_dates()
            return {"dates": dates}
        
        else:
            return {"error": f"Unknown function: {function_name}"}
    
    def _get_clinic_info(self, info_type: str) -> Dict:
        """Get clinic information"""
        if info_type == "location":
            return {"location": self.clinic_info["location"]}
        elif info_type == "hours":
            return {"hours": self.clinic_info["hours"]}
        elif info_type == "doctors":
            return {"doctors": self.clinic_info["doctors"]}
        elif info_type == "services":
            return {"services": self.clinic_info["services"]}
        else:
            return {
                "name": self.clinic_info["name"],
                "location": self.clinic_info["location"],
                "hours": self.clinic_info["hours"],
                "phone": self.clinic_info["location"]["phone"]
            }
    
    def _get_function_definitions(self) -> List[Dict]:
        """Define functions available to the LLM"""
        return [
            {
                "name": "check_available_slots",
                "description": "Check available appointment time slots for a specific date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "Date in YYYY-MM-DD format"
                        },
                        "doctor_id": {
                            "type": "string",
                            "description": "Optional doctor ID (dr_smith or dr_johnson)",
                            "enum": ["dr_smith", "dr_johnson"]
                        }
                    },
                    "required": ["date"]
                }
            },
            {
                "name": "get_next_available_dates",
                "description": "Get the next available dates with appointment slots",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "book_appointment",
                "description": "Book an appointment for a patient",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "patient_name": {
                            "type": "string",
                            "description": "Patient's full name"
                        },
                        "date": {
                            "type": "string",
                            "description": "Appointment date in YYYY-MM-DD format"
                        },
                        "time": {
                            "type": "string",
                            "description": "Appointment time in HH:MM format (24-hour)"
                        },
                        "doctor_id": {
                            "type": "string",
                            "description": "Doctor ID",
                            "enum": ["dr_smith", "dr_johnson"]
                        },
                        "appointment_type": {
                            "type": "string",
                            "description": "Type of appointment",
                            "enum": ["new_patient", "annual_physical", "follow_up", "sick_visit"]
                        },
                        "patient_phone": {
                            "type": "string",
                            "description": "Patient's phone number"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for visit"
                        }
                    },
                    "required": ["patient_name", "date", "time", "doctor_id"]
                }
            },
            {
                "name": "verify_insurance",
                "description": "Verify if an insurance provider is accepted",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "provider_name": {
                            "type": "string",
                            "description": "Insurance provider name (e.g., Blue Cross, Aetna, UnitedHealthcare)"
                        },
                        "plan_type": {
                            "type": "string",
                            "description": "Insurance plan type (PPO, HMO, EPO, etc.)"
                        }
                    },
                    "required": ["provider_name"]
                }
            },
            {
                "name": "get_clinic_info",
                "description": "Get information about the clinic",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "info_type": {
                            "type": "string",
                            "description": "Type of information requested",
                            "enum": ["general", "location", "hours", "doctors", "services"]
                        }
                    }
                }
            }
        ]
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        logger.info("Conversation reset")
    
    def get_greeting(self) -> str:
        """Get initial greeting"""
        return "Hello! Thank you for calling Riverside Medical Center. I'm an AI assistant. How can I help you today?"
