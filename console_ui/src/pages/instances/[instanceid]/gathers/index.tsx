import React from "react";
import {
	IResourceComponentsProps,
	useTranslate,
	GetManyResponse,
	useMany,
	useList,
} from "@refinedev/core";
import { useTable } from "@refinedev/react-table";
import { ColumnDef } from "@tanstack/react-table";
import { ScrollArea, Pagination } from "@mantine/core";
import { List, DateField, BooleanField } from "@refinedev/mantine";
import TableComponent from "@components/table";
import Link from "next/link";
import { useRouter } from "next/router";

export const GatherList: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const router = useRouter();
	const { instanceid } = router.query;

	const apiResponse = useList({
		resource: `instances/${instanceid}/gathers/apify`,
	});
	const listResponse = apiResponse?.data?.data || [];

	const columns = React.useMemo<ColumnDef<any>[]>(
		() => [
			{
				id: "description",
				accessorKey: "description",
				header: translate("gathers.fields.description"),
			},
			{
				id: "start_date",
				accessorKey: "start_date",
				header: translate("gathers.fields.start_date"),
				cell: function render({ getValue }) {
					return <DateField value={getValue<any>()} />;
				},
			},
			{
				id: "end_date",
				accessorKey: "end_date",
				header: translate("gathers.fields.end_date"),
				cell: function render({ getValue }) {
					return <DateField value={getValue<any>()} />;
				},
			},
			{
				id: "platform",
				accessorKey: "platform",
				header: translate("gathers.fields.platform"),
			},
			{
				id: "data_type",
				accessorKey: "data_type",
				header: translate("gathers.fields.data_type"),
			},
			{
				id: "instance_id",
				header: translate("gathers.fields.instance_id"),
				accessorKey: "instance_id",
				cell: function render({ getValue, table }) {
					const meta = table.options.meta as {
						instanceData: GetManyResponse;
					};

					const instance = meta.instanceData?.data?.find(
						(item) => item.id === getValue<any>()
					);

					return instance ? (
						<Link
							href={{
								pathname: "/instances/show/[instanceid]",
								query: { instanceid: instance?.id },
							}}
						>
							{instance?.name}
						</Link>
					) : (
						"Loading..."
					);
				},
			},
			{
				id: "limit_messages",
				accessorKey: "limit_messages",
				header: translate("gathers.fields.limit_messages"),
			},
			{
				id: "limit_replies",
				accessorKey: "limit_replies",
				header: translate("gathers.fields.limit_replies"),
			},
			{
				id: "nested_replies",
				accessorKey: "nested_replies",
				header: translate("gathers.fields.nested_replies"),
				cell: function render({ getValue }) {
					return <BooleanField value={getValue<any>()} />;
				},
			},
			{
				id: "id",
				accessorKey: "id",
				header: translate("gathers.fields.id"),
			},
			{
				id: "created_at",
				accessorKey: "created_at",
				header: translate("gathers.fields.created_at"),
				cell: function render({ getValue }) {
					return <DateField value={getValue<any>()} />;
				},
			},
			{
				id: "updated_at",
				accessorKey: "updated_at",
				header: translate("gathers.fields.updated_at"),
				cell: function render({ getValue }) {
					return <DateField value={getValue<any>()} />;
				},
			},
		],
		[translate]
	);
	const {
		getHeaderGroups,
		getRowModel,
		setOptions,
		refineCore: { setCurrent, pageCount, current },
	} = useTable({
		columns,
		data: listResponse,
	});

	const { data: tableData } = apiResponse;
	const { data: instanceData } = useMany({
		resource: "instances",
		ids: tableData?.data?.map((item) => item?.instance_id) ?? [],
		queryOptions: {
			enabled: !!tableData?.data,
		},
	});

	setOptions((prev) => ({
		...prev,
		meta: {
			...prev.meta,
			instanceData,
		},
	}));

	return (
		<List>
			<ScrollArea>
				<TableComponent
					headerGroups={getHeaderGroups}
					rowModel={getRowModel}
					data={apiResponse}
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

export default GatherList;
