import React from "react";
import { IResourceComponentsProps, useTranslate } from "@refinedev/core";
import { useTable } from "@refinedev/react-table";
import { ColumnDef, flexRender } from "@tanstack/react-table";
import { ScrollArea, Table, Pagination, Group } from "@mantine/core";
import {
	List,
	EditButton,
	ShowButton,
	DeleteButton,
	DateField,
} from "@refinedev/mantine";

export const InstanceList: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const columns = React.useMemo<ColumnDef<any>[]>(
		() => [
			{
				id: "name",
				accessorKey: "name",
				header: translate("instances.fields.name"),
			},
			{
				id: "status",
				accessorKey: "status",
				header: translate("instances.fields.status"),
			},
			{
				id: "created_at",
				accessorKey: "created_at",
				header: translate("instances.fields.created_at"),
				cell: function render({ getValue }) {
					return <DateField value={getValue<any>()} />;
				},
			},
			{
				id: "actions",
				accessorKey: "id",
				header: translate("table.actions"),
				cell: function render({ getValue }) {
					return (
						<Group spacing="xs" noWrap>
							<ShowButton hideText recordItemId={getValue() as string} />
							<EditButton hideText recordItemId={getValue() as string} />
							<DeleteButton hideText recordItemId={getValue() as string} />
						</Group>
					);
				},
			},
		],
		[translate]
	);

	const {
		getHeaderGroups,
		getRowModel,
		setOptions,
		refineCore: {
			setCurrent,
			pageCount,
			current,
			tableQueryResult: { data: tableData },
		},
	} = useTable({
		columns,
	});

	setOptions((prev) => ({
		...prev,
		meta: {
			...prev.meta,
		},
	}));

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

export default InstanceList;
