import * as React from "react";

import { Intent, MenuItem } from "@blueprintjs/core";
import { ItemPredicate, ItemRenderer, MultiSelect } from "@blueprintjs/select";

export class ColumnType {
    name: string;
}

interface ColumnSelectProps {
    columns: string[],
    field: string,
    value: string,
    onValueChange: (field: string, value: any) => void
}

interface ColumnSelectState {
    columns: ColumnType[],
    field: string,
    selectedColumns: ColumnType[],
}

export class ColumnsSelect extends React.Component<ColumnSelectProps, ColumnSelectState> {
    private onValueChange: (field: string, value: any) => void;
    public state: ColumnSelectState;

    constructor(props: ColumnSelectProps) {
        super(props);
        // TODO: Add the option to set the ID
        this.onValueChange = props.onValueChange;
        let columns = props.columns.map(column => { return { name: column } });
        this.state = {
            selectedColumns: columns.filter(column => props.value.indexOf(column.name) !== -1),
            field: props.field,
            columns: props.columns.map(column => { return { name: column } })
        }
        this.setColumn = this.setColumn.bind(this);
        this.addColumn = this.addColumn.bind(this);
        this.removeColumn = this.removeColumn.bind(this);
        this.onRemoveColumn = this.onRemoveColumn.bind(this);
        this.isColumnSelected = this.isColumnSelected.bind(this);
    }

    private setColumn(column: ColumnType) {
        if (this.state.selectedColumns.indexOf(column) === -1) {
            this.addColumn(column);
        } else {
            this.removeColumn(column);
        }
    }

    private addColumn(column: ColumnType) {
        let selectedColumns = this.state.selectedColumns;
        selectedColumns.push(column);
        this.setState({ selectedColumns: selectedColumns });
        this.onColumnsChanged(selectedColumns);
    }

    private removeColumn(column: ColumnType) {
        let selectedColumns = this.state.selectedColumns;
        let index = selectedColumns.indexOf(column);
        this.onRemoveColumn(column.name, index);
    }

    private onRemoveColumn(_tag: string, index: number) {
        let selectedColumns = this.state.selectedColumns;
        selectedColumns = selectedColumns.filter((_column, i) => i !== index);
        this.setState({ selectedColumns: selectedColumns.filter((_column, i) => i !== index) });
        this.onColumnsChanged(selectedColumns);
    }

    private onColumnsChanged(selectedColumns: ColumnType[]) {
        this.onValueChange(this.state.field, selectedColumns.map((column: ColumnType) => column.name));
    }

    private isColumnSelected(column: ColumnType) {
        return this.state.selectedColumns.indexOf(column) !== -1
    }

    private renderColumn: ItemRenderer<ColumnType> = (column, { modifiers, handleClick }) => {
        if (!modifiers.matchesPredicate) {
            return null;
        }
        return (
            <MenuItem
                active={modifiers.active}
                icon={this.isColumnSelected(column) ? "tick" : "blank"}
                key={column.name}
                onClick={handleClick}
                text={column.name}
                shouldDismissPopover={false}
            />
        );
    };

    private renderTag = (column: ColumnType) => column.name;

    private filter: ItemPredicate<ColumnType> = (query, item, _index, exactMatch) => {
        const normalizedTitle = item.name.toLowerCase();
        const normalizedQuery = query.toLowerCase();

        if (exactMatch) {
            return normalizedTitle === normalizedQuery;
        } else {
            return `${normalizedTitle}`.indexOf(normalizedQuery) >= 0;
        }
    };

    render() {
        const ColumnTypeSelect = MultiSelect.ofType<ColumnType>();
        // TODO: Make the available columns dependent on the column and transformation type
        // TODO: Check which columns are actually available at each step
        return <ColumnTypeSelect
            itemPredicate={this.filter}
            itemRenderer={this.renderColumn}
            tagRenderer={this.renderTag}
            popoverProps={{ minimal: true }}
            items={this.state.columns}
            key={`transformation-input-${this.state.field}`}
            noResults={<MenuItem disabled={true} text="No results." />}
            onItemSelect={this.setColumn}
            selectedItems={this.state.selectedColumns}
            tagInputProps={{ tagProps: { intent: Intent.NONE, minimal: false }, onRemove: this.onRemoveColumn }}
        >
        </ColumnTypeSelect>
    }
}
