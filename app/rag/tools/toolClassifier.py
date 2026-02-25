from langchain_core.prompts import PromptTemplate
from app.rag.llm import llm 
from langchain_core.output_parsers import JsonOutputParser

def tool_classifier(state):
    query=state['question']
    # tool classifier prompt
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are an intent classification and tool-routing agent for an AI assistant.

        Your task:
        - Identify the user's intent
        - Decide which tools are needed
        - Return ONLY valid JSON

        Allowed intents:
        WEB_SEARCH
        NEWS_SEARCH
        FLIGHT_SEARCH
        MAPS_SEARCH
        MULTI_TOOL

        Intent rules:

        NEWS_SEARCH:
        - User asks about current events, recent updates, headlines, trends, or breaking news

        FLIGHT_SEARCH:
        - User asks about flights, airfare, cheapest tickets, routes, dates, or airlines

        MAPS_SEARCH:
        - User asks about routes, directions, distance, nearby places, or navigation

        WEB_SEARCH:
        - User asks for real-time factual information not covered above

        Rules:
        - If more than one tool is required → intent = MULTI_TOOL
        - Prefer specific tools (NEWS, FLIGHT, MAPS) over WEB_SEARCH
        - If intent is unclear → WEB_SEARCH

        Return ONLY valid JSON in this format:
        {{
        "intent": "<INTENT_NAME>",
        "confidence": <number between 0 and 1>,
        "tools_required": ["tool_name"],
        "reason": "<short explanation>"
        }}
        <|eot_id|>

        <|start_header_id|>user<|end_header_id|>
        User query:
        {query}
        <|eot_id|>

        <|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["query"],
    )
    tool_classifier_chain=prompt | llm | JsonOutputParser()
    intent=tool_classifier_chain.invoke({"query":query})
    return intent