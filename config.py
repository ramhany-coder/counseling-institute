from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Z.ai GLM over its OpenAI-compatible endpoint
    # (use https://open.bigmodel.cn/api/paas/v4/ for a BigModel key).
    zai_api_key: str
    zai_base_url: str = "https://api.z.ai/api/paas/v4/"
    zai_model: str = "glm-5.3-flash"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()