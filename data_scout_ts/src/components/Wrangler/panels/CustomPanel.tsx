import * as React from "react";

import { Button, ButtonGroup, Tooltip } from "@blueprintjs/core";

export const CustomPanel: React.SFC<{newTransformation: (transformationType: string) => void}> = (props) => (
    <div>
        <ButtonGroup vertical={false} alignText="left">
            <Tooltip content="Sum multiple columns">
                <Button onClick={() => props.newTransformation("add")} outlined={true} icon="plus">SUM</Button>
            </Tooltip>
            <Tooltip content="Subtract B from A">
                <Button onClick={() => props.newTransformation("min")} outlined={true} icon="minus">MIN</Button>
            </Tooltip>
            <Tooltip content="Multiply multiple columns">
                <Button onClick={() => props.newTransformation("multiply")} outlined={true} icon="cross">MULTIPLY</Button>
            </Tooltip>
            <Tooltip content="Divide A by B">
                <Button onClick={() => props.newTransformation("divide")} outlined={true} icon="slash">DIVIDE</Button>
            </Tooltip>
        </ButtonGroup>

        {/* TODO: Link to a help page on the drawer */}
    </div>
);

