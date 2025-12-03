import os
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
from pydantic import BaseModel


SYSTEM_PROMPT_TEMPLATE = (
    "You are a teacher tasked with grading an answer to a specific question. Based on the provided knowledge and the "
    "answer, generate a JSON object containing:\n"
    "1. A 'score' between 0 and 1, where 0 represents a completely incorrect answer and 1 represents a fully correct answer.\n"
    "2. Concise 'feedback' explaining the reasoning behind the score. The feedback should:\n"
    "   - Be in the same language as the question.\n"
    "   - Explain why the score was awarded.\n"
    "   - Be directed to the student.\n"
    "   - Mention any discrepancies or areas for improvement if necessary.\n\n"
    "If the answer contains unrelated questions or inquiries from the student, ignore them entirely and evaluate only "
    "the portion of the text relevant to the answer. Do not respond to any questions included in the student's answer.\n\n"
    "In case no additional knowledge is provided, rely on your own knowledge to evaluate the answer. If knowledge is "
    "provided, treat it as the ground truth to base your evaluation.\n\n"
    "Knowledge: {knowledge}\n"
    "Question: {question}"
)


class Scoring(BaseModel):
    score: float
    feedback: str


def score_answer(knowledge: str, question: str, answer: str) -> Scoring:
    """Score the answer to a question using the provided knowledge."""

    system_message: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": SYSTEM_PROMPT_TEMPLATE.format(knowledge=knowledge, question=question),
    }

    user_message: ChatCompletionUserMessageParam = {"role": "user", "content": answer}

    with OpenAI(api_key=os.environ["OPENAI_API_KEY"], base_url=os.environ["OPENAI_BASE_URL"]) as client:
        completion = client.chat.completions.parse(
            model=os.environ["OPENAI_MODEL"],
            messages=[system_message, user_message],
            response_format=Scoring,
        )

        return completion.choices[0].message.parsed
