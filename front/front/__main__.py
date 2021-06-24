import os
from front.logging import logger_setup
from front.server import app

if __name__ == "__main__":
    logger_setup()
    app.run(
        debug=True,
        port=os.getenv("FRONT_PORT"),
    )
