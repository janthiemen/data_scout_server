import { Button, ButtonGroup } from "@blueprintjs/core";
import * as React from "react";

interface MergeTransformationState { }
interface MergeTransformationProps {
    newTransformation: (transformationType: string) => void;
}

export class MergeTransformationButton extends React.PureComponent<MergeTransformationProps, MergeTransformationState> {
    public state: MergeTransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Button onClick={() => this.props.newTransformation("merge-text")} text="Merge" />
            </ButtonGroup>
        );
    }
}