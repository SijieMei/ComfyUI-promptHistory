import { app } from "../../scripts/app.js"

app.registerExtension({ 
	name: "prmopt.history.extention",
	async setup() { 
		alert("Setup complete!")
	},
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeType.ComfyClass=="PromptHistory") { 
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function (side,slot,connect,link_info,output) {     
                const r = onConnectionsChange?.apply(this, arguments);   
                console.log("Someone changed my connection!");
                return r;
            }
        }
    }
})