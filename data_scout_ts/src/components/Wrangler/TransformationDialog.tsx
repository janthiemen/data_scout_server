import * as React from "react";
import autobind from 'class-autobind';
import { Transformation, TRANSFORMATIONS, transformationMakeTitle } from "./Transformation"
import { HTMLSelect, FormGroup, Button, Dialog, Classes, Intent, InputGroup, NumericInput, TextArea, Card, Elevation } from "@blueprintjs/core";
import { WranglerService } from "../../helpers/userService";
import { ColumnsSelect } from "./ColumnsSelect"
import { NumberInput } from "./NumberInput"; 


interface TransformationDialogProps {
    onClose: () => void,
    transformation: Transformation,
    setTransformation: () => void,
    wranglerService: WranglerService,
    isOpen: boolean,
    columns: { [key: string]: string}
}

interface TransformationDialogFieldSetProps {
    onFieldChange: (field: string, value: any) => void,
    fieldName: string,
    fields: { [key: string]: any },
    fieldValues: { [key: string]: any },
    columns: { [key: string]: string}
}

interface TransformationDialogState {
    onClose: () => void,
    transformation: Transformation,
    fieldValues: { [key: string]: any },
    isOpen: boolean,
    columns: { [key: string]: string}
}

interface TransformationDialogFieldSetState {
    fields: { [key: string]: any },
    fieldValues: { [key: string]: any },
    columns: { [key: string]: string}
}

class TransformationDialogFieldSet extends React.Component<TransformationDialogFieldSetProps, TransformationDialogFieldSetState> {
    protected onFieldChange: (field: string, value: any) => void;
    protected fieldName: string;

    constructor(props: TransformationDialogFieldSetProps) {
        super(props);
        autobind(this);
        this.state = {
            fields: props.fields,
            fieldValues: props.fieldValues,
            columns: props.columns
        };
        this.fieldName = props.fieldName;
        this.onFieldChange = props.onFieldChange;
    }

    /**
     * Called when new props are received.
     * @param props The new props
     */
    componentWillReceiveProps(props: TransformationDialogFieldSetProps) {
        this.setState({
            fields: props.fields,
            fieldValues: props.fieldValues,
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
        this.onFieldChange(this.fieldName, {});
    }

    /**
     * Called when an input (text or select) has been changed.
     * @param e The event
     */
    private onInputChange(e: React.ChangeEvent<HTMLSelectElement | HTMLInputElement | HTMLTextAreaElement>) {
        if (e.target.dataset["field"] !== undefined) {
            this.onValueChange(e.target.dataset["field"], e.target.value);
        }
    }

    private onNumericValueChange(valueAsNumber: number, valueAsString: string, e: React.ChangeEvent<HTMLSelectElement | HTMLInputElement>) {
        if (e.target.dataset["field"] !== undefined) {
            this.onValueChange(e.target.dataset["field"], valueAsNumber);
        }
    }

    /**
     * Renders an input field for a certain field.
     * @param key The key
     * @param field The field
     * @returns  
     */
    renderFieldInput(key: string, field: { [key: string]: any }) {
        // let field_values = JSON.parse(this.state.transformation.kwargs);
        if (field["input"] === "column" && field["multiple"]) {
            return <ColumnsSelect value={this.state.fieldValues[key]} columns={this.state.columns} columnType={field["column_type"]} field={key} onValueChange={this.onValueChange} />
        } else if (field["input"] === "column") {
            // TODO: Add filter on column type!
            return <HTMLSelect value={this.state.fieldValues[key]} id={`transformation-input-${key}`} data-field={key} onChange={this.onInputChange} key={`transformation-input-${key}`}>
                <option></option>
                {Object.keys(this.state.columns).map((column: string) => {
                    if (!("column_type" in field) || field["column_type"].indexOf(this.state.columns[column]) !== -1) {
                        return <option id={column} key={`transformation-input-${key}-option-${column}`}>{column}</option>
                    }
                })}
                {/* {Object.keys(this.state.columns).map(column => <option id={column} key={`transformation-input-${key}-option-${column}`}>{column}</option>)} */}
            </HTMLSelect>
        } else if (field["input"] === "select") {
            return <HTMLSelect value={this.state.fieldValues[key]} id={`transformation-input-${key}`} data-field={key} onChange={this.onInputChange} key={`transformation-input-${key}`}>
                <option></option>
                {Object.keys(field["options"]).map(option => <option value={option}>{field["options"][option]}</option>)}
            </HTMLSelect>
        } else if (field["input"] === "text") {
            return <InputGroup value={this.state.fieldValues[key]} key={`transformation-input-${key}`} data-field={key} onChange={this.onInputChange} id={`transformation-input-${key}`} />
        } else if (field["input"] === "text-area") {
            return <TextArea key={`transformation-input-${key}`} data-field={key} id={`transformation-input-${key}`} growVertically={true} large={true} onChange={this.onInputChange} value={this.state.fieldValues[key]} />
        } else if (field["input"] === "number") {
            // return <NumericInput min={0} minorStepSize={1} value={this.state.fieldValues[key]} key={`transformation-input-${key}`} data-field={key} onValueChange={this.onNumericValueChange} id={`transformation-input-${key}`} />
            return <NumberInput field={key} value={this.state.fieldValues[key]} onValueChange={this.onValueChange} />
        }
    }

    multipleAddRow(field: string) {
        // Initialize the kwargs with their default values
        let values: {[key: string]: any} = {};
        for (let [key, value] of Object.entries(this.state.fields[field]["sub_fields"])) {
            values[key] = value["default"];
        }
        let fieldValues = this.state.fieldValues;
        fieldValues[field].push(values);
        this.setState({ fieldValues: fieldValues });
    }

    multipleDeleteRow(field: string, index: number) {
        let fieldValues = this.state.fieldValues;
        fieldValues[field].splice(index, 1);
        this.setState({ fieldValues: fieldValues });
    }

    /**
     * Renders a field
     * @param key The key
     * @param field The field
     * @returns  
     */
    renderField(key: string, field: { [key: string]: any }) {
        let that = this;
        if ("optional" in field) {
            for (let optional_field in field["optional"]) {
                if (field["optional"][optional_field].indexOf(this.state.fieldValues[optional_field]) == -1) {
                    return;
                }
            }
        }

        if (field["input"] === "multiple") {
            return <div>
                <Button onClick={() => that.multipleAddRow(key)}>Add</Button>
                {this.state.fieldValues[key].map((subKey, i) => 
                    <Card interactive={false} elevation={Elevation.ONE} className="input-multiple-card">
                        <TransformationDialogFieldSet 
                            onFieldChange={that.onFieldChange} 
                            fieldName={""} 
                            fields={that.state.fields[key]["sub_fields"]} 
                            fieldValues={that.state.fieldValues[key][i]} 
                            columns={that.state.columns} />
                        <Button intent={Intent.DANGER} rightIcon="delete" onClick={() => that.multipleDeleteRow(key, i)}>Delete</Button>
                    </Card>
                )}
                </div>
        } else {
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
    }

    /**
     * Renders transformation dialog.
     * @returns  
     */
    render() {
        return <div className="transformation-dialog-fields">
                {Object.keys(this.state.fields).map((key, index) => this.renderField(key, this.state.fields[key]))}
            </div>
    }
}

export class TransformationDialog extends React.Component<TransformationDialogProps, TransformationDialogState> {
    private setTransformation: () => void;
    private wranglerService: WranglerService;

    constructor(props: TransformationDialogProps) {
        super(props);
        this.setTransformation = props.setTransformation;
        this.wranglerService = props.wranglerService;
        this.state = {
            transformation: props.transformation,
            isOpen: props.isOpen,
            fieldValues: JSON.parse(props.transformation.kwargs),
            onClose: props.onClose,
            columns: props.columns
        };
        this.onFieldChange = this.onFieldChange.bind(this);
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

    onFieldChange(key: string, value: any) {
        // TODO: Check if we actually need this ...
    }

    /**
     * Renders transformation dialog.
     * @returns  
     */
    render() {
        let transformation_meta = TRANSFORMATIONS[this.state.transformation.transformation]
        let title = transformationMakeTitle(this.state.transformation);
        return <Dialog icon="info-sign" title={title} {...this.state}>
            <div className={Classes.DIALOG_BODY}>
                <TransformationDialogFieldSet 
                    onFieldChange={this.onFieldChange} 
                    fieldName={""} 
                    fields={transformation_meta["fields"]} 
                    fieldValues={this.state.fieldValues} 
                    columns={this.state.columns} />
                {/* {Object.keys(transformation_meta["fields"]).map((key, index) => this.renderField(key, transformation_meta["fields"][key]))} */}
            </div>
            <div className={Classes.DIALOG_FOOTER}>
                <Button intent={Intent.PRIMARY} onClick={this.save}>Save</Button>
            </div>
        </Dialog>
    }
}
