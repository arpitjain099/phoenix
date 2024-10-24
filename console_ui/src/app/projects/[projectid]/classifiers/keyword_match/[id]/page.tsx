"use client";

import React from "react";
import { useShow, useTranslate } from "@refinedev/core";
import {
	Show,
	TextField,
	DateField,
	EditButton,
	EditButtonProps,
} from "@refinedev/mantine";
import { Accordion, Container, Group, Table, Title } from "@mantine/core";
import { useParams } from "next/navigation";
import URLInputList from "@components/gather/url-list";
import GatherViewBreadcrumb from "@components/breadcrumbs/gatherView";
import { statusTextStyle } from "src/utils";

export default function KeywordClassifierShow(): JSX.Element {
	const { projectid, id } = useParams();
	const translate = useTranslate();
	const { queryResult } = useShow({
		resource: `projects/${projectid}/classifiers`,
		id: id as string,
	});

	const { data, isLoading } = queryResult;

	const record = data?.data;

	const editButtonProps: EditButtonProps = {
		recordItemId: id as string,
	};

	return (
		<Show
			title={<Title order={3}>{record?.name}</Title>}
			breadcrumb={
				<GatherViewBreadcrumb record={record} projectid={projectid as string} />
			}
			isLoading={isLoading}
			headerButtons={() => <EditButton {...editButtonProps} />}
		>
			<TextField
				value={translate("classifiers.types.keyword_match.view.text")}
			/>
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
					defaultValue={["status", "general", "classes", "keywords"]}
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
					<Accordion.Item value="classes" mb="md">
						<Accordion.Control>
							<Title order={5}>
								{translate(
									`classifiers.types.keyword_match.view.accordion.classes`
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
													<td>{classItem?.name}</td>
													<td>{classItem?.description}</td>
												</tr>
											)
										)}
									</tbody>
								</Table>
							</Container>
						</Accordion.Panel>
					</Accordion.Item>

					<Accordion.Item value="keywords" mb="md">
						<Accordion.Control>
							<Title order={5}>
								{translate(
									`classifiers.types.keyword_match.view.accordion.keywords`
								)}
							</Title>
						</Accordion.Control>
						<Accordion.Panel>
							<Container className="mx-0 flex flex-col my-4">
								<Table highlightOnHover withBorder>
									<thead>
										<tr>
											<th>{translate("classifiers.fields.class_name")}</th>
											<th>{translate("classifiers.fields.keywords")}</th>
										</tr>
									</thead>
									<tbody>
										{record?.intermediatory_class_to_keyword_configs?.map(
											(classItem: any, classIndex: number) => (
												<tr key={classIndex}>
													<td>{classItem?.class_name}</td>
													<td>{classItem?.musts}</td>
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
