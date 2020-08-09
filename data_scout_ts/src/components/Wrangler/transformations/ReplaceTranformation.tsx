import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";

interface ReplaceTranformationMenuProps extends IProps {
    newTransformation: (transformationType: string) => void;
}

const ReplaceTranformationMenu: React.FunctionComponent<ReplaceTranformationMenuProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("replace-text")} text="Text" />
        <MenuItem onClick={() => props.newTransformation("replace-pattern")} text="Pattern (RegEx)" />
        <MenuItem onClick={() => props.newTransformation("replace-delimiters")} text="Between delimiters" />
        <MenuItem onClick={() => props.newTransformation("replace-positions")} text="Between positions" />
        <MenuItem onClick={() => props.newTransformation("replace-mismatched")} text="Mismatched values" />
        <MenuItem onClick={() => props.newTransformation("replace-missing")} text="Missing values" />
    </Menu>
);

interface ReplaceTransformationState { }
interface ReplaceTransformationProps {
    newTransformation: (transformationType: string) => void;
}

export class ReplaceTransformationButton extends React.PureComponent<ReplaceTransformationProps, ReplaceTransformationState> {
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