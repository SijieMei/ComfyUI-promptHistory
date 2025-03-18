from inspect import cleandoc

class PromptHistory:
    CATEGORY = "utils/promptHistory"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "outputPrompt"

    @classmethod    
    def INPUT_TYPES(cls):
        return { "required":  { "lastPromptIndex": ("INT", {"min": -100, "max": 0, "default": 0}) }, "optional": { "text": ("STRING",)} }
    
    def __init__(self):
        self.historyStack = []
        self.currentIndex = 0

    def outputPrompt(self, lastPromptIndex, text=""):
        # Add the new element to the history stack
        if lastPromptIndex == 0:
            if text != self.historyStack[-1]:
                self.historyStack.append(text)
            if len(self.historyStack) > 100:
                self.historyStack.pop(0)
        return (self.historyStack[lastPromptIndex],)
    
