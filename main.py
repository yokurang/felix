import logging
import os

from dotenv import load_dotenv

from db_handler import DBHandler
from gpt_handler import (
    GPTHandler,
)  # Make sure this import statement is correct based on your project structure

# Load environment variables
load_dotenv()

# Database credentials
MARIADB_USER = os.getenv("MARIADB_USER", "root")
MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD", "password")
MARIADB_HOST = os.getenv("MARIADB_HOST", "127.0.0.1")
MARIADB_PORT = os.getenv("MARIADB_PORT", "3306")
MARIADB_DATABASE_NAME = os.getenv("MARIADB_DATABASE_NAME", "evooq_test")

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/application.log"),
        logging.StreamHandler(),
    ],
)


def main():
    """
    The entry point of the application.
    """
    logging.info("Starting application...")

    # Initialize DBHandler with database credentials
    db_handler = DBHandler(
        MARIADB_USER,
        MARIADB_PASSWORD,
        MARIADB_HOST,
        MARIADB_PORT,
        MARIADB_DATABASE_NAME,
    )

    # Initialize GPTHandler
    gpt_handler = GPTHandler()

    # Ask user for the enriched_proposal_id
    enriched_proposal_id = int(input("Enter the enriched_proposal_id: "))

    # Fetch details from the database for the given enriched_proposal_id
    enriched_proposal_details = db_handler.get_enriched_proposal_details_by_id(
        enriched_proposal_id
    )

    # Extract constraints and orders details
    constraints_details = enriched_proposal_details[
        "enriched_proposal_evaluated_constraints"
    ]
    orders_details = enriched_proposal_details["enriched_proposals_orders"]

    # Generate financial advice using GPTHandler
    financial_advice = gpt_handler.generate_financial_advice(
        constraints_details, orders_details
    )

    # Log generated financial advice with lazy formatting
    logging.info(
        "\nFinancial advice for enriched_proposal_id %s:\n", enriched_proposal_id
    )
    logging.info(financial_advice)
    logging.info("Application finished successfully.")


if __name__ == "__main__":
    main()
