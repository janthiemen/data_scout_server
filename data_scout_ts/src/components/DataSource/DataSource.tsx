import * as React from "react";
import autobind from 'class-autobind';

import {
    MenuItem, IProps, IToastProps, Intent, 
    FormGroup, InputGroup, NumericInput, Switch, Button, FileInput, ControlGroup, Toaster, ProgressBar
} from "@blueprintjs/core";

import { Select, ItemRenderer, ItemPredicate } from "@blueprintjs/select";

import { DataSourceService } from "../../helpers/userService";
import { highlightText } from "../../helpers/select";
import { DataSource, newDataSource } from "./DataSources";


export class DataSourceType {
    name: string;
    fields: [];
}

/**
 * Render a data source in the select menu.
 * @param item The item to render
 * @param param1 ItemRenderer params
 */
const dataSourceTypeRenderer: ItemRenderer<DataSourceType> = (item, { handleClick, modifiers, query }) => {
    if (!modifiers.matchesPredicate) {
        return null;
    }
    const text = `${item.name}`;
    return (
        <MenuItem
            active={modifiers.active}
            disabled={modifiers.disabled}
            key={item.name}
            onClick={handleClick}
            text={highlightText(text, query)}
        />
    );
};

/**
 * Filter the data sources based on a query.
 * @param query The query to search for
 * @param item The item to check
 * @param _index The index
 * @param exactMatch Whether to look for an exact match or not
 */
const dataSourceTypeFilterer: ItemPredicate<DataSourceType> = (query, item, _index, exactMatch) => {
    const normalizedTitle = item.name.toLowerCase();
    const normalizedQuery = query.toLowerCase();

    if (exactMatch) {
        return normalizedTitle === normalizedQuery;
    } else {
        return `${normalizedTitle}`.indexOf(normalizedQuery) >= 0;
    }
};

/**
 * Data source props
 */
interface DataSourceProps extends IProps {
    dataSourceService: DataSourceService,
    addToast: (toast: IToastProps, key?: string) => string;
    getToaster: () => Toaster;
    updateDataSources: () => void;
    dataSourceType?: DataSourceType,
    dataSource: DataSource,
    types: DataSourceType[]
}

/**
 * Data source state
 */
interface DataSourceState {
    dataSource: DataSource,
    dataSourceType?: DataSourceType,
    fieldValues: { [key: string]: any },
    types: DataSourceType[];
}

/**
 * This class represents a data source object.
 */
export class DataSourceComponent extends React.Component<DataSourceProps, DataSourceState> {
    private dataSourceService: DataSourceService;
    private addToast: (toast: IToastProps, key?: string) => string;
    private getToaster: () => Toaster;
    private updateDataSources: () => void;
    private submitProgress = {
        "step": 0,
        "total_steps": 0,
        "key": undefined
    }
    private fileUploadQueue: {}[] = [];
    public state: DataSourceState = {
        dataSource: newDataSource(),
        dataSourceType: undefined,
        fieldValues: {},
        types: []
    }

    /**
     * Construct a new data source.
     * @param props The props
     */
    constructor(props: DataSourceProps) {
        super(props);
        autobind(this);
        this.dataSourceService = props.dataSourceService;
        this.updateDataSources = props.updateDataSources;
        this.addToast = props.addToast;
        this.getToaster = props.getToaster;
    }

    /**
     * Update the field vales in the state.
     */
    private updateFields() {
        let fields = this.getFields()
        let kwargs = this.state.dataSource.kwargs;

        let fieldValues: { [key: string]: string|{} } = {};
        for (let key in fields) {
            if (fields[key]["type"] === "file") {
                fieldValues[key] = {"id": key in kwargs && kwargs[key] !== null ? kwargs[key] : -1, "file": null};
            } else {
                fieldValues[key] = key in kwargs ? kwargs[key] : "";
            }
        }
        this.setState({ fieldValues: fieldValues })
    }

    /**
     * Called when new props are received.
     * @param props The new props
     */
    componentWillReceiveProps(props: DataSourceProps) {
        this.setState({
            dataSource: props.dataSource,
            dataSourceType: props.types.filter(item => item.name === props.dataSource.source)[0],
            types: props.types
        });
    }

    /**
     * Called when the state or the props are update. Currently only used to repopulate the field values.
     * @param prevProps The old props
     * @param prevState The old state
     */
    public componentDidUpdate(prevProps: DataSourceProps, prevState: DataSourceState) {
        if (this.state.dataSourceType !== prevState.dataSourceType || 
            this.state.dataSource !== prevState.dataSource) {
            // The data source has updated, so we ought to update the field values
            this.updateFields();
        }
    }

    /**
     * Get the fields that the current data source has.
     */
    private getFields(): { [key: string]: any } {
        return this.state.dataSourceType !== undefined ? this.state.dataSourceType.fields : {};
    }

    /**
     * Change the data source type.
     * @param newType The new type
     */
    private setType(newType: DataSourceType) {
        this.setState({ dataSourceType: newType });
    }

    /**
     * Update a field value, given a change event.
     * @param event The change event
     */
    private updateFieldValue(event: React.ChangeEvent<HTMLInputElement>) {
        let fieldValues = this.state.fieldValues;
        let fields = this.getFields();
        if (fields[event.target.id]["type"] === "boolean") {
            fieldValues[event.target.id] = event.target.checked;
        } else if (fields[event.target.id]["type"] === "file") {
            fieldValues[event.target.id]["file"] = event.target.files[0];
        } else {
            fieldValues[event.target.id] = event.target.value;
        }
        this.setState({ fieldValues: fieldValues });
    }

    /**
     * Updates the name in the state
     * @param event 
     */
    private updateName(event: React.ChangeEvent<HTMLInputElement>) {
        let dataSource = this.state.dataSource;
        dataSource.name = event.target.value;
        this.setState({ dataSource: dataSource });
    }

    /**
     * Submits the data source
     */
    private submitDataSource(event: React.SyntheticEvent) {
        if (event !== null) {
            event.preventDefault();
        }

        if (this.state.dataSourceType !== undefined) {
            let fields = this.getFields();
            let kwargs: { [key: string]: any } = {};

            // Check if there are file to be uploaded, if so, put them in the queue
            this.fileUploadQueue = [];
            for (let [key, fieldValue] of Object.entries(this.state.fieldValues)) {
                // TODO: On loading of the kwargs, replace the id in a file field by an object {"id": X, "file": null}
                if (fields[key]["type"] == "file" && fieldValue["file"] !== null) {
                    this.fileUploadQueue.push({"key": key, "id": fieldValue["id"], "file": fieldValue["file"]});
                }
            }

            this.submitProgress["step"] = -1;
            this.submitProgress["key"] = undefined;
            if (this.state.dataSource.id === -1 && this.fileUploadQueue.length > 0) {
                // Here we've got fileUploadQueue.length + 2 steps
                this.submitProgress["total_steps"] = this.fileUploadQueue.length + 2;
                this.renderProgress();
                // Upload the data source, without kwargs
                this.doSubmitDataSource({});
            } else if (this.fileUploadQueue.length > 0) {
                this.submitProgress["total_steps"] = this.fileUploadQueue.length + 1;
                this.renderProgress();
                this.uploadFile();
            } else {
                this.submitProgress["total_steps"] = 1;
                this.renderProgress();
                this.finalSubmitDataSource();
            }

        } else {
            this.addToast({ intent: Intent.WARNING, message: "Please select a data source type first." });
        }
    }

    private finalSubmitDataSource() {
        let fields = this.getFields();
        let kwargs: { [key: string]: any } = {};
        for (let [key, fieldValue] of Object.entries(this.state.fieldValues)) {
            if (fields[key]["type"] != "file") {
                kwargs[key] = fieldValue;
            } else {
                kwargs[key] = fieldValue["id"];
            }
        }
        this.doSubmitDataSource(kwargs);
    }

    private doSubmitDataSource(kwargs) {
        let data = {
            id: this.state.dataSource.id,
            name: this.state.dataSource.name,
            source: this.state.dataSourceType.name,
            kwargs: JSON.stringify(kwargs)
        }
        this.dataSourceService.save(data, this.finishSubmit);
    }

    /**
     * Handle the submit return
     * @param body 
     */
    private finishSubmit(body: {}) {
        if ("id" in body) {
            this.renderProgress();
            // There is an ID in there, so we'll set the current ID
            let dataSource = this.state.dataSource;
            dataSource.id = body["id"];
            this.setState({ dataSource: dataSource });
            // TODO: Add some sort of progress bar for uploading
            if (this.fileUploadQueue.length == 0) {
                this.updateDataSources();
            } else {
                this.uploadFile();
            }
        } else {
            this.addToast({ intent: Intent.WARNING, message: "Couldn't save the data source." });
        }
    }

    private createUserFile(key: string) {
        this.dataSourceService.saveFile({"data_source": this.state.dataSource.id, "field_name": key}, this.doUploadFile);
    }

    private uploadFile() {
        if (this.fileUploadQueue.length == 0) {
            this.finalSubmitDataSource();
        } else {
            let key = this.fileUploadQueue[this.fileUploadQueue.length-1]["key"];
            if (this.state.fieldValues[key]["id"] === -1) {
                this.createUserFile(key);
            } else {
                this.doUploadFile({"id": this.state.fieldValues[key]["id"], "field_name": key});
            }
        }
    }

    private doUploadFile(body: {}) {
        if ("id" in body) {
            this.renderProgress();
            let uploading = this.fileUploadQueue[this.fileUploadQueue.length-1];
            let fieldValues = this.state.fieldValues;
            fieldValues[uploading["key"]]["id"] = body["id"];
            this.setState({fieldValues: fieldValues});
            this.dataSourceService.uploadFile(uploading["file"], body["id"], this.finishUploadFile);
        } else {
            this.addToast({ intent: Intent.DANGER, message: "There was an error while uploading the file." });
        }
    }

    private finishUploadFile(body: {}) {
        if ("id" in body) {
            let uploading = this.fileUploadQueue.pop();
            let fieldValues = this.state.fieldValues;
            fieldValues[uploading["key"]]["file"] = null;
            this.setState({fieldValues: fieldValues});
            this.uploadFile();
        } else {
            this.addToast({ intent: Intent.DANGER, message: "There was an error while uploading the file." });
        }
    }

    private renderProgress() {
        this.submitProgress["step"]++;
        this.submitProgress["key"] = this.addToast({
            icon: "cloud-upload",
            message: (
                <ProgressBar
                    intent={this.submitProgress["step"] < this.submitProgress["total_steps"] ? Intent.PRIMARY : Intent.SUCCESS}
                    value={this.submitProgress["step"] / this.submitProgress["total_steps"]}
                />
            ),
            timeout: this.submitProgress["step"] < this.submitProgress["total_steps"] ? 0 : 2000,
        }, this.submitProgress["key"])
    }


    /**
     * Render a specific field.
     * @param key The key of the field
     * @param field The field
     */
    private renderField(key: string, field: { [key: string]: any }) {
        let paramsFormGroup = {
            "key": key,
            "helperText": field.help,
            "labelFor": key,
            "labelInfo": field.required ? "(required)" : ""
        }

        switch (field["type"]) {
            case "string":
                return <FormGroup {...paramsFormGroup} label={field.name}>
                    <InputGroup id={key} value={this.state.fieldValues[key]} onChange={this.updateFieldValue} />
                </FormGroup>
            case "number":
                return <FormGroup {...paramsFormGroup} label={field.name}>
                    <NumericInput id={key} min={field.min} max={field.max} value={this.state.fieldValues[key]} onChange={this.updateFieldValue} />
                </FormGroup>
            case "boolean":
                return <FormGroup {...paramsFormGroup}>
                    <Switch id={key} checked={this.state.fieldValues[key]} label={field.name} onChange={this.updateFieldValue} />
                </FormGroup>
            case "file":
                let title = "Choose file...";
                let downloadLink = false;
                if (this.state.fieldValues[key] !== undefined) {
                    if (this.state.fieldValues[key]["file"] !== null) {
                        title = this.state.fieldValues[key]["file"].name;
                    }
                    if (this.state.fieldValues[key]["id"] !== -1) {
                        downloadLink = true;
                    }
                }

                return <div>
                        <FormGroup {...paramsFormGroup}>
                            <ControlGroup>
                            <Button disabled={!downloadLink} onClick={() => this.dataSourceService.downloadUserFile(this.state.fieldValues[key]["id"])}>
                                Download current file
                            </Button>
                            <FileInput text={title} fill inputProps={{"id": key}} onInputChange={this.updateFieldValue} />
                            </ControlGroup>
                        </FormGroup>
                    </div>
            default:
                return <FormGroup {...paramsFormGroup} label={field.name}>
                    <InputGroup id={key} value={this.state.fieldValues[key]} onChange={this.updateFieldValue} />
                </FormGroup>
        }
    }

    /**
     * Render a data source, including a type selector and a name field, as well as the required data source specific fields.
     */
    render() {
        let fields = this.getFields();
        const DataSourceTypeSelect = Select.ofType<DataSourceType>();

        return <form onSubmit={this.submitDataSource}>
            <DataSourceTypeSelect
                itemPredicate={dataSourceTypeFilterer}
                itemRenderer={dataSourceTypeRenderer}
                items={this.state.types}
                noResults={<MenuItem disabled={true} text="No results." />}
                onItemSelect={this.setType}
            >
                <Button icon="database" rightIcon="caret-down" text={this.state.dataSourceType ? `${this.state.dataSourceType.name}` : "(No selection)"}
                />
            </DataSourceTypeSelect>
            <FormGroup label="Name" labelFor="name" labelInfo="(required)" helperText="The human readable name of the data source">
                <InputGroup id="name" placeholder="Placeholder text" onChange={this.updateName} value={this.state.dataSource.name} />
            </FormGroup>

            {Object.keys(fields).map((key: string) => this.renderField(key, fields[key]))}

            <Button type="submit" icon="floppy-disk" text="Save" disabled={this.state.dataSourceType === undefined} intent={Intent.SUCCESS} />
        </form>
    }
}
