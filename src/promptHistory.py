import json
from server import PromptServer
from aiohttp import web

class PromptHistory:
    CATEGORY = "utils/promptHistory"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "outputPrompt"

    def __init__(self):
        self.historyStack = ['']
        self.currentIndex = 0

    @classmethod    
    def INPUT_TYPES(cls):
        return { 
            "required": { 
                "prompt": ("STRING",), 
                "lastPromptIndex": ("INT", {"min": -10, "max": -1, "default": -1}) 
            }, 
            "optional": {
                "text": ("STRING", {"multiline": True, "placeholder": "Here is the current prompt", "forcedInput": True}),
            },
            "hidden": {"node_id": "UNIQUE_ID"},
        }

    def outputPrompt(self, prompt, lastPromptIndex, node_id, text=''):
        # Add the new element to the history stack
        if prompt != self.historyStack[-1]:
            self.historyStack.append(prompt)  # Corrected: Removed assignment
        if len(self.historyStack) > 100:
            self.historyStack.pop(0)
        print("values:", self.historyStack, lastPromptIndex, text, node_id)
        return (self.historyStack[lastPromptIndex],)
    
    @PromptServer.instance.routes.get("/promptHistory/historyStack")
    async def get_loras(self, request):
        return web.json_response(self.historyStack)