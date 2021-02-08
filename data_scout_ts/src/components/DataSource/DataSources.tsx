import * as React from "react";
import autobind from 'class-autobind';

import { Button, Icon, Intent, IToastProps } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import { History } from 'history'

import { Grid, Row, Col } from 'react-flexbox-grid';
import { PageProps } from "../../helpers/props";
import { DataSourceService, JoinService } from "../../helpers/userService";

import { DataSourceComponent } from "../DataSource/DataSource";
import { SearchTree, SearchTreeNode } from "../SearchTree/SearchTree";
import { Join, JoinDialog } from "../Join/JoinDialog";
import { withRouter } from "react-router-dom";

export interface DataSource {
    id: number,
    name: string,
    parent: number,
    source?: string,
    schema?: { [key: string]: string },
    kwargs: { [key: string]: any },
}

// TODO: Can we combine this with the recipe folder?
export interface DataSourceFolder {
    id: number,
    parent: number,
    name: string,
    child_folders: DataSourceFolder[],
    children: DataSource[],
    child_joins: Join[],
}

interface DataSourcesState {
    types: [],
    join?: Join,
    joins: Join[],
    dataSources: DataSource[],
    dataSource?: DataSource,
    dataSourceFolders: DataSourceFolder[],
}

/**
 * Empty data source object.
 */
export const newDataSource = function(): DataSource {
    return {
        id: -1,
        parent: undefined,
        name: "New data source",
        source: undefined,
        kwargs: {}
    }
}

/**
 * Empty data source object.
 */
export const parseDataSource = function(data_source: {}): DataSource {
    let kwargs: { [key: string]: any } = JSON.parse(data_source["kwargs"]);
    return { 
        id: data_source["id"], 
        name: data_source["name"], 
        source: data_source["source"], 
        parent: data_source["parent"], 
        kwargs: kwargs,
        schema: JSON.parse(data_source["schema"]) 
    };
}

/**
 * Empty join object.
 */
export const newJoin = function(): Join {
    return {
        id: -1,
        name: "New join",
        data_source_left: undefined,
        recipe_left: undefined,
        data_source_right: undefined,
        recipe_right: undefined,
        field_left: "",
        field_right: "",
        method: "inner",
        parent: null
    }
}

/**
 * The page with all the data sources.
 */
export class DataSourcesComponent extends React.Component<PageProps> {
    private dataSourceService: DataSourceService;
    private joinService: JoinService;
    private addToast: (toast: IToastProps, key?: string) => string;
    private history: History;
    public state: DataSourcesState = {
        types: [],
        dataSources: [],
        joins: [],
        dataSourceFolders: [],
        dataSource: newDataSource(),
        join: undefined,
    }

    /**
     * Creates an instance of data sources.
     * @param props 
     */
    constructor(props: PageProps) {
        super(props);
        autobind(this);
        this.dataSourceService = new DataSourceService(props.addToast, props.setLoggedIn);
        this.joinService = new JoinService(this.addToast, this.dataSourceService.setLoggedIn, false)
        this.history = props.history;
        this.dataSourceService.getTypes(this.setTypes);

        this.addToast = props.addToast;
        this.refresh();
    }


    /**
     * Receive types from the service
     * @param types 
     */
    public setTypes(types: {}) {
        this.setState({ types: types });
    }

    /**
     * Receive folders from the service
     * @param folders 
     */
    public setFolders(folders: any) {
        this.setState({ dataSourceFolders: folders["results"] });
    }

    /**
     * Refresh the data
     */
    public refresh() {
        this.dataSourceService.getFolders(this.setFolders);
        this.dataSourceService.get(this.setDataSources);
        this.joinService.get(this.setJoins);
    }

    /**
     * Sets data sources based on the API response
     * @param body 
     */
    private setDataSources(body: { [key: string]: any }) {
        let dataSources: DataSource[] = body["results"].map((result: {}) => parseDataSource(result));
        dataSources.push(newDataSource());
        this.setState({ dataSources: dataSources });
    }

    /**
     * Sets joins based on the API response
     * @param body 
     */
    private setJoins(body: { [key: string]: any }) {
        this.setState({ joins: body["results"] });
    }

    /**
     * Open a join dialog
     * @param id The ID of the join
     */
    private onOpenJoin(id: number) {
        this.setState({ join: this.state.joins.filter(join => join.id === id)[0] });
    }

    /**
     * Open the join dialog for a new join
     */
    private onNewJoin() {
        this.setState({ join: newJoin() });
    }

    /**
     * Close the join dialog
     */
    private onCloseJoin() {
        this.setState({ join: undefined });
    }

    /**
     * Renders data sources tree and a data source component
     * @returns  
     */
    render() {
        return (
            <Grid fluid>
                <JoinDialog addToast={this.addToast} joinService={this.joinService} isOpen={this.state.join !== undefined} join={this.state.join} onClose={this.onCloseJoin}></JoinDialog>
                <Row>
                    <Col md={3}>
                        <SearchTree onNewElement={this.onNewElement} 
                                    onNewFolder={this.onNewFolder} 
                                    onDelete={this.onDelete} 
                                    onDoubleClick={this.onDoubleClick} 
                                    onSetParent={this.onSetParent} 
                                    extraButton={<Button icon="data-lineage" outlined onClick={this.onNewJoin}>New join</Button>}
                                    nodes={this.makeNodesDataSources(this.state.dataSourceFolders, this.state.dataSources.filter((dataSource: DataSource) => dataSource.parent === null && dataSource.id !== -1),  this.state.joins.filter((join: Join) => join.parent === null && join.id !== -1))} 
                        />
                    </Col>
                    <Col md={6}>
                        <DataSourceComponent updateDataSources={this.refresh} types={this.state.types} dataSource={this.state.dataSource} dataSourceService={this.dataSourceService} addToast={this.addToast} />
                    </Col>
                </Row>
            </Grid>
        );
    }

    /**
     * Create the nodes that make up the tree.
     * @param dataSourceFolders The folders
     * @param dataSources The data sources
     * @param joins The joins
     */
    private makeNodesDataSources(dataSourceFolders: DataSourceFolder[], dataSources: DataSource[], joins: Join[]): SearchTreeNode[] {
        let nodes: SearchTreeNode[] = [];
        for (let dataSourceFolder of dataSourceFolders) {
            let childNodes = this.makeNodesDataSources(dataSourceFolder.child_folders, dataSourceFolder.children, dataSourceFolder.child_joins);
            let node = {
                id: `F-${dataSourceFolder.id}`,
                key: dataSourceFolder.id,
                icon: <Icon icon={IconNames.FOLDER_CLOSE} />,
                isExpanded: false,
                parent: dataSourceFolder.parent,
                label: dataSourceFolder.name,
                isFolder: true,
                hasCaret: childNodes.length > 0,
                childNodes: childNodes
            };
            nodes.push(node);
        }
        for (let dataSource of dataSources) {
            nodes.push({
                id: `D-${dataSource.id}`,
                key: dataSource.id,
                onClick: this.onClick,
                isFolder: false,
                parent: dataSource.parent,
                icon: <Icon icon={IconNames.DOCUMENT} />,
                label: dataSource.name,
            })
        }
        for (let join of joins) {
            nodes.push({
                id: `J-${join.id}`,
                key: join.id,
                onClick: this.onOpenJoin,
                isFolder: false,
                parent: join.parent,
                icon: <Icon icon={IconNames.DATA_LINEAGE} />,
                label: join.name,
            })
        }
      
        return nodes;
    }

    /**
     * Create a new data source.
     */
    private onNewElement() {
        // Create a new DataSource
        this.onClick(-1);
    }

    /**
     * Create a new folder or update an existing
     * @param name The folder's name
     * @param parent The folder's parent
     * @param id The folder's id (only if updating a folder, else null or undefined)
     */
    private onNewFolder(name: string, parent?: number, id?: number) {
        // Create a new folder
        this.dataSourceService.saveFolder({id: id, name: name, parent: parent}, this.finishUpdate);
    }

    /**
     * Finish the update and refresh the data.
     * @param body 
     */
    private finishUpdate(body: {}) {
        this.refresh();
        this.addToast({ intent: Intent.SUCCESS, message: `The Update has been processed.` });
    }

    /**
     * Delete a data source or folder
     * @param id 
     * @param isFolder 
     */
    private onDelete(id: number, isFolder: boolean) {
        if (isFolder) {
            this.dataSourceService.deleteFolder(id, this.finishUpdate);
        } else {
            this.dataSourceService.delete(id, this.finishUpdate);
        }
    }

    /**
     * Select a dataSource
     * @param id 
     */
    private onClick(id: number) {
        // Select a dataSource
        let dataSource = this.state.dataSources.filter(item => item.id === id)[0];
        this.setState({ dataSource: dataSource });
    }

    /**
     * Go to the recipes page.
     * @param id 
     */
    private onDoubleClick(id: number) {
        this.history.push(`/recipes`)
    }

    /**
     * Get a list of all data source folders (instead of a tree).
     * @param dataSourceFolders 
     */
    private flattenDataSourceFolders(dataSourceFolders: DataSourceFolder[]) {
        let folderItems: DataSourceFolder[] = [];
        for (let dataSourceFolder of dataSourceFolders) {
            folderItems.push(dataSourceFolder);
            if (dataSourceFolder.child_folders.length > 0) {
                folderItems = folderItems.concat(this.flattenDataSourceFolders(dataSourceFolder.child_folders));
            }
        }
        return folderItems;
    }

    /**
     * Set the parent for a folder, data source or join
     * @param id The ID in the tree. This starts with F- for folders, D- for data sources and J- for joins
     * @param key The ID of the object that is selected
     * @param isFolder Whether the item is a folder or not
     * @param parent The new parent of the object
     */
    private onSetParent(id: string, key: number, isFolder: boolean, parent: number) {
        // Set the parent for a dataSource
        if (isFolder) {
            // TODO: Check if you're not moving it to be its own child
            let dataSourceFolder = this.flattenDataSourceFolders(this.state.dataSourceFolders).filter(item => item.id === key)[0];
            this.dataSourceService.saveFolder({id: dataSourceFolder.id, name: dataSourceFolder.name, parent: parent}, this.finishUpdate);
        } else if (id.startsWith("J-")) {
            // If it starts with a J, it's a join
            let join = this.state.joins.filter(item => item.id === key)[0];
            join.parent = parent;
            this.joinService.save(join, this.finishUpdate);
        } else {
            let dataSource = this.state.dataSources.filter(item => item.id === key)[0];
            dataSource.parent = parent;
            this.dataSourceService.save({
                id: dataSource.id,
                name: dataSource.name,
                parent: dataSource.parent,
                source: dataSource.source,
                kwargs: JSON.stringify(dataSource.kwargs),            
            }, this.finishUpdate);
        }
    }
}

export const DataSources = withRouter(DataSourcesComponent)