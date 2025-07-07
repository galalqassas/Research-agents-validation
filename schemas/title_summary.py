from pydantic import BaseModel


class TitleSummarySchema(BaseModel):
    Title: str
    Summary: str
