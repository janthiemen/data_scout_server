import * as React from "react";

import {
    MenuItem, IProps, IToastProps, Intent, 
    FormGroup, InputGroup, Button, HTMLSelect
} from "@blueprintjs/core";

import { Select, ItemRenderer, ItemPredicate } from "@blueprintjs/select";

import { RecipeService } from "../../helpers/userService";
import { highlightText } from "../../helpers/select";
import { Recipe, newRecipe } from "./Recipes";
import { DataSource } from "../DataSource/DataSources";
import PropTypes from "prop-types";

/**
 * Render a data source in the select menu.
 * @param item The item to render
 * @param param1 ItemRenderer params
 */
const dataSourceRenderer: ItemRenderer<DataSource> = (item, { handleClick, modifiers, query }) => {
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
const dataSourceFilterer: ItemPredicate<DataSource> = (query, item, _index, exactMatch) => {
    const normalizedTitle = item.name.toLowerCase();
    const normalizedQuery = query.toLowerCase();

    if (exactMatch) {
        return normalizedTitle === normalizedQuery;
    } else {
        return `${normalizedTitle}`.indexOf(normalizedQuery) >= 0;
    }
};

/**
 * Data source props
 */
interface RecipeProps extends IProps {
    recipeService: RecipeService,
    addToast: (toast: IToastProps) => void;
    updateRecipes: () => void;
    dataSource?: DataSource,
    recipe: Recipe,
    dataSources: DataSource[],
    history: any,
}

/**
 * Data source state
 */
interface RecipeState {
    recipe: Recipe,
    dataSource?: DataSource,
    dataSources: DataSource[];
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
    private addToast: (toast: IToastProps) => void;
    private updateRecipes: () => void;
    public state: RecipeState = {
        recipe: newRecipe(),
        dataSource: undefined,
        dataSources: []
    }

    /**
     * Construct a new data source.
     * @param props The props
     */
    constructor(props: RecipeProps) {
        super(props);
        this.setDataSource = this.setDataSource.bind(this);
        this.updateName = this.updateName.bind(this);
        this.updateSamplingTechnique = this.updateSamplingTechnique.bind(this);
        this.submitRecipe = this.submitRecipe.bind(this);
        this.finishSubmit = this.finishSubmit.bind(this);
        this.recipeService = props.recipeService;
        this.updateRecipes = props.updateRecipes;
        this.addToast = props.addToast;
    }

    /**
     * Called when new props are received.
     * @param props The new props
     */
    componentWillReceiveProps(props: RecipeProps) {
        // TODO: Check if this selects the right one
        this.setState({
            recipe: props.recipe,
            dataSource: props.dataSources.filter(item => item.id === props.recipe.input)[0],
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
     * Change the data source type.
     * @param newType The new type
     */
    private setDataSource(newDataSource: DataSource) {
        this.setState({ dataSource: newDataSource });
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
            this.addToast({ intent: Intent.SUCCESS, message: "The data source has been saved" });
            this.updateRecipes();
        } else {
            this.addToast({ intent: Intent.WARNING, message: "Couldn't save the data source." });
        }
    }

    /**
     * Submits the recipe
     */
    private submitRecipe(event: React.SyntheticEvent) {
        event.preventDefault();

        if (this.state.dataSource !== undefined) {
            let data = {
                id: this.state.recipe.id,
                name: this.state.recipe.name,
                input: this.state.dataSource.id
            }
            this.recipeService.save(data, this.finishSubmit);
        } else {
            this.addToast({ intent: Intent.WARNING, message: "Please select a data source first." });
        }
    }

    /**
     * Render a data source, including a type selector and a name field, as well as the required data source specific fields.
     */
    render() {
        const DataSourceSelect = Select.ofType<DataSource>();

        return <form onSubmit={this.submitRecipe}>
            <FormGroup label="Input" labelFor="input" labelInfo="(required)" helperText="The data source that will be used as input">
                <DataSourceSelect
                    itemPredicate={dataSourceFilterer}
                    itemRenderer={dataSourceRenderer}
                    items={this.state.dataSources}
                    noResults={<MenuItem disabled={true} text="No results." />}
                    onItemSelect={this.setDataSource}
                >
                    <Button icon="database" rightIcon="caret-down" text={this.state.dataSource ? `${this.state.dataSource.name}` : "(No selection)"}
                    />
                </DataSourceSelect>
            </FormGroup>
            <FormGroup label="Name" labelFor="name" labelInfo="(required)" helperText="The human readable name of the data source">
                <InputGroup id="name" placeholder="Placeholder text" onChange={this.updateName} value={this.state.recipe.name} />
            </FormGroup>
            <FormGroup label="Sampling technique" labelFor="sampling_technique" labelInfo="(required)" helperText="The sampling technique used in the editor">
                <HTMLSelect fill value={this.state.recipe.sampling_technique} id="samping_technique" onChange={this.updateSamplingTechnique}>
                    <option value="top">Top</option>
                    <option value="random">Random</option>
                    <option value="stratified">Stratified</option>
                </HTMLSelect>
            </FormGroup>

            <Button type="submit" icon="floppy-disk" text="Save" disabled={this.state.dataSource === undefined} intent={Intent.SUCCESS} />
        </form>
    }
}

