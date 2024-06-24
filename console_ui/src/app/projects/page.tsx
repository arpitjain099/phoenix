"use client";

import React from "react";
import Link from "next/link";
import {
	IResourceComponentsProps,
	useGetIdentity,
	useTranslate,
} from "@refinedev/core";
import { ColumnDef } from "@tanstack/react-table";
import { Pagination, ScrollArea } from "@mantine/core";
import { DateField, List } from "@refinedev/mantine";
import { useTable } from "@refinedev/react-table";
import { UserInfo } from "src/interfaces/user";
import TableComponent from "../../components/table";

export const ProjectList: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const { data: user } = useGetIdentity<UserInfo>();
	const columns = React.useMemo<ColumnDef<any>[]>(
		() => [
			{
				id: "name",
				accessorKey: "name",
				header: translate("projects.fields.name"),
				cell: ({ row }) => {
					const { id, name } = row.original;
					return (
						<Link
							href={`/projects/show/${id}`}
							className="no-underline text-blue-500"
						>
							{name}
						</Link>
					);
				},
			},
			{
				id: "created_at",
				accessorKey: "created_at",
				header: translate("projects.fields.created_at"),
				cell: function render({ getValue }) {
					return getValue() ? (
						<DateField format="LLL" value={getValue<any>()} />
					) : (
						""
					);
				},
			},
			{
				id: "updated_at",
				accessorKey: "updated_at",
				header: translate("projects.fields.updated_at"),
				cell: function render({ getValue }) {
					return getValue() ? <DateField value={getValue<any>()} /> : "";
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
		<List canCreate={user?.app_role === "admin"}>
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
