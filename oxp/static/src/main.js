import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { Page, WebClient } from "./web_client";

const config = {
    dev: true,
    name: "OXP Hello Everyone",
};

// Mount the Playground component when the document.body is ready
whenReady(() => mountComponent(WebClient, document.body, config));
