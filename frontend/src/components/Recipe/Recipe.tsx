import * as React from "react";
import autobind from 'class-autobind';

import {
    IProps, IToastProps, Intent,
    FormGroup, InputGroup, Button, HTMLSelect
} from "@blueprintjs/core";

import { RecipeService } from "../../helpers/userService";
import { DefaultItem, DefaultSelect, defaultSelectSettings } from "../../helpers/select";
import { Recipe, newRecipe } from "./Recipes";
import { DataSource } from "../DataSource/DataSources";
import PropTypes from "prop-types";
import { Join } from "../Join/JoinDialog";

/**
 * Recipe props
 */
interface RecipeProps extends IProps {
    recipeService: RecipeService,
    addToast: (toast: IToastProps, key?: string) => string;
    updateRecipes: () => void;
    dataSource?: DataSource,
    recipe: Recipe,
    dataSources: DataSource[],
    joins: Join[],
    history: any,
}

interface InputItem extends DefaultItem {
    join?: Join;
    dataSource?: DataSource;
}

/**
 * Data source state
 */
interface RecipeState {
    recipe: Recipe,
    dataSource?: DataSource,
    join?: Join,
    dataSources: DataSource[];
    joins: Join[];
}

/**
 * This class represents a data source object.
 */
export class RecipeComponent extends React.Component<RecipeProps, RecipeState> {
    static propTypes = {
        match: PropTypes.object.isRequired,
        location: PropTypes.object.isRequired,
        history: PropTypes.object.isRequired
    };
    private recipeService: RecipeService;
    private addToast: (toast: IToastProps, key?: string) => string;
    private updateRecipes: () => void;
    public state: RecipeState = {
        recipe: newRecipe(),
        dataSource: undefined,
        dataSources: [],
        joins: []
    }

    /**
     * Construct a new data source.
     * @param props The props
     */
    constructor(props: RecipeProps) {
        super(props);
        autobind(this);
        this.recipeService = props.recipeService;
        this.updateRecipes = props.updateRecipes;
        this.addToast = props.addToast;
    }

    /**
     * Called when new props are received.
     * @param props The new props
     */
    componentWillReceiveProps(props: RecipeProps) {
        this.setState({
            recipe: props.recipe,
            dataSource: props.dataSources.filter(item => item.id === props.recipe.input)[0],
            join: props.joins.filter(item => item.id === props.recipe.input_join)[0],
            joins: props.joins,
            dataSources: props.dataSources
        });
    }

    /**
     * Called when the state or the props are update. Currently only used to repopulate the field values.
     * @param prevProps The old props
     * @param prevState The old state
     */
    public componentDidUpdate(prevProps: RecipeProps, prevState: RecipeState) {
        if (this.state.dataSource !== prevState.dataSource ||
            this.state.recipe !== prevState.recipe) {
        }
    }

    /**
     * Set the input of the pipeline
     * @param item 
     */
    private onInputChange(item: InputItem) {
        this.setState({ dataSource: item.dataSource, join: item.join })
    }

    /**
     * Updates the name in the state
     * @param event 
     */
    private updateName(event: React.ChangeEvent<HTMLInputElement>) {
        let recipe = this.state.recipe;
        recipe.name = event.target.value;
        this.setState({ recipe: recipe });
    }

    /**
     * Updates the name in the state
     * @param event 
     */
    private updateSamplingTechnique(event: React.ChangeEvent<HTMLSelectElement>) {
        let recipe = this.state.recipe;
        recipe.sampling_technique = event.target.value;
        this.setState({ recipe: recipe });
    }

    /**
     * Handle the submit return
     * @param body 
     */
    private finishSubmit(body: {}) {
        if ("id" in body) {
            // There is an ID in there, so we'll set the current ID
            let recipe = this.state.recipe;
            recipe.id = body["id"];
            recipe.input = body["input"];
            this.setState({ recipe: recipe });
            this.addToast({ intent: Intent.SUCCESS, message: "The recipe has been saved" });
            this.updateRecipes();
        } else {
            this.addToast({ intent: Intent.WARNING, message: "Couldn't save the recipe." });
        }
    }

    /**
     * Submits the recipe
     */
    private submitRecipe(event: React.SyntheticEvent) {
        event.preventDefault();

        if (this.state.dataSource !== undefined || this.state.join !== undefined) {
            let data = {
                id: this.state.recipe.id,
                name: this.state.recipe.name,
                input: this.state.dataSource ? this.state.dataSource.id : null,
                input_join: this.state.join ? this.state.join.id : null
            }
            this.recipeService.save(data, this.finishSubmit);
        } else {
            this.addToast({ intent: Intent.WARNING, message: "Please select a data source first." });
        }
    }

    /**
     * Render a recipe, including a type selector and a name field, as well as the required recipe specific fields.
     */
    render() {
        let itemsJoin: InputItem[] = this.state.joins.map((join: Join) => {
            return { title: join.name, id: join.id, label: "", join: join };
        });
        let itemsDataSource: InputItem[] = this.state.dataSources.map((dataSource: DataSource) => {
            return { title: dataSource.name, id: dataSource.id, label: "", dataSource: dataSource };
        });
        let items = itemsJoin.concat(itemsDataSource);

        return <form onSubmit={this.submitRecipe}>
            <FormGroup label="Input" labelFor="input" labelInfo="(required)" helperText="The data source that will be used as input">
                <DefaultSelect {...defaultSelectSettings} items={items} onItemSelect={this.onInputChange}>
                    <Button icon="database" rightIcon="caret-down" text={this.state.dataSource ? `${this.state.dataSource.name}` : this.state.join ? this.state.join.name: "(No selection)"} />
                </DefaultSelect>
            </FormGroup>
            <FormGroup label="Name" labelFor="name" labelInfo="(required)" helperText="The human readable name of the recipe">
                <InputGroup id="name" placeholder="Placeholder text" onChange={this.updateName} value={this.state.recipe.name} />
            </FormGroup>
            <FormGroup label="Sampling technique" labelFor="sampling_technique" labelInfo="(required)" helperText="The sampling technique used in the editor">
                <HTMLSelect fill value={this.state.recipe.sampling_technique} id="samping_technique" onChange={this.updateSamplingTechnique}>
                    <option value="top">Top</option>
                    <option value="random">Random</option>
                    <option value="stratified">Stratified</option>
                </HTMLSelect>
            </FormGroup>

            <Button type="submit" icon="floppy-disk" text="Save" disabled={this.state.dataSource === undefined && this.state.join === undefined} intent={Intent.SUCCESS} />
        </form>
    }
}

