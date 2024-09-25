"use client";

import React from "react";
import { useShow, useTranslate } from "@refinedev/core";
import { Show, TextField, DateField, NumberField } from "@refinedev/mantine";
import { Accordion, Container, Group, Title } from "@mantine/core";
import { useParams } from "next/navigation";
import URLInputList from "@components/gather/url-list";
import GatherViewStatus from "@components/gather/view_status";
import GatherViewBreadcrumb from "@components/breadcrumbs/gatherView";
import GatherViewHeaderButton from "@components/gather/header-button";

export default function ApifyFacebookPostShow(): JSX.Element {
	const { projectid, id } = useParams();
	const translate = useTranslate();
	const { queryResult } = useShow({
		resource: `projects/${projectid}/gathers`,
		id: id as string,
	});

	const { data, isLoading } = queryResult;

	const record = data?.data;

	return (
		<Show
			title={<Title order={3}>{record?.name}</Title>}
			breadcrumb={
				<GatherViewBreadcrumb record={record} projectid={projectid as string} />
			}
			isLoading={isLoading}
			headerButtons={() => (
				<GatherViewHeaderButton
					resource="apify_facebook_posts"
					id={id as string}
					projectid={projectid as string}
					record={record}
					isLoading={isLoading}
				/>
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
							<GatherViewStatus record={record} />
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
									<TextField
										className="capitalize"
										value={translate("gathers.fields.source.facebook")}
									/>
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate("gathers.fields.data_type")}:
									</Title>
									<TextField
										className="capitalize"
										value={translate("gathers.fields.source.posts")}
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
