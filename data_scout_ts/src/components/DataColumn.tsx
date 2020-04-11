import * as React from "react";

import { Menu, MenuItem } from "@blueprintjs/core";

import { AbstractSortableColumn, ISortCallback } from "./AbstractSortableColumn";

export class DataColumn extends AbstractSortableColumn {
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
