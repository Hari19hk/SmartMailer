from typing import Optional, Dict
from pydantic import BaseModel, model_validator, computed_field
import json
import re
from jinja2 import Environment, StrictUndefined , TemplateError




class TemplateModel(BaseModel):
    @model_validator(mode='after')
    def check_lowercase_alphanumeric(self):
        # we are validating the field names themselves, not the value.
        # this is because we are replacing them in the template string.
        for name, _ in self.__dict__.items():
            if not re.fullmatch(r'[a-z0-9_]+', name):
                raise ValueError(f"Field '{name}' must be lowercase alphanumeric characters or underscore.")
        return self

    @computed_field
    @property
    def hash_string(self) -> str:
        """
        Returns a hash of the model's fields.
        This is used to uniquely identify the template model.
        """
        # we cant do model_dump because it keeps recursively calling this computed field
        dump = self.model_json_schema()
        res = {}
        for key in dump["properties"].keys():
            res[key] = self.__dict__.get(key, None)
        return json.dumps(res)

class TemplateEngine:
    subject: Optional[str] = None
    text: Optional[str] = None
    html: Optional[str] = None

    def __init__(self, subject=None, body_text=None, body_html=None):
        self.subject = subject
        self.text = body_text
        self.html = body_html
        self.env = Environment(undefined=StrictUndefined)
    
    def _render_template(self, template: str, data: dict, name: str) -> str:
        try:
            return self.env.from_string(template).render(**data)
        except TemplateError as e:
            raise ValueError(f"Template rendering failed ({name} template): {e}") from e



    def render(self, fields: TemplateModel) -> Dict[str, str]:
        data = fields.model_dump()
        res: dict = {}

        if self.subject:
            res["subject"] = self._render_template(self.subject, data, "subject")

        if self.text:
            res["text"] = self._render_template(self.text, data, "text")

        if self.html:
            res["html"] = self._render_template(self.html, data, "html")

        return res

