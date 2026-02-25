from langchain_core.prompts import PromptTemplate
from app.rag.llm import llm
from langchain_core.output_parsers import JsonOutputParser


def grade_hallucination_generation_answer(state):
    question=state["question"]
    documents=state["documents"]
    generation=state["generation"]

    # Answer grader
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are an answer usefulness grader.

        Decide whether the answer is useful for resolving the question.
        An answer is useful if it directly addresses the question and provides sufficient, relevant information.
        An answer is not useful if it is vague, incomplete, off-topic, or does not clearly answer the question.

        Return ONLY a valid JSON object with a single key "score".
        The value must be either "yes" or "no".
        Do not include any explanation or extra text.
        <|eot_id|>

        <|start_header_id|>user<|end_header_id|>
        Question:
        {question}

        Answer:
        {generation}
        <|eot_id|>

        <|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["generation", "question"],
    )
    answer_grader=prompt | llm |JsonOutputParser()
    
    score=answer_grader.invoke({"question":question,"generation":generation})
    grade=score["score"]

    if(grade.lower() == "yes"):
        print("Generation grade score : ","Useful")
        return "useful"
    else:
        print("Generation grade score : ","Not Useful")
        return "not useful"