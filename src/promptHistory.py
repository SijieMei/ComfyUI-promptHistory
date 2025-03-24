import json
from server import PromptServer
from aiohttp import web

class PromptHistory:
    CATEGORY = "utils/promptHistory"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "outputPrompt"

    def __init__(self):
        self.historyStack = ['']

    @classmethod    
    def INPUT_TYPES(cls):
        return { 
            "required": { 
                "prompt": ("STRING",), 
                "lastPromptIndex": ("INT", {"min": -10, "max": -1, "default": -1}) 
            }, 
            # "optional": {
            #     "content": ("STRING", {"multiline": True, "placeholder": "Here is the current prompt"}),
            # },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    def outputPrompt(self, prompt, lastPromptIndex, unique_id=None, extra_pnginfo=None):
        # Add the new element to the history stack
        if prompt not in self.historyStack:
            self.historyStack.append(prompt)  # Corrected: Removed assignment

        PromptServer.instance.send_sync("update-history-stack",
                                {"node_id": unique_id, "historyStack": self.historyStack, "lastPromptIndex": lastPromptIndex})
    
        return (self.historyStack[lastPromptIndex],)
    
    @PromptServer.instance.routes.get("/promptHistory/historyStack")
    async def get_loras(self, request):
        return web.json_response(self.historyStack)