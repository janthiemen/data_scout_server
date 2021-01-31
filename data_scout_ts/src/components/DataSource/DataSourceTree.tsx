import * as React from "react";

import {
    Classes, ITreeNode, Tree, Intent, 
    ContextMenu, Menu, MenuItem, MenuDivider,
    IProps, IToastProps
} from "@blueprintjs/core";
import { DataSourceService } from "../../helpers/userService";
import { DataSource, newDataSource } from "./DataSources";
import { RouteComponentProps, withRouter } from "react-router-dom";
import { History } from 'history'

interface DataSourcesTreeState {
    dataSources: DataSource[];
    nodes: DataSourceNode[];
    nodeContextMenu?: DataSourceNode;
}

export interface DataSourceNode<T = {}> extends ITreeNode {
    isFolder?: boolean;
    childNodes?: DataSourceNode[];
}

interface DataSourcesTreeProps extends RouteComponentProps<any>, IProps {
    dataSourceService: DataSourceService;
    updateDataSources: () => void;
    onSelectDataSource: (dataSouce: DataSourceNode) => void;
    addToast: (toast: IToastProps) => void;
    dataSources: DataSource[];
}

/**
 * The component represents all of the data sources in a tree.
 */
export class DataSourcesTreeComponent extends React.Component<DataSourcesTreeProps> {
    public state: DataSourcesTreeState = { 
        dataSources: [],
        nodes: [],
        nodeContextMenu: undefined
    };
    private dataSourceService: DataSourceService;
    private updateDataSources: () => void;;
    private addToast: (toast: IToastProps) => void;
    public onSelectDataSource: (dataSouce: DataSourceNode) => void;
    private history: History;

    /**
     * Create a new data source tree.
     * @param props The props
     */
    constructor(props: DataSourcesTreeProps) {
        super(props);
        this.history = props.history;

        // This binding is necessary to make `this` work in the callback    
        this.onSelectDataSource = props.onSelectDataSource;
        this.updateDataSources = props.updateDataSources;
        this.addToast = props.addToast;
        this.dataSourceService = props.dataSourceService;
        this.showContextMenu = this.showContextMenu.bind(this);
        this.newDataSource = this.newDataSource.bind(this);
        this.finishDelete = this.finishDelete.bind(this);
        this.delete = this.delete.bind(this);
        this.useDataSource = this.useDataSource.bind(this);
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
     * Set the parent of a data source or folder (i.e. move it).
     * @param event TODO: Determine the event type
     */
    public useDataSource(event: any) {
        this.history.push(`/recipes`)
    }

    /**
     * Delete a data source or folder.
     * @param event TODO: Determine the event type
     */
    public delete(event: any) {
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
                <MenuItem icon="data-lineage" text="Use data source" onClick={this.useDataSource} />
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

export const DataSourcesTree = withRouter(DataSourcesTreeComponent);