from pydantic import BaseModel, Field, computed_field
from typing import List

# State Creation
class Analyst(BaseModel):
    affiliation: str = Field(
        description="Primary affiliation of the analyst.",
    )
    name: str = Field(
        description="Name of the analyst."
    )
    role: str = Field(
        description="Role of the analyst in the context of the topic."
    )
    description: str = Field(
        description="Description of the analyst focus, concerns, and motives."
    )
    # @computed_field: when used model_dump will show the computed field
    @property (# inbuilt decorator in Python)
    def persona(self) -> str:
        return f"Name: {self.name}\nRole: {self.role}\nAffiliation: {self.affiliation}\nDescription: {self.description}\n"

class Perspectives(BaseModel):
    analysts: List[Analyst] = Field(description="Comprehensive list of analysts with their roles and affiliations.")

# # model_dump: convert model instance to dictionary representation
# # model_validate: validate and create model instance from dictionary representation
# analyst1 = Analyst(name="John Doe", role="Senior Analyst", affiliation="ABC Corp", description="Experienced analyst with a focus on market trends.")
# analyst2 = Analyst(name="Jane Smith", role="Data Scientist", affiliation="XYZ Inc", description="Specializes in data analysis and predictive modeling.")

# perspectives = Perspectives(analysts=[analyst1, analyst2])
# dict_representation = perspectives.model_dump()
# model_reconstructed = Perspectives.model_validate(dict_representation)

# print(dict_representation)
# print(model_reconstructed.analysts[0].persona)

