import { Component ,useProps} from "@odoo/owl";

export class Card extends Component{
    static template='awesome_owl.card';
    setup() {
        this.props = useProps();
    }
}

    