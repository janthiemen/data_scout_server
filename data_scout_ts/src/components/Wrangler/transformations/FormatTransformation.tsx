import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";

interface FormatTranformationMenuProps extends IProps {
    newTransformation: (transformationType: string) => void;
}

const FormatTranformationMenu: React.FunctionComponent<FormatTranformationMenuProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("format-uppercase")} text="Convert to upper case" />
        <MenuItem onClick={() => props.newTransformation("format-lowercase")} text="Convert to lower case" />
        <MenuItem onClick={() => props.newTransformation("format-propercase")} text="Convert to proper case" />
        <MenuItem onClick={() => props.newTransformation("format-trim-whitespace")} text="Trim whitespaces" />
        <MenuItem onClick={() => props.newTransformation("format-trim-quotes")} text="Trim quotes" />
        <MenuItem onClick={() => props.newTransformation("format-remove-whitespace")} text="Remove whitespaces" />
        <MenuItem onClick={() => props.newTransformation("format-remove-symbols")} text="Remove symbols" />
        <MenuItem onClick={() => props.newTransformation("format-remove-accents")} text="Remove accents" />
        <MenuItem onClick={() => props.newTransformation("format-add-prefix")} text="Add prefix" />
        <MenuItem onClick={() => props.newTransformation("format-add-suffix")} text="Add suffix" />
        <MenuItem onClick={() => props.newTransformation("format-pad")} text="Add padding" />
        {/* This one should only be available for datetime columns */}
        <MenuItem onClick={() => props.newTransformation("format-datetime")} text="Change date/time format" />
    </Menu>
);

interface FormatTransformationState { }
interface FormatTransformationProps {
    newTransformation: (transformationType: string) => void;
}

export class FormatTransformationButton extends React.PureComponent<FormatTransformationProps, FormatTransformationState> {
    public state: FormatTransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<FormatTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="Format" />
                </Popover>
            </ButtonGroup>
        );
    }
}