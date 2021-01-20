import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps, TransformationState } from './BasicTransformation'

const ComparisonTranformationMenu: React.FunctionComponent<TranformationProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("comparison-logical", {})} text="Logical comparison" />
        <MenuItem onClick={() => props.newTransformation("comparison-if-else", {})} text="If/else statement" />
        <MenuItem onClick={() => props.newTransformation("comparison-compare-value", {})} text="Compare column to value" />
        <MenuItem onClick={() => props.newTransformation("comparison-compare-columns", {})} text="Compare column to column" />
        <MenuItem onClick={() => props.newTransformation("comparison-parity", {})} text="Is even/odd" />
        <MenuItem onClick={() => props.newTransformation("comparison-mismatched", {})} text="Is mismatched" />
        <MenuItem onClick={() => props.newTransformation("comparison-missing", {})} text="Is missing" />
        <MenuItem onClick={() => props.newTransformation("comparison-is-null", {})} text="Is null" />
        <MenuItem onClick={() => props.newTransformation("comparison-negate", {})} text="Negate column" />
        <MenuItem onClick={() => props.newTransformation("comparison-min", {})} text="Min of columns" />
        <MenuItem onClick={() => props.newTransformation("comparison-max", {})} text="Max of columns" />
        <MenuItem onClick={() => props.newTransformation("comparison-mean", {})} text="Mean of columns" />
        <MenuItem onClick={() => props.newTransformation("comparison-mode", {})} text="Mode of columns" />
        <MenuItem onClick={() => props.newTransformation("comparison-coalesce", {})} text="Coalesce columns" />
    </Menu>
);

export class ComparisonTransformationButton extends React.PureComponent<TranformationProps, TransformationState> {
    public state: TransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<ComparisonTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="Comparison" />
                </Popover>
            </ButtonGroup>
        );
    }
}