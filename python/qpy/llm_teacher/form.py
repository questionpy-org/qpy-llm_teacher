from pydantic import field_validator

from questionpy.form import FormModel, checkbox, is_not_checked, text_area, text_input


class MyModel(FormModel):
    question = text_input("Question", required=True)
    with_knowledge = checkbox(
        "Custom Knowledge", None, help="If selected, your custom knowledge will be used to score the answer."
    )
    knowledge = text_area("Knowledge", hide_if=[is_not_checked("with_knowledge")])

    @field_validator("knowledge", mode="after")
    @classmethod
    def context_required(cls, value, values):
        if values.data["with_knowledge"] and not value:
            raise ValueError("Knowledge is required when 'Custom Knowledge' is not checked.")
        return value
