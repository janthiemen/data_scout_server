import './App.css';

// tslint:disable max-classes-per-file

import * as React from "react";

import { Menu, MenuItem } from "@blueprintjs/core";

import {
	Cell,
	Column,
	ColumnHeaderCell,
	CopyCellsMenuItem,
	IMenuContext,
	SelectionModes,
	Table,
	Utils,
} from "@blueprintjs/table";

// tslint:disable-next-line:no-var-requires
const sumo = require("./sumo.json") as any[];

export type ICellLookup = (rowIndex: number, columnIndex: number) => any;
export type ISortCallback = (columnIndex: number, comparator: (a: any, b: any) => number) => void;

export interface ISortableColumn {
	getColumn(getCellData: ICellLookup, sortColumn: ISortCallback): JSX.Element;
}

abstract class AbstractSortableColumn implements ISortableColumn {
	constructor(protected name: string, protected index: number) { }

	public getColumn(getCellData: ICellLookup, sortColumn: ISortCallback) {
		const cellRenderer = (rowIndex: number, columnIndex: number) => (
			<Cell>{getCellData(rowIndex, columnIndex)}</Cell>
		);
		const menuRenderer = this.renderMenu.bind(this, sortColumn);
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

	protected abstract renderMenu(sortColumn: ISortCallback): JSX.Element;
}

class DataColumn extends AbstractSortableColumn {
	protected renderMenu(sortColumn: ISortCallback) {
		return (
			<Menu>
				<MenuItem icon="style" text="Transform">
					<MenuItem icon="bold" text="Bold" />
					<MenuItem icon="italic" text="Italic" />
					<MenuItem icon="underline" text="Underline" />
				</MenuItem>
			</Menu>
		);
	}
}

export class DataTable extends React.PureComponent {
	public state = {
		columns: [
			new DataColumn("Rikishi", 0),
			new DataColumn("Rank - Hatsu Basho", 1),
			new DataColumn("Record - Hatsu Basho", 2),
			new DataColumn("Rank - Haru Basho", 3),
			new DataColumn("Record - Haru Basho", 4),
			new DataColumn("Rank - Natsu Basho", 5),
			new DataColumn("Record - Natsu Basho", 6),
			new DataColumn("Rank - Nagoya Basho", 7),
			new DataColumn("Record - Nagoya Basho", 8),
			new DataColumn("Rank - Aki Basho", 9),
			new DataColumn("Record - Aki Basho", 10),
			new DataColumn("Rank - Kyūshū Basho", 11),
			new DataColumn("Record - Kyūshū Basho", 12),
		] as ISortableColumn[],
		data: sumo,
		sortedIndexMap: [] as number[],
	};

	public render() {
		const numRows = this.state.data.length;
		const columns = this.state.columns.map(col => col.getColumn(this.getCellData, this.sortColumn));
		return (
			<Table
				bodyContextMenuRenderer={this.renderBodyContextMenu}
				numRows={numRows}
				selectionModes={SelectionModes.COLUMNS_AND_CELLS}
			>
				{columns}
			</Table>
		);
	}

	private getCellData = (rowIndex: number, columnIndex: number) => {
		const sortedRowIndex = this.state.sortedIndexMap[rowIndex];
		if (sortedRowIndex != null) {
			rowIndex = sortedRowIndex;
		}
		return this.state.data[rowIndex][columnIndex];
	};

	private renderBodyContextMenu = (context: IMenuContext) => {
		return (
			<Menu>
				<CopyCellsMenuItem context={context} getCellData={this.getCellData} text="Copy" />
			</Menu>
		);
	};

	private sortColumn = (columnIndex: number, comparator: (a: any, b: any) => number) => {
		const { data } = this.state;
		const sortedIndexMap = Utils.times(data.length, (i: number) => i);
		sortedIndexMap.sort((a: number, b: number) => {
			return comparator(data[a][columnIndex], data[b][columnIndex]);
		});
		this.setState({ sortedIndexMap });
	};
}

function App() {
	return (
		<div className="App">
			<DataTable />
		</div>
	);
}

export default App;
