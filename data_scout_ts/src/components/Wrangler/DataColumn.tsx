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
		if (this.type === "datetime") {
			return <MenuItem /*icon="translate"*/ text="Datetime" >
				<MenuItem onClick={() => this.newTransformation("datetime-extract-year", {field: this.name})} text="Extract year" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-month", {field: this.name})} text="Extract month" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-monthname", {field: this.name})} text="Extract month name" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-endofmonth", {field: this.name})} text="Extract last day of month" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-day", {field: this.name})} text="Extract day of the month" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-week", {field: this.name})} text="Extract week number" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-dayofweek", {field: this.name})} text="Extract day of the week" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-dayofweekname", {field: this.name})} text="Extract name of day of the week" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-dayofyear", {field: this.name})} text="Extract day of the year" />
				<MenuDivider />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-hours", {field: this.name})} text="Extract the hour" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-minutes", {field: this.name})} text="Extract minutes" />
				<MenuItem onClick={() => this.newTransformation("datetime-extract-seconds", {field: this.name})} text="Extract the seconds" />
				<MenuDivider />
				<MenuItem onClick={() => this.newTransformation("datetime-format", {field: this.name})} text="Format datetime" />
				<MenuDivider />
				<MenuItem onClick={() => this.newTransformation("datetime-date-add", {field: this.name})} text="Datetime add" />
				<MenuItem onClick={() => this.newTransformation("datetime-date-diff", {field: this.name})} text="Datetime difference" />
				<MenuItem onClick={() => this.newTransformation("datetime-now", {field: this.name})} text="Current datetime" />
				<MenuItem onClick={() => this.newTransformation("datetime-today", {field: this.name})} text="Today" />
			</MenuItem>
		}
		return <MenuItem /*icon="translate"*/ disabled text="Datetime" />;
	}

	private number() {
		if (this.type === "number") {
			return <MenuItem /*icon="translate"*/ text="Number" >
				<MenuItem onClick={() => this.newTransformation("format-number", {field: this.name})} text="Change number format" />
			</MenuItem>
		}
		return <MenuItem /*icon="translate"*/ disabled text="Number" />;
	}

	private list() {
		if (this.type === "list") {
			return <MenuItem /*icon="translate"*/ text="List" >
				<MenuItem onClick={() => this.newTransformation("data-field-column", {field: this.name })} text="To columns" />
				<MenuItem onClick={() => this.newTransformation("array-index", {field: this.name})} text="Index by value" />
				<MenuItem onClick={() => this.newTransformation("array-at-index", {field: this.name})} text="Value at index" />
				<MenuItem onClick={() => this.newTransformation("array-slice", {field: this.name})} text="Slice" />
				<MenuItem onClick={() => this.newTransformation("array-length", {field: this.name})} text="Length" />
				<MenuItem onClick={() => this.newTransformation("array-mean", {field: this.name})} text="Mean" />
				<MenuItem onClick={() => this.newTransformation("array-sum", {field: this.name})} text="Sum" />
				<MenuItem onClick={() => this.newTransformation("array-min", {field: this.name})} text="Min" />
				<MenuItem onClick={() => this.newTransformation("array-max", {field: this.name})} text="Max" />
				<MenuItem onClick={() => this.newTransformation("array-mode", {field: this.name})} text="Mode" />
				<MenuItem onClick={() => this.newTransformation("array-std", {field: this.name})} text="Standard deviation" />
				<MenuItem onClick={() => this.newTransformation("array-var", {field: this.name})} text="Variance" />
				<MenuItem onClick={() => this.newTransformation("array-sort", {field: this.name})} text="Sort" />
				<MenuItem onClick={() => this.newTransformation("array-concat", {fields: [this.name]})} text="Concat" />
				<MenuItem onClick={() => this.newTransformation("array-intersect", {fields: [this.name]})} text="Intersect" />
				<MenuItem onClick={() => this.newTransformation("array-unique", {fields: [this.name]})} text="Unique" />
				<MenuItem onClick={() => this.newTransformation("array-filter", {field: this.name})} text="Filter" />
				<MenuItem onClick={() => this.newTransformation("array-to-dict", {field_keys: this.name})} text="To dictionary" />
				<MenuItem onClick={() => this.newTransformation("array-merge", {field: this.name})} text="Merge" />
				<MenuItem onClick={() => this.createTransformation("array-flatten", {field: this.name})} text="Flatten" />
			</MenuItem>
		}
		return <MenuItem /*icon="translate"*/ disabled text="List" />;
	}

	private dict() {
		if (this.type === "dict") {
			return <MenuItem /*icon="translate"*/ text="Dictionary" >
				<MenuItem onClick={() => this.newTransformation("data-field-column", {field: this.name })} text="To columns" />
				<MenuItem onClick={() => this.newTransformation("dict-get", {field: this.name})} text="Get by key" />
				<MenuItem onClick={() => this.newTransformation("dict-keys", {field: this.name})} text="Keys" />
				<MenuItem onClick={() => this.newTransformation("dict-values", {field: this.name})} text="Values" />
			</MenuItem>
		}
		return <MenuItem /*icon="translate"*/ disabled text="Dictionary" />;
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
				{this.number()}
				{this.list()}
				{this.dict()}
				<MenuItem text="Filter" >
					<MenuItem onClick={() => this.createTransformation("filter-value-missing", {field: this.name})} text="Missing" />
					<MenuItem onClick={() => this.createTransformation("filter-value-mismatched", {field: this.name})} text="Mismatched" />
				</MenuItem>
				<MenuItem onClick={() => this.createTransformation("duplicate-column", {field: this.name })} text="Duplicate column" />
				<MenuItem onClick={() => this.createTransformation("drop-column", {field: this.name })} text="Drop column" />
			</Menu>
		);
	}
}
