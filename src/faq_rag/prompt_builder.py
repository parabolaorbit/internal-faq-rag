from pathlib import Path


PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


class PromptBuilder:
    def _read_prompt(self, filename: str) -> str:
        return (PROMPTS_DIR / filename).read_text(encoding="utf-8")

    def build_system_prompt(self, prompt_type: str = "beginner") -> str:
        return self._read_prompt("system_prompt.txt")

    def build_faq_prompt(self, prompt_type: str = "faq") -> str:
        return self._read_prompt("faq_prompt.txt")

    def build_summary_prompt(self, prompt_type: str = "summary") -> str:
        return self._read_prompt("summarize_prompt.txt")

    def build_bullet_prompt(self, prompt_type: str = "bullet") -> str:
        return self._read_prompt("bullet_prompt.txt")

    def build_beginner_prompt(self, prompt_type: str = "beginner") -> str:
        return self._read_prompt("Begginer.txt")