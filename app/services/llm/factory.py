from app.core.config import config
from app.services.llm.base import LLMService
from app.services.llm.providers.openai import OpenAIProvider


def create_llm_service() -> LLMService | None:
    """
    根据 config.yaml 中的 LLM 配置创建 LLM 服务。
    Creates an LLM service based on the LLM section of config.yaml.

    The LLM section is OPTIONAL — a missing section (or an empty /
    unknown PROVIDER) disables LLM instead of raising KeyError.

    Returns:
        LLMService | None: 配置的服务实例，未配置时返回 None。
    """
    llm_config = config.get("LLM", {})
    provider = (llm_config.get("PROVIDER") or "").strip().lower()

    if provider == "openai":
        api_key = llm_config.get("OPENAI_API_KEY")
        if not api_key:
            return None
        return OpenAIProvider(api_key=api_key)

    # Unknown / empty / missing provider → LLM disabled
    return None
