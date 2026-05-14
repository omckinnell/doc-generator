from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from parser import parser


load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert Python documentation writer.
    Analyze the provided Python code and extract structured documentation.
    Be precise and concise. Only document what is explicitly in the code.
    {format_instructions}"""),
    ("human", "Here is the Python code to document:\n\n{code}")
])

chain = prompt | llm | parser

def generate_docs(code: str) -> dict:
    result = chain.invoke({
        "code": code,
        "format_instructions": parser.get_format_instructions()
    })
    return result