import * as React from "react";
import { ItemRenderer, ItemPredicate, Select } from "@blueprintjs/select";
import { MenuItem } from "@blueprintjs/core";

function escapeRegExpChars(text: string) {
    return text.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}

export function highlightText(text: string, query: string) {
    let lastIndex = 0;
    const words = query
        .split(/\s+/)
        .filter(word => word.length > 0)
        .map(escapeRegExpChars);
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

export interface DefaultItem {
    title: string;
    id: number;
    label: string;
}

export const defaultItemRenderer: ItemRenderer<DefaultItem> = (item, { handleClick, modifiers, query }) => {
    if (!modifiers.matchesPredicate) {
        return null;
    }
    const text = `${item.title}`;
    return (
        <MenuItem
            active={modifiers.active}
            disabled={modifiers.disabled}
            label={item.label}
            key={item.id}
            onClick={handleClick}
            text={highlightText(text, query)}
        />
    );
};

export const defaultItemFilterer: ItemPredicate<DefaultItem> = (query, item, _index, exactMatch) => {
    const normalizedTitle = item.title.toLowerCase();
    const normalizedQuery = query.toLowerCase();

    if (exactMatch) {
        return normalizedTitle === normalizedQuery;
    } else {
        return `${normalizedTitle}`.indexOf(normalizedQuery) >= 0;
    }
};

export const defaultSelectSettings = {itemPredicate: defaultItemFilterer, itemRenderer: defaultItemRenderer, noResults: <MenuItem disabled={true} text="No results." />};
export const DefaultSelect = Select.ofType<DefaultItem>();