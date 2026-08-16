from dataclasses import dataclass

@dataclass
class TokenUsage:
    input_tokens: int
    output_tokens: int

class Pricing:
    # $2 / MTok
    input_price: float = 2
    # $10 / MTok
    output_price: float = 10

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        return input_tokens / 1024 / 1024 * self.input_price + output_tokens / 1024 / 1024 * self.output_price