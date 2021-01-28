import { Button, ButtonGroup, Popover, Position, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps, TransformationState } from './BasicTransformation'

const StatsTranformationMenu: React.FunctionComponent<TranformationProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("stats-correlation", {})} text="Correlation" />
        <MenuItem onClick={() => props.newTransformation("stats-covariance", {})} text="Covariance" />
        <MenuItem onClick={() => props.newTransformation("stats-cumsum", {})} text="Cumulative sum" />
        <MenuItem onClick={() => props.newTransformation("stats-cummax", {})} text="Cumulative max" />
        <MenuItem onClick={() => props.newTransformation("stats-cummin", {})} text="Cumulative min" />
        <MenuItem onClick={() => props.newTransformation("stats-cumprod", {})} text="Cumulative product" />
        <MenuItem onClick={() => props.newTransformation("stats-mad", {})} text="Mean absolute deviation" />
        <MenuItem onClick={() => props.newTransformation("stats-skew", {})} text="Skew" />
        <MenuItem onClick={() => props.newTransformation("stats-kurtosis", {})} text="Kurtosis" />
        <MenuItem onClick={() => props.newTransformation("stats-median", {})} text="Median" />
        <MenuItem onClick={() => props.newTransformation("stats-mode", {})} text="Mode" />
        <MenuItem onClick={() => props.newTransformation("stats-max", {})} text="Max" />
        <MenuItem onClick={() => props.newTransformation("stats-min", {})} text="Min" />
        <MenuItem onClick={() => props.newTransformation("stats-sum", {})} text="Sum" />
        <MenuItem onClick={() => props.newTransformation("stats-std", {})} text="Standard deviation" />
        <MenuItem onClick={() => props.newTransformation("stats-var", {})} text="Variance" />
        <MenuItem onClick={() => props.newTransformation("stats-sem", {})} text="Standard error of mean" />
        <MenuItem onClick={() => props.newTransformation("stats-nunique", {})} text="N-unique" />
        <MenuItem onClick={() => props.newTransformation("stats-value-counts", {})} text="Value counts" />
    </Menu>
);

export class StatsTransformationButton extends React.PureComponent<TranformationProps, TransformationState> {
    public state: TransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<StatsTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="Statistics" />
                </Popover>
            </ButtonGroup>
        );
    }
}