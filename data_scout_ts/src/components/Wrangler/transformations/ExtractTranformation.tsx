import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";

interface ExtractTranformationMenuProps extends IProps {
    newTransformation: (transformationType: string) => void;
}

const ExtractTranformationMenu: React.FunctionComponent<ExtractTranformationMenuProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("extract-numbers")} text="Numbers" />
        <MenuItem onClick={() => props.newTransformation("extract-httpquerystrings")} text="HTTP Query strings" />
        <MenuItem onClick={() => props.newTransformation("extract-regex")} text="Pattern (regex)" />
        <MenuItem onClick={() => props.newTransformation("extract-datetime")} text="Datetime" />
        <MenuItem onClick={() => props.newTransformation("extract-characters-first")} text="First character(s)" />
        <MenuItem onClick={() => props.newTransformation("extract-characters-last")} text="Last character(s)" />
    </Menu>
);

interface ExtractTransformationState { }
interface ExtractTransformationProps {
    newTransformation: (transformationType: string) => void;
}

export class ExtractTransformationButton extends React.PureComponent<ExtractTransformationProps, ExtractTransformationState> {
    public state: ExtractTransformationState = {};

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