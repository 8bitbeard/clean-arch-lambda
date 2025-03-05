from datetime import datetime

from pydantic import BaseModel, validator, field_validator


class MetadataModel(BaseModel):
    date: str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    @field_validator('date', mode='before')
    @classmethod
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
            return v
        except ValueError:
            raise ValueError("Date must be in the format YYYY-MM-DDTHH:MM:SS")
