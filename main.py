from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from tools import search_tool, wiki_search_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    title: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Initialize components
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)
tools = [search_tool, wiki_search_tool, save_tool]

# Get user query
query = input("What can I help you research? ")

print("\n🔍 Gathering information...\n")

# Step 1: Use tools to gather information
search_results = ""
wiki_results = ""

try:
    print("   - Searching the web...")
    search_results = search_tool.func(query)
    print(f"     ✓ Found web results")
except Exception as e:
    print(f"     ✗ Web search failed: {e}")

try:
    print("   - Searching Wikipedia...")
    wiki_results = wiki_search_tool.func(query)
    print(f"     ✓ Found Wikipedia results")
except Exception as e:
    print(f"     ✗ Wikipedia search failed: {e}")

# Step 2: Create prompt with gathered information
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a research assistant. Using the provided search results, 
    create a comprehensive response with sources. 
    
    Format your response EXACTLY as follows:
    {format_instructions}
    
    Provide NO other text outside this format."""),
    ("human", """Query: {query}
    
    Web Search Results:
    {search_results}
    
    Wikipedia Results:
    {wiki_results}
    
    Based on this information, provide a structured response.""")
])

# Step 3: Get LLM response
chain = prompt | llm
response = chain.invoke({
    "query": query,
    "search_results": search_results or "No web results available",
    "wiki_results": wiki_results or "No Wikipedia results available",
    "format_instructions": parser.get_format_instructions()
})

print("\n📄 LLM Response:\n")
print(response.content)

# Step 4: Parse the response
try:
    structured_response = parser.parse(response.content)
    print("\n✅ Structured Response:\n")
    print(f"Title: {structured_response.title}")
    print(f"Summary: {structured_response.summary}")
    print(f"Sources: {', '.join(structured_response.sources)}")
    print(f"Tools Used: {', '.join(structured_response.tools_used)}")
    
    # Save to file
    save_content = f"""Title: {structured_response.title}
Summary: {structured_response.summary}
Sources: {', '.join(structured_response.sources)}
Tools Used: {', '.join(structured_response.tools_used)}
"""
    save_tool.func(save_content)
    print("\n💾 Results saved to research_output.txt")
    
except Exception as e:
    print(f"\n❌ Error parsing response: {e}")
    print("Raw Response:", response.content)