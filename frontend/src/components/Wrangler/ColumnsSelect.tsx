import * as React from "react";
import autobind from 'class-autobind';

import { Intent, MenuItem } from "@blueprintjs/core";
import { ItemPredicate, ItemRenderer, MultiSelect } from "@blueprintjs/select";

export class ColumnType {
    name: string;
}

interface ColumnSelectProps {
    columns: { [key: string]: string},
    columnType?: string[],
    field: string,
    value: string,
    onValueChange: (field: string, value: any) => void
}

interface ColumnSelectState {
    columns: ColumnType[],
    field: string,
    selectedColumns: ColumnType[],
}

/**
 * This component is used in the transformation dialog to select multiple column names.
 */
export class ColumnsSelect extends React.Component<ColumnSelectProps, ColumnSelectState> {
    private onValueChange: (field: string, value: any) => void;
    public state: ColumnSelectState;

    constructor(props: ColumnSelectProps) {
        super(props);
        autobind(this);
        // TODO: Add the option to set the ID
        this.onValueChange = props.onValueChange;
        let columns = Object.keys(props.columns).map(column => { return { name: column } });
        // Create a list of available columns. If only certain data types are allowed (e.g. strings), the column list is filtered to only show those.
        let availableColumns = columns.filter(function (column) {
            if (props.columnType === undefined || props.columnType.length === 0 || props.columnType.indexOf(props.columns[column.name]) !== -1) {
                return column
            }
            return false;
        });
        this.state = {
            selectedColumns: columns.filter(column => props.value.indexOf(column.name) !== -1),
            field: props.field,
            columns: availableColumns
        }
    }

    /**
     * Add or delete a column to/from the list of selected columns.
     * @param column 
     */
    private setColumn(column: ColumnType) {
        if (this.state.selectedColumns.indexOf(column) === -1) {
            this.addColumn(column);
        } else {
            this.removeColumn(column);
        }
    }

    /**
     * Add a column to the list of selected columns.
     * @param column 
     */
    private addColumn(column: ColumnType) {
        let selectedColumns = this.state.selectedColumns;
        selectedColumns.push(column);
        this.setState({ selectedColumns: selectedColumns });
        this.onColumnsChanged(selectedColumns);
    }

    /**
     * Call the method to delete a column from the list of selected columns.
     * @param column 
     */
    private removeColumn(column: ColumnType) {
        let selectedColumns = this.state.selectedColumns;
        let index = selectedColumns.indexOf(column);
        this.onRemoveColumn(column.name, index);
    }

    /**
     * Delete a column from the list of selected columns.
     * @param _tag The column name
     * @param index The index of the column in the list of selected columns
     */
     private onRemoveColumn(_tag: string, index: number) {
        let selectedColumns = this.state.selectedColumns;
        selectedColumns = selectedColumns.filter((_column, i) => i !== index);
        this.setState({ selectedColumns: selectedColumns.filter((_column, i) => i !== index) });
        this.onColumnsChanged(selectedColumns);
    }

    /**
     * Propagate the list of selected columns to the parent transformation.
     * @param selectedColumns 
     */
    private onColumnsChanged(selectedColumns: ColumnType[]) {
        this.onValueChange(this.state.field, selectedColumns.map((column: ColumnType) => column.name));
    }

    /**
     * Check if a column is currently selected
     * @param column 
     * @returns bool
     */
    private isColumnSelected(column: ColumnType) {
        return this.state.selectedColumns.indexOf(column) !== -1
    }

    /**
     * Render a column menu item for the select list.
     * @param column 
     * @param param1 
     * @returns 
     */
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

    /**
     * Filter the columns by name.
     * @param query 
     * @param item 
     * @param _index 
     * @param exactMatch 
     * @returns 
     */
    private filter: ItemPredicate<ColumnType> = (query, item, _index, exactMatch) => {
        const normalizedTitle = item.name.toLowerCase();
        const normalizedQuery = query.toLowerCase();

        if (exactMatch) {
            return normalizedTitle === normalizedQuery;
        } else {
            return `${normalizedTitle}`.indexOf(normalizedQuery) >= 0;
        }
    };

    /**
     * Render the input box.
     * @returns 
     */
    render() {
        const ColumnTypeSelect = MultiSelect.ofType<ColumnType>();
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
