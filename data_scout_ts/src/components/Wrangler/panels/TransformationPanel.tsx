import * as React from "react";

import { ButtonGroup, Tooltip, Divider } from "@blueprintjs/core";
import { ReplaceTransformationButton } from "../transformations/ReplaceTranformation";
import { CountTransformationButton } from "../transformations/CountTransformation";
import { MathTransformationButton } from "../transformations/MathTranformation";
import { FormatTransformationButton } from "../transformations/FormatTransformation";
import { ExtractTransformationButton } from "../transformations/ExtractTranformation";
import { SplitTransformationButton } from "../transformations/SplitColumnTransformation";
import { FilterTransformationButton } from "../transformations/FilterTransformation";
import { MergeTransformationButton } from "../transformations/MergeColumnTransformation";
import { GroupbyTransformationButton } from "../transformations/GroupByTransformation";

export const TransformationPanel: React.SFC<{newTransformation: (transformationType: string) => void}> = (props) => (
    <div>
        <ButtonGroup vertical={false} alignText="left">
            <Tooltip content="Replace one text with another">
                <ReplaceTransformationButton newTransformation={props.newTransformation} />
            </Tooltip>
            <ExtractTransformationButton newTransformation={props.newTransformation} />
            <Tooltip content="Count the number of occurances">
                <CountTransformationButton newTransformation={props.newTransformation} />
            </Tooltip>
            <FormatTransformationButton newTransformation={props.newTransformation} />
            <MathTransformationButton newTransformation={props.newTransformation} />
            <SplitTransformationButton newTransformation={props.newTransformation} />
            <FilterTransformationButton newTransformation={props.newTransformation} />
            <MergeTransformationButton newTransformation={props.newTransformation} />
            <GroupbyTransformationButton newTransformation={props.newTransformation} />
        </ButtonGroup>

        <input className="bp3-input" type="text" placeholder="Search help" />
 
        {/* TODO: Link to a help page on the drawer */}
    </div>
);

