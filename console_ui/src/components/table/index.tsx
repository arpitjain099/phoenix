import React from "react";
import { HeaderGroup, RowModel, flexRender } from "@tanstack/react-table";
import { Table, Skeleton } from "@mantine/core";

interface ITableProps {
	headerGroups: () => HeaderGroup<any>[];
	rowModel: () => RowModel<any>;
	data: any;
}

const TableComponent: React.FC<ITableProps> = ({
	headerGroups,
	rowModel,
	data,
}) => {
	if (data?.isLoading) {
		return <Skeleton />;
	}
	return (
		<Table highlightOnHover>
			<thead>
				{headerGroups().map((headerGroup) => (
					<tr key={headerGroup.id}>
						{headerGroup.headers.map((header) => (
							<th key={header.id}>
								{!header.isPlaceholder &&
									flexRender(
										header.column.columnDef.header,
										header.getContext()
									)}
							</th>
						))}
					</tr>
				))}
			</thead>
			<tbody>
				{rowModel().rows.map((row) => (
					<tr key={row.id}>
						{row.getVisibleCells().map((cell) => (
							<td key={cell.id}>
								{flexRender(cell.column.columnDef.cell, cell.getContext())}
							</td>
						))}
					</tr>
				))}
			</tbody>
		</Table>
	);
};

export default TableComponent;
