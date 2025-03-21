import { app } from "../../scripts/app.js"
import { api } from "../../../scripts/api.js"

console.log("PromptHistory.js loaded")

app.registerExtension({ 
	name: "prmopt.history.extention",
	async setup() { 
        const logToPanel = (message) => {
            app.ui.log(`[PromptHistory] ${message}`);
        };

        api.addEventListener("promptHistory.update.history.stack", (msg) => {
            this.historyStack = msg.data;
            logToPanel(`收到历史堆栈更新消息: ${JSON.stringify(this.historyStack)}`);
        });

        logToPanel("Setup complete!");
	},
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        console.log(222)
        if (nodeType.ComfyClass == "PromptHistory") {
            // Modify nodeType before registration

            const onConfigure = nodeType.prototype.onConfigure;
            nodeType.prototype.onConfigure = function(data) {
                onConfigure?.apply(this, arguments)
                console.log("PromptHistory node created")
                this.historyStack = []
                const indexWidget = this.widgets.find(w => w.name === "lastPromptIndex")
                if(indexWidget){
                    indexWidget.value = 0
                    indexWidget.callback = (value) => {
                        console.log("lastPromptIndex callback", value)
                        const promptWidget = this.widgets.find(w => w.name === "prompt")
                        promptWidget.value = "222"
                        // promptWidget.value = this.historyStack[value]
                    }
                    promptWidget.callback(0)
                }
                app.ui.log(`[PromptHistory] Node configured with data: ${JSON.stringify(data)}`);
            }

            const onPropertyChanged = nodeType.prototype.onPropertyChanged
            nodeType.prototype.onPropertyChanged = (property, value, prevValue) => {
                onPropertyChanged?.apply(this, arguments)
                app.ui.log(`Property changed: ${property}, New Value: ${value}, Previous Value: ${prevValue}`);
                // ...handle property change logic...
            }
        }
    }
})