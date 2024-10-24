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
import { Accordion, Container, Group, Title } from "@mantine/core";
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
					defaultValue="status"
				>
					<Accordion.Item value="status" className="mb-4">
						<Accordion.Control>
							<Title order={5}>
								{translate(
									"gathers.types.apify_facebook_posts.view.accordion.status"
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
									"gathers.types.apify_facebook_posts.view.accordion.general"
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
										Latest version applyed at:
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
										Latest edits made at:
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
									`gathers.types.apify_facebook_posts.view.accordion.source`
								)}
							</Title>
						</Accordion.Control>
						<Accordion.Panel>
							<Container className="mx-0 flex flex-col my-4">
								<Group>
									<Title my="xs" order={5}>
										{translate(
											`gathers.types.apify_facebook_posts.view.accordion.source_title`
										)}
										:
									</Title>
									{record?.account_url_list?.length}{" "}
									{translate(`gathers.fields.source.input_values`)}
								</Group>
								{record?.account_url_list?.length > 0 && (
									<URLInputList list={record?.account_url_list} />
								)}
							</Container>
						</Accordion.Panel>
					</Accordion.Item>
				</Accordion>
			</div>
		</Show>
	);
}
