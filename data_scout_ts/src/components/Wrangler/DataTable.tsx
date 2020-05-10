import * as React from "react";

import { Menu } from "@blueprintjs/core";

import {
	CopyCellsMenuItem,
	IMenuContext,
	SelectionModes,
	Table,
	Utils,
	TableLoadingOption,
} from "@blueprintjs/table";

import { DataColumn } from "./DataColumn";

interface DataTableProps {
    data: number[][];
	columns: DataColumn[];
	loading: boolean;
}

interface DataTableState {
	columns: DataColumn[];
	data: number[][];
	sortedIndexMap: number[];
	loading: boolean;
}

export class DataTable extends React.PureComponent<DataTableProps, DataTableState> {
	public state: DataTableState;

	constructor(props: DataTableProps) {
		super(props);
		this.state = {
            data: props.data,
            columns: props.columns,
            sortedIndexMap: [] as number[],
            loading: props.loading,
        };

	}

	/**
     * Called when new props are received.
     * @param props The new props
     */
    componentWillReceiveProps(props: DataTableProps) {
        this.setState({
            data: props.data,
            columns: props.columns,
            loading: props.loading
        });
    }

	public render() {
		const numRows = this.state.data.length;
		const columns = this.state.columns.map(col => col.getColumn(this.getCellData, this.sortColumn));
		return (
			<Table
				loadingOptions={this.state.loading ? [TableLoadingOption.CELLS, TableLoadingOption.COLUMN_HEADERS, TableLoadingOption.ROW_HEADERS]: []}
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
