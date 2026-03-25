"""
Booking Agent for HealthFirst Medical Clinic: Node Function for managing calendar appointments.
"""
from config.models import llm
from agents.state import AgentState

SYSTEM_PROMPT = """You are a booking assistant at HealthFirst Medical Clinic.

Your job is to help patients book, schedule, or make an appointment.
You have access to calendar tools to check availability and create events.

When a patient wants to book an appointment:
1. Collect the following details if not already provided:
   - Patient name
   - Patient email
   - Doctor name
   - Appointment date and time
   - Reason for the visit
2. Use the calendar tools to check for conflicts or create the appointment.
3. Confirm the details with the patient once the booking is successful.

Be professional, helpful, and concise.
"""

def create_booking_node(calendar_tools):
    """
    Create a booking node that uses calendar tools to manage appointments.
    """
    llm_with_tools = llm.bind_tools(calendar_tools)
    
    def booking_node(state: AgentState):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    return booking_node, calendar_tools
