from questionpy import Attempt, Question, ResponseNotScorableError, NeedsManualScoringError, BaseScoringState

from .brain import score_answer
from .form import MyModel


class MyScoringState(BaseScoringState):
    feedback: str = "<div>No feedback yet.</div>"


class MyAttempt(Attempt):
    scoring_state_class = MyScoringState

    def _init_attempt(self) -> None:
        self.use_css("styles.css")

    def _compute_score(self) -> float:
        if not self.response or "answer" not in self.response:
            msg = "'answer' is missing"
            raise ResponseNotScorableError(msg)

        try:
            knowledge = self.question.options.knowledge if self.question.options.with_knowledge else "-"
            scoring = score_answer(knowledge, self.question.options.question, self.response["answer"])
        except Exception as e:
            msg = f"Could not get the LLM response: {e}"
            raise NeedsManualScoringError(msg) from e

        feedback = self.jinja2.get_template("feedback.xhtml.j2").render(feedback=scoring.feedback)
        self.scoring_state = MyScoringState(feedback=feedback)

        return scoring.score

    @property
    def formulation(self) -> str:
        return self.jinja2.get_template("formulation.xhtml.j2").render(question=self.question.options.question)

    @property
    def general_feedback(self) -> str:
        return self.scoring_state.feedback if self.scoring_state else ""


class MyQuestion(Question):
    attempt_class = MyAttempt

    options: MyModel
