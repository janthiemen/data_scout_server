import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps, TransformationState } from './BasicTransformation'

const ArrayTranformationMenu: React.FunctionComponent<TranformationProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("array-index", {})} text="Index by value" />
        <MenuItem onClick={() => props.newTransformation("array-at-index", {})} text="Value at index" />
        <MenuItem onClick={() => props.newTransformation("array-slice", {})} text="Slice" />
        <MenuItem onClick={() => props.newTransformation("array-length", {})} text="Length" />
        <MenuItem onClick={() => props.newTransformation("array-mean", {})} text="Mean" />
        <MenuItem onClick={() => props.newTransformation("array-sum", {})} text="Sum" />
        <MenuItem onClick={() => props.newTransformation("array-min", {})} text="Min" />
        <MenuItem onClick={() => props.newTransformation("array-max", {})} text="Max" />
        <MenuItem onClick={() => props.newTransformation("array-mode", {})} text="Mode" />
        <MenuItem onClick={() => props.newTransformation("array-std", {})} text="Standard deviation" />
        <MenuItem onClick={() => props.newTransformation("array-var", {})} text="Variance" />
        <MenuItem onClick={() => props.newTransformation("array-sort", {})} text="Sort" />
        <MenuItem onClick={() => props.newTransformation("array-concat", {})} text="Concat" />
        <MenuItem onClick={() => props.newTransformation("array-intersect", {})} text="Intersect" />
        <MenuItem onClick={() => props.newTransformation("array-unique", {})} text="Unique" />
        <MenuItem onClick={() => props.newTransformation("array-filter", {})} text="Filter" />
        <MenuItem onClick={() => props.newTransformation("array-to-dict", {})} text="To dictionary" />
        <MenuItem onClick={() => props.newTransformation("array-merge", {})} text="Merge" />
        <MenuItem onClick={() => props.newTransformation("array-flatten", {})} text="Flatten" />
    </Menu>
);

export class ArrayTransformationButton extends React.PureComponent<TranformationProps, TransformationState> {
    public state: TransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<ArrayTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="List" />
                </Popover>
            </ButtonGroup>
        );
    }
}