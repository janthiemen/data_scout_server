import * as React from "react";

import {IToastProps } from "@blueprintjs/core";

import { Grid, Row, Col } from 'react-flexbox-grid';
import { PageProps } from "../../helpers/props";
import { RecipeService } from "../../helpers/userService";

import { RecipeNode, RecipesTreeWithRouter } from "./RecipeTree";
import { RecipeComponent } from "./Recipe";
import { DataSource } from "../DataSource/DataSources";
import { withRouter } from "react-router-dom";


interface RecipesState {
    dataSources: DataSource[],
    dataSource?: DataSource,
    recipes: Recipe[],
    recipe: Recipe
}

export interface Recipe {
    id: number,
    name: string,
    input: number,
    sampling_technique: string,
}

/**
 * Empty data source object.
 */
export const newRecipe = function(): Recipe {
    return {
        id: -1,
        name: "New data source",
        input: undefined,
        sampling_technique: "top"
    }
}

/**
 * The page with all the data sources.
 */
export class RecipesComponent extends React.Component<PageProps> {
    private recipeService: RecipeService;
    private addToast: (toast: IToastProps) => void;
    public state: RecipesState = {
        dataSources: [],
        dataSource: undefined,
        recipes: [],
        recipe: newRecipe()
    }

    /**
     * Creates an instance of data sources.
     * @param props 
     */
    constructor(props: PageProps) {
        super(props);
        this.recipeService = new RecipeService(props.addToast, props.setLoggedIn);
        this.setDataSources = this.setDataSources.bind(this);
        this.setRecipes = this.setRecipes.bind(this);
        this.onSelectRecipe = this.onSelectRecipe.bind(this);
        this.updateRecipes = this.updateRecipes.bind(this);
        this.addToast = props.addToast;
        this.recipeService.getDataSources(this.setDataSources);
        this.updateRecipes();
    }

    /**
     * Sets data sources
     * @param types 
     */
    public setDataSources(dataSources: []) {
        this.setState({ dataSources: dataSources["results"] });
    }

    public updateRecipes() {
        this.recipeService.get(this.setRecipes);
    }

    /**
     * Selects data source
     * @param node 
     */
    public onSelectRecipe(node: RecipeNode) {
        let recipe = this.state.recipes.filter(item => item.id === node.id)[0];
        this.setState({ recipe: recipe });
    }

    /**
     * Sets data sources based on the API response
     * @param body 
     */
    private setRecipes(body: { [key: string]: any }) {
        let recipes: Recipe[] = [];
        body["results"].forEach((result: { id: number, name: string, source: string, kwargs: string }) => {
            recipes.push({ id: result["id"], name: result["name"], input: result["input"], sampling_technique: result["sampling_technique"] });
        }); 
        recipes.push(newRecipe());
        this.setState({ recipes: recipes });
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
                        <RecipesTreeWithRouter updateRecipes={this.updateRecipes} recipeService={this.recipeService} recipes={this.state.recipes} onSelectRecipe={this.onSelectRecipe} addToast={this.addToast} />
                    </Col>
                    <Col md={6}>
                        <RecipeComponent updateRecipes={this.updateRecipes} dataSources={this.state.dataSources} recipe={this.state.recipe} recipeService={this.recipeService} addToast={this.addToast} />
                    </Col>
                </Row>
            </Grid>
        );
    }
}

export const Recipes = withRouter(RecipesComponent)