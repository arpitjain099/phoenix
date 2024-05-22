import React, { useState } from "react";
import {
	IResourceComponentsProps,
	useTranslate,
	useMany,
	useList,
} from "@refinedev/core";
import { useTable } from "@refinedev/react-table";
import { ColumnDef } from "@tanstack/react-table";
import { ScrollArea, Pagination, Group, Button } from "@mantine/core";
import { List, DateField } from "@refinedev/mantine";
import TableComponent from "@components/table";
import { useRouter } from "next/router";
import BreadcrumbsComponent from "@components/breadcrumbs";
import { statusTextStyle } from "src/utils";
import { IconPlayerPlay, IconRefresh, IconTrash } from "@tabler/icons";
import GatherRunModal from "@components/modals/gather-run";

export const GatherList: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const router = useRouter();
	const { projectid } = router.query || {};
	const [opened, setOpened] = useState(false);
	const [selected, setSelected] = useState(null);

	const breadcrumbs = [
		{ title: translate("projects.projects"), href: "/projects" },
		{ title: translate("gathers.gathers"), href: "#" },
	];

	const apiResponse = useList({
		resource: projectid ? `projects/${projectid}/gathers` : "",
	});
	const listResponse = apiResponse?.data?.data || [];

	const columns = React.useMemo<ColumnDef<any>[]>(
		() => [
			{
				id: "source",
				accessorKey: "source",
				header: translate("gathers.fields.source"),
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
				id: "description",
				accessorKey: "description",
				header: translate("gathers.fields.description"),
			},
			{
				id: "last_run_started_at",
				accessorKey: "last_run_started_at",
				header: translate("gathers.fields.last_run_started_at"),
				cell: function render({ getValue }) {
					return <DateField value={getValue<any>()} />;
				},
			},
			{
				id: "run_status",
				accessorKey: "run_status",
				header: translate("projects.fields.status"),
				cell: function render({ getValue }) {
					return (
						<span
							className={`${statusTextStyle(getValue())}`}
						>{`${getValue()}`}</span>
					);
				},
			},
			{
				id: "actions",
				accessorKey: "id",
				header: translate("table.actions"),
				cell: function render({ row }) {
					const { run_status } = row.original;
					return (
						<Group spacing="xs" noWrap>
							{run_status === "in_queue" &&
								run_status === "processing" &&
								!run_status && (
									<Button p={0} variant="subtle" onClick={() => {}}>
										<IconRefresh size={20} color="blue" />
									</Button>
								)}
							{run_status === "yet_to_run" && (
								<Button
									p={0}
									variant="subtle"
									color="green"
									onClick={() => {
										setSelected(row.original);
										setOpened(true);
									}}
								>
									<IconPlayerPlay size={20} color="green" />
								</Button>
							)}
							{run_status === "failed" && (
								<Button p={0} variant="subtle" color="red" onClick={() => {}}>
									<IconTrash size={20} color="red" className="cursor-pointer" />
								</Button>
							)}
							{run_status === "completed" && (
								<Button p={0} variant="subtle" color="red" onClick={() => {}}>
									<IconTrash size={20} color="red" className="cursor-pointer" />
								</Button>
							)}
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
		<>
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
			<GatherRunModal
				opened={opened}
				setOpened={setOpened}
				gatherDetail={selected}
			/>
		</>
	);
};

export default GatherList;
