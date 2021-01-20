import * as React from "react";

import { Menu, MenuItem, MenuDivider } from "@blueprintjs/core";

import { AbstractSortableColumn, ISortCallback } from "./AbstractSortableColumn";

export class DataColumn extends AbstractSortableColumn {
	// Create transformation creates a transformation directly, new transformation show a popup where the user can change settings.
	private createTransformation: (transformation: string, kwargs: { [key: string]: any }) => void;
	private newTransformation: (transformation: string, kwargs: { [key: string]: any }) => void;
	private type: string;

	constructor(name: string, index: number, type: string,
				createTransformation: (transformation: string, kwargs: { [key: string]: any }) => void, 
				newTransformation: (transformation: string, kwargs: { [key: string]: any }) => void) {
		super(name, index);
		this.type = type;
		this.createTransformation = createTransformation;
		this.newTransformation = newTransformation;
	}

	public getName(): string {
		return this.name;
	}

	private datetime() {
		if (this.type == "datetime") {
			return <MenuItem /*icon="translate"*/ text="Datetime" >
				<MenuItem onClick={() => this.newTransformation("datetime-extract-year", {field: this.name})} text="Extract year" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-month", {field: this.name})} text="Extract month" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-day", {field: this.name})} text="Extract day of the month" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-week", {field: this.name})} text="Extract week number" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-dayofweek", {field: this.name})} text="Extract day of the week" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-dayofyear", {field: this.name})} text="Extract day of the year" />
				<MenuDivider />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-hours", {field: this.name})} text="Extract the hour" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-minutes", {field: this.name})} text="Extract minutes" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-seconds", {field: this.name})} text="Extract the seconds" />
				<MenuDivider />
				<MenuItem onClick={() => this.newTransformation("datetime-format", {field: this.name})} text="Format datetime" />
			</MenuItem>
		}
		return <MenuItem /*icon="translate"*/ disabled text="Datetime" />;
	}

	private filter() {
		if (this.type == "datetime") {
			return <MenuItem /*icon="translate"*/ text="Datetime" >
				<MenuItem onClick={() => this.newTransformation("datetime-extract-timestamp", {field: this.name})} text="Extract timestamp" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-year", {field: this.name})} text="Extract year" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-month", {field: this.name})} text="Extract month" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-day", {field: this.name})} text="Extract day of the month" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-week", {field: this.name})} text="Extract week number" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-dayofweek", {field: this.name})} text="Extract day of the week" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-dayofyear", {field: this.name})} text="Extract day of the year" />
				<MenuDivider />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-hours", {field: this.name})} text="Extract the hour" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-minutes", {field: this.name})} text="Extract minutes" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-seconds", {field: this.name})} text="Extract the seconds" />
				<MenuDivider />
				<MenuItem onClick={() => this.newTransformation("datetime-format", {field: this.name})} text="Format datetime" />
			</MenuItem>
		}
		return <MenuItem /*icon="translate"*/ disabled text="Datetime" />;
	}

	protected renderMenu(sortColumn: ISortCallback) {
		let convertStringMethod = this.type == "datetime" ? this.newTransformation : this.createTransformation;
		let convertStringTransformation = this.type == "datetime" ? "datetime-format": "data-convert";
		let convertStringKwargs = this.type == "datetime" ? {field: this.name} : {to: "string", field: this.name };
		return (
			<Menu>
				<MenuItem icon="translate" text="Convert">
					<MenuItem disabled={this.type == "int"} onClick={() => this.createTransformation("data-convert", {to: "int", field: this.name })} text="Integer" />
					<MenuItem disabled={this.type == "float"} onClick={() => this.createTransformation("data-convert", {to: "float", field: this.name })} text="Floating point number" />
					<MenuItem disabled={this.type == "str"} onClick={() => convertStringMethod(convertStringTransformation, convertStringKwargs)} text="Text" />
					<MenuItem disabled={this.type == "datetime"} onClick={() => this.newTransformation("data-convert-datetime", {field: this.name })} text="Datetime" />
				</MenuItem>
				{this.datetime()}
				<MenuItem disabled={this.type != "list" && this.type != "dict"} onClick={() => this.newTransformation("data-field-column", {field: this.name })} text="To columns" />
				<MenuItem text="Filter" >
					<MenuItem onClick={() => this.createTransformation("filter-value-missing", {field: this.name})} text="Missing" />
					<MenuItem onClick={() => this.createTransformation("filter-value-mismatched", {field: this.name})} text="Mismatched" />
				</MenuItem>
			</Menu>
		);
	}
}
