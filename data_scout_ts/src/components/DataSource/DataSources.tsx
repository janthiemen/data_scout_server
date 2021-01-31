import * as React from "react";

import {IToastProps } from "@blueprintjs/core";

import { Grid, Row, Col } from 'react-flexbox-grid';
import { PageProps } from "../../helpers/props";
import { DataSourceService } from "../../helpers/userService";

import { DataSourcesTree, DataSourceNode } from "./DataSourceTree";
import { DataSourceComponent, DataSourceType } from "./DataSource";
import { withRouter } from "react-router-dom";


interface DataSourcesState {
    types: DataSourceType[],
    dataSourceType?: DataSourceType,
    dataSources: DataSource[],
    dataSource: DataSource
}

export interface DataSource {
    id: number,
    name: string,
    source?: string,
    kwargs: { [key: string]: any },
}

/**
 * Empty data source object.
 */
export const newDataSource = function(): DataSource {
    return {
        id: -1,
        name: "New data source",
        source: undefined,
        kwargs: {}
    }
}

/**
 * The page with all the data sources.
 */
class DataSourcesComponent extends React.Component<PageProps> {
    private dataSourceService: DataSourceService;
    private addToast: (toast: IToastProps) => void;
    public state: DataSourcesState = {
        types: [],
        dataSourceType: undefined,
        dataSources: [],
        dataSource: newDataSource()
    }

    /**
     * Creates an instance of data sources.
     * @param props 
     */
    constructor(props: PageProps) {
        super(props);
        this.dataSourceService = new DataSourceService(props.addToast, props.setLoggedIn);
        this.setTypes = this.setTypes.bind(this);
        this.setDataSources = this.setDataSources.bind(this);
        this.onSelectDataSource = this.onSelectDataSource.bind(this);
        this.updateDataSources = this.updateDataSources.bind(this);
        this.addToast = props.addToast;
        this.dataSourceService.getTypes(this.setTypes);
        this.updateDataSources();
    }

    /**
     * Sets types
     * @param types 
     */
    public setTypes(types: {}) {
        this.setState({ types: types });
    }

    public updateDataSources() {
        this.dataSourceService.get(this.setDataSources);
    }

    /**
     * Selects data source
     * @param node 
     */
    public onSelectDataSource(node: DataSourceNode) {
        let dataSource = this.state.dataSources.filter(item => item.id === node.id)[0];
        this.setState({ dataSource: dataSource });
    }

    /**
     * Sets data sources based on the API response
     * @param body 
     */
    private setDataSources(body: { [key: string]: any }) {
        let dataSources: DataSource[] = [];
        body["results"].forEach((result: { id: number, name: string, source: string, kwargs: string }) => {
            let kwargs: { [key: string]: any } = JSON.parse(result["kwargs"]);
            dataSources.push({ id: result["id"], name: result["name"], source: result["source"], kwargs: kwargs });
        });
        dataSources.push(newDataSource());
        this.setState({ dataSources: dataSources });
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
                        <DataSourcesTree updateDataSources={this.updateDataSources} dataSourceService={this.dataSourceService} dataSources={this.state.dataSources} onSelectDataSource={this.onSelectDataSource} addToast={this.addToast} />
                    </Col>
                    <Col md={6}>
                        <DataSourceComponent updateDataSources={this.updateDataSources} types={this.state.types} dataSource={this.state.dataSource} dataSourceService={this.dataSourceService} addToast={this.addToast} />
                    </Col>
                </Row>
            </Grid>
        );
    }
}

export const DataSources = withRouter(DataSourcesComponent);