import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { Page } from "./page/page";

const config = {
    dev: true,
    name: "Owl Tutorial",
};

// Mount the Playground component when the document.body is ready
whenReady(() => mountComponent(Page, document.body, config));
