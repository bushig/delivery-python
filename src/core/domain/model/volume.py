from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class Volume(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: Decimal

    def model_post_init(self, __context: object) -> None:
        if self.value <= 0:
            raise ValueError("Volume can't be negative or zero")
