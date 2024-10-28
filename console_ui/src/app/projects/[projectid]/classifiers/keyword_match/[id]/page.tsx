"use client";

import React, { useState } from "react";
import { useShow, useTranslate } from "@refinedev/core";
import {
	Show,
	TextField,
	DateField,
	EditButton,
	EditButtonProps,
} from "@refinedev/mantine";
import {
	Accordion,
	ActionIcon,
	Button,
	Container,
	Group,
	Space,
	Table,
	TextInput,
	Title,
	Tooltip,
} from "@mantine/core";
import { useParams } from "next/navigation";
import { statusTextStyle } from "src/utils";
import { IconChevronDown, IconChevronUp, IconInfoCircle } from "@tabler/icons";
import { classifierService } from "src/services";
import { showNotification } from "@mantine/notifications";
import ClassifierViewBreadcrumb from "@components/breadcrumbs/classifierView";

export default function KeywordClassifierShow(): JSX.Element {
	const { projectid, id } = useParams();
	const translate = useTranslate();
	const [openRows, setOpenRows] = useState<{ [key: number]: boolean }>({});
	const { queryResult } = useShow({
		resource: `projects/${projectid}/classifiers`,
		id: id as string,
	});

	const { data, isLoading } = queryResult;

	const record = data?.data;

	const editButtonProps: EditButtonProps = {
		recordItemId: id as string,
	};

	const showRow = (index: number) => {
		setOpenRows((prev) => ({ ...prev, [index]: true }));
	};

	const toggleRow = (index: number) => {
		setOpenRows((prev) => ({ ...prev, [index]: !prev[index] }));
	};

	const handleApplyClassifier = async (): Promise<void> => {
		try {
			await classifierService.runKeywordClassifier({
				project_id: projectid,
				classifier_id: id,
			});
			showNotification({
				title: "Success",
				message: translate("classifiers.success.success"),
			});
		} catch (error: any) {
			showNotification({
				title: "Error",
				color: "red",
				message: error?.response?.data?.message || "An Error Occured",
			});
			console.error("Error applying classifier", error);
		}
	};

	return (
		<Show
			title={<Title order={3}>{record?.name}</Title>}
			breadcrumb={
				<ClassifierViewBreadcrumb
					record={record}
					projectid={projectid as string}
				/>
			}
			isLoading={isLoading}
			headerButtons={() => null}
		>
			<TextField
				value={translate("classifiers.types.keyword_match.view.text")}
			/>
			<Space h="md" />
			{!record?.latest_version && record?.last_edited_at && (
				<p className="flex items-center text-red-500">
					{translate("classifiers.cautions.not_run.title")}
					<Tooltip
						multiline
						width={350}
						label={translate("classifiers.cautions.not_run.description")}
					>
						<span className="flex">
							<IconInfoCircle size={12} />
						</span>
					</Tooltip>
				</p>
			)}
			{(!record?.latest_version ||
				(record?.latest_version &&
					new Date(record?.latest_version?.created_at) <
						new Date(record?.last_edited_at))) && (
				<p className="flex items-center text-red-500">
					{translate("classifiers.cautions.not_applied.title")}
					<Tooltip
						multiline
						width={350}
						label={translate("classifiers.cautions.not_applied.description")}
					>
						<span className="flex">
							<IconInfoCircle size={12} />
						</span>
					</Tooltip>
				</p>
			)}
			<Space h="md" />
			<div className="flex gap-4 items-center mb-4">
				<EditButton {...editButtonProps} />
				<Button
					variant="filled"
					color="blue"
					onClick={handleApplyClassifier}
					disabled={
						!record?.latest_version ||
						(record?.latest_version &&
							new Date(record?.latest_version?.created_at) <
								new Date(record?.last_edited_at))
					}
				>
					{translate("classifiers.types.keyword_match.run")}
				</Button>
			</div>
			<div className="w-full">
				<Accordion
					styles={{
						control: {
							paddingLeft: 0,
						},
						item: {
							"&[data-active]": {
								backgroundColor: "none",
							},
						},
					}}
					multiple
					defaultValue={["status", "general", "configuration"]}
				>
					<Accordion.Item value="status" className="mb-4">
						<Accordion.Control>
							<Title order={5}>
								{translate(
									"classifiers.types.keyword_match.view.accordion.status"
								)}
							</Title>
						</Accordion.Control>
						<Accordion.Panel>
							<Container className="mx-0 flex flex-col my-4">
								<Group>
									<Title my="xs" order={5}>
										{translate("gathers.fields.status")}:
									</Title>
									<span
										className={`${statusTextStyle(record?.latest_job_run?.status)}`}
									>
										{record?.latest_job_run?.status
											? translate(`status.${record.latest_job_run.status}`)
											: "-"}
									</span>
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate("gathers.fields.started_processing_at")}:
									</Title>
									{record?.latest_job_run?.started_processing_at ? (
										<DateField
											format="LLL"
											value={record?.latest_job_run.started_processing_at}
										/>
									) : (
										"-"
									)}
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate("gathers.fields.completed_at")}:
									</Title>
									{record?.latest_job_run?.completed_at ? (
										<DateField
											format="LLL"
											value={record?.latest_job_run.completed_at}
										/>
									) : (
										"-"
									)}
								</Group>{" "}
							</Container>
						</Accordion.Panel>
					</Accordion.Item>
					<Accordion.Item value="general" mb="md">
						<Accordion.Control>
							<Title order={5}>
								{translate(
									"classifiers.types.keyword_match.view.accordion.general"
								)}
							</Title>
						</Accordion.Control>
						<Accordion.Panel>
							<Container className="mx-0 flex flex-col my-4">
								<Group>
									<Title my="xs" order={5}>
										{translate("gathers.fields.name")}:
									</Title>
									<TextField className="capitalize" value={record?.name} />
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate("projects.fields.description")}:
									</Title>
									<TextField
										className="capitalize"
										value={record?.description}
									/>
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate("gathers.fields.created_at")}:
									</Title>
									{record?.created_at ? (
										<DateField format="LLL" value={record?.created_at} />
									) : (
										"-"
									)}
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate("classifiers.fields.latest_version_applyed_at")}:
									</Title>
									{record?.latest_version?.created_at ? (
										<DateField
											format="LLL"
											value={record?.latest_version?.created_at}
										/>
									) : (
										"-"
									)}
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate("classifiers.fields.latest_edits_made_at")}:
									</Title>
									{record?.last_edited_at ? (
										<DateField format="LLL" value={record?.last_edited_at} />
									) : (
										"-"
									)}
								</Group>
							</Container>
						</Accordion.Panel>
					</Accordion.Item>
					<Accordion.Item value="configuration" mb="md">
						<Accordion.Control>
							<Title order={5}>
								{translate(
									`classifiers.types.keyword_match.view.accordion.configuration`
								)}
							</Title>
						</Accordion.Control>
						<Accordion.Panel>
							<Container className="mx-0 flex flex-col my-4">
								<Table highlightOnHover withBorder>
									<thead>
										<tr>
											<th aria-label="Accordion Control" />
											<th>{translate("classifiers.fields.class_name")}</th>
											<th>{translate("projects.fields.description")}</th>
											<th className="flex items-center justify-center">
												{translate("classifiers.fields.keywords")}
											</th>
										</tr>
									</thead>
									<tbody>
										{record?.intermediatory_classes?.map(
											(classItem: any, classIndex: number) => (
												<tr key={classIndex}>
													<td className="align-baseline">
														<ActionIcon
															color="dark"
															variant="light"
															onClick={() => toggleRow(classIndex)}
														>
															{openRows[classIndex] ? (
																<IconChevronUp size={16} />
															) : (
																<IconChevronDown size={16} />
															)}
														</ActionIcon>
													</td>
													<td className="align-baseline">{classItem?.name}</td>
													<td className="align-baseline">
														{classItem?.description}
													</td>
													<td className="!pt-0">
														<Table>
															<tbody className="flex flex-col items-center">
																{openRows[classIndex]
																	? record?.intermediatory_class_to_keyword_configs
																			?.filter(
																				(group: any) =>
																					group.class_id === classItem?.id
																			)
																			.map(
																				(
																					keywordGroup: any,
																					keywordIndex: number
																				) => (
																					<>
																						<tr key={keywordIndex}>
																							<td>
																								<TextInput
																									placeholder="Keywords"
																									value={keywordGroup.musts}
																									contentEditable={false}
																								/>
																							</td>
																						</tr>
																						{record
																							?.intermediatory_class_to_keyword_configs
																							?.length > 0 &&
																							keywordIndex <
																								record.intermediatory_class_to_keyword_configs.filter(
																									(group: any) =>
																										group.class_id ===
																										classItem?.id
																								).length -
																									1 && (
																								<td className="text-center">
																									or
																								</td>
																							)}
																					</>
																				)
																			)
																	: `${
																			record?.intermediatory_class_to_keyword_configs?.filter(
																				(group: any) =>
																					group.class_id === classItem?.id
																			).length
																		} added`}
															</tbody>
														</Table>
													</td>
												</tr>
											)
										)}
									</tbody>
								</Table>
							</Container>
						</Accordion.Panel>
					</Accordion.Item>
				</Accordion>
			</div>
		</Show>
	);
}
