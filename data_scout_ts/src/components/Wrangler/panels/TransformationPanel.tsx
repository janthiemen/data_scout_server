import * as React from "react";

import { ButtonGroup, Tooltip, Divider, Button } from "@blueprintjs/core";
import { StringTransformationButton } from "../transformations/StringTranformation";
import { ArrayTransformationButton } from "../transformations/ArrayTransformation";
import { DatetimeTransformationButton } from "../transformations/DatetimeTransformation";
import { DictTransformationButton } from "../transformations/DictTransformation";
import { LiteralTransformationButton } from "../transformations/LiteralTransformation";
import { MathTransformationButton } from "../transformations/MathTranformation";
import { PreprocessingTransformationButton } from "../transformations/PreprocessingTransformation";
import { DataTransformationButton } from "../transformations/DataTransformation";
import { ComparisonTransformationButton } from "../transformations/ComparisonTransformation";
import { FilterTransformationButton } from "../transformations/FilterTransformation";
import { StatsTransformationButton } from "../transformations/StatsTransformation";
import { QuickAccess } from "../QuickAccess";

export const TransformationPanel: React.SFC<{newTransformation: (transformationType: string, kwargs: { [key: string]: any }) => void}> = (props) => (
    <div>
        <ButtonGroup vertical={false} alignText="left">
            <StringTransformationButton newTransformation={props.newTransformation} />
            <DatetimeTransformationButton newTransformation={props.newTransformation} />
            <ArrayTransformationButton newTransformation={props.newTransformation} />
            <DictTransformationButton newTransformation={props.newTransformation} />
            <LiteralTransformationButton newTransformation={props.newTransformation} />
            {/* <ExtractTransformationButton newTransformation={props.newTransformation} /> */}
            {/* <Tooltip content="Count the number of occurances">
                <CountTransformationButton newTransformation={props.newTransformation} />
            </Tooltip> */}
            <MathTransformationButton newTransformation={props.newTransformation} />
            <ComparisonTransformationButton newTransformation={props.newTransformation} />
            <PreprocessingTransformationButton newTransformation={props.newTransformation} />
            {/* <SplitTransformationButton newTransformation={props.newTransformation} /> */}
            <FilterTransformationButton newTransformation={props.newTransformation} />
            {/* <MergeTransformationButton newTransformation={props.newTransformation} /> */}
            <DataTransformationButton newTransformation={props.newTransformation} />
            <StatsTransformationButton newTransformation={props.newTransformation} />
        </ButtonGroup>
        <QuickAccess />
        {/* <input className="bp3-input" type="text" placeholder="Search help" /> */}
 
        {/* TODO: Link to a help page on the drawer */}
    </div>
);

