import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

class AppointmentService:
    """Handles appointment scheduling logic"""
    
    def __init__(self, data_path: Optional[str] = None):
        """
    Initialize appointment service
    
    Args:
        data_path: Optional custom path to appointments.json
                  If None, uses data/appointments.json relative to project root
       """
        if data_path is None:
        # Get project root directory
            base_dir = Path(__file__).parent.parent
            self.data_path = base_dir / "data" / "appointments.json"
        else:
            self.data_path = Path(data_path)
        # Load appointment data from file
        self.appointments_data = self._load_data()
        
    def _load_data(self) -> dict:
        """Load appointments data from JSON file"""
        with open(self.data_path, 'r') as f:
            return json.load(f)
    
    def _save_data(self):
        """Save appointments data to JSON file"""
        with open(self.data_path, 'w') as f:
            json.dump(self.appointments_data, f, indent=2)
    
    def get_available_slots(self, date: str, doctor_id: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Get available time slots for a specific date
        
        Args:
            date: Date in YYYY-MM-DD format
            doctor_id: Optional specific doctor ID
            
        Returns:
            Dictionary of doctor_id -> list of available times
        """
        available = self.appointments_data.get("available_slots", {}).get(date, {})
        
        if doctor_id:
            return {doctor_id: available.get(doctor_id, [])}
        
        return available
    
    def get_next_available_dates(self, num_dates: int = 5) -> List[str]:
        """Get next N dates with available slots"""
        all_dates = sorted(self.appointments_data.get("available_slots", {}).keys())
        return all_dates[:num_dates]
    
    def book_appointment(self, 
                        patient_name: str,
                        date: str,
                        time: str,
                        doctor_id: str,
                        appointment_type: str = "follow_up",
                        patient_phone: Optional[str] = None,
                        reason: Optional[str] = None) -> Dict:
        """
        Book an appointment
        
        Returns:
            Dictionary with booking confirmation details
        """
        # Check if slot is available
        available_slots = self.get_available_slots(date, doctor_id)
        
        if doctor_id not in available_slots or time not in available_slots[doctor_id]:
            return {
                "success": False,
                "message": "This time slot is not available."
            }
        
        # Generate appointment ID
        apt_id = f"apt_{len(self.appointments_data.get('booked_appointments', [])) + 1:03d}"
        
        # Create appointment
        appointment = {
            "id": apt_id,
            "patient_name": patient_name,
            "patient_phone": patient_phone,
            "date": date,
            "time": time,
            "doctor_id": doctor_id,
            "type": appointment_type,
            "reason": reason,
            "booked_at": datetime.now().isoformat(),
            "status": "confirmed"
        }
        
        # Add to booked appointments
        if "booked_appointments" not in self.appointments_data:
            self.appointments_data["booked_appointments"] = []
        
        self.appointments_data["booked_appointments"].append(appointment)
        
        # Remove from available slots
        if time in self.appointments_data["available_slots"][date][doctor_id]:
            self.appointments_data["available_slots"][date][doctor_id].remove(time)
        
        # Save changes
        self._save_data()
        
        # Get doctor name
        doctor_name = self._get_doctor_name(doctor_id)
        
        return {
            "success": True,
            "appointment_id": apt_id,
            "patient_name": patient_name,
            "date": date,
            "time": time,
            "doctor_name": doctor_name,
            "message": f"Appointment confirmed for {patient_name} on {date} at {time} with {doctor_name}."
        }
    
    def _get_doctor_name(self, doctor_id: str) -> str:
        """Get doctor's full name from ID"""
        doctor_names = {
            "dr_smith": "Dr. Emily Smith",
            "dr_johnson": "Dr. Michael Johnson",
            "dr_garcia": "Dr. Sofia Garcia"
        }
        return doctor_names.get(doctor_id, "the doctor")
    
    def get_appointment_types(self) -> List[Dict]:
        """Get list of available appointment types"""
        return self.appointments_data.get("appointment_types", [])
    
    def format_date_friendly(self, date: str) -> str:
        """Convert YYYY-MM-DD to friendly format like 'Monday, November 3rd'"""
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        day_suffix = self._get_day_suffix(date_obj.day)
        return date_obj.strftime(f"%A, %B {date_obj.day}{day_suffix}")
    
    def _get_day_suffix(self, day: int) -> str:
        """Get ordinal suffix for day (st, nd, rd, th)"""
        if 11 <= day <= 13:
            return "th"
        suffix_map = {1: "st", 2: "nd", 3: "rd"}
        return suffix_map.get(day % 10, "th")
