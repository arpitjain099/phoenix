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
import { DateField } from "@refinedev/mantine";
import TableComponent from "@components/table";
import {
	isJobRunRunning,
	PHEONIX_MANUAL_URL,
	statusTextStyle,
} from "src/utils";
import { IconPlayerPlay, IconSquarePlus, IconTrash } from "@tabler/icons";
import GatherRunModal from "@components/modals/gather-run";
import { jobRunService } from "src/services";
import { GatherResponse } from "src/interfaces/gather";
import Link from "next/link";
import GatherDeleteModal from "@components/modals/delete-gather";

interface IGatherProps {
	projectid: any;
	refetch: any;
}

const GatherComponent: React.FC<IGatherProps> = ({ projectid, refetch }) => {
	const translate = useTranslate();
	const [opened, setOpened] = useState(false);
	const [deleteModalOpen, setDeleteModalOpen] = useState(false);
	const [selected, setSelected] = useState(null);
	const [gatherList, setGatherList] = useState<any>([]);
	const [loadingStates, setLoadingStates] = useState<{
		[key: string]: boolean;
	}>({});

	const apiResponse = useList({
		resource: projectid ? `projects/${projectid}/gathers` : "",
		pagination: {
			mode: "client",
		},
	});

	const handleGatherRefresh = useCallback(
		async (gatherDetail: GatherResponse) => {
			setLoadingStates((prev) => ({ ...prev, [gatherDetail.id]: true }));
			try {
				const latest_job_run_fetch = await jobRunService.fetchJobRun({
					project_id: gatherDetail.project_id,
					id: gatherDetail?.latest_job_run?.id,
					type: "gather",
				});
				let delete_job_run_fetch = { data: null };
				if (gatherDetail?.delete_job_run) {
					delete_job_run_fetch = await jobRunService.fetchJobRun({
						project_id: gatherDetail.project_id,
						id: gatherDetail?.delete_job_run?.id,
						type: "delete_gather",
					});
				}
				setGatherList((prevList: GatherResponse[]) =>
					prevList.map((gather) =>
						gather.id === gatherDetail.id
							? {
									...gather,
									latest_job_run: latest_job_run_fetch.data,
									delete_job_run: delete_job_run_fetch.data,
								}
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

	const handleGatherUpdate = useCallback(
		async (gatherDetail: GatherResponse) => {
			setLoadingStates((prev) => ({ ...prev, [gatherDetail.id]: true }));
			try {
				setGatherList((prevList: GatherResponse[]) =>
					prevList.map((gather) =>
						gather.id === gatherDetail.id ? gatherDetail : gather
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
				id: "name",
				accessorKey: "name",
				header: translate("gathers.fields.name"),
				cell: ({ row }) => {
					const { id, name, child_type, project_id } = row.original;
					return (
						<Link
							href={`/projects/${project_id}/gathers/${child_type}/${id}`}
							className="no-underline text-blue-500"
						>
							{name}
						</Link>
					);
				},
			},
			{
				id: "started_processing_at",
				accessorKey: "latest_job_run.started_processing_at",
				header: translate("gathers.fields.started_run_at"),
				cell: function render({ row }) {
					const { latest_job_run, delete_job_run } = row.original;
					const started_processing_at = latest_job_run
						? latest_job_run.started_processing_at
						: null;
					return started_processing_at ? (
						<span
							className={`${delete_job_run?.status === "completed_sucessfully" ? statusTextStyle("deleted") : ""}`}
						>
							<DateField format="LLL" value={started_processing_at} />
						</span>
					) : (
						""
					);
				},
			},
			{
				id: "completed_at",
				accessorKey: "latest_job_run.completed_at",
				header: translate("gathers.fields.completed_at"),
				cell: function render({ row }) {
					const { latest_job_run, delete_job_run } = row.original;
					const completed_at = latest_job_run
						? latest_job_run.completed_at
						: null;
					return completed_at ? (
						<span
							className={`${delete_job_run?.status === "completed_sucessfully" ? statusTextStyle("deleted") : ""}`}
						>
							<DateField format="LLL" value={completed_at} />
						</span>
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
					const { latest_job_run, delete_job_run } = row.original;
					const status = latest_job_run ? latest_job_run.status : null;
					return (
						<span
							className={`${statusTextStyle(delete_job_run?.status === "completed_sucessfully" ? "deleted" : delete_job_run?.status ? delete_job_run?.status : status)}`}
						>
							{delete_job_run
								? translate(`status.delete_status.${delete_job_run.status}`)
								: status
									? translate(`status.${status}`)
									: ""}
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
					const { latest_job_run, delete_job_run } = row.original;
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
									{(isJobRunRunning(latest_job_run) ||
										isJobRunRunning(delete_job_run)) && <Loader size="sm" />}
									{latest_job_run?.completed_at &&
										!isJobRunRunning(delete_job_run) &&
										delete_job_run?.status !== "completed_sucessfully" && (
											<Tooltip label="Delete">
												<Button
													p={0}
													variant="subtle"
													color="red"
													onClick={() => {
														setSelected(row.original);
														setDeleteModalOpen(true);
													}}
												>
													<IconTrash size={20} color="red" />
												</Button>
											</Tooltip>
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
		refineCore: { setCurrent, pageCount, current },
	} = useTable({
		columns,
		data: gatherList,
		refineCoreProps: {
			pagination: {
				mode: "off",
			},
		},
	});

	useEffect(() => {
		if (apiResponse?.data?.data) {
			setGatherList(apiResponse.data.data);
		}
	}, [apiResponse?.data?.data]);

	useEffect(() => {
		let interval: NodeJS.Timeout | undefined;
		if (
			gatherList.some(
				(gather: any) =>
					!gather.latest_job_run?.completed_at ||
					(gather.delete_job_run && !gather.delete_job_run?.completed_at)
			)
		) {
			interval = setInterval(() => {
				const pendingGathers = gatherList.filter(
					(gather: any) =>
						(gather.latest_job_run && !gather.latest_job_run?.completed_at) ||
						(gather.delete_job_run && !gather.delete_job_run?.completed_at)
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
	}, [gatherList, handleGatherRefresh, handleGatherUpdate]);

	return (
		<>
			<div className="p-4">
				<Group className="mb-4">
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
					<Link href={`/projects/${projectid}/gathers/select_type`}>
						<Button leftIcon={<IconSquarePlus />}>
							{translate("actions.create")}
						</Button>
					</Link>
				</Group>
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
			</div>
			<GatherRunModal
				opened={opened}
				setOpened={setOpened}
				gatherDetail={selected}
				handleRefresh={handleGatherRefresh}
			/>
			<GatherDeleteModal
				opened={deleteModalOpen}
				setOpened={setDeleteModalOpen}
				gatherDetail={selected}
				handleUpdate={handleGatherUpdate}
			/>
		</>
	);
};

export default GatherComponent;
