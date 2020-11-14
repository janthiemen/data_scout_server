import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";

interface SplitTranformationMenuProps extends IProps {
    newTransformation: (transformationType: string) => void;
}

const SplitTranformationMenu: React.FunctionComponent<SplitTranformationMenuProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("split-delimiter")} text="At delimiter" />
        <MenuItem onClick={() => props.newTransformation("split-delimiters-between")} text="Between delimiters" />
        <MenuItem onClick={() => props.newTransformation("split-delimiters")} text="At multiple delimiters" />
        <MenuItem onClick={() => props.newTransformation("split-position")} text="At position" />
        <MenuItem onClick={() => props.newTransformation("split-position-between")} text="Between positions" />
        <MenuItem onClick={() => props.newTransformation("split-interval")} text="At intervals" />
    </Menu>
);

interface SplitTransformationState { }
interface SplitTransformationProps {
    newTransformation: (transformationType: string) => void;
}

export class SplitTransformationButton extends React.PureComponent<SplitTransformationProps, SplitTransformationState> {
    public state: SplitTransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<SplitTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="Split" />
                </Popover>
            </ButtonGroup>
        );
    }
}