"""Top-level package for prompt_history."""


from .src.promptHistory import PromptHistory

WEB_DIRECTORY = "./web/js"

NODE_CLASS_MAPPINGS = {
    "PromptHistory": PromptHistory
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptHistory": "Prompt History"
}

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """WalkingMeat"""
__email__ = "245798972@qq.com"
__version__ = "0.0.1"