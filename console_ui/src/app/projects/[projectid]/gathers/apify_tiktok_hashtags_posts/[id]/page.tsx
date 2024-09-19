"use client";

import React from "react";
import { useShow, useTranslate } from "@refinedev/core";
import {
	Show,
	TextField,
	EditButtonProps,
	EditButton,
	NumberField,
} from "@refinedev/mantine";
import { Accordion, Button, Container, Group, Title } from "@mantine/core";
import { useParams } from "next/navigation";
import { IconCopy } from "@tabler/icons";
import Link from "next/link";
import URLInputList from "@components/gather/url-list";
import BreadcrumbsComponent from "@components/breadcrumbs";
import GatherViewStatus from "@components/gather/view_status";
import { hashTagPostBaseLink } from "src/utils/constants";

export default function ApifyTiktokHashtagPostShow(): JSX.Element {
	const { projectid, id } = useParams();
	const translate = useTranslate();
	const { queryResult } = useShow({
		resource: `projects/${projectid}/gathers`,
		id: id as string,
	});

	const { data, isLoading } = queryResult;

	const record = data?.data;

	const editButtonProps: EditButtonProps = {
		resource: `apify_tiktok_hashtags_posts`,
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
						href={`/projects/${projectid}/gathers/apify_tiktok_hashtags_posts/duplicate/${id}`}
					>
						<Button leftIcon={<IconCopy size={18} />}>
							{translate("buttons.duplicate")}
						</Button>
					</Link>
					<EditButton {...editButtonProps} />
				</>
			)}
		>
			<TextField
				value={translate("gathers.types.apify_tiktok_hashtags_posts.view.text")}
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
									"gathers.types.apify_tiktok_hashtags_posts.view.accordion.status"
								)}
							</Title>
						</Accordion.Control>
						<Accordion.Panel>
							<GatherViewStatus record={record} />
						</Accordion.Panel>
					</Accordion.Item>
					<Accordion.Item value="general" mb="md">
						<Accordion.Control>
							<Title order={5}>
								{translate(
									"gathers.types.apify_tiktok_hashtags_posts.view.accordion.general"
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
									<TextField
										className="capitalize"
										value={translate("gathers.fields.source.tiktok")}
									/>
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate("gathers.fields.data_type")}:
									</Title>
									<TextField
										className="capitalize"
										value={translate("gathers.fields.source.hashtag_posts")}
									/>
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate(
											"gathers.types.apify_tiktok_hashtags_posts.fields.limit_posts_per_hashtag"
										)}
										:
									</Title>
									<NumberField value={record?.limit_posts_per_hashtag} />
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate(
											"gathers.types.apify_tiktok_hashtags_posts.fields.proxy_country_to_gather_from"
										)}
										:
									</Title>
									<TextField
										className="capitalize"
										value={record?.proxy_country_to_gather_from}
									/>
								</Group>
							</Container>
						</Accordion.Panel>
					</Accordion.Item>
					<Accordion.Item value="source" mb="md">
						<Accordion.Control>
							<Title order={5}>
								{translate(
									`gathers.types.apify_tiktok_hashtags_posts.view.accordion.source`
								)}
							</Title>
						</Accordion.Control>
						<Accordion.Panel>
							<Container className="mx-0 flex flex-col my-4">
								<Group>
									<Title my="xs" order={5}>
										{translate(
											`gathers.types.apify_tiktok_hashtags_posts.view.accordion.source_title`
										)}
										:
									</Title>
									{record?.hashtag_list?.length}{" "}
									{translate(`gathers.fields.source.input_values`)}
								</Group>
								{record?.hashtag_list?.length > 0 && (
									<URLInputList
										list={record?.hashtag_list}
										template_url_for_input={hashTagPostBaseLink}
									/>
								)}
							</Container>
						</Accordion.Panel>
					</Accordion.Item>
				</Accordion>
			</div>
		</Show>
	);
}
