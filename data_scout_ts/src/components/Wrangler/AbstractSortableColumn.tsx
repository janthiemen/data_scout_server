import * as React from "react";

import {
	Cell,
	Column,
	ColumnHeaderCell,
} from "@blueprintjs/table";

export type ICellLookup = (rowIndex: number, columnIndex: number) => any;
export type ISortCallback = (columnIndex: number, comparator: (a: any, b: any) => number) => void;


export abstract class AbstractSortableColumn {
	constructor(protected name: string, protected index: number) { }

	public getColumn(getCellData: ICellLookup, sortColumn: ISortCallback) {
		const cellRenderer = (rowIndex: number, columnIndex: number) => (
			<Cell>{getCellData(rowIndex, columnIndex)}</Cell>
		);
		const menuRenderer = this.renderMenu.bind(this, sortColumn, "test");
		const columnHeaderCellRenderer = () => <ColumnHeaderCell name={this.name} menuRenderer={menuRenderer} />;
		return (
			<Column
				cellRenderer={cellRenderer}
				columnHeaderCellRenderer={columnHeaderCellRenderer}
				key={this.index}
				name={this.name}
			/>
		);
	}

	protected abstract renderMenu(sortColumn: ISortCallback, test: string): JSX.Element;
}
