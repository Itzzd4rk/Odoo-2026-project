/** @odoo-module **/
import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class EsgDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({ loaded: false, kpis: { leaders: [] } });
        onWillStart(async () => {
            this.state.kpis = await this.orm.call("esg.dashboard", "get_kpis", []);
            this.state.loaded = true;
        });
    }
}
EsgDashboard.template = "esg_management.EsgDashboard";
registry.category("actions").add("esg_management.dashboard", EsgDashboard);
