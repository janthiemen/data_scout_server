import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps, TransformationState } from './BasicTransformation'

const CountTranformationMenu: React.FunctionComponent<TranformationProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("count-exact", {})} text="Text" />
        <MenuItem onClick={() => props.newTransformation("count-pattern", {})} text="Pattern (RegEx)" />
        <MenuItem onClick={() => props.newTransformation("count-delimiters", {})} text="Between delimiters" />
    </Menu>
);

export class CountTransformationButton extends React.PureComponent<TranformationProps, TransformationState> {
    public state: TransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<CountTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="Count" />
                </Popover>
            </ButtonGroup>
        );
    }
}