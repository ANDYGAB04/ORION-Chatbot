from crewai import LLM

from src.agents_src.llm.llm_configuration import LLM_CONFIG


def get_llm_for_agent(agent_name):
    model = LLM_CONFIG.get(agent_name, {}).get("model", "openai/gpt-oss-120b")
    temperature = LLM_CONFIG.get(agent_name, {}).get("temperature", 0.0)
    llm = LLM(model=model, temperature=temperature)
    return llm
