import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps, TransformationState } from './BasicTransformation'

const DataTranformationMenu: React.FunctionComponent<TranformationProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("groupby", {})} text="Group by" />
        <MenuItem onClick={() => props.newTransformation("sortby", {})} text="Sort by" />
        <MenuItem onClick={() => props.newTransformation("window", {})} text="Window" />
        <MenuItem onClick={() => props.newTransformation("pivot", {})} text="Pivot" />
        <MenuItem onClick={() => props.newTransformation("unpivot", {})} text="Unpivot" />
    </Menu>
);

export class DataTransformationButton extends React.PureComponent<TranformationProps, TransformationState> {
    public state: TransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<DataTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="Data" />
                </Popover>
            </ButtonGroup>
        );
    }
}