"""
A class that handles the connection to the MariaDB database
"""

import json
import logging
import os
import sys
from datetime import datetime
from decimal import Decimal
from typing import List

import mariadb
from dotenv import load_dotenv

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
        logging.FileHandler("logs/db_handler.log"),
        logging.StreamHandler(),
    ],
)


def process_row(row):
    """
    Process a database row, converting non-serializable types (bytes, Decimal, datetime) to serializable types.
    """
    processed = {}
    for key, value in row.items():
        if isinstance(value, bytes):
            # Convert bytes to string assuming UTF-8 encoding; adjust as necessary.
            processed[key] = value.decode("utf-8")
        elif isinstance(value, Decimal):
            # Convert Decimal to float
            processed[key] = float(value)
        elif isinstance(value, datetime):
            # Convert datetime to ISO 8601 string format (YYYY-MM-DDTHH:MM:SS)
            processed[key] = value.isoformat()
        else:
            processed[key] = value
    return processed


class DBHandler:
    """
    The class that handles the connection to the MariaDB database
    """

    def __init__(
        self, user: str, password: str, hostname: str, port: str, database_name: str
    ):
        self.user = user
        self.password = password
        self.hostname = hostname
        self.port = port
        self.database_name = database_name
        self.connection = None
        self.cursor = None
        self.start_mariadb_connection()

    def start_mariadb_connection(self):
        """
        This function starts the connection with the MariaDB database
        """
        try:
            self.connection = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.hostname,
                port=int(self.port),
                database=self.database_name,
            )
            self.cursor = self.connection.cursor()
        except mariadb.Error as error:
            print(f"Error connecting to MariaDB Platform: {error}")
            sys.exit(1)

    def query_enriched_proposal_evaluated_constraints_by_id(
        self, enriched_proposal_id: int
    ) -> List[dict]:
        """
        Fetches violated constraints for a given enriched_proposal_id.

        Args:
            enriched_proposal_id (int): The ID of the enriched proposal.

        Returns:
            List[dict]: A list of dictionaries containing the fetched constraint details.
        """
        query = """
        SELECT enriched_proposal_id, name, violated, rule_scope, validation_mode, rule_group_type
        FROM enriched_proposal_evaluated_constraints
        WHERE enriched_proposal_id = %s AND violated = 1;
        """
        try:
            self.cursor.execute(query, (enriched_proposal_id,))
            rows = self.cursor.fetchall()
            return [
                process_row(dict(zip([col[0] for col in self.cursor.description], row)))
                for row in rows
            ]
            # return [
            #     dict(zip([col[0] for col in self.cursor.description], row))
            #     for row in rows
            # ]
        except mariadb.Error as error:
            print(f"Error fetching constraints: {error}")
            return []

    def query_enriched_proposals_orders_by_id(
        self, enriched_proposal_id: int
    ) -> List[dict]:
        """
        Fetches orders for a given enriched_proposal_id.

        Args:
            enriched_proposal_id (int): The ID of the enriched proposal.

        Returns:
            List[dict]: A list of dictionaries containing the fetched order details.
        """
        query = """
        SELECT id, transaction_type, isin, quantity, cash_currency_used, adjusted_quantity, target_quantity
        FROM enriched_proposals_orders
        WHERE enriched_proposals_id = %s;

        """
        try:
            self.cursor.execute(query, (enriched_proposal_id,))
            rows = self.cursor.fetchall()
            return [
                process_row(dict(zip([col[0] for col in self.cursor.description], row)))
                for row in rows
            ]
            # return [
            #     dict(zip([col[0] for col in self.cursor.description], row))
            #     for row in rows
            # ]
        except mariadb.Error as error:
            print(f"Error fetching orders: {error}")
            return []

    def get_enriched_proposal_details_by_id(self, enriched_proposal_id: int) -> dict:
        """
        Fetches specified details from enriched_proposals_orders and
        enriched_proposal_evaluated_constraints tables for a given enriched_proposal_id.
        Args:
            enriched_proposal_id (int): The ID of the enriched proposal.

        Returns:
            dict: A dictionary containing the fetched details from both tables.
        """
        constraints = self.query_enriched_proposal_evaluated_constraints_by_id(
            enriched_proposal_id
        )
        orders = self.query_enriched_proposals_orders_by_id(enriched_proposal_id)

        details = {
            "enriched_proposal_evaluated_constraints": constraints,
            "enriched_proposals_orders": orders,
        }

        return details

    def get_details_for_all_enriched_proposals(self) -> List[dict]:
        """
        Fetches detailed information for all enriched proposals by their IDs directly from the
        enriched_proposal_evaluated_constraints table, without needing to first query all unique IDs.

        Returns:
            List[dict]: A list of dictionaries, each containing the fetched details for an enriched proposal.
        """
        query = """
        SELECT DISTINCT enriched_proposal_id
        FROM enriched_proposal_evaluated_constraints;
        """
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            enriched_proposal_ids = [row[0] for row in rows]
        except mariadb.Error as error:
            print(f"Error fetching unique proposal IDs: {error}")
            return []

        details_list = []
        for proposal_id in enriched_proposal_ids:
            details = self.get_enriched_proposal_details_by_id(proposal_id)
            details_list.append(details)

        return details_list


def main():
    """
    A function to see what data our database has.
    """
    # Initialize DBHandler with database credentials
    db_handler = DBHandler(
        MARIADB_USER,
        MARIADB_PASSWORD,
        MARIADB_HOST,
        MARIADB_PORT,
        MARIADB_DATABASE_NAME,
    )

    # Fetch details for all enriched proposals
    all_details = db_handler.get_details_for_all_enriched_proposals()
    # Define the file path relative to the project root
    file_path = "data/all_enriched_proposal_details.json"

    # # Save the details to a JSON file
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(all_details, json_file, indent=4)

    logging.info("Details for all enriched proposals have been saved to %s.", file_path)


if __name__ == "__main__":
    main()
