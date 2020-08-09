import * as React from "react";

import { ButtonGroup, Tooltip, Divider } from "@blueprintjs/core";
import { ReplaceTransformationButton } from "../transformations/ReplaceTranformation";
import { CountTransformationButton } from "../transformations/CountTransformation";
import { MathTransformationButton } from "../transformations/MathTranformation";
import { FormatTransformationButton } from "../transformations/FormatTransformation";

export const TransformationPanel: React.SFC<{newTransformation: (transformationType: string) => void}> = (props) => (
    <div>
        <ButtonGroup vertical={false} alignText="left">
            <Tooltip content="Replace one text with another">
                <ReplaceTransformationButton newTransformation={props.newTransformation} />
            </Tooltip>
            <Tooltip content="Count the number of occurances">
                <CountTransformationButton newTransformation={props.newTransformation} />
            </Tooltip>
            <FormatTransformationButton newTransformation={props.newTransformation} />
            <MathTransformationButton newTransformation={props.newTransformation} />
        </ButtonGroup>

        <input className="bp3-input" type="text" placeholder="Search help" />
 
        {/* TODO: Link to a help page on the drawer */}
    </div>
);

