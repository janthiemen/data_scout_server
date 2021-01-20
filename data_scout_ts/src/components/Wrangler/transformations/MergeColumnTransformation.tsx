import { Button, ButtonGroup } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps, TransformationState } from './BasicTransformation'

export class MergeTransformationButton extends React.PureComponent<TranformationProps, TransformationState> {
    public state: TransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Button onClick={() => this.props.newTransformation("merge-text", {})} text="Merge" />
            </ButtonGroup>
        );
    }
}