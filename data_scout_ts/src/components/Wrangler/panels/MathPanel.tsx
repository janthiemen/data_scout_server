import * as React from "react";

import { Button, ButtonGroup, Tooltip } from "@blueprintjs/core";

export const MathPanel: React.SFC<{newTransformation: (transformationType: string) => void}> = (props) => (
    <div>
        <ButtonGroup vertical={false} alignText="left">
            <Tooltip content="Sum multiple columns">
                <Button onClick={() => props.newTransformation("add")} minimal={true} icon="plus">Sum</Button>
            </Tooltip>
            <Tooltip content="Subtract B from A">
                <Button onClick={() => props.newTransformation("min")} minimal={true} icon="minus">Min</Button>
            </Tooltip>
            <Tooltip content="Multiply multiple columns">
                <Button onClick={() => props.newTransformation("multiply")} minimal={true} icon="cross">Multiply</Button>
            </Tooltip>
            <Tooltip content="Divide A by B">
                <Button onClick={() => props.newTransformation("divide")} minimal={true} icon="slash">Divide</Button>
            </Tooltip>
            {/* TODO: */}
            <Tooltip content="Custom math">
                <Button onClick={() => props.newTransformation("math-custom")} minimal={true} icon="slash">Divide</Button>
            </Tooltip>
        </ButtonGroup>

        {/* TODO: Link to a help page on the drawer */}
    </div>
);

