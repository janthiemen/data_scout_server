import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps, TransformationState } from './BasicTransformation'

const LiteralTranformationMenu: React.FunctionComponent<TranformationProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("literal-string", {})} text="String" />
        <MenuItem onClick={() => props.newTransformation("literal-Integer", {})} text="Integer" />
        <MenuItem onClick={() => props.newTransformation("literal-float", {})} text="Float" />
        <MenuItem onClick={() => props.newTransformation("literal-null", {})} text="Null" />
        <MenuItem onClick={() => props.newTransformation("literal-rand-between", {})} text="Random float" />
        <MenuItem onClick={() => props.newTransformation("literal-rand-int", {})} text="Random integer" />
    </Menu>
);

export class LiteralTransformationButton extends React.PureComponent<TranformationProps, TransformationState> {
    public state: TransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<LiteralTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="Literal" />
                </Popover>
            </ButtonGroup>
        );
    }
}