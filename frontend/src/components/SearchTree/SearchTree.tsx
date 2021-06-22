import * as React from "react";

import {
    Classes, ITreeNode, Tree, Intent,
    ContextMenu, Menu, MenuItem, MenuDivider,
    Alert, ButtonGroup, Button, IProps, Dialog, FormGroup, InputGroup
} from "@blueprintjs/core";
import { RouteComponentProps } from "react-router-dom";
import { withRouter } from "react-router";
import { ConfirmDeleteProps } from "../../helpers/props";
import { DefaultItem, DefaultSelect, defaultSelectSettings } from "../../helpers/select";
import autobind from 'class-autobind';

interface DeleteState {
    isOpen: boolean;
    title: string;
    isFolder: boolean;
    id?: number;
}

interface NewFolderState {
    isOpen: boolean;
    name: string;
    parent?: number;
    id?: number;
}

interface SetParentState {
    isOpen: boolean;
    isFolder: boolean;
    parent: DefaultItem;
    id: string;
    key: number;
}

export interface SearchTreeNode<T = {}> extends ITreeNode {
    key: number;
    onClick?: (id: number) => void;
    isFolder?: boolean;
    parent?: number;
    childNodes?: SearchTreeNode[];
}

interface SearchTreeState {
    delete: DeleteState;
    newFolder: NewFolderState;
    setParent: SetParentState;
    nodeContextMenu?: SearchTreeNode;
    nodes: SearchTreeNode[];
}

interface SearchTreeProps extends RouteComponentProps<any>, IProps {
    onNewElement: () => void;
    onNewFolder: (name: string, id?: number) => void;
    onDelete: (id: number, isFolder: boolean) => void;
    onDoubleClick: (id: number) => void;
    onSetParent: (id: string, key: number, isFolder: boolean, parent: number) => void;
    nodes: SearchTreeNode[];
    extraButton: any;
}

/**
 * This component creates a tree view.
 */
class SearchTreeComponent extends React.Component<SearchTreeProps> {
    public state: SearchTreeState = {
        delete: {isOpen: false, title: "", id: undefined, isFolder: false},
        newFolder: {isOpen: false, name: "", id: undefined, parent: undefined},
        setParent: {isOpen: false, isFolder: false, parent: undefined, id: undefined, key: undefined},
        nodeContextMenu: undefined,
        nodes: [],
    };

    /**
     * An extra button that will be displayed next to the "New" button.
     */
    private extraButton: any;
    private onNewElement: () => void;
    private onNewFolder: (name: string, parent?: number, id?: number) => void;
    private onDelete: (id: number, isFolder: boolean) => void;
    private onDoubleClick: (id: number) => void;
    private onSetParent: (id: string, key: number, isFolder: boolean, parent: number) => void;

    /**
     * Create a new data source tree.
     * @param props The props
     */
    constructor(props: SearchTreeProps) {
        super(props);
        autobind(this);

        this.onNewElement = props.onNewElement
        this.onNewFolder = props.onNewFolder
        this.onDelete = props.onDelete
        this.onDoubleClick = props.onDoubleClick
        this.onSetParent = props.onSetParent
        this.extraButton = props.extraButton
    }


    /**
     * Called when new props are received.
     * @param props The new props
     */
    componentWillReceiveProps(props: SearchTreeProps) {
        this.setState({ nodes: props.nodes })
    }

    /**
     * Create a new element.
     */
    public newElement(event: any) {
        this.onNewElement();
    }

    /**
     * Open the new folder dialog.
     */
    public openNewFolder(event: any) {
        let newFolder = this.state.newFolder;
        newFolder.isOpen = true;
        if (this.state.nodeContextMenu.isFolder) {
            newFolder.parent = Number(this.state.nodeContextMenu.key);
        }
        this.setState({newFolder: newFolder});
    }

    /**
     * Open the update folder dialog.
     */
    public openUpdateFolder(event: any) {
        if (this.state.nodeContextMenu.isFolder) {
            let newFolder = this.state.newFolder;
            newFolder.isOpen = true;
            newFolder.id = Number(this.state.nodeContextMenu.key);
            newFolder.name = String(this.state.nodeContextMenu.label);
            newFolder.parent = this.state.nodeContextMenu.parent === null ? this.state.nodeContextMenu.parent : Number(this.state.nodeContextMenu.parent);
            this.setState({newFolder: newFolder});
        }
    }

    /**
     * Close the new folder dialog.
     */
    public closeNewFolder(event: any) {
        let newFolder = this.state.newFolder;
        newFolder.isOpen = false;
        this.setState({newFolder: newFolder});
    }

    /**
     * Create a new folder.
     */
    public newFolder() {
        this.onNewFolder(this.state.newFolder.name, this.state.newFolder.parent, this.state.newFolder.id);
        this.closeNewFolder(undefined);
    }

    /**
     * Update the name of the folder in the state.
     */
    public onNewFolderName(e: React.ChangeEvent<HTMLInputElement>) {
        let newFolder = this.state.newFolder;
        newFolder.name = e.target.value;
        this.setState({newFolder: newFolder});
    }

    /**
     * Open the set parent dialog.
     */
    public openSetParent(event: any) {
        let setParent = this.state.setParent;
        setParent.isOpen = true;
        setParent.id = String(this.state.nodeContextMenu.id);
        setParent.key = Number(this.state.nodeContextMenu.key);
        setParent.isFolder = this.state.nodeContextMenu.isFolder;
        this.setState({setParent: setParent})
    }

    /**
     * Close the set parent dialog.
     */
    public closeSetParent(event: any) {
        let setParent = this.state.setParent;
        setParent.isOpen = false;
        setParent.parent = undefined;
        this.setState({setParent: setParent})
    }

    /**
     * Select the new parent of an item or folder.
     */
    public selectParent(item: DefaultItem) {
        let setParent = this.state.setParent;
        setParent.parent = item;
        this.setState({setParent: setParent})
    }

    /**
     * Set the parent of an item or folder (i.e. move it).
     */
    public setParent(event: any) {
        this.onSetParent(this.state.setParent.id, this.state.setParent.key, this.state.setParent.isFolder, this.state.setParent.parent.id);
        this.closeSetParent(undefined);
    }

    /**
     * Open the delete (confirm or cancel) dialog.
     */
    public delete(event: any) {
        this.setState({ delete: { 
            isOpen: true, 
            title: this.state.nodeContextMenu.label, 
            id: this.state.nodeContextMenu.key, 
            isFolder: this.state.nodeContextMenu.isFolder
        }});
    }

    /**
     * Cancel the delete action.
     */
    private handleDeleteCancel() {
        this.setState({ delete: { isOpen: false, title: "", id: undefined } });
    }

    /**
     * Confirm the delete action and call the delete method.
     */
    private handleDeleteConfirm() {
        this.onDelete(this.state.delete.id, this.state.delete.isFolder);
        this.setState({ delete: { isOpen: false, title: "", id: undefined } });
    }

    /**
     * Handle node click
     */
    private handleNodeClick = (nodeData: SearchTreeNode, _nodePath: number[], e: React.MouseEvent<HTMLElement>) => {
        if (nodeData.isFolder) {
            this.handleNodeCollapseExpand(nodeData);
        } else {
            nodeData.onClick(Number(nodeData.key))
        }
    };

    /**
     * Handle node double click
     */
    private handleNodeDoubleClick = (nodeData: SearchTreeNode, _nodePath: number[], e: React.MouseEvent<HTMLElement>) => {
        this.onDoubleClick(Number(nodeData.key));
    };

    /**
     * Call the double click method
     */
    private use = (event: any) => {
        this.onDoubleClick(Number(this.state.nodeContextMenu.key))
    };

    /**
     * Handle node collapse
     */
    private handleNodeCollapseExpand = (nodeData: SearchTreeNode) => {
        nodeData.isExpanded = !nodeData.isExpanded;
        this.setState(this.state);
    };


    /**
     * Show a context menu
     * @param nodeData The node
     * @param path The path to the node
     * @param e An event
     */
    public showContextMenu(nodeData: SearchTreeNode, path: any, e: any) {
        e.preventDefault();
        this.setState({ nodeContextMenu: nodeData });

        ContextMenu.show(<Menu>
            {nodeData.isFolder &&
                <MenuItem icon="edit" text="Rename" onClick={this.openUpdateFolder} />
            }
            <MenuItem icon="document" onClick={this.newElement} text="New" />
            <MenuItem icon="folder-close" onClick={this.openNewFolder} text="New folder" />
            <MenuItem icon="add-to-folder" onClick={this.openSetParent} text="Move" />
            <MenuItem icon="trash" onClick={this.delete} text="Remove" />
            <MenuDivider />
            {!nodeData.isFolder &&
                <MenuItem icon="data-lineage" text="Use" onClick={this.use} />
            }
        </Menu>, { left: e.clientX, top: e.clientY }
        );
    };

    /**
     * Render extra warning in case the user wants to delete a folder.
     */
    renderDeleteFolder() {
        if (this.state.delete.isFolder) {
            return <b><i>This will delete all subfolders and recipes in the folder!</i></b>
        } else {
            return <></>;
        }
    }

    /**
     * Flatten the folders in the tree to a list.
     * @param nodes 
     */
    flattenFolders(nodes: SearchTreeNode[]) {
        let folderItems: DefaultItem[] = [];
        for (let node of nodes) {
            if (node.isFolder) {
                folderItems.push({title: String(node.label), id: Number(node.key), label: ""});
                if (node.childNodes.length > 0) {
                    folderItems = folderItems.concat(this.flattenFolders(node.childNodes));
                }
            }
        }
        return folderItems;
    }

    /**
     * Render the tree.
     */
    render() {
        let folderSelectItems: DefaultItem[] = this.flattenFolders(this.state.nodes);

        return (
            <div>
                <Alert {... ConfirmDeleteProps} icon={"trash"} isOpen={this.state.delete.isOpen} onCancel={this.handleDeleteCancel} onConfirm={this.handleDeleteConfirm}>
                    <p>Are you sure you want to delete <b>{this.state.delete.title}</b>? <br />{this.renderDeleteFolder()}</p>
                </Alert>

                <Dialog icon="folder-close" title="New folder" isOpen={this.state.newFolder.isOpen} onClose={this.closeNewFolder}>
                    <div className={Classes.DIALOG_BODY}>
                    {/* TODO: Add input */}
                    <FormGroup label="Folder name" labelFor="input" labelInfo="(required)" helperText="What should be the name of the new folder?">
                        <InputGroup value={this.state.newFolder.name} key="new-folder-name" onChange={this.onNewFolderName} id="new-folder-name" />
                    </FormGroup>
                    </div>
                    <div className={Classes.DIALOG_FOOTER}>
                        <ButtonGroup fill>
                            <Button outlined intent={Intent.PRIMARY} onClick={this.closeNewFolder}>Cancel</Button>
                            <Button outlined intent={Intent.SUCCESS} onClick={this.newFolder}>Save</Button>
                        </ButtonGroup>
                    </div>
                </Dialog>

                <Dialog icon="folder-close" title="Move to folder" isOpen={this.state.setParent.isOpen} onClose={this.closeSetParent}>
                    <div className={Classes.DIALOG_BODY}>
                    <FormGroup label="Folder" labelFor="input" labelInfo="(required)" helperText="To which folder should it be moved?">
                        <DefaultSelect {... defaultSelectSettings} items={folderSelectItems} onItemSelect={this.selectParent}>
                            <Button icon="folder-close" rightIcon="caret-down" text={this.state.setParent.parent ? `${this.state.setParent.parent.title}` : "(No selection)"} />
                        </DefaultSelect>
                    </FormGroup>

                    </div>
                    <div className={Classes.DIALOG_FOOTER}>
                        <ButtonGroup fill>
                            <Button outlined intent={Intent.PRIMARY} onClick={this.closeSetParent}>Cancel</Button>
                            <Button outlined intent={Intent.SUCCESS} onClick={this.setParent}>Save</Button>
                        </ButtonGroup>
                    </div>
                </Dialog>

                <Tree
                    onNodeContextMenu={this.showContextMenu}
                    contents={this.state.nodes}
                    onNodeClick={this.handleNodeClick}
                    onNodeDoubleClick={this.handleNodeDoubleClick}
                    onNodeCollapse={this.handleNodeCollapseExpand}
                    onNodeExpand={this.handleNodeCollapseExpand}
                    className={Classes.ELEVATION_0}
                />

                <ButtonGroup fill={true} className="pagination">
                    <Button icon="plus" outlined onClick={this.newElement}>New</Button>
                    {this.extraButton}
                </ButtonGroup>

            </div>
        );
    }

}

export const SearchTree = withRouter(SearchTreeComponent);
