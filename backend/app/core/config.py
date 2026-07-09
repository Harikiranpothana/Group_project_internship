from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    PROJECT_ID = os.getenv("PROJECT_ID")

    DATASET_ID = os.getenv("DATASET_ID")

    GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS"
    )

    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "gemini-2.5-flash"
    )


settings = Settings()