"use client";

import React, { useCallback, useEffect, useState } from "react";
import { useShow, useTranslate } from "@refinedev/core";
import {
	Show,
	TextField,
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
	Title,
	Tooltip,
} from "@mantine/core";
import { useParams, useRouter } from "next/navigation";
import { IconChevronDown, IconChevronUp, IconInfoCircle } from "@tabler/icons";
import { classifierService } from "src/services";
import { showNotification } from "@mantine/notifications";
import ClassifierViewBreadcrumb from "@components/breadcrumbs/classifierView";
import ClassifierViewStatus from "@components/classifier/view-status";
import ClassifierViewGeneral from "@components/classifier/view-general";
import { Author } from "../model";

export default function ManualPostClassifierShow(): JSX.Element {
	const { projectid, id } = useParams();
	const translate = useTranslate();
	const router = useRouter();
	const [authors, setAuthors] = useState<Author[]>([]);
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
				title: translate("status.success"),
				message: translate("classifiers.success.success"),
			});
			router.replace(`/projects/show/${projectid}?activeItem=classify`);
		} catch (error: any) {
			showNotification({
				title: translate("status.error"),
				color: "red",
				message: error?.response?.data?.message || "An Error Occured",
			});
			console.error("Error applying classifier", error);
		}
	};

	// Fetch initial data on mount
	const fetchData = useCallback(async () => {
		try {
			const authorsResponse = await classifierService.getManualPostAuthors({
				project_id: projectid as string,
				classifier_id: id as string,
			});
			setAuthors(authorsResponse?.data);
		} catch (error) {
			console.error("Error fetching classifier data", error);
		}
	}, [id, projectid]);

	useEffect(() => {
		if (id && projectid) {
			fetchData();
		}
	}, [id, projectid, fetchData]);

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
				value={translate("classifiers.types.manual_post_authors.view.text")}
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
			{record?.latest_version &&
				new Date(record?.latest_version?.created_at) <
					new Date(record?.last_edited_at) && (
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
						(!record?.latest_version && !record?.last_edited_at) ||
						(record?.latest_job_run && !record?.latest_job_run?.completed_at) ||
						(record?.latest_version &&
							new Date(record?.latest_version?.created_at) >
								new Date(record?.last_edited_at))
					}
				>
					{translate("classifiers.run")}
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
					defaultValue={["status", "general", "classes", "authors"]}
				>
					<Accordion.Item value="status" className="mb-4">
						<Accordion.Control>
							<Title order={5}>
								{translate(
									"classifiers.types.manual_post_authors.view.accordion.status"
								)}
							</Title>
						</Accordion.Control>
						<Accordion.Panel>
							<ClassifierViewStatus record={record} />
						</Accordion.Panel>
					</Accordion.Item>
					<Accordion.Item value="general" mb="md">
						<Accordion.Control>
							<Title order={5}>
								{translate(
									"classifiers.types.manual_post_authors.view.accordion.general"
								)}
							</Title>
						</Accordion.Control>
						<Accordion.Panel>
							<ClassifierViewGeneral record={record} />
						</Accordion.Panel>
					</Accordion.Item>
					<Accordion.Item value="classes" mb="md">
						<Accordion.Control>
							<Title order={5}>
								{translate(
									"classifiers.types.manual_post_authors.view.accordion.class_configuration"
								)}
							</Title>
						</Accordion.Control>
						<Accordion.Panel>
							<Container className="mx-0 flex flex-col my-4">
								<Table highlightOnHover withBorder>
									<thead>
										<tr>
											<th>{translate("classifiers.fields.class_name")}</th>
											<th>{translate("projects.fields.description")}</th>
										</tr>
									</thead>
									<tbody>
										{record?.intermediatory_classes?.map(
											(classItem: any, classIndex: number) => (
												<tr key={classIndex}>
													<td className="align-baseline">{classItem?.name}</td>
													<td className="align-baseline">
														{classItem?.description}
													</td>
												</tr>
											)
										)}
									</tbody>
								</Table>
							</Container>
						</Accordion.Panel>
					</Accordion.Item>
					<Accordion.Item value="authors" mb="md">
						<Accordion.Control>
							<Title order={5}>
								{translate(
									"classifiers.types.manual_post_authors.view.accordion.author_configuration"
								)}
							</Title>
						</Accordion.Control>
						<Accordion.Panel>
							<Container className="mx-0 flex flex-col my-4">
								<Table highlightOnHover withBorder>
									<thead>
										<tr>
											<th aria-label="Accordion Control" />
											<th>
												{translate(
													"classifiers.types.manual_post_authors.fields.classes"
												)}
											</th>
											<th>
												{translate(
													"classifiers.types.manual_post_authors.fields.author_name"
												)}
											</th>
											<th>
												{translate(
													"classifiers.types.manual_post_authors.fields.author_link"
												)}
											</th>
											<th>
												{translate(
													"classifiers.types.manual_post_authors.fields.no_of_posts"
												)}
											</th>
											<th>
												{translate(
													"classifiers.types.manual_post_authors.fields.author_platform"
												)}
											</th>
											<th>
												{translate(
													"classifiers.types.manual_post_authors.fields.author_anon_id"
												)}
											</th>
										</tr>
									</thead>
									<tbody>
										{authors.map((author, authorIndex) => (
											<tr key={author.phoenix_platform_message_author_id}>
												<td className="align-baseline">
													<ActionIcon
														color="dark"
														variant="light"
														onClick={() => toggleRow(authorIndex)}
													>
														{openRows[authorIndex] ? (
															<IconChevronUp size={16} />
														) : (
															<IconChevronDown size={16} />
														)}
													</ActionIcon>
												</td>
												<td>
													<div className="flex flex-wrap">
														{openRows[authorIndex]
															? author.intermediatory_author_classes.map(
																	(cls) => (
																		<span
																			key={cls.class_id}
																			className="mr-2 mb-2 px-2 py-1 bg-gray-200 rounded text-sm sm:text-base"
																		>
																			{cls.class_name}
																		</span>
																	)
																)
															: `${
																	author.intermediatory_author_classes.length
																} ${translate("classifiers.types.manual_post_authors.fields.classes")}`}
													</div>
												</td>
												<td>{author.pi_platform_message_author_name}</td>
												<td>{author.phoenix_platform_message_author_id}</td>
												<td>{author.post_count}</td>
												<td className="capitalize">{author.platform}</td>
												<td>{author.pi_platform_message_author_id}</td>
											</tr>
										))}
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
