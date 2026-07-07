from pathlib import Path


class PromptManager:
    _template_dir = Path(__file__).parent / "templates"

    @classmethod
    def load(cls, template_name: str) -> str:
        path = cls._template_dir / template_name

        if not path.exists():
            raise FileNotFoundError(f"Prompt template not found: {path}")

        return path.read_text(encoding="utf-8").strip()

    @classmethod
    def render(cls, template_name: str, **kwargs) -> str:
        template = cls.load(template_name)
        return template.format(**kwargs)

    @classmethod
    def system_prompt(cls) -> str:
        return cls.load("system.md")

    @classmethod
    def answer_prompt(cls, question: str, context: str) -> str:
        return cls.render(
            "answer.md",
            question=question,
            context=context,
        )

    @classmethod
    def refusal_message(cls) -> str:
        return cls.load("refusal.md")
