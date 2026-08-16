from faq_rag.tools.calculator import calculate
from faq_rag.tools.datetime_tool import get_current_date

TOOL_FUNCTIONS = {
    "get_current_date": get_current_date,
    "calculate": calculate,
}

TOOL_DEFINITIONS = [
    {
        "name": "get_current_date",
        "description": "現在の日付をYYYY-MM-DD形式で取得します。",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "calculate",
        "description": "数式を計算します。",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "計算する数式",
                },
            },
            "required": ["expression"],
        },
    }
]