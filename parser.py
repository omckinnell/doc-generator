from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser

class FunctionDoc(BaseModel):
    name: str = Field(description="Function name")
    description: str = Field(description="What the function does")
    parameters: List[str] = Field(description="List of parameters with types and descriptions")
    returns: str = Field(description="What the function returns")
    example: str = Field(description="A short usage example")

class ModuleDoc(BaseModel):
    module_summary: str = Field(description="High level summary of what this file does")
    dependencies: List[str] = Field(description="Libraries or modules imported")
    functions: List[FunctionDoc] = Field(description="All functions found in the file")
    notes: Optional[str] = Field(description="Any warnings, TODOs, or important notes found")

parser = PydanticOutputParser(pydantic_object=ModuleDoc)