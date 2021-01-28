import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps, TransformationState } from './BasicTransformation'

const DictTranformationMenu: React.FunctionComponent<TranformationProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("dict-get", {})} text="Get by key" />
        <MenuItem onClick={() => props.newTransformation("dict-keys", {})} text="Keys" />
        <MenuItem onClick={() => props.newTransformation("dict-values", {})} text="Values" />
        <MenuItem onClick={() => props.newTransformation("dict-create", {})} text="Create" />
    </Menu>
);

export class DictTransformationButton extends React.PureComponent<TranformationProps, TransformationState> {
    public state: TransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<DictTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="Dictionary" />
                </Popover>
            </ButtonGroup>
        );
    }
}