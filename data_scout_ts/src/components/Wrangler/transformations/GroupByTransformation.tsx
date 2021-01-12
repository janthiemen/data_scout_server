import { Button, ButtonGroup } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps } from './BasicTransformation'

interface GroupbyTransformationState { }

export class GroupbyTransformationButton extends React.PureComponent<TranformationProps, GroupbyTransformationState> {
    public state: GroupbyTransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Button onClick={() => this.props.newTransformation("groupby", {})} text="Group by" />
            </ButtonGroup>
        );
    }
}