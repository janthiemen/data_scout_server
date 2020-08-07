import * as React from "react";
import { Transformation, TRANSFORMATIONS, transformationMakeTitle } from "./Transformation"
import { HTMLSelect, FormGroup, Button, Dialog, Classes, Intent, InputGroup } from "@blueprintjs/core";
import { WranglerService } from "../../helpers/userService";
import { ColumnsSelect } from "./ColumnsSelect"


interface TransformationDialogProps {
    onClose: () => void,
    transformation: Transformation,
    setTransformation: () => void,
    wranglerService: WranglerService,
    isOpen: boolean,
    columns: string[]
}

interface TransformationDialogState {
    onClose: () => void,
    transformation: Transformation,
    fieldValues: { [key: string]: any },
    isOpen: boolean,
    columns: string[]
}

export class TransformationDialog extends React.Component<TransformationDialogProps, TransformationDialogState> {
    private setTransformation: () => void;
    private wranglerService: WranglerService;

    constructor(props: TransformationDialogProps) {
        super(props);
        console.log(props);
        this.setTransformation = props.setTransformation;
        this.wranglerService = props.wranglerService;
        this.state = {
            transformation: props.transformation,
            isOpen: props.isOpen,
            fieldValues: JSON.parse(props.transformation.kwargs),
            onClose: props.onClose,
            columns: props.columns
        };
        this.onValueChange = this.onValueChange.bind(this);
        this.onInputChange = this.onInputChange.bind(this);
        this.save = this.save.bind(this);
        this.finishUpdate = this.finishUpdate.bind(this);
    }

    /**
     * Called when new props are received.
     * @param props The new props
     */
    componentWillReceiveProps(props: TransformationDialogProps) {
        this.setState({
            transformation: props.transformation,
            fieldValues: JSON.parse(props.transformation.kwargs),
            isOpen: props.isOpen,
            columns: props.columns
        });
    }

    /**
     * Update the field's value on change.
     * @param field The field that was updated
     * @param value The new value
     */
    private onValueChange(field: string, value: any) {
        let fieldValues = this.state.fieldValues;
        fieldValues[field] = value;
        this.setState({ fieldValues: fieldValues });
    }

    /**
     * Called when an input (text or select) has been changed.
     * @param e The event
     */
    private onInputChange(e: React.ChangeEvent<HTMLSelectElement | HTMLInputElement>) {
        if (e.target.dataset["field"] !== undefined) {
            this.onValueChange(e.target.dataset["field"], e.target.value);
        }
    }

    /**
     * Saves the transformation.
     */
    private save() {
        let transformation = this.state.transformation;
        transformation.kwargs = JSON.stringify(this.state.fieldValues);
        this.setState({ transformation: transformation });
        if (this.state.transformation.id > 0) {
            this.wranglerService.putTransformation(this.state.transformation.id, transformation, this.finishUpdate)
        } else {
            // If the ID is below zero it means it doesn't exist yet.
            this.wranglerService.postTransformation(transformation, this.finishUpdate)
        }
    }

    /**
     * Finishes update
     * @param body The response body
     */
    private finishUpdate(body: {}) {
        this.setTransformation();
        this.state.onClose();
    }

    /**
     * Renders an input field for a certain field.
     * @param key The key
     * @param field The field
     * @returns  
     */
    renderFieldInput(key: string, field: { [key: string]: any }) {
        let field_values = JSON.parse(this.state.transformation.kwargs);

        if (field["input"] === "column" && field["multiple"]) {
            return <ColumnsSelect value={field_values[key]} columns={this.state.columns} field={key} onValueChange={this.onValueChange} />
        } else if (field["input"] === "column") {
            return <HTMLSelect value={this.state.fieldValues[key]} id={`transformation-input-${key}`} data-field={key} onChange={this.onInputChange} key={`transformation-input-${key}`}>
                <option></option>
                {this.state.columns.map(column => <option id={column} key={`transformation-input-${key}-option-${column}`}>{column}</option>)}
            </HTMLSelect>
        } else if (field["input"] === "select") {
            return <HTMLSelect value={this.state.fieldValues[key]} id={`transformation-input-${key}`} data-field={key} onChange={this.onInputChange} key={`transformation-input-${key}`}>
                <option></option>
                {Object.keys(field["options"]).map(option => <option value={option}>{field["options"][option]}</option>)}
            </HTMLSelect>
        } else if (field["input"] === "text") {
            return <InputGroup value={this.state.fieldValues[key]} key={`transformation-input-${key}`} data-field={key} onChange={this.onInputChange} id={`transformation-input-${key}`} />
        }
    }

    /**
     * Renders a field
     * @param key The key
     * @param field The field
     * @returns  
     */
    renderField(key: string, field: { [key: string]: any }) {
        return <FormGroup
            helperText={field["help"]}
            label={field["name"]}
            labelFor={`transformation-input-${key}`}
            key={`transformation-label-${key}`}
            labelInfo={field["required"] ? "(required)" : ""}
        >
            {this.renderFieldInput(key, field)}
        </FormGroup>

    }

    /**
     * Renders transformation dialog.
     * @returns  
     */
    render() {
        let transformation_meta = TRANSFORMATIONS[this.state.transformation.transformation]
        console.log(transformation_meta);
        console.log(this.state.fieldValues);
        let title = transformationMakeTitle(this.state.transformation);
        return <Dialog icon="info-sign" title={title} {...this.state}>
            <div className={Classes.DIALOG_BODY}>
                {Object.keys(transformation_meta["fields"]).map((key, index) => this.renderField(key, transformation_meta["fields"][key]))}
            </div>
            <div className={Classes.DIALOG_FOOTER}>
                <Button intent={Intent.PRIMARY} onClick={this.save}>Save</Button>
            </div>
        </Dialog>
    }

}
