"use client";

import React from "react";
import { useShow, useTranslate } from "@refinedev/core";
import {
	Show,
	TextField,
	DateField,
	EditButtonProps,
	EditButton,
	NumberField,
} from "@refinedev/mantine";
import { Accordion, Button, Container, Group, Title } from "@mantine/core";
import { useParams } from "next/navigation";
import { statusTextStyle } from "src/utils";
import { IconCopy } from "@tabler/icons";
import Link from "next/link";
import URLInputList from "@components/gather/url-list";
import BreadcrumbsComponent from "@components/breadcrumbs";

export default function ApifyFacebookPostShow(): JSX.Element {
	const { projectid, id } = useParams();
	const translate = useTranslate();
	const { queryResult } = useShow({
		resource: `projects/${projectid}/gathers`,
		id: id as string,
	});

	const { data, isLoading } = queryResult;

	const record = data?.data;

	const editButtonProps: EditButtonProps = {
		resource: `apify_facebook_posts`,
		recordItemId: id as string,
		...(isLoading ||
		(record?.latest_job_run &&
			record?.latest_job_run?.status !== "awaiting_start")
			? { disabled: true }
			: {}),
	};

	const breadcrumbs = [
		{ title: translate("projects.projects"), href: "/projects" },
		{
			title: projectid as string,
			href: `/projects/show/${projectid}`,
			replaceWithProjectName: true,
		},
		{
			title: translate("gathers.gathers"),
			href: `/projects/show/${projectid}?activeItem=gather`,
		},
		{ title: record?.name, href: "" },
	];

	return (
		<Show
			title={<Title order={3}>{record?.name}</Title>}
			breadcrumb={
				<BreadcrumbsComponent
					breadcrumbs={breadcrumbs}
					projectid={projectid as string}
				/>
			}
			isLoading={isLoading}
			headerButtons={() => (
				<>
					<Link
						href={`/projects/${projectid}/gathers/apify_facebook_posts/duplicate/${id}`}
					>
						<Button leftIcon={<IconCopy size={18} />}>Duplicate</Button>
					</Link>
					<EditButton {...editButtonProps} />
				</>
			)}
		>
			<TextField
				value={translate("gathers.types.apify_facebook_posts.view.text")}
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
								</Group>
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
										{translate("gathers.fields.from")}:
									</Title>
									<TextField
										className="capitalize"
										value={translate(`gathers.fields.source.apify`)}
									/>
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate("gathers.fields.platform")}:
									</Title>
									<TextField className="capitalize" value={record?.platform} />
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate("gathers.fields.data_type")}:
									</Title>
									<TextField
										className="capitalize"
										value={record?.child_type}
									/>
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate(
											"gathers.types.apify_facebook_posts.fields.posts_created_after"
										)}
										:
									</Title>
									<DateField format="LLL" value={record?.posts_created_after} />
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate(
											"gathers.types.apify_facebook_posts.fields.posts_created_before"
										)}
										:
									</Title>
									<DateField
										format="LLL"
										value={record?.posts_created_before}
									/>
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate(
											"gathers.types.apify_facebook_posts.fields.limit_posts_per_account"
										)}
										:
									</Title>
									<NumberField value={record?.limit_posts_per_account} />
								</Group>
							</Container>
						</Accordion.Panel>
					</Accordion.Item>
					<Accordion.Item value="source" mb="md">
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
