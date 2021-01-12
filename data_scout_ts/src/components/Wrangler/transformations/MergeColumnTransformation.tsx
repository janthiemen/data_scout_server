import { Button, ButtonGroup } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps } from './BasicTransformation'

interface MergeTransformationState { }

export class MergeTransformationButton extends React.PureComponent<TranformationProps, MergeTransformationState> {
    public state: MergeTransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Button onClick={() => this.props.newTransformation("merge-text", {})} text="Merge" />
            </ButtonGroup>
        );
    }
}