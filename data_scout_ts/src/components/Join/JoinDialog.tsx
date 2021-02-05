import * as React from "react";
import autobind from 'class-autobind';
import { HTMLSelect, FormGroup, Button, Dialog, MultistepDialog, Classes, Intent, InputGroup, TextArea, Card, Elevation, ControlGroup, DialogStep, IToastProps } from "@blueprintjs/core";
import { Grid, Row, Col } from 'react-flexbox-grid';
import { DefaultItem, DefaultSelect, defaultSelectSettings } from "../../helpers/select";

import { JoinService } from "../../helpers/userService";
import { parseRecipe, Recipe } from "../Recipe/Recipes";
import { DataSource, parseDataSource } from "../DataSource/DataSources";


interface JoinDialogProps {
    onClose: () => void,
    joinService: JoinService,
    join: Join,
    isOpen: boolean,
}

interface JoinItem extends DefaultItem {
    recipe?: Recipe;
    dataSource?: DataSource;
}

export interface Join {
    id: number;
    name: string;
    data_source_left?: DataSource;
    recipe_left?: Recipe;
    data_source_right?: DataSource;
    recipe_right?: Recipe;
    field_left: string;
    field_right: string;
    method: string;
}

interface JoinState {
    id: number,
    name: string,
    left: JoinItem,
    left_type: string,
    right: JoinItem,
    right_type: string,
    method: string,
    fields: string[][]
}

interface JoinDialogState {
    onClose: () => void,
    isOpen: boolean,
    recipes: Recipe[],
    dataSources: DataSource[],
    join: JoinState
}

export class JoinDialog extends React.Component<JoinDialogProps, JoinDialogState> {
    private joinService: JoinService;

    private dataSourceToItem(dataSource: DataSource): JoinItem {
        if (dataSource === undefined || dataSource === null) {
            return undefined;
        } else {
            return {
                title: dataSource["name"], 
                id: dataSource["id"], 
                label: "", 
                dataSource: parseDataSource(dataSource)
            };
        }
    }

    private recipeToItem(recipe: Recipe): JoinItem {
        if (recipe === undefined || recipe === null) {
            return undefined;
        } else {
            return {
                title: recipe["name"], 
                id: recipe["id"], 
                label: "", 
                recipe: parseRecipe(recipe)
            };
        }
    }

    private parseJoin(join: Join) {
        if (join === undefined) {
            return {
                id: -1,
                name: "",
                left: undefined,
                left_type: "data_source",
                right: undefined,
                right_type: "data_source",
                method: "inner",
                fields: [],
            };
        }
        let dataSourceLeft = this.dataSourceToItem(join["data_source_left"])
        let recipeLeft = this.recipeToItem(join["recipe_left"])
        let dataSourceRight = this.dataSourceToItem(join["data_source_right"])
        let recipeRight = this.recipeToItem(join["recipe_right"])

        let fieldsLeft = join["field_left"].split(",");
        let fieldsRight = join["field_right"].split(",");
        let fields = fieldsLeft.map(function(e, i) {
            return [e, fieldsRight[i]];
        });
        return {
            id: join["id"],
            name: join["name"],
            left: dataSourceLeft !== undefined ? dataSourceLeft : recipeLeft,
            left_type: dataSourceLeft !== undefined ? "pipeline" : "data_source",
            right: dataSourceRight !== undefined ? dataSourceRight : recipeRight,
            right_type: recipeRight !== undefined ? "pipeline" : "data_source",
            method: join["method"],
            fields: fields,
        };
    }

    constructor(props: JoinDialogProps) {
        super(props);
        this.joinService = props.joinService;
        autobind(this);

        this.state = {
            join: this.parseJoin(props.join),
            isOpen: props.isOpen,
            recipes: [],
            dataSources: [],
            onClose: props.onClose
        };

        this.joinService.getRecipes(this.getRecipes)
        this.joinService.getDataSources(this.getDataSources)
    }

    public getRecipes(body: {}) {
        let recipes = body["results"].map((recipe: { [key: string]: string }) => parseRecipe(recipe));
        this.setState({ recipes: recipes })
    }

    public getDataSources(body: {}) {
        let dataSources = body["results"].map((dataSource: { [key: string]: string }) => parseDataSource(dataSource));
        this.setState({ dataSources: dataSources })
    }

    /**
     * Called when new props are received.
     * @param props The new props
     */
    componentWillReceiveProps(props: JoinDialogProps) {
        this.setState({
            isOpen: props.isOpen,
            onClose: props.onClose,
            join: this.parseJoin(props.join),
        });
    }

    /**
     * Saves the join.
     */
    private save() {
        // TODO: Set the methd
        let join: JoinState = this.state.join;
        this.joinService.save({
            "id": join.id,
            "name": join.name,
            "data_source_left": join.left.dataSource === undefined ? null : join.left.dataSource.id,
            "recipe_left": join.left.recipe === undefined ? null : join.left.recipe.id,
            "data_source_right": join.right.dataSource === undefined ? null : join.right.dataSource.id,
            "recipe_right": join.right.recipe === undefined ? null : join.right.recipe.id,
            "field_left": join.fields.map(fields => fields[0]).join(","),
            "field_right": join.fields.map(fields => fields[1]).join(","),
            "method": join.method
        }, this.saveFinish)
    }

    private saveFinish(body: {}) {
        if ("id" in body) {
            this.joinService.addToast({ intent: Intent.SUCCESS, message: `The join has been save.` });
            this.setState({isOpen: false});
        } else {
            this.joinService.addToast({ intent: Intent.SUCCESS, message: `The was an error while saving the join.` });
        }
    }

    /**
     * Set the type of the left or right input.
     */
    public onInputTypeChange(event: React.ChangeEvent<HTMLSelectElement>) {
        let join: JoinState = this.state.join;
        if (event.target.dataset["side"] == "left") {
            join.left_type = event.target.value;
        } else {
            join.right_type = event.target.value;
        }
        this.setState({ join: join });
    }

    /**
     * Set the left or right input
     */
    public onInputLeftChange(item: JoinItem) {
        let join: JoinState = this.state.join;
        join.left = item;
        this.setState({ join: join });
    }
    public onInputRightChange(item: JoinItem) {
        let join: JoinState = this.state.join;
        join.right = item;
        this.setState({ join: join });
    }

    /**
     * Set the parent of an item or folder (i.e. move it).
     */
    public onInputFieldChange(event: React.ChangeEvent<HTMLSelectElement>) {
        let join: JoinState = this.state.join;
        let side = event.target.dataset["side"] === "left" ? 0 : 1;
        join.fields[event.target.dataset["field"]][side] = event.target.value;
        this.setState({ join: join });

    }

    public addField() {
        let join: JoinState = this.state.join;
        join.fields.push(["", ""]);
        this.setState({ join: join });
    }

    public onMethodChange(event: React.ChangeEvent<HTMLSelectElement>) {
        let join: JoinState = this.state.join;
        join.method = event.target.value
        this.setState({ join: join });
    }

    public onInputNameChange(event: React.ChangeEvent<HTMLInputElement>) {
        let join: JoinState = this.state.join;
        join.name = event.target.value
        this.setState({ join: join });
    }

    private getSchema(item: JoinItem) {
        if (item !== undefined) {
            if (item.recipe !== undefined) {
                return item.recipe.schema;
            } else {
                return item.dataSource.schema;
            }
        } else {
            return {};
        }
    }

    /**
     * Renders transformation dialog.
     * @returns  
     */
    render() {
        let join: JoinState = this.state.join;
        let itemsRecipe: JoinItem[] = this.state.recipes.map((recipe: Recipe) => {
            return { title: recipe.name, id: recipe.id, label: "", recipe: recipe };
        });
        let itemsDataSource: JoinItem[] = this.state.dataSources.map((dataSource: DataSource) => {
            return { title: dataSource.name, id: dataSource.id, label: "", dataSource: dataSource };
        });
        let itemsLeft = join.left_type == "pipeline" ? itemsRecipe : itemsDataSource;
        let itemsRight = join.right_type == "pipeline" ? itemsRecipe : itemsDataSource;

        // [{ title: "a", id: 1, label: "" }, { title: "b", id: 2, label: "" }, { title: "c", id: 3, label: "" }]

        return <MultistepDialog icon="data-lineage" title={"Join"} isOpen={this.state.isOpen} onClose={this.state.onClose}
            finalButtonProps={{ intent: "primary", onClick: this.save, text: "Save" }}>
            <DialogStep
                id="left" title="Left"
                panel={
                    <div className={Classes.DIALOG_BODY}>
                        <p>Which data source or recipe should be used as the input on the left side of the join?</p>
                        <FormGroup labelFor="input">
                            <ControlGroup fill>
                                <HTMLSelect value={join.left_type} data-side="left" onChange={this.onInputTypeChange}>
                                    <option value="data_source">Data source</option>
                                    <option value="pipeline">Pipeline</option>
                                </HTMLSelect>
                                <DefaultSelect {...defaultSelectSettings} items={itemsLeft} onItemSelect={this.onInputLeftChange}>
                                    <Button icon="database" rightIcon="caret-down" text={join.left ? `${join.left.title}` : "(No selection)"} />
                                </DefaultSelect>
                            </ControlGroup>
                        </FormGroup>
                    </div>
                }
            />
            <DialogStep
                id="right" title="Right"
                panel={
                    <div className={Classes.DIALOG_BODY}>
                        <p>Which data source or recipe should be used as the input on the right side of the join?</p>
                        <FormGroup labelFor="input">
                            <ControlGroup fill>
                                <HTMLSelect value={join.right_type} data-side="right" onChange={this.onInputTypeChange}>
                                    <option value="data_source">Data source</option>
                                    <option value="pipeline">Pipeline</option>
                                </HTMLSelect>
                                <DefaultSelect {...defaultSelectSettings} items={itemsRight} onItemSelect={this.onInputRightChange}>
                                    <Button icon="database" rightIcon="caret-down" text={join.right ? `${join.right.title}` : "(No selection)"} />
                                </DefaultSelect>
                            </ControlGroup>
                        </FormGroup>
                    </div>
                }
            />
            <DialogStep
                id="fields" title="Fields"
                panel={
                    <div className={Classes.DIALOG_BODY}>
                        <p>On which fields should the data be joined?</p>
                        <FormGroup labelFor="input">
                            {join.fields.map((field: string[], i: number) =>
                                <ControlGroup fill className="input-multiple-card">
                                    <HTMLSelect value={field[0]} data-field={i} data-side="left" onChange={this.onInputFieldChange}>
                                        <option></option>
                                        {Object.entries(this.getSchema(join.left)).map(([key, val]) => <option value={key}>{key} ({val})</option>)}
                                    </HTMLSelect>
                                    <HTMLSelect value={field[1]} data-field={i} data-side="right" onChange={this.onInputFieldChange}>
                                        <option></option>
                                        {Object.entries(this.getSchema(join.right)).map(([key, val]) => <option value={key}>{key} ({val})</option>)}
                                    </HTMLSelect>
                                </ControlGroup>
                            )}

                            <Button fill icon="plus" className="input-multiple-card" onClick={this.addField}>Add</Button>
                        </FormGroup>
                    </div>
                }
            />
            <DialogStep
                id="method" title="Method"
                panel={
                    <div className={Classes.DIALOG_BODY}>
                        <p>What should be the name of the join?</p>
                        <FormGroup labelFor="input" label="Name">
                            <InputGroup value={this.state.join.name} onChange={this.onInputNameChange} />
                        </FormGroup>
                        <p>How should the sides be joined?</p>
                        <FormGroup labelFor="input" label="Method">
                            <HTMLSelect value={join.method} onChange={this.onMethodChange}>
                                <option value="inner">Inner</option>
                                <option value="outer">Outer</option>
                                <option value="left">Left</option>
                                <option value="right">Right</option>
                            </HTMLSelect>
                        </FormGroup>
                    </div>
                }
            />
        </MultistepDialog>
    }
}
