"""
A module to categorize commands for the LLM application.
"""

from typing import Optional, Union

from pydantic import BaseModel, Field


class ProposalToRationaleQuery(BaseModel):
    """
    An SQL query to convert a proposal to a rationale.
    """

    proposal: str = Field(
        description="""The proposal that needs to be converted
        to a rationale."""
    )


class RationaleToProposalQuery(BaseModel):
    """
    An SQL query to convert a rationale to a proposal.
    """

    rationale: str = Field(
        description="""The rationale that needs to be converted
        to a proposal."""
    )


class MarketOpportunityQuery(BaseModel):
    """
    An SQL query to find market opportunities.
    """

    proposal: str = Field(
        description="""The proposal that needs to be converted
        to a rationale."""
    )


class Error(BaseModel):
    """
    An unviable query from the user.
    """

    error_reason: str = Field("The reason why the query is invalid.")


class MaybeResponse(BaseModel):
    """
    A response from the LLM application.
    """

    response: Union[
        ProposalToRationaleQuery,
        RationaleToProposalQuery,
        MarketOpportunityQuery,
        Error,
    ] = Field(
        description="""The response from the LLM application.
        It can be a proposal to rationale query, a rationale to
        proposal query, a market opportunity query, or an error."""
    )


class UserResponse(BaseModel):
    """
    The response from the LLM application to the user.
    """

    result: Optional[MaybeResponse] = Field(default=None)
    is_error: bool = Field(default=False)
    message: Optional[str] = Field(default=None)
