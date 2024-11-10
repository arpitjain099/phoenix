"use client";

import React, { useEffect, useState, useMemo, useCallback } from "react";
import { useTranslate, useList } from "@refinedev/core";
import { ColumnDef } from "@tanstack/react-table";
import {
	Group,
	Button,
	Loader,
	Text,
	Title,
	Anchor,
	Tooltip,
	Popover,
} from "@mantine/core";
import { DateField } from "@refinedev/mantine";
import TableComponent from "@components/table";
import { isJobRunRunning, statusTextStyle } from "src/utils";
import {
	IconSquarePlus,
	IconArchive,
	IconCreativeCommonsSa,
	IconAlertTriangle,
	IconPlayerPlay,
} from "@tabler/icons";
import { classifierService, jobRunService } from "src/services";
import { GatherResponse } from "src/interfaces/gather";
import Link from "next/link";
import { ClassifierResponse } from "src/interfaces/classifier";
import { showNotification } from "@mantine/notifications";

const PHEONIX_MANUAL_CLASSIFIER =
	"https://howtobuildup.notion.site/Decide-how-you-want-to-classify-data-43a8b3a25fd84eadaa67a03dd8b06175";

interface IClassifierProps {
	projectid: any;
	refetch: any;
}

const ClassifyComponent: React.FC<IClassifierProps> = ({
	projectid,
	refetch,
}) => {
	const translate = useTranslate();
	const [loadingAction, setIsLoading] = useState(false);
	const [classifierList, setClassifierList] = useState<any>([]);
	const [loadingStates, setLoadingStates] = useState<{
		[key: string]: boolean;
	}>({});

	const apiResponse = useList({
		resource: projectid ? `projects/${projectid}/classifiers` : "",
		pagination: {
			mode: "off",
		},
	});

	const handleClassifierRefresh = useCallback(
		async (classifierDetail: ClassifierResponse) => {
			setLoadingStates((prev) => ({ ...prev, [classifierDetail.id]: true }));
			try {
				const updatedClassifier = await jobRunService.fetchJobRun({
					project_id: classifierDetail.project_id,
					id: classifierDetail?.latest_job_run?.id,
				});
				setClassifierList((prevList: ClassifierResponse[]) =>
					prevList.map((classifier) =>
						classifier.id === classifierDetail.id
							? {
									...updatedClassifier.data,
								}
							: classifier
					)
				);
			} catch (error) {
				console.error("Error fetching classifier details:", error);
			} finally {
				refetch();
				setLoadingStates((prev) => ({ ...prev, [classifierDetail.id]: false }));
			}
		},
		[refetch]
	);

	const handleClassifierUpdate = useCallback(
		async (classifierDetail: ClassifierResponse) => {
			setLoadingStates((prev) => ({ ...prev, [classifierDetail.id]: true }));
			try {
				setClassifierList((prevList: ClassifierResponse[]) =>
					prevList.map((classifier) =>
						classifier.id === classifierDetail.id
							? classifierDetail
							: classifier
					)
				);
			} catch (error) {
				console.error("Error fetching classifier details:", error);
			} finally {
				refetch();
				setLoadingStates((prev) => ({ ...prev, [classifierDetail.id]: false }));
			}
		},
		[refetch]
	);

	const handleArchive = useCallback(
		async (classifierDetail: any) => {
			setIsLoading(true);
			try {
				const updatedClassifier = await classifierService.archiveClassifier({
					project_id: projectid,
					id: classifierDetail.id,
				});
				showNotification({
					title: "Success",
					message: translate("classifiers.success.archive"),
				});

				setClassifierList((prevList: ClassifierResponse[]) =>
					prevList.map((classifier) =>
						classifier.id === classifierDetail.id
							? {
									...updatedClassifier.data,
								}
							: classifier
					)
				);
			} catch (error: any) {
				showNotification({
					title: "Error",
					message: error?.response?.data?.detail,
				});
				console.error("Error archiving classifier:", error);
			} finally {
				setIsLoading(false);
			}
		},
		[projectid, translate]
	);

	const handleRestore = useCallback(
		async (classifierDetail: any) => {
			setIsLoading(true);
			try {
				const updatedClassifier = await classifierService.restoreClassifier({
					project_id: projectid,
					id: classifierDetail.id,
				});
				showNotification({
					title: "Success",
					message: translate("classifiers.success.restore"),
				});

				setClassifierList((prevList: ClassifierResponse[]) =>
					prevList.map((classifier) =>
						classifier.id === classifierDetail.id
							? {
									...updatedClassifier.data,
								}
							: classifier
					)
				);
			} catch (error: any) {
				showNotification({
					title: "Error",
					message: error?.response?.data?.detail,
				});
				console.error("Error archiving classifier:", error);
			} finally {
				setIsLoading(false);
			}
		},
		[projectid, translate]
	);

	const columns = useMemo<ColumnDef<any>[]>(
		() => [
			{
				id: "name",
				accessorKey: "name",
				header: translate("gathers.fields.name"),
				cell: ({ row }) => {
					const { id, name, type, project_id, latest_version, last_edited_at } =
						row.original;
					return (
						<div className="flex items-center">
							{(!latest_version ||
								(latest_version &&
									new Date(latest_version?.created_at) <
										new Date(last_edited_at))) && (
								<Tooltip
									multiline
									width={350}
									label={translate("classifiers.caution")}
								>
									<Button p={0} variant="subtle" color="black">
										<IconAlertTriangle size={20} color="black" />
									</Button>
								</Tooltip>
							)}
							<Link
								href={`/projects/${project_id}/classifiers/${type}/${id}`}
								className="no-underline text-blue-500"
							>
								{name}
							</Link>
						</div>
					);
				},
			},
			{
				id: "started_processing_at",
				accessorKey: "latest_job_run.started_processing_at",
				header: translate("gathers.fields.started_run_at"),
				cell: function render({ row }) {
					const { latest_job_run, latest_version } = row.original;
					const started_processing_at = latest_job_run
						? latest_job_run.started_processing_at
						: null;
					return started_processing_at && latest_version ? (
						<DateField format="LLL" value={started_processing_at} />
					) : (
						"-"
					);
				},
			},
			{
				id: "completed_at",
				accessorKey: "latest_job_run.completed_at",
				header: translate("gathers.fields.completed_at"),
				cell: function render({ row }) {
					const { latest_job_run, latest_version } = row.original;
					const completed_at = latest_job_run
						? latest_job_run.completed_at
						: null;
					return completed_at && latest_version ? (
						<DateField format="LLL" value={completed_at} />
					) : (
						"-"
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
					const type = latest_job_run ? latest_job_run.foreign_job_type : null;
					return (
						<span className={statusTextStyle(status)}>
							{status ? translate(`status.${type}.${status}`) : "-"}
						</span>
					);
				},
			},
			{
				id: "actions",
				accessorKey: "id",
				header: translate("table.actions"),
				cell: function render({ row }) {
					const { project_id } = row.original;
					const classifierId = row.original.id;
					const classifierType = row.original.type;
					const { latest_job_run } = row.original;
					const status = latest_job_run ? latest_job_run.status : null;
					const type = latest_job_run ? latest_job_run.foreign_job_type : null;
					const isLoading = loadingStates[classifierId];
					return (
						<Group spacing="xs" noWrap>
							{isLoading ? (
								<Loader size="sm" />
							) : (
								<>
									{!status && (
										<Tooltip
											label={translate(
												"classifiers.actions.titles.view_and_run"
											)}
										>
											<Button
												component="a"
												p={0}
												href={`/projects/${project_id}/classifiers/${classifierType}/${classifierId}`}
												variant="subtle"
												color="green"
											>
												<IconPlayerPlay size={20} color="green" />
											</Button>
										</Tooltip>
									)}
									{type === "classify_tabulate" &&
										isJobRunRunning(latest_job_run) && <Loader size="sm" />}
									{type === "classifier_archive" &&
										isJobRunRunning(latest_job_run) && <Loader size="sm" />}
									{type === "classifier_restore" &&
										isJobRunRunning(latest_job_run) && <Loader size="sm" />}
									{type === "classify_tabulate" &&
										status === "completed_successfully" && (
											<Popover position="bottom" withArrow shadow="md">
												<Popover.Target>
													<Tooltip
														label={translate(
															"classifiers.actions.titles.archive"
														)}
													>
														<Button p={0} variant="subtle" color="black">
															<IconArchive size={20} color="black" />
														</Button>
													</Tooltip>
												</Popover.Target>
												<Popover.Dropdown>
													<Group className="flex flex-col">
														<Text size="sm" fw={600}>
															{translate("classifiers.actions.text.archive")}
														</Text>
														<Group>
															<Button
																loading={loadingAction}
																onClick={() => {
																	handleArchive(row.original);
																}}
															>
																{translate("classifiers.actions.button")}
															</Button>
														</Group>
													</Group>
												</Popover.Dropdown>
											</Popover>
										)}
									{type === "classify_tabulate" &&
										!isJobRunRunning(latest_job_run) &&
										status !== "completed_successfully" && (
											<Popover position="bottom" withArrow shadow="md">
												<Popover.Target>
													<Tooltip
														label={translate(
															"classifiers.actions.titles.archive"
														)}
													>
														<Button p={0} variant="subtle" color="black">
															<IconArchive size={20} color="black" />
														</Button>
													</Tooltip>
												</Popover.Target>
												<Popover.Dropdown>
													<Group className="flex flex-col">
														<Text size="sm" fw={600}>
															{translate("classifiers.actions.text.archive")}
														</Text>
														<Group>
															<Button
																loading={loadingAction}
																onClick={() => {
																	handleArchive(row.original);
																}}
															>
																{translate("classifiers.actions.button")}
															</Button>
														</Group>
													</Group>
												</Popover.Dropdown>
											</Popover>
										)}
									{type === "classifier_archive" &&
										!isJobRunRunning(latest_job_run) &&
										status !== "completed_successfully" && (
											<Popover position="bottom" withArrow shadow="md">
												<Popover.Target>
													<Tooltip
														label={translate(
															"classifiers.actions.titles.archive"
														)}
													>
														<Button p={0} variant="subtle" color="black">
															<IconArchive size={20} color="black" />
														</Button>
													</Tooltip>
												</Popover.Target>
												<Popover.Dropdown>
													<Group className="flex flex-col">
														<Text size="sm" fw={600}>
															{translate("classifiers.actions.text.archive")}
														</Text>
														<Group>
															<Button
																loading={loadingAction}
																onClick={() => {
																	handleArchive(row.original);
																}}
															>
																{translate("classifiers.actions.button")}
															</Button>
														</Group>
													</Group>
												</Popover.Dropdown>
											</Popover>
										)}
									{type === "classifier_restore" &&
										!isJobRunRunning(latest_job_run) && (
											<Popover position="bottom" withArrow shadow="md">
												<Popover.Target>
													<Tooltip
														label={translate(
															"classifiers.actions.titles.archive"
														)}
													>
														<Button p={0} variant="subtle" color="black">
															<IconArchive size={20} color="black" />
														</Button>
													</Tooltip>
												</Popover.Target>
												<Popover.Dropdown>
													<Group className="flex flex-col">
														<Text size="sm" fw={600}>
															{translate("classifiers.actions.text.archive")}
														</Text>
														<Group>
															<Button
																loading={loadingAction}
																onClick={() => {
																	handleArchive(row.original);
																}}
															>
																{translate("classifiers.actions.button")}
															</Button>
														</Group>
													</Group>
												</Popover.Dropdown>
											</Popover>
										)}
									{type === "classifier_archive" &&
										status === "completed_successfully" && (
											<Popover position="bottom" withArrow shadow="md">
												<Popover.Target>
													<Tooltip
														label={translate(
															"classifiers.actions.titles.restore"
														)}
													>
														<Button p={0} variant="subtle" color="black">
															<IconCreativeCommonsSa size={20} color="black" />
														</Button>
													</Tooltip>
												</Popover.Target>
												<Popover.Dropdown>
													<Group className="flex flex-col">
														<Text size="sm" fw={600}>
															{translate("classifiers.actions.text.restore")}
														</Text>
														<Group>
															<Button
																loading={loadingAction}
																onClick={() => {
																	handleRestore(row.original);
																}}
															>
																{translate("classifiers.actions.button")}
															</Button>
														</Group>
													</Group>
												</Popover.Dropdown>
											</Popover>
										)}
								</>
							)}
						</Group>
					);
				},
			},
		],
		[translate, loadingStates, handleArchive, handleRestore, loadingAction]
	);

	useEffect(() => {
		if (apiResponse?.data?.data) {
			setClassifierList(apiResponse.data.data);
		}
	}, [apiResponse?.data?.data]);

	useEffect(() => {
		let interval: NodeJS.Timeout | undefined;
		if (
			classifierList.some(
				(classifier: any) =>
					!classifier.latest_job_run?.completed_at ||
					(classifier.delete_job_run &&
						!classifier.delete_job_run?.completed_at)
			)
		) {
			interval = setInterval(() => {
				const pendingClassifiers = classifierList.filter(
					(classifier: any) =>
						classifier.latest_job_run &&
						!classifier.latest_job_run?.completed_at
				);
				Promise.all(
					pendingClassifiers.map((classifier: any) =>
						handleClassifierRefresh(classifier)
					)
				).catch((error) =>
					console.error("Error refreshing classifiers:", error)
				);
			}, 10000);
		}
		return () => {
			if (interval) {
				clearInterval(interval);
			}
		};
	}, [classifierList, handleClassifierRefresh, handleClassifierUpdate]);

	return (
		<div className="p-4">
			<Group className="mb-4">
				<div className="flex flex-col gap-4">
					<Title order={3}>{translate("projects.tabs.classifier.title")}</Title>
					<Text fz="sm">
						{translate("projects.tabs.classifier.description.part1.a")}
						<Anchor
							className="font-normal text-inherit hover:text-blue-500 text-sm underline"
							href={PHEONIX_MANUAL_CLASSIFIER}
							target="_blank"
						>
							{translate("projects.tabs.classifier.description.part1.b")}
						</Anchor>
						{translate("projects.tabs.classifier.description.part1.c")}
					</Text>
				</div>
				<Link href={`/projects/${projectid}/classifiers/select_type`}>
					<Button leftIcon={<IconSquarePlus />}>
						{translate("actions.create")}
					</Button>
				</Link>
			</Group>
			<TableComponent columns={columns} data={apiResponse?.data?.data || []} />
		</div>
	);
};

export default ClassifyComponent;
