import { Button, ButtonGroup, Popover, Position, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps, TransformationState } from './BasicTransformation'

const PreprocessingTranformationMenu: React.FunctionComponent<TranformationProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("preprocessing-impute", {})} text="Impute missing values" />
        <MenuItem onClick={() => props.newTransformation("preprocessing-scale", {})} text="Scale" />
        <MenuItem onClick={() => props.newTransformation("preprocessing-categorical-encoding", {})} text="Categorical encoding" />
        <MenuItem onClick={() => props.newTransformation("preprocessing-discretize-bin", {})} text="Discretize (binning)" />
        <MenuItem onClick={() => props.newTransformation("preprocessing-binarize", {})} text="Binarize" />
        <MenuItem onClick={() => props.newTransformation("preprocessing-normalize", {})} text="Normalize" />
        <MenuItem onClick={() => props.newTransformation("preprocessing-polynomial", {})} text="Polynomial features" />
    </Menu>
);

export class PreprocessingTransformationButton extends React.PureComponent<TranformationProps, TransformationState> {
    public state: TransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<PreprocessingTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="Preprocessing" />
                </Popover>
            </ButtonGroup>
        );
    }
}