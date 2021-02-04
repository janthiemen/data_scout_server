/*
 * Copyright 2017 Palantir Technologies, Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import * as React from "react";
import autobind from 'class-autobind';

import {
    Button,
    ButtonGroup,
    Hotkey,
    Hotkeys,
    HotkeysTarget,
    MenuItem,
    Position,
    Toaster,
} from "@blueprintjs/core";

import { ItemPredicate, ItemRenderer, Omnibar } from "@blueprintjs/select";

import { TransformationMetaQA, TRANSFORMATIONS } from './Transformation'

const QAOmnibar = Omnibar.ofType<TransformationMetaQA>();

interface QuickAccessProps {
    newTransformation: (transformationType: string, kwargs: { [key: string]: any }) => void;
}

interface QuickAccessState {
    isOpen: boolean;
}

@HotkeysTarget
export class QuickAccess extends React.PureComponent<QuickAccessProps, QuickAccessState> {
    private newTransformation: (transformationType: string, kwargs: { [key: string]: any }) => void;
    public state: QuickAccessState = {
        isOpen: false,
    };

    private toaster: Toaster;

    private refHandlers = {
        toaster: (ref: Toaster) => (this.toaster = ref),
    };

    constructor(props: QuickAccessProps) {
        super(props);
        autobind(this);
        this.newTransformation = props.newTransformation;
    }

    public renderHotkeys() {
        return (
            <Hotkeys>
                <Hotkey
                    global={true}
                    combo="shift + o"
                    label="Show Omnibar"
                    onKeyDown={this.handleToggle}
                    // prevent typing "O" in omnibar input
                    preventDefault={true}
                />
            </Hotkeys>
        );
    }

    protected escapeRegExpChars(text: string) {
        return text.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
    }

    protected highlightText(text: string, query: string) {
        let lastIndex = 0;
        const words = query
            .split(/\s+/)
            .filter(word => word.length > 0)
            .map(this.escapeRegExpChars);
        if (words.length === 0) {
            return [text];
        }
        const regexp = new RegExp(words.join("|"), "gi");
        const tokens: React.ReactNode[] = [];
        while (true) {
            const match = regexp.exec(text);
            if (!match) {
                break;
            }
            const length = match[0].length;
            const before = text.slice(lastIndex, regexp.lastIndex - length);
            if (before.length > 0) {
                tokens.push(before);
            }
            lastIndex = regexp.lastIndex;
            tokens.push(<strong key={lastIndex}>{match[0]}</strong>);
        }
        const rest = text.slice(lastIndex);
        if (rest.length > 0) {
            tokens.push(rest);
        }
        return tokens;
    }

    protected filterTransformation: ItemPredicate<TransformationMetaQA> = (query, transformation, _index, exactMatch) => {
        const normalizedTitle = transformation.key.toLowerCase();
        const normalizedQuery = query.toLowerCase();
    
        if (exactMatch) {
            return normalizedTitle === normalizedQuery;
        } else {
            return `${normalizedTitle}`.indexOf(normalizedQuery) >= 0;
        }
    };

    protected areTransformationsEqual(transformationA: TransformationMetaQA, transformationB: TransformationMetaQA) {
        // Compare only the titles (ignoring case) just for simplicity.
        return transformationA.key.toLowerCase() === transformationB.key.toLowerCase();
    }

    protected renderTransformation: ItemRenderer<TransformationMetaQA> = (transformation, { handleClick, modifiers, query }) => {
        if (!modifiers.matchesPredicate) {
            return null;
        }
        const text = `${transformation.key}`;
        return (
            <MenuItem
                active={modifiers.active}
                disabled={modifiers.disabled}
                // label={transformation.key}
                key={transformation.id}
                onClick={handleClick}
                text={this.highlightText(text, query)}
            />
        );
    };

    public render() {
        return (
            <span>
                <ButtonGroup minimal={true}>
                    <Button icon="search" text="Quick Access" onClick={this.handleClick} />
                </ButtonGroup>

                <QAOmnibar
                    {...this.state}
                    inputProps={{placeholder: "Search (use Shift + O to open)"}}
                    itemsEqual={this.areTransformationsEqual}
                    itemPredicate={this.filterTransformation}
                    itemRenderer={this.renderTransformation}
                    noResults={<MenuItem disabled={true} text="No results." />}
                    onItemSelect={this.handleItemSelect}
                    onClose={this.handleClose}
                    items={Object.keys(TRANSFORMATIONS).map((key, index) => ({ ...TRANSFORMATIONS[key], id: key }))}
                />
                <Toaster position={Position.TOP} ref={this.refHandlers.toaster} />
            </span>
        );
    }

    private handleClick = (_event: React.MouseEvent<HTMLElement>) => {
        this.setState({ isOpen: true });
    };

    private handleItemSelect = (transformation: TransformationMetaQA) => {
        this.setState({ isOpen: false });
        this.newTransformation(transformation.id, {})
    };

    private handleClose = () => this.setState({ isOpen: false });

    private handleToggle = () => this.setState({ isOpen: !this.state.isOpen });
}
