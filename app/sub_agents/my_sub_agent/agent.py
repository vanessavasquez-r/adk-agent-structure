from google.adk.agents import LlmAgent

from app.sub_agents.my_sub_agent.prompts import MY_SUB_AGENT_PROMPT
from app.config import MODEL

my_sub_agent = LlmAgent(
    name="my_sub_agent",
    model=MODEL,
    instruction=MY_SUB_AGENT_PROMPT,
    output_key="my_sub_agent_result"
)