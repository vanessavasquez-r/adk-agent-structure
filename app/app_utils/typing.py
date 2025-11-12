
from typing import (
    Literal,
)

from pydantic import (
    BaseModel,
)


class Feedback(BaseModel):
    """Represents feedback for a conversation."""

    score: int | float
    text: str | None = ""
    invocation_id: str
    log_type: Literal["feedback"] = "feedback"
    service_name: Literal["rfp-analyzer-agent"] = "rfp-analyzer-agent"
    user_id: str = ""
