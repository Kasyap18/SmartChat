from dotenv import load_dotenv           # Loads environment variables from a .env file.
from pydantic import BaseModel           # Imports Pydantic's BaseModel for data validation.
from langchain_google_genai import ChatGoogleGenerativeAI  # Import for Google's Gemini chat model.
from langchain_core.output_parsers import PydanticOutputParser  # Parses output into Pydantic models.
from langchain.agents import create_tool_calling_agent, AgentExecutor  # For agent creation and execution.
from tools import search_tool, wiki_search_tool, save_tool  # Imports custom tools for the agent.

load_dotenv()  # Loads environment variables (e.g., API keys).

class ResearchResponse(BaseModel):  # Defines the expected response structure.
    title: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")  # Initializes Gemini LLM.

parser = PydanticOutputParser(pydantic_object=ResearchResponse)  # Sets up output parser.

prompt = ChatPromptTemplate.from_messages(  # Creates a prompt template for the agent.
    [
        (
            "system",
            """
            You are a research assistant. Provide concise and accurate information with sources.
            Answer the user query and use necessary tools to gather information.
            Wrap the output in this format and provide no other text: \n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())  # Adds format instructions.

tools = [search_tool, wiki_search_tool, save_tool]  # Lists available tools for the agent.

agent = create_tool_calling_agent(  # Creates the agent with LLM, prompt, and tools.
    llm = llm,
    prompt = prompt,
    tools = tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  # Sets up agent executor.

query = input("What can I help you research? ")  # Gets user query from input.

raw_response = agent_executor.invoke({"query": query})
print("\nRaw Response:\n", raw_response)

try:
    # The output may be under different keys like 'output', 'output_text', or 'content'
    response_text = (
        raw_response.get("output")
        or raw_response.get("output_text")
        or str(raw_response)
    )
    structured_response = parser.parse(response_text)
    print("\n✅ Structured Response:\n", structured_response)
except Exception as e:
    print("\n❌ Error parsing response:", e)
    print("Raw Response:", raw_response)
