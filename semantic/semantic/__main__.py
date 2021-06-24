import os
from semantic.logging import logger_setup
from semantic.server import app

if __name__ == "__main__":
    logger_setup()
    app.run(
        debug=True,
        port=os.getenv("SEMANTIC_PORT"),
    )
