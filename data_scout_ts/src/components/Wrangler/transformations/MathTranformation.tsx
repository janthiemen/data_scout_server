import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";

interface MathTranformationMenuProps extends IProps {
    newTransformation: (transformationType: string) => void;
}

const MathTranformationMenu: React.FunctionComponent<MathTranformationMenuProps> = props => (
    <Menu>
        <MenuItem icon="plus" onClick={() => props.newTransformation("math-add")} text="Sum" />
        <MenuItem icon="minus" onClick={() => props.newTransformation("math-min")} text="Min" />
        <MenuItem icon="cross" onClick={() => props.newTransformation("math-multiply")} text="Multiply" />
        <MenuItem icon="slash" onClick={() => props.newTransformation("math-divide")} text="Divide" />
        {/* TODO: */}
        <MenuItem icon="edit" onClick={() => props.newTransformation("math-custom")} text="Custom equation" />
    </Menu>
);

interface MathTransformationState { }
interface MathTransformationProps {
    newTransformation: (transformationType: string) => void;
}

export class MathTransformationButton extends React.PureComponent<MathTransformationProps, MathTransformationState> {
    public state: MathTransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<MathTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="Math" />
                </Popover>
            </ButtonGroup>
        );
    }
}