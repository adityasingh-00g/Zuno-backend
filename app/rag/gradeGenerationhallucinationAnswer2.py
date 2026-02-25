from langchain_core.prompts import PromptTemplate
from app.rag.llm import llm
from langchain_core.output_parsers import JsonOutputParser


def grade_hallucination_generation_answer(state):
    question=state["question"]
    documents=state["documents"]
    generation=state["generation"]
    context="\n\n".join(doc.page_content for doc in documents)
    # Hallucination grader
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a factual grounding grader.

        Your task is to determine whether the given answer is fully supported by the provided context.
        An answer is considered grounded ONLY if all factual statements in the answer
        can be directly verified from the context.

        If the answer contains any information that is not supported by the context,
        even if partially correct, respond "no".

        Return ONLY a valid JSON object with a single key "score".
        The value must be either "yes" or "no".
        Do not include any explanation, reasoning, or extra text.
        <|eot_id|>

        <|start_header_id|>user<|end_header_id|>
        Context:
        {documents}

        Answer:
        {generation}
        <|eot_id|>

        <|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["documents", "generation"],
    )
    hallucination_grader=prompt | llm | JsonOutputParser()
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
    
    score=hallucination_grader.invoke({"documents":context,"generation":generation})
    grade=score["score"]

    if(grade.lower() == "yes"):
        score=answer_grader.invoke({"question":question,"generation":generation})
        grade=score["score"]
        if(grade.lower() == "yes"):
            return "useful"
        else:
            return "not useful"
    else:
        return "not supported"