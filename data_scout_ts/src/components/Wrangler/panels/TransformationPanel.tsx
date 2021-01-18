import * as React from "react";

import { ButtonGroup, Tooltip, Divider } from "@blueprintjs/core";
import { StringTransformationButton } from "../transformations/StringTranformation";
import { CountTransformationButton } from "../transformations/CountTransformation";
import { MathTransformationButton } from "../transformations/MathTranformation";
// import { ExtractTransformationButton } from "../transformations/ExtractTranformation";
import { SplitTransformationButton } from "../transformations/SplitColumnTransformation";
import { FilterTransformationButton } from "../transformations/FilterTransformation";
import { MergeTransformationButton } from "../transformations/MergeColumnTransformation";
import { GroupbyTransformationButton } from "../transformations/GroupByTransformation";

export const TransformationPanel: React.SFC<{newTransformation: (transformationType: string, kwargs: { [key: string]: any }) => void}> = (props) => (
    <div>
        <ButtonGroup vertical={false} alignText="left">
            <StringTransformationButton newTransformation={props.newTransformation} />
            {/* <ExtractTransformationButton newTransformation={props.newTransformation} /> */}
            <Tooltip content="Count the number of occurances">
                <CountTransformationButton newTransformation={props.newTransformation} />
            </Tooltip>
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

