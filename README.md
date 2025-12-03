# LLM Teacher
This package uses a large language model (LLM) to automatically evaluate students' responses and deliver feedback.
A custom knowledge context can be provided to increase the quality of the evaluation.

## Environment variables
The QuestionPy server must pass the following environment variables to the package:
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`

## Caution
Currently, this package may only work as expected when the Python version used to package the package and the Python
version on the QuestionPy server match. This is due to the `openai` dependency `jiter` which is an extension module.
