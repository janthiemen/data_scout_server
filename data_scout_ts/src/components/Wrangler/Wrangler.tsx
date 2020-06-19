import * as React from "react";

import { DataColumn } from "./DataColumn"
import { PageProps } from "../../helpers/props";
import { Row, Col, Grid } from "react-flexbox-grid";
import { DataTable } from "./DataTable";
import { Tabs, Tab, H3, Intent, IToastProps, HTMLTable, Divider } from "@blueprintjs/core";
import { WranglerService } from "../../helpers/userService";
import { ReactSortable, Sortable, SortableEvent } from "react-sortablejs";

import { Transformation, TRANSFORMATIONS } from "./Transformation"
import { TransformationButton } from "./TransformationButton"
import { TransformationDialog } from "./TransformationDialog"
import { MathPanel } from "./panels/MathPanel"
import { TextPanel } from "./panels/TextPanel"
import { CustomPanel } from "./panels/CustomPanel"
import { SettingsPanel } from "./panels/SettingsPanel"

const DUMMY_DATA = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]];
const DUMMY_COLUMNS = ["Loading", "Loading", "Loading", "Loading"]


interface WranglerState {
    columns: DataColumn[];
    isOpen: boolean;
    loading: boolean;
    recipe: number;
    recipeStep: number;
    transformationsUpdating: number[];
    recipeObject?: Recipe;
    selectedTransformation?: Transformation;
    data: number[][];
}


interface Recipe {
    id: number,
    input: number,
    name: string,
    output: number,
    transformations: Transformation[]
}


export class Wrangler extends React.Component<PageProps, WranglerState> {
    private wranglerService: WranglerService;
    private addToast: (toast: IToastProps) => void;

    constructor(props: any) {
        super(props);
        this.wranglerService = new WranglerService(props.addToast, props.setLoggedIn);

        this.state = {
            recipe: 1,
            isOpen: false,
            loading: true,
            recipeStep: 3,
            transformationsUpdating: [],
            recipeObject: undefined,
            columns: this.createColumns(DUMMY_COLUMNS),
            data: DUMMY_DATA,
        };

        this.addToast = props.addToast;
        this.getData = this.getData.bind(this);
        this.receiveData = this.receiveData.bind(this);
        this.receiveRecipe = this.receiveRecipe.bind(this);
        this.handleOpenTransformation = this.handleOpenTransformation.bind(this);
        this.handleCloseTransformation = this.handleCloseTransformation.bind(this);
        this.createTransformation = this.createTransformation.bind(this);
        this.deleteTransformation = this.deleteTransformation.bind(this);
        this.finishUpdate = this.finishUpdate.bind(this);
        this.finishUpdateOrdering = this.finishUpdateOrdering.bind(this);
        this.endUpdateOrdering = this.endUpdateOrdering.bind(this);
        this.newTransformation = this.newTransformation.bind(this);
        this.refresh = this.refresh.bind(this);
        this.refresh();
    }

    /**
     * Refresh the recipe and the data
     */
    private refresh() {
        this.setState({ loading: true });
        this.getData();
        this.getRecipe();
    }

    /**
     * Get the data.
     */
    public getData() {
        this.wranglerService.getData(this.state.recipe, this.state.recipeStep, this.receiveData)
    }

    /**
     * Get the recipe
     */
    public getRecipe() {
        this.wranglerService.getRecipe(this.state.recipe, this.receiveRecipe)
    }

    /**
     * Receive the recipe (receiveRecipe callback).
     */
    public receiveRecipe(body: { [key: string]: any }) {
        let transformation = body.transformations.filter((item: any) => item["previous"] === null)[0];
        let transformations = [];
        while (transformation !== undefined) {
            let nextId = transformation["id"];
            transformations.push(transformation);
            transformation = body.transformations.filter((item: any) => item["previous"] !== null && item["previous"] === nextId)[0];
        }
        body["transformations"] = transformations;
        this.setState({ recipeObject: body as Recipe });
    }

    /**
     * Creates a new transformation.
     * @param transformation The name of the transformation
     * @param kwargs The arguments
     */
    protected createTransformation(transformation: string, kwargs: { [key: string]: any }) {
        this.wranglerService.postTransformation({
            id: 0,
            kwargs: JSON.stringify(kwargs),
            previous: this.getTransformations().length > 0 ? this.getTransformations()[this.getTransformations().length - 1].id : null,
            next: [],
            recipe: this.state.recipe,
            transformation: transformation,
        }, this.finishUpdate);
    }

    protected finishUpdate(body: { [key: string]: any }) {
        this.refresh();
    }

    private createColumns(column_names: string[]): DataColumn[] {
        let columns: DataColumn[] = [];
        for (let c in column_names) {
            columns.push(new DataColumn(column_names[c], parseInt(c), this.createTransformation))
        }
        return columns;
    }

    /**
     * Receive the data (getData callback).
     */
    public receiveData(body: { [key: string]: any }) {
        if (body["success"]) {
            let columns = this.createColumns(body["data"]["columns"]);
            this.setState({ columns: columns, data: body["data"]["records"], loading: false });
        } else {
            if (body["messages"] != null &&
                typeof body["messages"][Symbol.iterator] === 'function') {
                for (let message of body["messages"]) {
                    this.addToast({
                        intent: Intent.DANGER,
                        message: `${message["code"]}: ${message["message"]}`,
                    });
                }
            } else {
                console.log(body["messages"]);
            }
        }
    }

    /**
     * Gets the transformations from the state
     * @returns transformations 
     */
    private getTransformations(): Transformation[] {
        if (this.state.recipeObject !== undefined) {
            return this.state.recipeObject.transformations;
        }
        return [];
    }

    /**
     * Handles the opening of the transformation dialog.
     * @param transformation 
     */
    private handleOpenTransformation(transformation: Transformation) {
        this.setState({ isOpen: true, selectedTransformation: transformation });
    }

    /**
     * Handles the closing of the transformation dialog.
     */
    private handleCloseTransformation = () => this.setState({ isOpen: false });

    private deleteTransformation(transformation: Transformation) {
        this.wranglerService.deleteTransformation(transformation.id, this.finishUpdate);
    }

    /**
     * Renders transformation button
     * @param transformation 
     * @param index 
     * @returns  
     */
    public renderTransformationButton(transformation: Transformation, index: number) {
        return <TransformationButton key={transformation.id} deleteTransformation={this.deleteTransformation}
            transformation={transformation} index={index} handleOpen={this.handleOpenTransformation} />
    }

    /**
     * Renders transformation dialog
     * @returns  
     */
    public renderTransformationDialog(transformation?: Transformation) {
        if (transformation === undefined && this.state.selectedTransformation !== undefined) {
            transformation = this.state.selectedTransformation;
        }
        if (transformation !== undefined) {
            return <TransformationDialog
                setTransformation={this.refresh}
                wranglerService={this.wranglerService}
                isOpen={this.state.isOpen}
                transformation={transformation}
                onClose={this.handleCloseTransformation} 
                columns={this.state.columns.map(value => value.getName())}/>
        } else {
            return <span></span>;
        }
    }

    /**
     * Creates a new transformation.
     * @param transformation 
     */
    protected newTransformation(transformationType: string) {
        if (this.state.recipeObject === undefined) {
            this.addToast({
                intent: Intent.DANGER,
                message: `No recipe has been loaded yet.`,
            });
        } else if (transformationType in TRANSFORMATIONS) {
            let previous = this.state.recipeObject.transformations[this.state.recipeObject.transformations.length - 1].id

            // Initialize the kwargs with their default values
            let kwargs: { [key: string]: any } = {};
            for (let [key, value] of Object.entries(TRANSFORMATIONS[transformationType]["fields"])) {
                kwargs[key] = value["default"];
            }

            let transformation: Transformation = { id: -1, kwargs: JSON.stringify(kwargs), previous: previous, next: [], recipe: this.state.recipe, transformation: transformationType };
            this.handleOpenTransformation(transformation);
            this.renderTransformationDialog(transformation); 
        } else {
            this.addToast({
                intent: Intent.DANGER,
                message: `Couldn't create a transformation of type ${transformationType}`,
            });
        }
    }

    public updateOrdering(newState: Transformation[], sortable: Sortable | null) {
        // console.log(newState);
        // console.log(sortable);
    }

    public endUpdateOrdering(event: SortableEvent) {
        if (event.oldIndex !== undefined && event.newIndex !== undefined && event.oldIndex !== event.newIndex) {
            let t = this.getTransformations();
            let oldIdx = event.oldIndex;
            let newIdx = event.newIndex;
            let indicesToUpdate: number[] = [oldIdx, newIdx];
            if (t.length > oldIdx + 1) {
                t[oldIdx + 1].previous = t[oldIdx].previous;
                indicesToUpdate.push(oldIdx + 1)
            }
            if (event.oldIndex < event.newIndex) {
                // We're moving the element down in the list
                t[oldIdx].previous = t[newIdx].id;
                if (t.length > newIdx + 1) {
                    t[newIdx + 1].previous = t[oldIdx].id;
                    indicesToUpdate.push(newIdx + 1)
                }
            } else {
                // We're moving the element up in the list
                t[oldIdx].previous = t[newIdx].previous;
                t[newIdx].previous = t[oldIdx].id;
            }
            let transformationsUpdating = [];
            for (let idx of indicesToUpdate) {
                transformationsUpdating.push(t[idx].id);
                t[idx]['next'] = undefined;
                this.wranglerService.putTransformation(t[idx].id, t[idx], this.finishUpdateOrdering)
            }
            this.setState({ transformationsUpdating: transformationsUpdating });
        }
    }

    protected finishUpdateOrdering(body: { [key: string]: any }) {
        if ("id" in body) {
            let transformationsUpdating = this.state.transformationsUpdating.filter(id => id !== body["id"]);
            this.setState({ transformationsUpdating: transformationsUpdating });
            if (transformationsUpdating.length === 0) {
                this.refresh();
            }
        } else {
            this.addToast({
                intent: Intent.DANGER,
                message: `Something went wrong while updating the transformations`,
            });
        }
    }

    /**
     * Renders wrangler
     * @returns  
     */
    public render() {
        return (
            <Grid fluid>
                <Row>
                    <Col md={12}>
                        <Tabs id="TabsExample" animate={true} key={"horizontal"} renderActiveTabPanelOnly={true} vertical={false}>
                            <Tab id="panel-math" title="Math" panel={<MathPanel newTransformation={this.newTransformation} />} />
                            <Tab id="panel-text" title="Text" panel={<TextPanel newTransformation={this.newTransformation} />} panelClassName="ember-panel" />
                            <Tab id="panel-custom" title="Custom" panel={<CustomPanel newTransformation={this.newTransformation} />} />
                            <Tab id="panel-settings" title="Settings" panel={<SettingsPanel newTransformation={this.newTransformation} />} />
                            <Tabs.Expander />
                            <input className="bp3-input" type="text" placeholder="Search help" />
                        </Tabs>
                    </Col>
                </Row>
                <Divider />
                <Row>
                    <Col md={2}>
                        <H3>Recipe</H3>
                        <div>
                            <HTMLTable striped={true}>
                                <ReactSortable
                                    tag="tbody"
                                    list={this.getTransformations()}
                                    setList={this.updateOrdering}
                                    onEnd={this.endUpdateOrdering}
                                >
                                    {this.getTransformations().map((transformation: Transformation, index: number) => this.renderTransformationButton(transformation, index))}
                                </ReactSortable>
                            </HTMLTable>
                            {this.renderTransformationDialog()}
                        </div>
                    </Col>
                    <Col md={10}>
                        <DataTable loading={this.state.loading} data={this.state.data} columns={this.state.columns} />
                    </Col>
                </Row>
            </Grid>
        );
    }
}
