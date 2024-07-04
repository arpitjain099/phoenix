"use client";

import React, { useEffect, useState } from "react";
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
import BreadcrumbsComponent from "@components/breadcrumbs";
import { statusTextStyle } from "src/utils";
import { IconPlayerPlay, IconRefresh, IconTrash } from "@tabler/icons";
import GatherRunModal from "@components/modals/gather-run";
import { jobRunService } from "src/services";
import { GatherResponse } from "src/interfaces/gather";
import Link from "next/link";

interface IGatherProps {
	projectid: any;
}

const GatherComponent: React.FC<IGatherProps> = ({ projectid }) => {
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

	const handleGatherRefresh = async (gatherDetail: GatherResponse) => {
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
				id: "created_at",
				accessorKey: "latest_job_run.created_at",
				header: translate("gathers.fields.started_run_at"),
				cell: function render({ getValue }) {
					return getValue() ? (
						<DateField format="LLL" value={getValue<any>()} />
					) : (
						""
					);
				},
			},
			{
				id: "started_processing_at",
				accessorKey: "latest_job_run.started_processing_at",
				header: translate("gathers.fields.started_processing_at"),
				cell: function render({ getValue }) {
					return getValue() ? (
						<DateField format="LLL" value={getValue<any>()} />
					) : (
						""
					);
				},
			},
			{
				id: "status",
				accessorKey: "latest_job_run.status",
				header: translate("projects.fields.status"),
				cell: ({ getValue }) => {
					const status = getValue() || ""; // Default to empty string if getValue() is null or undefined
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
									) && (
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
									{/* {["failed", "completed_sucessfully"].includes(status) && (
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
									)} */}
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

	return (
		<>
			<List
				breadcrumb={false}
				createButtonProps={{
					onClick: () => router.push(`/projects/${projectid}/gathers/create`),
				}}
				title={
					<div className="flex flex-col">
						<Title order={3}>{translate("projects.tabs.gather.title")}</Title>
						<Text fz="sm" c="dimmed">
							{translate("projects.tabs.gather.description.part1.a")}
							<Anchor
								className="underline underline-offset-1"
								href="https://docs.google.com/document/d/1Rs3WYgvkAtZJ9y1ho68AnGfC8mDuOFE9aG52bkJSG24/edit"
								target="_blank"
							>
								{translate("projects.tabs.gather.description.part1.b")}
							</Anchor>
							{translate("projects.tabs.gather.description.part1.c")}
						</Text>
						<Text fz="sm" c="dimmed" mt={4}>
							{translate("projects.tabs.gather.description.part2.a")}
							<Anchor
								className="underline underline-offset-1"
								href="https://docs.google.com/document/d/1Rs3WYgvkAtZJ9y1ho68AnGfC8mDuOFE9aG52bkJSG24/edit"
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
