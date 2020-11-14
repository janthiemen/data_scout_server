import { Button, ButtonGroup } from "@blueprintjs/core";
import * as React from "react";

interface GroupbyTransformationState { }
interface GroupbyTransformationProps {
    newTransformation: (transformationType: string) => void;
}

export class GroupbyTransformationButton extends React.PureComponent<GroupbyTransformationProps, GroupbyTransformationState> {
    public state: GroupbyTransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Button onClick={() => this.props.newTransformation("groupby")} text="Group by" />
            </ButtonGroup>
        );
    }
}