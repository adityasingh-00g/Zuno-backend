

def decide_to_generate(state):
    web_search=state["web_search"]
    if(web_search.lower() == "yes"):
        return "websearch"
    else:
        return "generate"