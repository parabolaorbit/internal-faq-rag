from pathlib import Path

from faq_rag.prompt_types import PromptType


PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


class PromptBuilder:
    PROMPT_FILES = {
        PromptType.FAQ: "faq_prompt.txt",
        PromptType.BEGINNER: "beginner_prompt.txt",
        PromptType.BULLET: "bullet_prompt.txt",
        PromptType.SUMMARY: "summarize_prompt.txt",
        PromptType.STRUCTURED_FAQ: "structured_faq_prompt.txt",
    }
    
    def _read_prompt(self, filename: str) -> str:
        return (PROMPTS_DIR / filename).read_text(encoding="utf-8")

    def build_system_prompt(self, prompt_type: PromptType) -> str:
        filename = self.PROMPT_FILES.get(prompt_type)
        if not filename:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
        return self._read_prompt(filename)
