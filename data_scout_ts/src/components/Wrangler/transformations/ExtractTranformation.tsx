import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps, TransformationState } from './BasicTransformation'

const ExtractTranformationMenu: React.FunctionComponent<TranformationProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("extract-numbers", {})} text="Numbers" />
        <MenuItem onClick={() => props.newTransformation("extract-httpquerystrings", {})} text="HTTP Query strings" />
        <MenuItem onClick={() => props.newTransformation("extract-regex", {})} text="Pattern (regex)" />
        {/* <MenuItem onClick={() => props.newTransformation("extract-datetime", {})} text="Datetime" /> */}
        <MenuItem onClick={() => props.newTransformation("extract-positions", {})} text="Between positions" />
    </Menu>
);

export class ExtractTransformationButton extends React.PureComponent<TranformationProps, TransformationState> {
    public state: TransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<ExtractTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="Extract" />
                </Popover>
            </ButtonGroup>
        );
    }
}