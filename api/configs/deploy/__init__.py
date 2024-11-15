from pydantic import Field
from pydantic_settings import BaseSettings


class DeploymentConfig(BaseSettings):
    """
    Configuration settings for application deployment
    """

    APPLICATION_NAME: str = Field(
        description="Name of the application, used for identification and logging purposes",
        default="langgenius/dify",
    )

    DEBUG: bool = Field(
        description="Enable debug mode for additional logging and development features",
        default=False,
    )

    TESTING: bool = Field(
        description="Enable testing mode for running automated tests",
        default=False,
    )

    EDITION: str = Field(
        description="Deployment edition of the application (e.g., 'SELF_HOSTED', 'CLOUD')",
        default="SELF_HOSTED",
    )

    RACIO_ACCOUNT_ENABLED: bool = Field(
        description="Enable for RACIO_ACCOUNT feature",
        default=False,
    )

    DEPLOY_ENV: str = Field(
        description="Deployment environment (e.g., 'PRODUCTION', 'DEVELOPMENT'), default to PRODUCTION",
        default="PRODUCTION",
    )
