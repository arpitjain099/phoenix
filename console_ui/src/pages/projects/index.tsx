import React from "react";
import { IResourceComponentsProps, useTranslate } from "@refinedev/core";
import { ColumnDef } from "@tanstack/react-table";
import { Group, Pagination, ScrollArea } from "@mantine/core";
import { EditButton, ShowButton, DateField, List } from "@refinedev/mantine";
import { useTable } from "@refinedev/react-table";
import TableComponent from "../../components/table";

export const ProjectList: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const columns = React.useMemo<ColumnDef<any>[]>(
		() => [
			{
				id: "name",
				accessorKey: "name",
				header: translate("projects.fields.name"),
			},
			{
				id: "status",
				accessorKey: "status",
				header: translate("projects.fields.status"),
			},
			{
				id: "created_at",
				accessorKey: "created_at",
				header: translate("projects.fields.created_at"),
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

	return (
		<List>
			<ScrollArea>
				<TableComponent
					headerGroups={getHeaderGroups}
					rowModel={getRowModel}
					data={tableQueryResult}
				/>
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

export default ProjectList;
