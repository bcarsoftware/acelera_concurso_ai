from typing import Optional, List

from pydantic import BaseModel


class PromptDTO(BaseModel):
    prompt: str
    params: Optional[List[str]] = None

    @property
    def string(self) -> str:
        template = f"prompt: {self.prompt}\n"

        if self.params:
            param_str = ", ".join(self.params) + "."
            template += f"params: {param_str}\n"

        return template

