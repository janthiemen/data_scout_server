import * as React from "react";
import autobind from 'class-autobind';

import { Icon, Intent, IToastProps } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import { History } from 'history'

import { Grid, Row, Col } from 'react-flexbox-grid';
import { PageProps } from "../../helpers/props";
import { RecipeService } from "../../helpers/userService";

import { RecipeComponent } from "./Recipe";
import { DataSource } from "../DataSource/DataSources";
import { SearchTree, SearchTreeNode } from "../SearchTree/SearchTree";
import { withRouter } from "react-router-dom";
import { Join } from "../Join/JoinDialog";

export interface Recipe {
    id: number,
    name: string,
    parent?: number,
    input: number,
    input_join: number,
    sampling_technique: string,
    schema?: {[key: string]: string},
}

export interface RecipeFolder {
    id: number,
    parent: number,
    name: string,
    child_folders: RecipeFolder[],
    children: Recipe[],
}


interface RecipesState {
    joins: Join[],
    dataSources: DataSource[],
    dataSource?: DataSource,
    recipes: Recipe[],
    recipeFolders: RecipeFolder[],
    recipe: Recipe,
}


/**
 * Empty recipe object.
 */
export const newRecipe = function(): Recipe {
    return {
        id: -1,
        name: "New recipe",
        input: undefined,
        input_join: undefined,
        parent: undefined,
        sampling_technique: "top"
    }
}

/**
 * Parse a recipe.
 * @param recipe 
 */
export const parseRecipe = function(recipe: {}): Recipe {
    return {
        id: recipe["id"],
        name: recipe["name"],
        input: recipe["input"],
        input_join: recipe["input_join"], 
        parent: recipe["parent"],
        sampling_technique: recipe["sampling_technique"],
        schema: JSON.parse(recipe["schema"])
    }
}

/**
 * The page with all the pipelines.
 */
export class RecipesComponent extends React.Component<PageProps> {
    private recipeService: RecipeService;
    private addToast: (toast: IToastProps, key?: string) => string;
    private history: History;
    public state: RecipesState = {
        joins: [],
        dataSources: [],
        dataSource: undefined,
        recipes: [],
        recipeFolders: [],
        recipe: newRecipe(),
    }

    /**
     * Creates an instance of recipes.
     * @param props 
     */
    constructor(props: PageProps) {
        super(props);
        autobind(this);
        this.recipeService = new RecipeService(props.addToast, props.setLoggedIn);
        this.history = props.history;

        this.addToast = props.addToast;
        this.recipeService.getDataSources(this.setDataSources);
        this.recipeService.getJoins(this.setJoins);
        this.refresh();
    }

    /**
     * Receive the folders
     * @param folders 
     */
    public setFolders(folders: any) {
        this.setState({ recipeFolders: folders["results"] });
    }

    /**
     * Receive the data sources
     * @param types 
     */
    public setDataSources(dataSources: []) {
        this.setState({ dataSources: dataSources["results"] });
    }
    /**
     * Receive the joins
     * @param joins 
     */
    public setJoins(joins: {}) {
        this.setState({ joins: joins["results"] });
    }

    /**
     * Refresh the data
     */
    public refresh() {
        this.recipeService.getFolders(this.setFolders);
        this.recipeService.get(this.setRecipes);
    }

    /**
     * Receive the recipes
     * @param body 
     */
    private setRecipes(body: { [key: string]: any }) {
        let recipes: Recipe[] = body["results"].map((recipe: {}) => parseRecipe(recipe));
        recipes.push(newRecipe());
        this.setState({ recipes: recipes });
    }

    /**
     * Renders recipes
     * @returns  
     */
    render() {
        return (
            <Grid fluid>
                <Row>
                    <Col md={3}>
                        <SearchTree onNewElement={this.onNewElement} 
                                    onNewFolder={this.onNewFolder} 
                                    onDelete={this.onDelete} 
                                    onDoubleClick={this.onDoubleClick} 
                                    onSetParent={this.onSetParent} 
                                    extraButton={<></>}
                                    nodes={this.makeNodes(this.state.recipeFolders, this.state.recipes.filter((recipe: Recipe) => recipe.parent === null && recipe.id !== -1))} 
                        />
                    </Col>
                    <Col md={6}>
                        <RecipeComponent updateRecipes={this.refresh} dataSources={this.state.dataSources} joins={this.state.joins} recipe={this.state.recipe} recipeService={this.recipeService} addToast={this.addToast} />
                    </Col>
                </Row>
            </Grid>
        );
    }


    /**
     * Create the nodes that make up the tree.
     * @param recipeFolders The folders
     * @param recipes The recipes
     */
    private makeNodes(recipeFolders: RecipeFolder[], recipes: Recipe[]): SearchTreeNode[] {
        let nodes: SearchTreeNode[] = [];
        for (let recipeFolder of recipeFolders) {
            let childNodes = this.makeNodes(recipeFolder.child_folders, recipeFolder.children);
            let node = {
                id: `F-${recipeFolder.id}`,
                key: recipeFolder.id,
                icon: <Icon icon={IconNames.FOLDER_CLOSE} />,
                isExpanded: false,
                parent: recipeFolder.parent,
                label: recipeFolder.name,
                isFolder: true,
                hasCaret: childNodes.length > 0,
                childNodes: childNodes
            };
            nodes.push(node);
        }
        for (let recipe of recipes) {
            nodes.push({
                id: `R-${recipe.id}`,
                key: recipe.id,
                onClick: this.onClick,
                isFolder: false,
                parent: recipe.parent,
                icon: <Icon icon={IconNames.DOCUMENT} />,
                label: recipe.name,
            })
        }
      
        return nodes;
    }

    /**
     * Create a new reco[e].
     */
    private onNewElement() {
        // Create a new Recipe
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
        this.recipeService.saveFolder({id: id, name: name, parent: parent}, this.finishUpdate.bind("TEST"));
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
     * Delete a recipe or folder
     * @param id 
     * @param isFolder 
     */
    private onDelete(id: number, isFolder: boolean) {
        // Delete a recipe or folder
        if (isFolder) {
            this.recipeService.deleteFolder(id, this.finishUpdate);
        } else {
            this.recipeService.delete(id, this.finishUpdate);
        }
    }

    /**
     * Select a recipe
     * @param id 
     */
    private onClick(id: number) {
        let recipe = this.state.recipes.filter(item => item.id === id)[0];
        this.setState({ recipe: recipe });
    }

    /**
     * Open the wrangler with this pipeline.
     * @param id 
     */
    private onDoubleClick(id: number) {
        // Open recipe in wrangler
        this.history.push(`/wrangler/${id}`)
    }

    /**
     * Get a list of all recipe folders (instead of a tree).
     * @param dataSourceFolders 
     */
    private flattenRecipeFolders(recipeFolders: RecipeFolder[]) {
        let folderItems: RecipeFolder[] = [];
        for (let recipeFolder of recipeFolders) {
            folderItems.push(recipeFolder);
            if (recipeFolder.child_folders.length > 0) {
                folderItems = folderItems.concat(this.flattenRecipeFolders(recipeFolder.child_folders));
            }
        }
        return folderItems;
    }

    /**
     * Set the parent for a folder or recipe.
     * @param id The ID in the tree
     * @param key The ID of the object that is selected
     * @param isFolder Whether the item is a folder or not
     * @param parent The new parent of the object
     */
    private onSetParent(id: string, key: number, isFolder: boolean, parent: number) {
        // Set the parent for a recipe
        if (isFolder) {
            // TODO: Check if you're not moving it to be its own child
            let recipeFolder = this.flattenRecipeFolders(this.state.recipeFolders).filter(item => item.id === key)[0];
            this.recipeService.saveFolder({id: recipeFolder.id, name: recipeFolder.name, parent: parent}, this.finishUpdate);
        } else {
            let recipe = this.state.recipes.filter(item => item.id === key)[0];
            recipe.parent = parent;
            this.recipeService.save(recipe, this.finishUpdate);
        }
    }
}

export const Recipes = withRouter(RecipesComponent)