import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";

interface CountTranformationMenuProps extends IProps {
    newTransformation: (transformationType: string) => void;
}

const CountTranformationMenu: React.FunctionComponent<CountTranformationMenuProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("count-exact")} text="Text" />
        <MenuItem onClick={() => props.newTransformation("count-pattern")} text="Pattern (RegEx)" />
        <MenuItem onClick={() => props.newTransformation("count-delimiters")} text="Between delimiters" />
    </Menu>
);

interface CountTransformationState { }
interface CountTransformationProps {
    newTransformation: (transformationType: string) => void;
}

export class CountTransformationButton extends React.PureComponent<CountTransformationProps, CountTransformationState> {
    public state: CountTransformationState = {};

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