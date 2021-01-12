import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps } from './BasicTransformation'

const ReplaceTranformationMenu: React.FunctionComponent<TranformationProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("replace-text", {})} text="Text" />
        <MenuItem onClick={() => props.newTransformation("replace-regex", {})} text="Pattern (RegEx)" />
        <MenuItem onClick={() => props.newTransformation("replace-delimiters", {})} text="Between delimiters" />
        <MenuItem onClick={() => props.newTransformation("replace-positions", {})} text="Between positions" />
        <MenuItem onClick={() => props.newTransformation("replace-mismatched", {})} text="Mismatched values" />
        <MenuItem onClick={() => props.newTransformation("replace-missing", {})} text="Missing values" />
    </Menu>
);

interface ReplaceTransformationState { }

export class ReplaceTransformationButton extends React.PureComponent<TranformationProps, ReplaceTransformationState> {
    public state: ReplaceTransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<ReplaceTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="Replace" />
                </Popover>
            </ButtonGroup>
        );
    }
}