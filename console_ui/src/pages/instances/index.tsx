import React from "react";
import { IResourceComponentsProps, useTranslate } from "@refinedev/core";
import { ColumnDef } from "@tanstack/react-table";
import { Group } from "@mantine/core";
import {
	EditButton,
	ShowButton,
	DeleteButton,
	DateField,
} from "@refinedev/mantine";
import TableComponent from "../../components/table";

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
						</Group>
					);
				},
			},
		],
		[translate]
	);

	return <TableComponent columns={columns} />;
};

export default InstanceList;
