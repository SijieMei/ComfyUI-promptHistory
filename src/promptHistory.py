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

        if unique_id is not None and extra_pnginfo is not None:
            if not isinstance(extra_pnginfo, list):
                    print("Error: extra_pnginfo is not a list")
            elif (
                not isinstance(extra_pnginfo[0], dict)
                or "workflow" not in extra_pnginfo[0]
            ):
                print("Error: extra_pnginfo[0] is not a dict or missing 'workflow' key")
            else:
                workflow = extra_pnginfo[0]["workflow"]
                node = next(
                    (x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])),
                    None,
                )
                if node:
                    node["widgets_values"] = [prompt, lastPromptIndex, self.historyStack[lastPromptIndex]]
    
        return (self.historyStack[lastPromptIndex],)
    
    @PromptServer.instance.routes.get("/promptHistory/historyStack")
    async def get_loras(self, request):
        return web.json_response(self.historyStack)