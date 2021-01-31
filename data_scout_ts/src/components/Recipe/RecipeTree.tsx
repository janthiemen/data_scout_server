import * as React from "react";

import {
    Classes, ITreeNode, Tree, Intent, 
    ContextMenu, Menu, MenuItem, MenuDivider,
    IToastProps, Alert
} from "@blueprintjs/core";
import { RecipeService } from "../../helpers/userService";
import { Recipe, newRecipe } from "./Recipes";
import { RouteComponentProps } from "react-router-dom";
import { History } from 'history'
import { withRouter } from "react-router";

interface DeleteState {
    isOpen: boolean;
    title: string;
    id?: number;
}

interface RecipesTreeState {
    recipes: Recipe[];
    nodes: RecipeNode[];
    nodeContextMenu?: RecipeNode;
    delete: DeleteState;
}

export interface RecipeNode<T = {}> extends ITreeNode {
    isFolder?: boolean;
    childNodes?: RecipeNode[];
}

interface RecipesTreeProps extends RouteComponentProps<any>, React.Props<any> {
// interface RecipesTreeProps extends IProps {
    recipeService: RecipeService;
    updateRecipes: () => void;
    onSelectRecipe: (dataSouce: RecipeNode) => void;
    addToast: (toast: IToastProps) => void;
    recipes: Recipe[];
}

/**
 * The component represents all of the data sources in a tree.
 */
class RecipesTree extends React.Component<RecipesTreeProps> {
    public state: RecipesTreeState = { 
        recipes: [],
        nodes: [],
        nodeContextMenu: undefined,
        delete: {
            isOpen: false,
            title: "",
            id: undefined
        }
    };
    private history: History;
    private recipeService: RecipeService;
    private updateRecipes: () => void;;
    private addToast: (toast: IToastProps) => void;
    public onSelectRecipe: (dataSouce: RecipeNode) => void;

    /**
     * Create a new data source tree.
     * @param props The props
     */
    constructor(props: RecipesTreeProps) {
        super(props);
        this.history = props.history;

        // This binding is necessary to make `this` work in the callback    
        this.onSelectRecipe = props.onSelectRecipe;
        this.updateRecipes = props.updateRecipes;
        this.addToast = props.addToast;
        this.recipeService = props.recipeService;
        this.showContextMenu = this.showContextMenu.bind(this);
        this.newRecipe = this.newRecipe.bind(this);
        this.finishDelete = this.finishDelete.bind(this);
        this.delete = this.delete.bind(this);
        this.useRecipe = this.useRecipe.bind(this);
        this.handleNodeClick = this.handleNodeClick.bind(this);
        this.handleDeleteCancel = this.handleDeleteCancel.bind(this);
        this.handleDeleteConfirm = this.handleDeleteConfirm.bind(this);
    }

    
    /**
     * Called when new props are received.
     * @param props The new props
     */
    componentWillReceiveProps(props: RecipesTreeProps) {
        let nodes: RecipeNode[] = [];
        for (let recipe of props.recipes) {
            nodes.push(this.convertRecipeToNode(recipe));
        }
        this.setState({ recipes: props.recipes, nodes: nodes });
    }

    /**
     * Create a new data source.
     * @param event TODO: Determine the event type
     */
    public newRecipe(event: any) {
        this.onSelectRecipe(this.convertRecipeToNode(newRecipe()));
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
     */
    public delete(event: any) {
        this.setState({ delete: {isOpen: true, title: this.state.nodeContextMenu.label, id: this.state.nodeContextMenu.id} });        
    }

    private handleDeleteCancel() {
        this.setState({ delete: {isOpen: false, title: "", id: undefined} });        
    }

    private handleDeleteConfirm() {
        this.recipeService.delete(this.state.delete.id, this.finishDelete);
        this.setState({ delete: {isOpen: false, title: "", id: undefined} });        
    }

    public finishDelete(body: {}) {
        this.addToast({ intent: Intent.SUCCESS, message: "The recipe has been deleted." });
        this.updateRecipes();
    }

    /**
     * Show a context menu
     * @param nodeData The node
     * @param path The path to the node
     * @param e An event
     */
    public showContextMenu(nodeData: RecipeNode, path: any, e: any) {
        e.preventDefault();
        this.setState({ nodeContextMenu: nodeData });

        ContextMenu.show(<Menu>
            <MenuItem icon="document" onClick={this.newRecipe} text="New recipe" />
            {/* <MenuItem icon="folder-close" onClick={this.newFolder} text="New folder" /> */}
            {/* <MenuItem icon="add-to-folder" onClick={this.setParent} text="Move" /> */}
            <MenuItem icon="trash" onClick={this.delete} text="Remove" />
            <MenuDivider />
            {!nodeData.isFolder &&
                <MenuItem icon="data-lineage" text="Use recipe" onClick={this.useRecipe} />
            }
        </Menu>, { left: e.clientX, top: e.clientY }
        );
    };

    /**
     * Converts data source to node
     * @param recipe 
     * @returns data source to node 
     */
    private convertRecipeToNode(recipe: Recipe): RecipeNode {
        return { id: recipe.id, icon: "document", label: recipe.name };
    }

    /**
     * Render the tree.
     */
    render() {
        return (
            <div>
                <Alert
                    canEscapeKeyCancel={true}
                    canOutsideClickCancel={true}
                    cancelButtonText="No"
                    confirmButtonText="Yes"
                    icon="trash"
                    intent={Intent.DANGER}
                    isOpen={this.state.delete.isOpen}
                    onCancel={this.handleDeleteCancel}
                    onConfirm={this.handleDeleteConfirm}
                >
                    <p>Are you sure you want to delete <b>{this.state.delete.title}</b>?</p>
                </Alert>

                <Tree
                    onNodeContextMenu={this.showContextMenu}
                    contents={this.state.nodes}
                    onNodeClick={this.handleNodeClick}
                    onNodeDoubleClick={this.handleNodeDoubleClick}
                    onNodeCollapse={this.handleNodeCollapse}
                    onNodeExpand={this.handleNodeExpand}
                    className={Classes.ELEVATION_0}
                />
            </div>
        );
    }

    /**
     * Handle node click of data sources tree
     */
    private handleNodeClick = (nodeData: RecipeNode, _nodePath: number[], e: React.MouseEvent<HTMLElement>) => {
        const originallySelected = nodeData.isSelected;
        if (!e.shiftKey) {
            this.forEachNode(this.state.nodes, n => (n.isSelected = false));
        }
        nodeData.isSelected = originallySelected == null ? true : !originallySelected;
        this.setState(this.state);
        this.onSelectRecipe(nodeData);
    };

    /**
     * Handle node click of data sources tree
     */
    private handleNodeDoubleClick = (nodeData: RecipeNode, _nodePath: number[], e: React.MouseEvent<HTMLElement>) => {
        this.history.push(`/wrangler/${nodeData.id}`)
    };

    /**
     * Open the wrangler from the context menu
     */
    private useRecipe = (event: any) => {
        this.history.push(`/wrangler/${this.state.nodeContextMenu.id}`)
    };

    /**
     * Handle node collapse of data sources tree
     */
    private handleNodeCollapse = (nodeData: RecipeNode) => {
        nodeData.isExpanded = false;
        this.setState(this.state);
    };

    /**
     * Handle node expand of data sources tree
     */
    private handleNodeExpand = (nodeData: RecipeNode) => {
        nodeData.isExpanded = true;
        this.setState(this.state);
    };

    /**
     * For each node
     * @param nodes 
     * @param callback 
     * @returns  
     */
    private forEachNode(nodes: RecipeNode[] | undefined, callback: (node: RecipeNode) => void) {
        if (nodes == null) {
            return;
        }

        for (const node of nodes) {
            callback(node);
            this.forEachNode(node.childNodes, callback);
        }
    }
}

export const RecipesTreeWithRouter = withRouter(RecipesTree);
