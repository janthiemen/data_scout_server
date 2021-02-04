import * as React from "react";
import autobind from 'class-autobind';
import { HTMLSelect, FormGroup, Button, Dialog, MultistepDialog, Classes, Intent, InputGroup, TextArea, Card, Elevation, ControlGroup } from "@blueprintjs/core";
import { Grid, Row, Col } from 'react-flexbox-grid';
import { DefaultItem, DefaultSelect, defaultSelectSettings } from "../../helpers/select";

import { JoinService } from "../../helpers/userService";


interface JoinDialogProps {
    onClose: () => void,
    joinService: JoinService,
    isOpen: boolean,
}

interface JoinDialogState {
    onClose: () => void,
    isOpen: boolean,
    left: DefaultItem,
    left_type: string,
    right: DefaultItem,
    right_type: string,
}

export class JoinDialog extends React.Component<JoinDialogProps, JoinDialogState> {
    private joinService: JoinService;

    constructor(props: JoinDialogProps) {
        super(props);
        this.joinService = props.joinService;
        autobind(this);
        this.state = {
            isOpen: props.isOpen,
            onClose: props.onClose,
            left: null,
            left_type: "data_source",
            right: null,
            right_type: "data_source",
        };
    }

    /**
     * Called when new props are received.
     * @param props The new props
     */
    componentWillReceiveProps(props: JoinDialogProps) {
        this.setState({
            isOpen: props.isOpen,
            onClose: props.onClose,
        });
    }

    /**
     * Saves the join.
     */
    private save() {
        // TODO
    }

    /**
     * Set the parent of an item or folder (i.e. move it).
     */
    public selectItem(item: DefaultItem) {
        console.log(item);
    }

    /**
     * Set the parent of an item or folder (i.e. move it).
     */
    public onInputTypeChange(event: React.ChangeEvent<HTMLSelectElement>) {
        console.log(event.target.value);
    }

    /**
     * Renders transformation dialog.
     * @returns  
     */
    render() {
        let recipeItems: DefaultItem[] = [{ title: "a", id: 1, label: "" }, { title: "b", id: 2, label: "" }, { title: "c", id: 3, label: "" }]

        return <MultistepDialog icon="info-sign" title={"Join"} {...this.state}>
            <div className={Classes.DIALOG_BODY}>
                <Grid fluid>
                    <Row>
                        <Col md={6}>
                            <FormGroup label="Left" labelFor="input" labelInfo="(required)" helperText="What should be on the left side?">
                                <ControlGroup>
                                    <HTMLSelect value={this.state.left_type} onChange={this.onInputTypeChange}>
                                        <option>Data source</option>
                                        <option>Pipeline</option>
                                    </HTMLSelect>
                                    <DefaultSelect {...defaultSelectSettings} items={recipeItems} onItemSelect={this.selectItem}>
                                        <Button icon="database" rightIcon="caret-down" text={this.state.left ? `${this.state.left}` : "(No selection)"} />
                                    </DefaultSelect>
                                </ControlGroup>
                            </FormGroup>
                        </Col>
                        <Col md={6}>
                            <FormGroup label="Right" labelFor="input" labelInfo="(required)" helperText="What should be on the right side?">
                                <DefaultSelect {...defaultSelectSettings} items={recipeItems} onItemSelect={this.selectItem}>
                                    <Button icon="database" rightIcon="caret-down" text={this.state.left ? `${this.state.left}` : "(No selection)"} />
                                </DefaultSelect>
                            </FormGroup>
                        </Col>
                    </Row>
                </Grid>

            </div>
            <div className={Classes.DIALOG_FOOTER}>
                <Button intent={Intent.PRIMARY} onClick={this.save}>Save</Button>
            </div>
        </MultistepDialog>
    }
}
