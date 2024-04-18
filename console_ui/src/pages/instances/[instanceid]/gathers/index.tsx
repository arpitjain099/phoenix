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
import {
	ScrollArea,
	Pagination,
	Anchor,
	Breadcrumbs,
	Group,
} from "@mantine/core";
import { List, DateField } from "@refinedev/mantine";
import TableComponent from "@components/table";
import Link from "next/link";
import { useRouter } from "next/router";

const breadcrumbs = [
	{ title: "Instances", href: "/instances" },
	{ title: "Gathers", href: "#" },
].map((item) => (
	<Group key={item.title}>
		<Anchor color="gray" size="sm" href={item.href}>
			{item.title}
		</Anchor>
	</Group>
));

export const GatherList: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const router = useRouter();
	const { instanceid } = router.query;

	const apiResponse = useList({
		resource: `instances/${instanceid}/gathers`,
	});
	const listResponse = apiResponse?.data?.data || [];

	const columns = React.useMemo<ColumnDef<any>[]>(
		() => [
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
				id: "created_at",
				accessorKey: "created_at",
				header: translate("gathers.fields.created_at"),
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
		<List breadcrumb={<Breadcrumbs>{breadcrumbs}</Breadcrumbs>}>
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
