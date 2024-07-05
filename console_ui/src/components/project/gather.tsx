"use client";

import React, { useEffect, useState, useMemo, useCallback } from "react";
import { useTranslate, useList } from "@refinedev/core";
import { useTable } from "@refinedev/react-table";
import { ColumnDef } from "@tanstack/react-table";
import {
	ScrollArea,
	Pagination,
	Group,
	Button,
	Tooltip,
	Loader,
	Text,
	Title,
	Anchor,
} from "@mantine/core";
import { List, DateField } from "@refinedev/mantine";
import TableComponent from "@components/table";
import { useRouter } from "next/navigation";
import { PHEONIX_MANUAL_URL, statusTextStyle } from "src/utils";
import { IconPlayerPlay } from "@tabler/icons";
import GatherRunModal from "@components/modals/gather-run";
import { jobRunService } from "src/services";
import { GatherResponse } from "src/interfaces/gather";

interface IGatherProps {
	projectid: any;
	refetch: any;
}

const GatherComponent: React.FC<IGatherProps> = ({ projectid, refetch }) => {
	const translate = useTranslate();
	const router = useRouter();
	const [opened, setOpened] = useState(false);
	const [selected, setSelected] = useState(null);
	const [gatherList, setGatherList] = useState<any>([]);
	const [loadingStates, setLoadingStates] = useState<{
		[key: string]: boolean;
	}>({});

	const apiResponse = useList({
		resource: projectid ? `projects/${projectid}/gathers` : "",
	});

	const handleGatherRefresh = useCallback(
		async (gatherDetail: GatherResponse) => {
			setLoadingStates((prev) => ({ ...prev, [gatherDetail.id]: true }));
			try {
				const { data } = await jobRunService.fetchJobRun({
					project_id: gatherDetail.project_id,
					id: gatherDetail?.latest_job_run?.id,
					type: "gather",
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
				refetch();
				setLoadingStates((prev) => ({ ...prev, [gatherDetail.id]: false }));
			}
		},
		[refetch]
	);

	const columns = useMemo<ColumnDef<any>[]>(
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
				id: "created_at",
				accessorKey: "latest_job_run.created_at",
				header: translate("gathers.fields.started_run_at"),
				cell: function render({ row }) {
					const { latest_job_run } = row.original;
					const created_at = latest_job_run ? latest_job_run.created_at : null;
					return created_at ? (
						<DateField format="LLL" value={created_at} />
					) : (
						""
					);
				},
			},
			{
				id: "started_processing_at",
				accessorKey: "latest_job_run.started_processing_at",
				header: translate("gathers.fields.started_processing_at"),
				cell: function render({ row }) {
					const { latest_job_run } = row.original;
					const started_processing_at = latest_job_run
						? latest_job_run.started_processing_at
						: null;
					return started_processing_at ? (
						<DateField format="LLL" value={started_processing_at} />
					) : (
						""
					);
				},
			},
			{
				id: "status",
				accessorKey: "latest_job_run.status",
				header: translate("projects.fields.status"),
				cell: function render({ row }) {
					const { latest_job_run } = row.original;
					const status = latest_job_run ? latest_job_run.status : null;
					return (
						<span className={`${statusTextStyle(status)}`}>
							{status ? translate(`status.${status}`) : ""}
						</span>
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
									{!status && (
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
									{["in_queue", "processing", "awaiting_start"].includes(
										status
									) && <Loader size="sm" />}
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
		refineCore: { setCurrent, pageCount, current },
	} = useTable({
		columns,
		data: gatherList,
	});

	useEffect(() => {
		if (apiResponse?.data?.data) {
			setGatherList(apiResponse.data.data);
		}
	}, [apiResponse?.data?.data]);

	useEffect(() => {
		let interval: NodeJS.Timeout | undefined;
		if (
			gatherList.some((gather: any) => !gather.latest_job_run?.completed_at)
		) {
			interval = setInterval(() => {
				const pendingGathers = gatherList.filter(
					(gather: any) =>
						gather.latest_job_run && !gather.latest_job_run?.completed_at
				);
				Promise.all(
					pendingGathers.map((gather: any) => handleGatherRefresh(gather))
				).catch((error) => console.error("Error refreshing gathers:", error));
			}, 10000);
		}
		return () => {
			if (interval) {
				clearInterval(interval);
			}
		};
	}, [gatherList, handleGatherRefresh]);

	return (
		<>
			<List
				breadcrumb={false}
				createButtonProps={{
					onClick: () => router.push(`/projects/${projectid}/gathers/create`),
				}}
				title={
					<div className="flex flex-col gap-4">
						<Title order={3}>{translate("projects.tabs.gather.title")}</Title>
						<Text fz="sm">
							{translate("projects.tabs.gather.description.part1.a")}
							<Anchor
								className="font-normal text-inherit hover:text-blue-500 text-sm underline"
								href={PHEONIX_MANUAL_URL}
								target="_blank"
							>
								{translate("projects.tabs.gather.description.part1.b")}
							</Anchor>
							{translate("projects.tabs.gather.description.part1.c")}
						</Text>
						<Text fz="sm">
							{translate("projects.tabs.gather.description.part2.a")}
							<Anchor
								className="font-normal text-inherit hover:text-blue-500 text-sm underline"
								href={PHEONIX_MANUAL_URL}
								target="_blank"
							>
								{translate("projects.tabs.gather.description.part2.b")}
							</Anchor>
							{translate("projects.tabs.gather.description.part2.c")}
						</Text>
					</div>
				}
			>
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

export default GatherComponent;
