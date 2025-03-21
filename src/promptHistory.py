import json
from inspect import cleandoc
from server import PromptServer

class PromptHistory:
    CATEGORY = "utils/promptHistory"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "outputPrompt"

    @classmethod    
    def INPUT_TYPES(cls):
        return { 
            "required": { "prompt": ("STRING",), "lastPromptIndex": ("INT", {"min": -100, "max": 0, "default": 0}) }, 
            "optional": {"text": ("STRING", {"multiline": True, "placeholder": "Here is the current prompt", "forceInput": True}), },
            "hidden": {"node_id": "UNIQUE_ID",
        }}
    
    def __init__(self):
        self.historyStack = ['']
        self.currentIndex = 0

    def outputPrompt(self, prompt, lastPromptIndex, text, node_id):
        # Add the new element to the history stack
        if lastPromptIndex == 0:
            if prompt != self.historyStack[-1]:
                self.historyStack.append(prompt)
            if len(self.historyStack) > 100:
                self.historyStack.pop(0)
        # Convert historyStack to JSON string
        history_json = json.dumps(self.historyStack)
        PromptServer.instance.send_sync("promptHistory.update.history.stack", {"node": node_id, "data": history_json})
        return (self.historyStack[lastPromptIndex],)