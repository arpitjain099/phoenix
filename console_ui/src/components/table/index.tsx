import React from "react";
import { useTable } from "@refinedev/react-table";
import { flexRender } from "@tanstack/react-table";
import { ScrollArea, Table, Pagination, Skeleton } from "@mantine/core";
import { List } from "@refinedev/mantine";

interface ITableProps {
	columns: any;
}

const TableComponent: React.FC<ITableProps> = ({ columns }) => {
	const {
		getHeaderGroups,
		getRowModel,
		setOptions,
		refineCore: { setCurrent, pageCount, current, tableQueryResult },
	} = useTable({
		columns,
	});

	setOptions((prev) => ({
		...prev,
		meta: {
			...prev.meta,
		},
	}));

	if (tableQueryResult?.isLoading) {
		return <Skeleton />;
	}
	return (
		<List>
			<ScrollArea>
				<Table highlightOnHover>
					<thead>
						{getHeaderGroups().map((headerGroup) => (
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
						{getRowModel().rows.map((row) => (
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
			</ScrollArea>
			<br />
			<Pagination
				position="right"
				total={pageCount}
				page={current}
				onChange={setCurrent}
			/>
		</List>
	);
};

export default TableComponent;
