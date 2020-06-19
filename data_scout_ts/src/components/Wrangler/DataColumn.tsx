import * as React from "react";

import { Menu, MenuItem } from "@blueprintjs/core";

import { AbstractSortableColumn, ISortCallback } from "./AbstractSortableColumn";

export class DataColumn extends AbstractSortableColumn {
	private createTransformation: (transformation: string, kwargs: { [key: string]: any }) => void;

	constructor(name: string, index: number, createTransformation: (transformation: string, kwargs: { [key: string]: any }) => void) {
		super(name, index);
		this.createTransformation = createTransformation;
	}

	public getName(): string {
		return this.name;
	}

	protected renderMenu(sortColumn: ISortCallback) {
		return (
			<Menu>
				<MenuItem icon="translate" text="Convert">
					<MenuItem onClick={() => this.createTransformation("convert", {to: "int", field: this.name })} text="Integer" />
					<MenuItem onClick={() => this.createTransformation("convert", {to: "float", field: this.name })} text="Floating point number" />
					<MenuItem onClick={() => this.createTransformation("convert", {to: "string", field: this.name })} text="Text" />
				</MenuItem>
			</Menu>
		);
	}
}
