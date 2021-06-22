import * as React from "react";
import autobind from 'class-autobind';
import { Dialog, Classes, Button, Intent } from "@blueprintjs/core";
import { WranglerService } from "../../helpers/userService";


interface ExportDialogProps {
    wranglerService: WranglerService;
    recipe: number;
    isOpen: boolean;
    close: () => void;
}
interface ExportDialogState {
    recipe: number;
    isOpen: boolean;
    definition: string;
}

/**
 * This dialog allows the user to download the code for their pipeline.
 */
export class ExportDialog extends React.Component<ExportDialogProps, ExportDialogState> {
    private wranglerService: WranglerService;
    private close: () => void;

    constructor(props: ExportDialogProps) {
        super(props);
        autobind(this);
        this.wranglerService = props.wranglerService;
        this.close = props.close;
        this.state = {
            recipe: props.recipe,
            isOpen: props.isOpen,
            definition: ""
        };
        this.wranglerService.getDefinition(props.recipe, this.receiveDefinition)
    }

    /**
     * Called when new props are received.
     * @param props The new props
     */
    componentWillReceiveProps(props: ExportDialogProps) {
        this.setState({
            recipe: props.recipe,
            isOpen: props.isOpen
        });
    }

    /**
     * Callback when the definition is available.
     * @param body 
     */
    private receiveDefinition(body: {}) {
        this.setState({ definition: JSON.stringify(body, null, 2) })
    }

    /**
     * Request the code for the pipeline definition from the server.
     */
    private downloadCode() {
        this.wranglerService.downloadCode(this.state.recipe);
    }

    /**
     * Renders export dialog.
     * @returns  
     */
    render() {
        return <Dialog icon="data-lineage" title="Pipeline definition" isOpen={this.state.isOpen} onClose={this.close}>
            <div className={Classes.DIALOG_BODY}>
                <Button fill outlined intent={Intent.SUCCESS} onClick={this.downloadCode}>Download Python</Button>
                <pre className="code-block">
                    {this.state.definition}
                </pre>
            </div>
        </Dialog>
    }
}
