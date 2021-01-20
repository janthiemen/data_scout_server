import { Button, ButtonGroup, Popover, Position, IProps, Menu, MenuItem } from "@blueprintjs/core";
import * as React from "react";
import { TranformationProps, TransformationState } from './BasicTransformation'

const StringTranformationMenu: React.FunctionComponent<TranformationProps> = props => (
    <Menu>
        <MenuItem text="Replace">
            <MenuItem onClick={() => props.newTransformation("replace-text", {})} text="Text" />
            <MenuItem onClick={() => props.newTransformation("replace-regex", {})} text="Pattern (RegEx)" />
            <MenuItem onClick={() => props.newTransformation("replace-delimiters", {})} text="Between delimiters" />
            <MenuItem onClick={() => props.newTransformation("replace-positions", {})} text="Between positions" />
            <MenuItem onClick={() => props.newTransformation("replace-mismatched", {})} text="Mismatched values" />
            <MenuItem onClick={() => props.newTransformation("replace-missing", {})} text="Missing values" />
        </MenuItem>
        <MenuItem text="Format">
            <MenuItem onClick={() => props.newTransformation("format-uppercase", {})} text="Convert to upper case" />
            <MenuItem onClick={() => props.newTransformation("format-lowercase", {})} text="Convert to lower case" />
            <MenuItem onClick={() => props.newTransformation("format-propercase", {})} text="Convert to proper case" />
            <MenuItem onClick={() => props.newTransformation("format-trim-whitespace", {})} text="Trim whitespaces" />
            <MenuItem onClick={() => props.newTransformation("format-trim-quotes", {})} text="Trim quotes" />
            <MenuItem onClick={() => props.newTransformation("format-remove-whitespace", {})} text="Remove whitespaces" />
            <MenuItem onClick={() => props.newTransformation("format-remove-symbols", {})} text="Remove symbols" />
            <MenuItem onClick={() => props.newTransformation("format-remove-accents", {})} text="Remove accents" />
            <MenuItem onClick={() => props.newTransformation("format-add-prefix", {})} text="Add prefix" />
            <MenuItem onClick={() => props.newTransformation("format-add-suffix", {})} text="Add suffix" />
            <MenuItem onClick={() => props.newTransformation("format-pad", {})} text="Add padding" />
            {/* This one should only be available for datetime columns */}
            <MenuItem onClick={() => props.newTransformation("format-datetime", {})} text="Change date/time format" />
        </MenuItem>
        <MenuItem text="Substring">
            <MenuItem onClick={() => props.newTransformation("string-substring-left", {})} text="Left" />
            <MenuItem onClick={() => props.newTransformation("string-substring-right", {})} text="Right" />
            <MenuItem onClick={() => props.newTransformation("string-substring", {})} text="Substring" />
        </MenuItem>
        <MenuItem text="Find">
            <MenuItem onClick={() => props.newTransformation("string-find-left", {})} text="Left" />
            <MenuItem onClick={() => props.newTransformation("string-find-right", {})} text="Left" />
        </MenuItem>
        <MenuItem onClick={() => props.newTransformation("string-length", {})} text="Length" />
        <MenuItem onClick={() => props.newTransformation("string-merge", {})} text="Merge" />
        <MenuItem onClick={() => props.newTransformation("string-repeat", {})} text="Repeat" />
        <MenuItem text="Test">
            <MenuItem onClick={() => props.newTransformation("string-test-contains", {})} text="Contains" />
            <MenuItem onClick={() => props.newTransformation("string-test-startswith", {})} text="Starts with" />
            <MenuItem onClick={() => props.newTransformation("string-test-endswith", {})} text="Ends with" />
            <MenuItem onClick={() => props.newTransformation("string-test-regex", {})} text="Regex" />
            <MenuItem onClick={() => props.newTransformation("string-test-exact", {})} text="Exact" />
            <MenuItem onClick={() => props.newTransformation("string-test-greater", {})} text="Greater then" />
            <MenuItem onClick={() => props.newTransformation("string-test-greater-equal", {})} text="Greater or equal" />
            <MenuItem onClick={() => props.newTransformation("string-test-less", {})} text="Less then" />
            <MenuItem onClick={() => props.newTransformation("string-test-less-equal", {})} text="Less or equal" />
        </MenuItem>
        <MenuItem text="Extract">
            <MenuItem onClick={() => props.newTransformation("extract-numbers", {})} text="Numbers" />
            <MenuItem onClick={() => props.newTransformation("extract-httpquerystrings", {})} text="HTTP Query strings" />
            <MenuItem onClick={() => props.newTransformation("extract-regex", {})} text="Pattern (regex)" />
            {/* <MenuItem onClick={() => props.newTransformation("extract-datetime", {})} text="Datetime" /> */}
            <MenuItem onClick={() => props.newTransformation("extract-positions", {})} text="Between positions" />
        </MenuItem>

        <MenuItem text="Split">
            <MenuItem onClick={() => props.newTransformation("split-delimiter", {})} text="At delimiter" />
            <MenuItem onClick={() => props.newTransformation("split-delimiters-between", {})} text="Between delimiters" />
            <MenuItem onClick={() => props.newTransformation("split-delimiters", {})} text="At multiple delimiters" />
            <MenuItem onClick={() => props.newTransformation("split-position", {})} text="At position" />
            <MenuItem onClick={() => props.newTransformation("split-position-between", {})} text="Between positions" />
            <MenuItem onClick={() => props.newTransformation("split-interval", {})} text="At intervals" />
        </MenuItem>

        <MenuItem text="Count">
            <MenuItem onClick={() => props.newTransformation("count-exact", {})} text="Text" />
            <MenuItem onClick={() => props.newTransformation("count-pattern", {})} text="Pattern (RegEx)" />
            <MenuItem onClick={() => props.newTransformation("count-delimiters", {})} text="Between delimiters" />
        </MenuItem>

        <MenuItem text="Encoding">
            <MenuItem onClick={() => props.newTransformation("string-base64-encode", {})} text="Base64 encode" />
            <MenuItem onClick={() => props.newTransformation("string-base64-decode", {})} text="Base64 decode" />
        </MenuItem>

    </Menu>
);

export class StringTransformationButton extends React.PureComponent<TranformationProps, TransformationState> {
    public state: TransformationState = {};

    public render() {
        return (
            <ButtonGroup minimal={true}>
                <Popover content={<StringTranformationMenu newTransformation={this.props.newTransformation} />} position={Position.BOTTOM_LEFT}>
                    <Button rightIcon="caret-down" text="String" />
                </Popover>
            </ButtonGroup>
        );
    }
}