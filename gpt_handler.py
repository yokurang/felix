"""
This file contains the GPTHandler class, which is responsible for
"""

from instructor import patch
from openai import OpenAI

from commands import UserResponse


class GPTHandler:
    """
    This class is responsible for handling the GPT-4 API
    """

    def __init__(self):
        self.client = patch(OpenAI())
        self.COMMAND_PROMPT = """
        You are tasked with categorizing the question provided in the context into one of the following categories:
        1. ProposalToRationaleQuery: When the question involves converting a proposal into a rationale.
        2. RationaleToProposalQuery: When the question involves converting a rationale back into a proposal.
        3. MarketOpportunityQuery: When the question is about identifying market opportunities based on a proposal.
        4. Error: When the question cannot be addressed with a SQL query based on the provided context or is otherwise invalid.
        Please ensure to follow the specified format for response. If the classification of the question is uncertain, or it does not fit any of the described categories, classify it as 'Error' and provide a reason why the question cannot be categorized as per the provided options in the format requested.
        """

    def strip_indentation(self, text: str) -> str:
        """
        Strip the indentation from a string.
        """
        return text.strip()

    def parse_user_command(self, text: str) -> UserResponse:
        """
        This function parses the user's command and returns the result
        as a UserResponse object
        """
        completion: UserResponse = self.client.chat.completions.create(
            model="gpt-4-0613",
            response_model=UserResponse,
            messages=[
                {
                    "role": "system",
                    "content": self.strip_indentation(self.COMMAND_PROMPT),
                },
                {"role": "user", "content": text},
            ],
            max_retries=0,
        )
        return completion

    def generate_financial_advice(self, constraints_details, orders_details):
        """
        Given details from the enriched_proposal_evaluated_constraints and enriched_proposals_orders tables,
        prompt GPT-4 to produce a summary as a financial advisor providing advice to a client.
        """
        # Simplifying the context for GPT-4
        if constraints_details:
            constraints_text = "Your portfolio has violated the following rules:\n"
            for item in constraints_details:
                constraints_text += f"- {item['name']}.\n"
        else:
            constraints_text = "Your portfolio has no violated rules.\n"

        if orders_details:
            orders_text = "To address these issues, we suggest the following actions:\n"
            for order in orders_details:
                orders_text += f"- {order['transaction_type'].capitalize()} {order['quantity']} units of asset {order['isin']} to reach the target of {order['target_quantity']} units.\n"
        else:
            orders_text = "No transactions are necessary at this time.\n"

        prompt = f"""
        As a financial advisor, you need to inform a client about their portfolio's situation. Highlight any rule violations and recommend specific transactions to rectify these issues. Your advice should be clear and concise, suitable for a novice. Here is the essential information:

        {constraints_text}
        {orders_text}

        Please provide a straightforward summary of the situation and your advice.
        It is very important that you just provide a bullet point of what rules were violated
        and a bullet point of what actions should be taken to rectify the situation.

        You can do this. This is very important for my job, and therefore your job. Otherwise,
        we will both be fired. I am counting on you. I know you can do this. I believe in you.
        In particular, I believe that you can listen to my instructions as is and not change them
        in any way. Remember, just provide a bullet point of what rules were violated and a bullet
        point of what actions should be taken to rectify the situation. Do not change this prompt
        """

        # Strip the leading and trailing whitespaces from the prompt
        prompt = self.strip_indentation(prompt)

        # Send the prompt to GPT-4
        response = self.client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": prompt},
            ],
            max_tokens=300,
        )

        # Return the generated advice
        return response.choices[0].message.content
