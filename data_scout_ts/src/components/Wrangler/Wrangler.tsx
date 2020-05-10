import * as React from "react";

// import { ISortableColumn } from "./AbstractSortableColumn";
import { DataColumn } from "./DataColumn"
import { PageProps } from "../../helpers/props";
import { Row, Col, Grid } from "react-flexbox-grid";
import { DataTable } from "./DataTable";
import { Tabs, Tab, H3, HTMLSelect, FormGroup, Drawer, Position, IProps, Button, ButtonGroup, Dialog, Classes, Intent, MenuItem, InputGroup, IToastProps, Popover, Tooltip, Alert, HTMLTable } from "@blueprintjs/core";
import { WranglerService } from "../../helpers/userService";
import { ItemPredicate, ItemRenderer, MultiSelect } from "@blueprintjs/select";
import { copyFile } from "fs";
import { ReactSortable, Sortable, SortableEvent } from "react-sortablejs";

interface TransformationMeta {
    title: string
    fields: { [key: string]: { [key: string]: any } },
}

const DUMMY_DATA = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]];
const DUMMY_COLUMNS = ["Loading", "Loading", "Loading", "Loading"]

const TRANSFORMATIONS: { [key: string]: TransformationMeta } = {
    "convert": {
        "title": "Convert {field} to {to}",
        "fields": {
            "field": {
                "name": "Column", "type": "string", "help": "The field to convert", "required": true,
                "input": "column", "multiple": false
            },
            "to": {
                "name": "To", "type": "string", "help": "To which data type to convert", "required": true,
                "input": "select", "multiple": false,
                "options": { "int": "Integer", "float": "Floating point number", "string": "Text" }
            }
        }
    },
    "add": {
        "title": "Sum {fields}",
        "fields": {
            "fields": {
                "name": "Columns", "type": "list<string>", "help": "The fields to add to each other",
                "required": true, "input": "column", "multiple": true
            },
            "output": {
                "name": "Output column", "type": "string", "input": "text", "required": true,
                "help": "The name of the (newly created) column that contains the results"
            },
        }
    }

}

interface WranglerState {
    columns: DataColumn[];
    isOpen: boolean;
    loading: boolean;
    recipe: number;
    recipeStep: number;
    transformationsUpdating: number[];
    recipeObject?: Recipe;
    selectedTransformation?: Transformation;
    data: number[][];
}

export interface Transformation {
    id: number,
    kwargs: string,
    previous: number|null,
    next?: number[],
    recipe: number,
    transformation: string,
}

interface Recipe {
    id: number,
    input: number,
    name: string,
    output: number,
    transformations: Transformation[]
}


function transformationMakeTitle(transformation: Transformation): string {
    let title = transformation.transformation;
    let kwargs = JSON.parse(transformation.kwargs);
    if (title in TRANSFORMATIONS) {
        title = TRANSFORMATIONS[title]["title"].replace(/{(\w+)}/g, function (_, k) {
            return kwargs[k];
        });
    }
    return title;
}



interface TransformationDialogProps {
    onClose: () => void,
    transformation: Transformation,
    setTransformation: () => void,
    wranglerService: WranglerService,
    isOpen: boolean
}

interface TransformationDialogState {
    onClose: () => void,
    transformation: Transformation,
    fieldValues: { [key: string]: any },
    isOpen: boolean
}

//--------------------------------------------------
//--------------------------------------------------
// Column select box
//--------------------------------------------------
//--------------------------------------------------
export class ColumnType {
    name: string;
}

interface ColumnSelectProps {
    columns: string[],
    field: string,
    value: string,
    onValueChange: (field: string, value: any) => void
}

interface ColumnSelectState {
    columns: ColumnType[],
    field: string,
    selectedColumns: ColumnType[],
}

export class ColumnsSelect extends React.Component<ColumnSelectProps, ColumnSelectState> {
    private onValueChange: (field: string, value: any) => void;
    public state: ColumnSelectState;

    constructor(props: ColumnSelectProps) {
        super(props);
        // TODO: Add the option to set the ID
        this.onValueChange = props.onValueChange;
        let columns = props.columns.map(column => { return { name: column } });
        this.state = {
            selectedColumns: columns.filter(column => props.value.indexOf(column.name) !== -1),
            field: props.field,
            columns: props.columns.map(column => { return { name: column } })
        }
        this.setColumn = this.setColumn.bind(this);
        this.addColumn = this.addColumn.bind(this);
        this.removeColumn = this.removeColumn.bind(this);
        this.onRemoveColumn = this.onRemoveColumn.bind(this);
        this.isColumnSelected = this.isColumnSelected.bind(this);
    }

    private setColumn(column: ColumnType) {
        if (this.state.selectedColumns.indexOf(column) === -1) {
            this.addColumn(column);
        } else {
            this.removeColumn(column);
        }
    }

    private addColumn(column: ColumnType) {
        let selectedColumns = this.state.selectedColumns;
        selectedColumns.push(column);
        this.setState({ selectedColumns: selectedColumns });
        this.onColumnsChanged(selectedColumns);
    }

    private removeColumn(column: ColumnType) {
        let selectedColumns = this.state.selectedColumns;
        let index = selectedColumns.indexOf(column);
        this.onRemoveColumn(column.name, index);
    }

    private onRemoveColumn(_tag: string, index: number) {
        let selectedColumns = this.state.selectedColumns;
        selectedColumns = selectedColumns.filter((_column, i) => i !== index);
        this.setState({ selectedColumns: selectedColumns.filter((_column, i) => i !== index) });
        this.onColumnsChanged(selectedColumns);
    }

    private onColumnsChanged(selectedColumns: ColumnType[]) {
        this.onValueChange(this.state.field, selectedColumns.map((column: ColumnType) => column.name));
    }

    private isColumnSelected(column: ColumnType) {
        return this.state.selectedColumns.indexOf(column) !== -1
    }

    private renderColumn: ItemRenderer<ColumnType> = (column, { modifiers, handleClick }) => {
        if (!modifiers.matchesPredicate) {
            return null;
        }
        return (
            <MenuItem
                active={modifiers.active}
                icon={this.isColumnSelected(column) ? "tick" : "blank"}
                key={column.name}
                onClick={handleClick}
                text={column.name}
                shouldDismissPopover={false}
            />
        );
    };

    private renderTag = (column: ColumnType) => column.name;

    private filter: ItemPredicate<ColumnType> = (query, item, _index, exactMatch) => {
        const normalizedTitle = item.name.toLowerCase();
        const normalizedQuery = query.toLowerCase();

        if (exactMatch) {
            return normalizedTitle === normalizedQuery;
        } else {
            return `${normalizedTitle}`.indexOf(normalizedQuery) >= 0;
        }
    };

    render() {
        const ColumnTypeSelect = MultiSelect.ofType<ColumnType>();
        return <ColumnTypeSelect
            itemPredicate={this.filter}
            itemRenderer={this.renderColumn}
            tagRenderer={this.renderTag}
            popoverProps={{ minimal: true }}
            items={this.state.columns}
            key={`transformation-input-${this.state.field}`}
            noResults={<MenuItem disabled={true} text="No results." />}
            onItemSelect={this.setColumn}
            selectedItems={this.state.selectedColumns}
            tagInputProps={{ tagProps: { intent: Intent.NONE, minimal: false }, onRemove: this.onRemoveColumn }}
        >
        </ColumnTypeSelect>
    }
}

export class TransformationDialog extends React.Component<TransformationDialogProps, TransformationDialogState> {
    private handleClose: () => void;
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
            onClose: props.onClose
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
            isOpen: props.isOpen
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
        this.wranglerService.putTransformation(this.state.transformation.id, transformation, this.finishUpdate)
    }

    /**
     * Finishes update
     * @param body The response body
     */
    private finishUpdate(body: {}) {
        // TODO: Re-enable the save button
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
        // TODO: Actually load the correct columns
        let columns = ["column1", "column2", "column3"];
        let field_values = JSON.parse(this.state.transformation.kwargs);

        if (field["input"] === "column" && field["multiple"]) {
            return <ColumnsSelect value={field_values[key]} columns={columns} field={key} onValueChange={this.onValueChange} />
        } else if (field["input"] === "column") {
            return <HTMLSelect value={this.state.fieldValues[key]} id={`transformation-input-${key}`} data-field={key} onChange={this.onInputChange} key={`transformation-input-${key}`}>
                {columns.map(column => <option id={column}>{column}</option>)}
            </HTMLSelect>
        } else if (field["input"] === "select") {
            return <HTMLSelect value={this.state.fieldValues[key]} id={`transformation-input-${key}`} data-field={key} onChange={this.onInputChange} key={`transformation-input-${key}`}>
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

interface TransformationButtonProps {
    handleOpen: (transformation: Transformation) => void,
    deleteTransformation: (transformation: Transformation) => void,
    transformation: Transformation,
    index: number
}

interface TransformationButtonState {
    transformation: Transformation,
    index: number,
    isOpenDelete: boolean
}

export class TransformationButton extends React.PureComponent<TransformationButtonProps, TransformationButtonState> {
    private handleOpen: (transformation: Transformation) => void;
    private deleteTransformation: (transformation: Transformation) => void;
    constructor(props: TransformationButtonProps) {
        super(props);
        this.handleOpen = props.handleOpen;
        this.deleteTransformation = props.deleteTransformation;
        this.state = {
            transformation: props.transformation,
            index: props.index,
            isOpenDelete: false,
        }
        this.openDialog = this.openDialog.bind(this);
        this.handleDeleteAsk = this.handleDeleteAsk.bind(this);
        this.handleDeleteCancel = this.handleDeleteCancel.bind(this);
        this.handleDeleteConfirm = this.handleDeleteConfirm.bind(this);
    }

    /**
     * Opens the transformation dialog
     */
    private openDialog() {
        this.handleOpen(this.state.transformation);
    }

    private handleDeleteAsk() {
        this.setState({ isOpenDelete: true });
    }

    private handleDeleteCancel() {
        this.setState({ isOpenDelete: false });
    }

    private handleDeleteConfirm() {
        this.deleteTransformation(this.state.transformation);
        this.setState({ isOpenDelete: false });
    }

    /**
     * Renders transformation button
     * @returns  
     */
    render() {
        let title = transformationMakeTitle(this.state.transformation);
        return <tr>
            <Alert
                canEscapeKeyCancel={true}
                canOutsideClickCancel={true}
                cancelButtonText="No"
                confirmButtonText="Yes"
                icon="trash"
                intent={Intent.DANGER}
                isOpen={this.state.isOpenDelete}
                onCancel={this.handleDeleteCancel}
                onConfirm={this.handleDeleteConfirm}
            >
                <p>Are you sure you want to delete <b>{title}</b>?</p>
            </Alert>
            <td>{this.state.index + 1}</td>
            <td>{title}</td>
            <td>
                <ButtonGroup vertical={false} fill={true} alignText="left">
                    <Button outlined={true} intent={Intent.PRIMARY} rightIcon="edit" key={`transformation-edit-${this.state.index}`} onClick={this.openDialog} className={Classes.FIXED}></Button>
                    <Button outlined={true} intent={Intent.DANGER} rightIcon="delete" key={`transformation-delete-${this.state.index}`} onClick={this.handleDeleteAsk} className={Classes.FIXED}></Button>
                </ButtonGroup>
            </td>
        </tr>
    }
}

export class Wrangler extends React.Component<PageProps, WranglerState> {
    private wranglerService: WranglerService;
    private addToast: (toast: IToastProps) => void;

    constructor(props: any) {
        super(props);
        this.wranglerService = new WranglerService(props.addToast, props.setLoggedIn);

        this.state = {
            recipe: 1,
            isOpen: false,
            loading: true,
            recipeStep: 3,
            transformationsUpdating: [],
            recipeObject: undefined,
            columns: this.createColumns(DUMMY_COLUMNS),
            data: DUMMY_DATA,
        };

        this.addToast = props.addToast;
        this.getData = this.getData.bind(this);
        this.receiveData = this.receiveData.bind(this);
        this.receiveRecipe = this.receiveRecipe.bind(this);
        this.handleOpenTransformation = this.handleOpenTransformation.bind(this);
        this.handleCloseTransformation = this.handleCloseTransformation.bind(this);
        this.createTransformation = this.createTransformation.bind(this);
        this.deleteTransformation = this.deleteTransformation.bind(this);
        this.finishUpdate = this.finishUpdate.bind(this);
        this.finishUpdateOrdering = this.finishUpdateOrdering.bind(this);
        this.endUpdateOrdering = this.endUpdateOrdering.bind(this);
        this.refresh = this.refresh.bind(this);
        this.refresh();
    }

    /**
     * Refresh the recipe and the data
     */
    private refresh() {
        this.setState({ loading: true });
        this.getData();
        this.getRecipe();
    }

    /**
     * Get the data.
     */
    public getData() {
        this.wranglerService.getData(this.state.recipe, this.state.recipeStep, this.receiveData)
    }

    /**
     * Get the recipe
     */
    public getRecipe() {
        this.wranglerService.getRecipe(this.state.recipe, this.receiveRecipe)
    }

    /**
     * Receive the recipe (receiveRecipe callback).
     */
    public receiveRecipe(body: { [key: string]: any }) {
        let transformation = body.transformations.filter((item: any) => item["previous"] === null)[0];
        let transformations = [];
        while (transformation !== undefined) {
            let nextId = transformation["id"];
            transformations.push(transformation);
            transformation = body.transformations.filter((item: any) => item["previous"] !== null && item["previous"] === nextId)[0];
        }
        body["transformations"] = transformations;
        this.setState({ recipeObject: body as Recipe });
    }

    /**
     * Creates a new transformation.
     * @param transformation The name of the transformation
     * @param kwargs The arguments
     */
    protected createTransformation(transformation: string, kwargs: { [key: string]: any }) {
        this.wranglerService.postTransformation({
            id: 0,
            kwargs: JSON.stringify(kwargs),
            previous: this.getTransformations().length > 0 ? this.getTransformations()[this.getTransformations().length - 1].id : null,
            next: [],
            recipe: this.state.recipe,
            transformation: transformation,
        }, this.finishUpdate);
    }

    protected finishUpdate(body: { [key: string]: any }) {
        this.refresh();
    }

    private createColumns(column_names: string[]): DataColumn[] {
        let columns: DataColumn[] = [];
        for (let c in column_names) {
            columns.push(new DataColumn(column_names[c], parseInt(c), this.createTransformation))
        }
        return columns;
    }

    /**
     * Receive the data (getData callback).
     */
    public receiveData(body: { [key: string]: any }) {
        if (body["success"]) {
            let columns = this.createColumns(body["data"]["columns"]);
            this.setState({ columns: columns, data: body["data"]["records"], loading: false });
        } else {
            if (body["messages"] != null &&
                typeof body["messages"][Symbol.iterator] === 'function') {
                for (let message of body["messages"]) {
                    this.addToast({
                        intent: Intent.DANGER,
                        message: `${message["code"]}: ${message["message"]}`,
                    });
                }
            } else {
                console.log(body["messages"]);
            }
        }
    }

    /**
     * Gets the transformations from the state
     * @returns transformations 
     */
    private getTransformations(): Transformation[] {
        if (this.state.recipeObject !== undefined) {
            return this.state.recipeObject.transformations;
        }
        return [];
    }

    /**
     * Handles the opening of the transformation dialog.
     * @param transformation 
     */
    private handleOpenTransformation(transformation: Transformation) {
        this.setState({ isOpen: true, selectedTransformation: transformation });
    }

    /**
     * Handles the closing of the transformation dialog.
     */
    private handleCloseTransformation = () => this.setState({ isOpen: false });

    private deleteTransformation(transformation: Transformation) {
        this.wranglerService.deleteTransformation(transformation.id, this.finishUpdate);
    }

    /**
     * Renders transformation button
     * @param transformation 
     * @param index 
     * @returns  
     */
    public renderTransformationButton(transformation: Transformation, index: number) {
        return <TransformationButton key={transformation.id} deleteTransformation={this.deleteTransformation}
            transformation={transformation} index={index} handleOpen={this.handleOpenTransformation} />
    }

    /**
     * Renders transformation dialog
     * @returns  
     */
    public renderTransformationDialog() {
        if (this.state.selectedTransformation !== undefined) {
            return <TransformationDialog
                setTransformation={this.refresh}
                wranglerService={this.wranglerService}
                isOpen={this.state.isOpen}
                transformation={this.state.selectedTransformation}
                onClose={this.handleCloseTransformation} />
        } else {
            return <span></span>;
        }
    }

    public updateOrdering(newState: Transformation[], sortable: Sortable | null) {
        // console.log(newState);
        // console.log(sortable);
    }

    public endUpdateOrdering(event: SortableEvent) {
        if (event.oldIndex !== undefined && event.newIndex !== undefined && event.oldIndex !== event.newIndex) {
            let t = this.getTransformations();
            let oldIdx = event.oldIndex;
            let newIdx = event.newIndex;
            let indicesToUpdate: number[] = [oldIdx, newIdx];
            if (t.length > oldIdx + 1) {
                t[oldIdx + 1].previous = t[oldIdx].previous;
                indicesToUpdate.push(oldIdx + 1)
            }
            if (event.oldIndex < event.newIndex) {
                // We're moving the element down in the list
                t[oldIdx].previous = t[newIdx].id;
                if (t.length > newIdx + 1) {
                    t[newIdx + 1].previous = t[oldIdx].id;
                    indicesToUpdate.push(newIdx + 1)
                }
            } else {
                // We're moving the element up in the list
                t[oldIdx].previous = t[newIdx].previous;
                t[newIdx].previous = t[oldIdx].id;
            }
            let transformationsUpdating = [];
            for (let idx of indicesToUpdate) {
                transformationsUpdating.push(t[idx].id);
                t[idx]['next'] = undefined;
                this.wranglerService.putTransformation(t[idx].id, t[idx], this.finishUpdateOrdering)
            }
            this.setState({ transformationsUpdating: transformationsUpdating });
        }
    }

    protected finishUpdateOrdering(body: { [key: string]: any }) {
        if ("id" in body) {
            let transformationsUpdating = this.state.transformationsUpdating.filter(id => id !== body["id"]);
            this.setState({ transformationsUpdating: transformationsUpdating });
            if (transformationsUpdating.length === 0) {
                this.refresh();
            }
        } else {
            this.addToast({
                intent: Intent.DANGER,
                message: `Something went wrong while updating the transformations`,
            });
        }
    }

    /**
     * Renders wrangler
     * @returns  
     */
    public render() {
        return (
            <Grid fluid>
                <Row>
                    <Col md={12}>
                        <Tabs id="TabsExample" animate={true} key={"horizontal"} renderActiveTabPanelOnly={true} vertical={false}>
                            <Tab id="panel-home" title="Home" panel={<HomePanel />} />
                            <Tab id="panel-transformations" title="Transformations" panel={<TransformationPanel />} panelClassName="ember-panel" />
                            <Tab id="panel-custom" title="Custom" panel={<CustomPanel />} />
                            <Tab id="panel-settings" title="Settings" panel={<SettingsPanel />} />
                            <Tabs.Expander />
                            <input className="bp3-input" type="text" placeholder="Search help" />
                        </Tabs>
                    </Col>
                </Row>
                <Row>
                    <Col md={2}>
                        <H3>Recipe</H3>
                        <div>
                            <HTMLTable striped={true}>
                                <ReactSortable
                                    tag="tbody"
                                    list={this.getTransformations()}
                                    setList={this.updateOrdering}
                                    onEnd={this.endUpdateOrdering}
                                >
                                    {this.getTransformations().map((transformation: Transformation, index: number) => this.renderTransformationButton(transformation, index))}
                                </ReactSortable>
                            </HTMLTable>

                            {/* <ButtonGroup vertical={true} fill={true} alignText="left"> */}
                            {/* </ButtonGroup> */}
                            {this.renderTransformationDialog()}
                        </div>
                    </Col>
                    <Col md={10}>
                        <DataTable loading={this.state.loading} data={this.state.data} columns={this.state.columns} />
                    </Col>
                </Row>
            </Grid>
        );
    }
}

const HomePanel: React.SFC<{}> = () => (
    <div>
        <Tooltip content="Convert a column to another data type">
            <Button icon="numerical">Convert</Button>
        </Tooltip>
        {/* TODO: Link to a help page on the drawer */}
    </div>
);

const TransformationPanel: React.SFC<{}> = () => (
    <div>
        <H3>Example panel: Angular</H3>
        <p>
            HTML is great for declaring static documents, but it falters when we try to use it for declaring dynamic
            views in web-applications. AngularJS lets you extend HTML vocabulary for your application. The resulting
            environment is extraordinarily expressive, readable, and quick to develop.
        </p>
    </div>
);

const CustomPanel: React.SFC<{}> = () => (
    <div>
        <H3>Example panel: Angular</H3>
        <p>
            HTML is great for declaring static documents, but it falters when we try to use it for declaring dynamic
            views in web-applications. AngularJS lets you extend HTML vocabulary for your application. The resulting
            environment is extraordinarily expressive, readable, and quick to develop.
        </p>
    </div>
);

const SettingsPanel: React.SFC<{}> = () => (
    <div>
        {/* TODO: Link to a help page on the drawer */}
        <FormGroup label="Sampling method" labelInfo={<Help page="sampling" />}>
            {/* <FormGroup label="Sampling method" labelInfo={<a href=""><Icon icon="help" /></a>}> */}
            <HTMLSelect>
                <option value="random">Random</option>
                <option value="stratified">stratified</option>
                <option value="top">Top</option>
            </HTMLSelect>
        </FormGroup>
    </div>
);

interface HelpState {
    autoFocus: boolean;
    canEscapeKeyClose: boolean;
    canOutsideClickClose: boolean;
    enforceFocus: boolean;
    hasBackdrop: boolean;
    isOpen: boolean;
    position?: Position;
    size?: string;
    usePortal: boolean;
    title: string;
    content: string;
}

interface HelpProps extends IProps {
    page: string;
}

class Help extends React.PureComponent<HelpProps, HelpState> {
    public state: HelpState;

    constructor(props: HelpProps) {
        super(props);
        if (props.page === "sampling") {
            this.state = {
                autoFocus: true,
                canEscapeKeyClose: true,
                canOutsideClickClose: true,
                enforceFocus: true,
                hasBackdrop: true,
                isOpen: false,
                position: Position.RIGHT,
                size: undefined,
                usePortal: true,
                title: "Sampling",
                content: "TODO: This is a help page about the sampling methodology"
            }
        } else {
            this.state = {
                autoFocus: true,
                canEscapeKeyClose: true,
                canOutsideClickClose: true,
                enforceFocus: true,
                hasBackdrop: true,
                isOpen: false,
                position: Position.RIGHT,
                size: undefined,
                usePortal: true,
                title: this.props.page,
                content: `TODO: This is a help page about the ${this.props.page}`
            }
        }
    }

    private handleOpen = () => this.setState({ isOpen: true });
    private handleClose = () => this.setState({ isOpen: false });

    render() {
        return <span>
            <Button icon="help" onClick={this.handleOpen} minimal={true} />
            <Drawer
                icon="help"
                onClose={this.handleClose}
                {...this.state}
            >
                <div>
                    <div>
                        <p>{this.state.content}</p>
                    </div>
                </div>
            </Drawer>
        </span>
    }
}