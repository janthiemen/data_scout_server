import * as React from "react";
import autobind from 'class-autobind';

import { Icon, Intent, IToastProps } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import { History } from 'history'

import { Grid, Row, Col } from 'react-flexbox-grid';
import { PageProps } from "../../helpers/props";
import { DataSourceService, JoinService } from "../../helpers/userService";

import { DataSourceComponent } from "../DataSource/DataSource";
import { SearchTree, SearchTreeNode } from "../SearchTree/SearchTree";
import { JoinDialog } from "../Join/JoinDialog";
import { withRouter } from "react-router-dom";

export interface DataSource {
    id: number,
    name: string,
    parent: number,
    source?: string,
    kwargs: { [key: string]: any },
}

// TODO: Can we combine this with the recipe folder?
export interface DataSourceFolder {
    id: number,
    parent: number,
    name: string,
    child_folders: DataSourceFolder[],
    children: DataSource[],
}

interface DataSourcesState {
    types: [],
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
 * The page with all the data sources.
 */
export class DataSourcesComponent extends React.Component<PageProps> {
    private dataSourceService: DataSourceService;
    private addToast: (toast: IToastProps, key?: string) => string;
    private history: History;
    public state: DataSourcesState = {
        types: [],
        dataSources: [],
        dataSourceFolders: [],
        dataSource: newDataSource(),
    }

    /**
     * Creates an instance of data sources.
     * @param props 
     */
    constructor(props: PageProps) {
        super(props);
        autobind(this);
        this.dataSourceService = new DataSourceService(props.addToast, props.setLoggedIn);
        this.history = props.history;
        this.dataSourceService.getTypes(this.setTypes);

        this.addToast = props.addToast;
        this.refresh();
    }


    /**
     * Sets types
     * @param types 
     */
    public setTypes(types: {}) {
        this.setState({ types: types });
    }

    public setFolders(folders: any) {
        this.setState({ dataSourceFolders: folders["results"] });
    }

    public refresh() {
        this.dataSourceService.getFolders(this.setFolders);
        this.dataSourceService.get(this.setDataSources);
    }

    /**
     * Sets data sources based on the API response
     * @param body 
     */
    private setDataSources(body: { [key: string]: any }) {
        let dataSources: DataSource[] = [];
        body["results"].forEach((result: { id: number, name: string, source: string, kwargs: string }) => {
            let kwargs: { [key: string]: any } = JSON.parse(result["kwargs"]);
            dataSources.push({ id: result["id"], name: result["name"], source: result["source"], parent: result["parent"], kwargs: kwargs });
        });
        dataSources.push(newDataSource());
        this.setState({ dataSources: dataSources });
    }

    onCloseJoin() {
        console.log("TODO: Close join!")
    }

    /**
     * Renders data sources
     * @returns  
     */
    render() {
        return (
            <Grid fluid>
                <JoinDialog joinService={new JoinService(this.addToast, this.dataSourceService.setLoggedIn)} isOpen={true} onClose={this.onCloseJoin}></JoinDialog>
                <Row>
                    <Col md={3}>
                        <SearchTree onNewElement={this.onNewElement} 
                                    onNewFolder={this.onNewFolder} 
                                    onDelete={this.onDelete} 
                                    onClick={this.onClick} 
                                    onDoubleClick={this.onDoubleClick} 
                                    onSetParent={this.onSetParent} 
                                    nodes={this.makeNodes(this.state.dataSourceFolders, this.state.dataSources.filter((dataSource: DataSource) => dataSource.parent === null && dataSource.id !== -1))} 
                        />
                    </Col>
                    <Col md={6}>
                        <DataSourceComponent updateDataSources={this.refresh} types={this.state.types} dataSource={this.state.dataSource} dataSourceService={this.dataSourceService} addToast={this.addToast} />
                    </Col>
                </Row>
            </Grid>
        );
    }


    //-----------------------------------------------
    // Methods for the search tree
    //-----------------------------------------------
    private makeNodes(dataSourceFolders: DataSourceFolder[], dataSources: DataSource[]): SearchTreeNode[] {
        let nodes: SearchTreeNode[] = [];
        for (let dataSourceFolder of dataSourceFolders) {
            let childNodes = this.makeNodes(dataSourceFolder.child_folders, dataSourceFolder.children);
            let node = {
                id: dataSourceFolder.id,
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
                id: dataSource.id,
                isFolder: false,
                parent: dataSource.parent,
                icon: <Icon icon={IconNames.DOCUMENT} />,
                label: dataSource.name,
            })
        }
      
        return nodes;
    }

    private onNewElement() {
        // Create a new DataSource
        this.onClick(-1);
    }
    private onNewFolder(name: string, parent?: number, id?: number) {
        // Create a new folder
        this.dataSourceService.saveFolder({id: id, name: name, parent: parent}, this.finishUpdate.bind("TEST"));
    }

    private finishUpdate(body: {}) {
        this.refresh();
        this.addToast({ intent: Intent.SUCCESS, message: `The Update has been processed.` });
    }

    private onDelete(id: number, isFolder: boolean) {
        // Delete a dataSource or folder
        if (isFolder) {
            this.dataSourceService.deleteFolder(id, this.finishUpdate);
        } else {
            this.dataSourceService.delete(id, this.finishUpdate);
        }
    }

    private onClick(id: number) {
        // Select a dataSource
        let dataSource = this.state.dataSources.filter(item => item.id === id)[0];
        this.setState({ dataSource: dataSource });
    }

    private onDoubleClick(id: number) {
        // Open dataSource in wrangler
        this.history.push(`/recipes`)
    }

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

    private onSetParent(id: number, isFolder: boolean, parent: number) {
        // Set the parent for a dataSource
        if (isFolder) {
            // TODO: Check if you're not moving it to be its own child
            let dataSourceFolder = this.flattenDataSourceFolders(this.state.dataSourceFolders).filter(item => item.id === id)[0];
            this.dataSourceService.saveFolder({id: dataSourceFolder.id, name: dataSourceFolder.name, parent: parent}, this.finishUpdate);
        } else {
            let dataSource = this.state.dataSources.filter(item => item.id === id)[0];
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