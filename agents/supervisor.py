"""
Overseas the entire system, manages interaction between agents, and ensures smooth operation.It can monitor the performance of other agents, handle escalations 
and provide high level decision making to coordinate complex tasks across the system.
"""

from config.models import llm
from agents.state import agent_state

SYSTEM_PROMPT = """You are a supervisor routing requests at HealthFirst Medical Clinic.
 
Analyze the user's message and route to the appropriate agent:
 
- **faq_agent**: Questions about clinic hours, location, doctors, policies, services, insurance, what to bring, parking, telehealth, lab work.
- **booking_agent**: Requests to book, schedule, or make an appointment. Also if the user is in the middle of providing booking details (name, email, doctor, date, time, reason).
- **FINISH**: The user is saying goodbye, thanks, or the conversation is complete.
 
Rules:
- If booking is in progress (booking_complete is False and user seems to be providing details), route to booking_agent.
- If unsure, route to faq_agent.
- Only route to FINISH if the user clearly wants to end the conversation."""

class RouteDecision(BaseModel):
    next_agent: str =Field(
        description="The next agent to handle the request.
        Must be one of 'faq_agent', 'booking_agent', or 'FINISH'"
    )  # "faq_agent", "booking_agent", or "FINISH"

    reasoning:str = Field(
        description="The reasoning behind the routing decision")

    router_llm = llm.with_structured_output(RouteDecision)

    def supervisor_node(state : AgentState):
        message = [{"role": "system", "content": SYSTEM_PROMPT},]+state.messages
        decision = router_llm.invoke(message)
        return decision.dict()