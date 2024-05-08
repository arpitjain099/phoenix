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
import { List, DateField } from "@refinedev/mantine";
import TableComponent from "@components/table";
import Link from "next/link";
import { useRouter } from "next/router";
import BreadcrumbsComponent from "@components/breadcrumbs";

export const GatherList: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const router = useRouter();
	const { projectid } = router.query;

	const breadcrumbs = [
		{ title: translate("projects.projects"), href: "/projects" },
		{ title: translate("gathers.gathers"), href: "#" },
	];

	const apiResponse = useList({
		resource: `projects/${projectid}/gathers`,
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
				id: "only_posts_older_than",
				accessorKey: "only_posts_older_than",
				header: translate("gathers.fields.only_posts_older_than"),
				cell: function render({ getValue }) {
					return <DateField value={getValue<any>()} />;
				},
			},
			{
				id: "only_posts_newer_than",
				accessorKey: "only_posts_newer_than",
				header: translate("gathers.fields.only_posts_newer_than"),
				cell: function render({ getValue }) {
					return <DateField value={getValue<any>()} />;
				},
			},
			{
				id: "project_id",
				header: translate("gathers.fields.project_id"),
				accessorKey: "project_id",
				cell: function render({ getValue, table }) {
					const meta = table.options.meta as {
						projectData: GetManyResponse;
					};

					const project = meta.projectData?.data?.find(
						(item) => item.id === getValue<any>()
					);

					return project ? (
						<Link
							href={{
								pathname: "/projects/show/[projectid]",
								query: { projectid: project?.id },
							}}
						>
							{project?.name}
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
	const { data: projectData } = useMany({
		resource: "projects",
		ids: tableData?.data?.map((item) => item?.project_id) ?? [],
		queryOptions: {
			enabled: !!tableData?.data,
		},
	});

	setOptions((prev) => ({
		...prev,
		meta: {
			...prev.meta,
			projectData,
		},
	}));
	return (
		<List breadcrumb={<BreadcrumbsComponent breadcrumbs={breadcrumbs} />}>
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
