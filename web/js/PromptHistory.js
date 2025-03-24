import { app } from "../../scripts/app.js"
import { api } from "../../scripts/api.js"
import { ComfyWidgets } from "../../scripts/widgets.js"

function nodeFeedbackHandler(event) {
	let nodes = app.graph._nodes_by_id
	let node = nodes[parseInt(event.detail.node_id)]
	if(node) {
        const w = node.widgets.find((w) => 'content' === w.name)
		if(w) {
			w.value = event.detail.historyStack[event.detail.historyStack.length + parseInt(event.detail.lastPromptIndex)]
		}
	}
}

api.addEventListener("update-history-stack", nodeFeedbackHandler);

app.registerExtension({ 
	name: "prmopt.history.extention",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "PromptHistory") {
            // Modify nodeType before registration

            // const onConfigure = nodeType.prototype.onConfigure;
            // nodeType.prototype.onConfigure = function() {
            //     onConfigure?.apply(this, arguments)
            // }

            const onPropertyChanged = nodeType.prototype.onPropertyChanged
            nodeType.prototype.onPropertyChanged = function (property, value, prevValue) {
                console.log(5555,property, value, prevValue)
                onPropertyChanged?.apply(this, arguments)
                // if (this.widgets) {
				// 	const pos = this.widgets.findIndex((w) => w.name === "content2");
				// 	if (pos !== -1) {
				// 		for (let i = pos; i < this.widgets.length; i++) {
				// 			this.widgets[i].onRemove?.();
				// 		}
				// 		this.widgets.length = pos;
				// 	}
				// }
                // const resp = await api.fetchApi("/promptHistory/historyStack", { cache: "no-store" });
                // const data = JSON.stringify(resp)

                if (this.widgets) {
                    const pos = this.widgets.findIndex((w) => w.name === "content");
                    if (pos !== -1) {
                        for (let i = pos; i < this.widgets.length; i++) {
                            this.widgets[i].onRemove?.();
                        }
                        this.widgets.length = pos;
                    }
                }
				const w = ComfyWidgets["STRING"](this, "content", ["STRING", { multiline: true }], app).widget;
				w.inputEl.readOnly = true;
				w.inputEl.style.opacity = 0.6;
				w.value = [property, value, prevValue].join(" | "); // data;
            }
            
            const onExecuted = nodeType.prototype.onExecuted
            // nodeType.prototype.onExecuted = function (message) {
            //     onExecuted?.apply(this, arguments)
            //     console.log(this, message)
            //     // const resp = await api.fetchApi("/promptHistory/historyStack", { cache: "no-store" });
            //     // const data = JSON.stringify(resp)
            //     if (this.widgets) {
            //         const pos = this.widgets.findIndex((w) => w.name === "content");
            //         if (pos !== -1) {
            //             for (let i = pos; i < this.widgets.length; i++) {
            //                 this.widgets[i].onRemove?.();
            //             }
            //             this.widgets.length = pos;
            //         }
            //     }
			// 	const w = ComfyWidgets["STRING"](this, "content", ["STRING", { multiline: true }], app).widget;
			// 	w.inputEl.readOnly = true;
			// 	w.inputEl.style.opacity = 0.6;
			// 	w.value = message; // data;
            // }
        }
    }
})