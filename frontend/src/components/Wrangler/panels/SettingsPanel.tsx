import * as React from "react";

import { FormGroup, HTMLSelect } from "@blueprintjs/core";
import { Help } from "../Help";

export const SettingsPanel: React.SFC<{newTransformation: (transformationType: string) => void}> = (props) => (
    <div>
        {/* TODO: Link to a help page on the drawer */}
        <FormGroup label="Sampling method" labelInfo={<Help page="sampling" />}>
            {/* <FormGroup label="Sampling method" labelInfo={<a href=""><Icon icon="help" /></a>}> */}
            {/* TODO: Actually update the sampling methodology */}
            <HTMLSelect>
                <option value="random">Random</option>
                <option value="stratified">stratified</option>
                <option value="top">Top</option>
            </HTMLSelect>
        </FormGroup>
    </div>
);

