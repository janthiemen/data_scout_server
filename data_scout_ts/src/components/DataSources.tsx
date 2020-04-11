import * as React from "react";

import {
    Classes, ITreeNode, Tree,
    ContextMenu,
    Menu,
    MenuItem,
    MenuDivider,
    IProps,
    FormGroup,
    InputGroup,
    IToastProps,
    NumericInput,
    Switch,
    Intent
} from "@blueprintjs/core";

import { Select, ItemRenderer, ItemPredicate } from "@blueprintjs/select";

import { Grid, Row, Col } from 'react-flexbox-grid';
import { PageProps } from "../helpers/props";
import { DataSourceService } from "../helpers/userService";

import { Button } from "@blueprintjs/core";
import { highlightText } from "../helpers/select";

export interface DataSourcesTreeState {
    dataSources: DataSource[];
    nodes: DataSourceNode[];
    nodeContextMenu?: DataSourceNode;
}

interface DataSourceNode<T = {}> extends ITreeNode {
    isFolder?: boolean;
    childNodes?: DataSourceNode[];
}

export interface DataSourcesTreeProps extends IProps {
    dataSourceService: DataSourceService;
    updateDataSources: () => void;
    onSelectDataSource: (dataSouce: DataSourceNode) => void;
    addToast: (toast: IToastProps) => void;
    dataSources: DataSource[];
}

/**
 * The component represents all of the data sources in a tree.
 */
export class DataSourcesTree extends React.Component<DataSourcesTreeProps> {
    public state: DataSourcesTreeState = { 
        dataSources: [],
        nodes: [],
        nodeContextMenu: undefined
    };
    private dataSourceService: DataSourceService;
    private updateDataSources: () => void;;
    private addToast: (toast: IToastProps) => void;
    public onSelectDataSource: (dataSouce: DataSourceNode) => void;

    /**
     * Create a new data source tree.
     * @param props The props
     */
    constructor(props: DataSourcesTreeProps) {
        super(props);

        // This binding is necessary to make `this` work in the callback    
        this.onSelectDataSource = props.onSelectDataSource;
        this.updateDataSources = props.updateDataSources;
        this.addToast = props.addToast;
        this.dataSourceService = props.dataSourceService;
        this.showContextMenu = this.showContextMenu.bind(this);
        this.newDataSource = this.newDataSource.bind(this);
        this.finishDelete = this.finishDelete.bind(this);
        this.delete = this.delete.bind(this);
        this.handleNodeClick = this.handleNodeClick.bind(this);
    }

    
    /**
     * Called when new props are received.
     * @param props The new props
     */
    componentWillReceiveProps(props: DataSourcesTreeProps) {
        let nodes: DataSourceNode[] = [];
        for (let dataSource of props.dataSources) {
            nodes.push(this.convertDataSourceToNode(dataSource));
        }
        this.setState({ dataSources: props.dataSources, nodes: nodes });
    }

    /**
     * Create a new data source.
     * @param event TODO: Determine the event type
     */
    public newDataSource(event: any) {
        this.onSelectDataSource(this.convertDataSourceToNode(newDataSource()));
    }

    /**
     * Create a new folder.
     * @param event TODO: Determine the event type
     */
    public newFolder(event: any) {
        //TODO
        console.log("NEW FOLDER!");
    }

    /**
     * Set the parent of a data source or folder (i.e. move it).
     * @param event TODO: Determine the event type
     */
    public setParent(event: any) {
        //TODO
        console.log("NEW FOLDER!");
    }

    /**
     * Delete a data source or folder.
     * @param event TODO: Determine the event type
     */
    public delete(event: any) {
        //TODO
        console.log(event);
        if (this.state.nodeContextMenu !== undefined) {
            this.dataSourceService.delete(this.state.nodeContextMenu.id, this.finishDelete);
        } else {
            this.addToast({ intent: Intent.WARNING, message: "Please open the context menu on a data source." });
        }
    }

    public finishDelete(body: {}) {
        this.addToast({ intent: Intent.SUCCESS, message: "The data source has been deleted." });
        this.updateDataSources();
    }

    /**
     * Show a context menu
     * @param nodeData The node
     * @param path The path to the node
     * @param e An event
     */
    public showContextMenu(nodeData: DataSourceNode, path: any, e: any) {
        e.preventDefault();
        this.setState({ nodeContextMenu: nodeData });

        ContextMenu.show(<Menu>
            <MenuItem icon="document" onClick={this.newDataSource} text="New data source" />
            <MenuItem icon="folder-close" onClick={this.newFolder} text="New folder" />
            <MenuItem icon="add-to-folder" onClick={this.setParent} text="Move" />
            <MenuItem icon="trash" onClick={this.delete} text="Remove" />
            <MenuDivider />
            {!nodeData.isFolder &&
                <MenuItem icon="data-lineage" text="Use data source" />
            }
        </Menu>, { left: e.clientX, top: e.clientY }
        );
    };

    /**
     * Converts data source to node
     * @param dataSource 
     * @returns data source to node 
     */
    private convertDataSourceToNode(dataSource: DataSource): DataSourceNode {
        return { id: dataSource.id, icon: "document", label: dataSource.name };
    }

    /**
     * Render the tree.
     */
    render() {
        return (
            <Tree
                onNodeContextMenu={this.showContextMenu}
                contents={this.state.nodes}
                onNodeClick={this.handleNodeClick}
                onNodeCollapse={this.handleNodeCollapse}
                onNodeExpand={this.handleNodeExpand}
                className={Classes.ELEVATION_0}
            />
        );
    }

    /**
     * Handle node click of data sources tree
     */
    private handleNodeClick = (nodeData: DataSourceNode, _nodePath: number[], e: React.MouseEvent<HTMLElement>) => {
        const originallySelected = nodeData.isSelected;
        if (!e.shiftKey) {
            this.forEachNode(this.state.nodes, n => (n.isSelected = false));
        }
        nodeData.isSelected = originallySelected == null ? true : !originallySelected;
        this.setState(this.state);
        this.onSelectDataSource(nodeData);
    };

    /**
     * Handle node collapse of data sources tree
     */
    private handleNodeCollapse = (nodeData: DataSourceNode) => {
        nodeData.isExpanded = false;
        this.setState(this.state);
    };

    /**
     * Handle node expand of data sources tree
     */
    private handleNodeExpand = (nodeData: DataSourceNode) => {
        nodeData.isExpanded = true;
        this.setState(this.state);
    };

    /**
     * For each node
     * @param nodes 
     * @param callback 
     * @returns  
     */
    private forEachNode(nodes: DataSourceNode[] | undefined, callback: (node: DataSourceNode) => void) {
        if (nodes == null) {
            return;
        }

        for (const node of nodes) {
            callback(node);
            this.forEachNode(node.childNodes, callback);
        }
    }
}

class DataSourceType {
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

interface DataSourcesState {
    types: DataSourceType[],
    dataSourceType?: DataSourceType,
    dataSources: DataSource[],
    dataSource: DataSource
}

interface DataSourceProps extends IProps {
    dataSourceService: DataSourceService,
    addToast: (toast: IToastProps) => void;
    updateDataSources: () => void;
    dataSourceType?: DataSourceType,
    dataSource: DataSource,
    types: DataSourceType[]
}

interface DataSourceState {
    dataSource: DataSource,
    dataSourceType?: DataSourceType,
    fieldValues: { [key: string]: any },
    types: DataSourceType[];
}

/**
 * This class represents a data source object.
 */
class DataSourceComponent extends React.Component<DataSourceProps, DataSourceState> {
    private dataSourceService: DataSourceService;
    private addToast: (toast: IToastProps) => void;
    private updateDataSources: () => void;
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
        this.getFields = this.getFields.bind(this);
        this.setType = this.setType.bind(this);
        this.updateFieldValue = this.updateFieldValue.bind(this);
        this.updateName = this.updateName.bind(this);
        this.submitDataSource = this.submitDataSource.bind(this);
        this.finishSubmit = this.finishSubmit.bind(this);
        this.dataSourceService = props.dataSourceService;
        this.updateDataSources = props.updateDataSources;
        this.addToast = props.addToast;
    }

    /**
     * Update the field vales in the state.
     */
    private updateFields() {
        let fields = this.getFields()
        let kwargs = this.state.dataSource.kwargs;

        let fieldValues: { [key: string]: string } = {};
        for (let key in fields) {
            fieldValues[key] = key in kwargs ? kwargs[key] : "";
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
     * Handle the submit return
     * @param body 
     */
    private finishSubmit(body: {}) {
        if ("id" in body) {
            // There is an ID in there, so we'll set the current ID
            let dataSource = this.state.dataSource;
            dataSource.id = body["id"];
            this.setState({ dataSource: dataSource });
            this.addToast({ intent: Intent.SUCCESS, message: "The data source has been saved" });
            this.updateDataSources();
        } else {
            console.log(body);
            this.addToast({ intent: Intent.WARNING, message: "Couldn't save the data source." });
        }
    }

    /**
     * Submits the data source
     */
    private submitDataSource(event: React.SyntheticEvent) {
        event.preventDefault();

        if (this.state.dataSourceType !== undefined) {
            let data = {
                id: this.state.dataSource.id,
                name: this.state.dataSource.name,
                source: this.state.dataSourceType.name,
                kwargs: JSON.stringify(this.state.fieldValues)
            }
            this.dataSourceService.save(data, this.finishSubmit);
        } else {
            this.addToast({ intent: Intent.WARNING, message: "Please select a data source type first." });
        }
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

interface DataSource {
    id: number,
    name: string,
    source?: string,
    kwargs: { [key: string]: any },
}

/**
 * Empty data source object.
 */
const newDataSource = function(): DataSource {
    return {
        id: -1,
        name: "New data source",
        source: undefined,
        kwargs: {}
    }
}

/**
 * The page with all the data sources.
 */
export class DataSources extends React.Component<PageProps> {
    private dataSourceService: DataSourceService;
    private addToast: (toast: IToastProps) => void;
    public state: DataSourcesState = {
        types: [],
        dataSourceType: undefined,
        dataSources: [],
        dataSource: newDataSource()
    }

    /**
     * Creates an instance of data sources.
     * @param props 
     */
    constructor(props: PageProps) {
        super(props);
        this.dataSourceService = new DataSourceService(props.addToast, props.setLoggedIn);
        this.setTypes = this.setTypes.bind(this);
        this.setDataSources = this.setDataSources.bind(this);
        this.onSelectDataSource = this.onSelectDataSource.bind(this);
        this.updateDataSources = this.updateDataSources.bind(this);
        this.addToast = props.addToast;
        this.dataSourceService.getTypes(this.setTypes);
        this.updateDataSources();
    }

    /**
     * Sets types
     * @param types 
     */
    public setTypes(types: {}) {
        this.setState({ types: types });
    }

    public updateDataSources() {
        this.dataSourceService.get(this.setDataSources);
    }

    /**
     * Selects data source
     * @param node 
     */
    public onSelectDataSource(node: DataSourceNode) {
        console.log(node);
        // We're sure that there's only one data source for each id, so we can just pick the first
        // TODO: Maybe in the future we want to add a check on this
        let dataSource = this.state.dataSources.filter(item => item.id === node.id)[0];
        console.log(dataSource);
        this.setState({ dataSource: dataSource });
        /*
        TODO: 
        1. Get the data source info based on the ID -> data source object, data source type object
        2. Get all available data source types
        3. Split the kwargs
        4. Build the form
        */
    }

    /**
     * Sets data sources based on the API response
     * @param body 
     */
    private setDataSources(body: { [key: string]: any }) {
        let dataSources: DataSource[] = [];
        body["results"].forEach((result: { id: number, name: string, source: string, kwargs: string }) => {
            let kwargs: { [key: string]: any } = JSON.parse(result["kwargs"]);
            dataSources.push({ id: result["id"], name: result["name"], source: result["source"], kwargs: kwargs });
        });
        dataSources.push(newDataSource());
        this.setState({ dataSources: dataSources });
    }

    /**
     * Renders data sources
     * @returns  
     */
    render() {
        return (
            <Grid fluid>
                <Row>
                    <Col md={3}>
                        <DataSourcesTree updateDataSources={this.updateDataSources} dataSourceService={this.dataSourceService} dataSources={this.state.dataSources} onSelectDataSource={this.onSelectDataSource} addToast={this.addToast} />
                    </Col>
                    <Col md={6}>
                        <DataSourceComponent updateDataSources={this.updateDataSources} types={this.state.types} dataSource={this.state.dataSource} dataSourceService={this.dataSourceService} addToast={this.addToast} />
                    </Col>
                </Row>
            </Grid>
        );
    }
}
