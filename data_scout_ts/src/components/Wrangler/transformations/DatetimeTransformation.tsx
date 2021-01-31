import { Button, ButtonGroup, Popover, Position, Menu, MenuItem, MenuDivider } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps, TransformationState } from './BasicTransformation'

const DatetimeTranformationMenu: React.FunctionComponent<TranformationProps> = props => (
    <Menu>
        <MenuItem onClick={() => props.newTransformation("datetime-extract-year", { })} text="Extract year" />
        <MenuItem onClick={() => props.newTransformation("datetime-extract-month", { })} text="Extract month" />
        <MenuItem onClick={() => props.newTransformation("datetime-extract-monthname", { })} text="Extract month name" />
		<MenuItem onClick={() => props.newTransformation("datetime-extract-endofmonth", { })} text="Extract last day of month" />
        <MenuItem onClick={() => props.newTransformation("datetime-extract-day", { })} text="Extract day of the month" />
        <MenuItem onClick={() => props.newTransformation("datetime-extract-week", { })} text="Extract week number" />
        <MenuItem onClick={() => props.newTransformation("datetime-extract-dayofweek", { })} text="Extract day of the week" />
        <MenuItem onClick={() => props.newTransformation("datetime-extract-dayofweekname", { })} text="Extract name of day of the week" />
        <MenuItem onClick={() => props.newTransformation("datetime-extract-dayofyear", { })} text="Extract day of the year" />
        <MenuDivider />
        <MenuItem onClick={() => props.newTransformation("datetime-extract-hours", { })} text="Extract the hour" />
        <MenuItem onClick={() => props.newTransformation("datetime-extract-minutes", { })} text="Extract minutes" />
        <MenuItem onClick={() => props.newTransformation("datetime-extract-seconds", { })} text="Extract the seconds" />
        <MenuDivider />
        <MenuItem onClick={() => props.newTransformation("datetime-format", { })} text="Format datetime" />
        <MenuDivider />
        <MenuItem onClick={() => props.newTransformation("datetime-date-add", { })} text="Datetime add" />
        <MenuItem onClick={() => props.newTransformation("datetime-date-diff", { })} text="Datetime difference" />
        <MenuItem onClick={() => props.newTransformation("datetime-now", { })} text="Current datetime" />
        <MenuItem onClick={() => props.newTransformation("datetime-today", { })} text="Today" />
    </Menu>
);

export class DatetimeTransformationButton extends React.PureComponent<TranformationProps, TransformationState> {
    public state: TransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<DatetimeTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="Datetime" />
                </Popover>
            </ButtonGroup>
        );
    }
}