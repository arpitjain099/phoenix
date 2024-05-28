import React, { useEffect, useState } from "react";
import {
	IResourceComponentsProps,
	useTranslate,
	useMany,
	useList,
} from "@refinedev/core";
import { useTable } from "@refinedev/react-table";
import { ColumnDef } from "@tanstack/react-table";
import {
	ScrollArea,
	Pagination,
	Group,
	Button,
	Tooltip,
	Loader,
} from "@mantine/core";
import { List, DateField } from "@refinedev/mantine";
import TableComponent from "@components/table";
import { useRouter } from "next/router";
import BreadcrumbsComponent from "@components/breadcrumbs";
import { statusTextStyle } from "src/utils";
import { IconPlayerPlay, IconRefresh, IconTrash } from "@tabler/icons";
import GatherRunModal from "@components/modals/gather-run";
import { gatherService } from "src/services";
import { GatherResponse } from "src/interfaces/gather";

export const GatherList: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const router = useRouter();
	const { projectid } = router.query || {};
	const [opened, setOpened] = useState(false);
	const [selected, setSelected] = useState(null);
	const [gatherList, setGatherList] = useState<any>([]);
	const [loadingStates, setLoadingStates] = useState<{
		[key: string]: boolean;
	}>({});

	const breadcrumbs = [
		{ title: translate("projects.projects"), href: "/projects" },
		{ title: translate("gathers.gathers"), href: "#" },
	];

	const apiResponse = useList({
		resource: projectid ? `projects/${projectid}/gathers` : "",
	});

	const handleGatherRefresh = async (gatherDetail: GatherResponse) => {
		setLoadingStates((prev) => ({ ...prev, [gatherDetail.id]: true }));
		try {
			const { data } = await gatherService.fetchJobRun({
				project_id: gatherDetail.project_id,
				id: gatherDetail?.latest_job_run?.id,
			});
			setGatherList((prevList: GatherResponse[]) =>
				prevList.map((gather) =>
					gather.id === gatherDetail.id
						? { ...gather, latest_job_run: data }
						: gather
				)
			);
		} catch (error) {
			console.error("Error fetching gather details:", error);
		} finally {
			setLoadingStates((prev) => ({ ...prev, [gatherDetail.id]: false }));
		}
	};

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
				accessorKey: "latest_job_run.started_processing_at",
				header: translate("gathers.fields.last_run_started_at"),
				cell: function render({ getValue }) {
					return getValue() ? <DateField value={getValue<any>()} /> : "";
				},
			},
			{
				id: "status",
				accessorKey: "latest_job_run.status",
				header: translate("projects.fields.status"),
				cell: function render({ getValue }) {
					const status = getValue() || ""; // Default to empty string if getValue() is null or undefined
					return (
						<span className={`${statusTextStyle(status)}`}>{`${status}`}</span>
					);
				},
			},
			{
				id: "actions",
				accessorKey: "id",
				header: translate("table.actions"),
				cell: function render({ row }) {
					const gatherId = row.original.id;
					const { latest_job_run } = row.original;
					const status = latest_job_run ? latest_job_run.status : null;
					const isLoading = loadingStates[gatherId];
					return (
						<Group spacing="xs" noWrap>
							{isLoading ? (
								<Loader size="sm" />
							) : (
								<>
									{(status === "awaiting_start" || status === "processing") && (
										<Tooltip label="Refresh">
											<Button
												p={0}
												variant="subtle"
												onClick={() => handleGatherRefresh(row.original)}
											>
												<IconRefresh size={20} color="blue" />
											</Button>
										</Tooltip>
									)}
									{(status === "yet_to_run" || !status) && (
										<Tooltip label="Start">
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
										</Tooltip>
									)}
									{status === "failed" && (
										<Button
											p={0}
											variant="subtle"
											color="red"
											onClick={() => {}}
										>
											<IconTrash
												size={20}
												color="red"
												className="cursor-pointer"
											/>
										</Button>
									)}
									{status === "completed_sucessfully" && (
										<Button
											p={0}
											variant="subtle"
											color="red"
											onClick={() => {}}
										>
											<IconTrash
												size={20}
												color="red"
												className="cursor-pointer"
											/>
										</Button>
									)}
								</>
							)}
						</Group>
					);
				},
			},
		],
		[translate, loadingStates]
	);
	const {
		getHeaderGroups,
		getRowModel,
		setOptions,
		refineCore: { setCurrent, pageCount, current },
	} = useTable({
		columns,
		data: gatherList,
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

	useEffect(() => {
		if (apiResponse?.data?.data) {
			setGatherList(apiResponse.data.data);
		}
	}, [apiResponse?.data?.data]);

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
				handleRefresh={handleGatherRefresh}
			/>
		</>
	);
};

export default GatherList;
