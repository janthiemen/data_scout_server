import { Button, ButtonGroup } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps, TransformationState } from './BasicTransformation'

export class GroupbyTransformationButton extends React.PureComponent<TranformationProps, TransformationState> {
    public state: TransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Button onClick={() => this.props.newTransformation("groupby", {})} text="Group by" />
            </ButtonGroup>
        );
    }
}