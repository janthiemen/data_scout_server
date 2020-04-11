import * as React from "react";

import { Menu } from "@blueprintjs/core";

import {
	CopyCellsMenuItem,
	IMenuContext,
	SelectionModes,
	Table,
	Utils,
} from "@blueprintjs/table";

import { ISortableColumn } from "./AbstractSortableColumn";
import {DataColumn} from "./DataColumn"

interface IProps {
	/** An object of data to display. */
    data?: [][];
}

interface IState {
	columns: ISortableColumn[];
	data: [][];
	sortedIndexMap: number[];
}

export class DataTable extends React.PureComponent<IProps, IState> {
	constructor(props: any) {
		super(props);
		this.state = {
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
			data: props.data as [],
			sortedIndexMap: [] as number[],
		};
		this.setState({data: props.data});
	}

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
