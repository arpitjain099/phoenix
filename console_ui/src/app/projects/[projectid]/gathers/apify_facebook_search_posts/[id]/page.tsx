"use client";

import React from "react";
import { useShow, useTranslate } from "@refinedev/core";
import { Show, TextField, NumberField } from "@refinedev/mantine";
import { Accordion, Container, Group, Title } from "@mantine/core";
import { useParams } from "next/navigation";
import GatherViewStatus from "@components/gather/view_status";
import GatherViewBreadcrumb from "@components/breadcrumbs/gatherView";
import GatherViewHeaderButton from "@components/gather/header-button";
import { countryList } from "src/utils/constants";

export default function ApifyFacebookSearchPostShow(): JSX.Element {
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
					resource="apify_facebook_search_posts"
					id={id as string}
					projectid={projectid as string}
					record={record}
					isLoading={isLoading}
				/>
			)}
		>
			<TextField
				value={translate("gathers.types.apify_facebook_search_posts.view.text")}
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
									"gathers.types.apify_facebook_search_posts.view.accordion.status"
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
									"gathers.types.apify_facebook_search_posts.view.accordion.general"
								)}
							</Title>
						</Accordion.Control>
						<Accordion.Panel>
							<Container className="mx-0 flex flex-col my-4">
								<Group>
									<Title my="xs" order={5}>
										{translate(
											"gathers.types.apify_facebook_search_posts.fields.search_query"
										)}
										:
									</Title>
									<TextField
										className="capitalize"
										value={record?.search_query}
									/>
								</Group>
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
											"gathers.types.apify_facebook_search_posts.fields.limit_posts"
										)}
										:
									</Title>
									<NumberField value={record?.limit_posts} />
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate(
											"gathers.types.apify_facebook_search_posts.fields.limit_retries"
										)}
										:
									</Title>
									<NumberField value={record?.limit_retries} />
								</Group>
								<Group>
									<Title my="xs" order={5}>
										{translate(
											"gathers.types.apify_facebook_search_posts.fields.recent_posts"
										)}
										:
									</Title>
									<TextField
										className="capitalize"
										value={record?.recent_posts?.toString()}
									/>
								</Group>
							</Container>
						</Accordion.Panel>
					</Accordion.Item>
					<Accordion.Item value="source" mb="md">
						<Accordion.Control>
							<Title order={5}>
								{translate(
									`gathers.types.apify_facebook_search_posts.view.accordion.proxy_setting`
								)}
							</Title>
						</Accordion.Control>
						<Accordion.Panel>
							<Container className="mx-0 flex flex-col my-4">
								<Group>
									<Title my="xs" order={5}>
										{translate(
											"gathers.types.apify_facebook_search_posts.fields.proxy_groups"
										)}
										:
									</Title>
									<TextField
										className="capitalize"
										value={
											record?.proxy?.use_apify_proxy
												? record?.proxy?.apify_proxy_groups[0]
												: translate(
														"gathers.types.apify_facebook_search_posts.fields.no_proxy"
													)
										}
									/>
								</Group>
								{record?.proxy?.use_apify_proxy && (
									<Group>
										<Title my="xs" order={5}>
											{translate(
												"gathers.types.apify_facebook_search_posts.fields.proxy_country"
											)}
											:
										</Title>
										<TextField
											className="capitalize"
											value={
												record?.proxy?.apify_proxy_country
													? countryList.find(
															(country) =>
																country.value ===
																record?.proxy?.apify_proxy_country
														)?.label
													: translate(
															"gathers.types.apify_facebook_search_posts.fields.anywhere"
														)
											}
										/>
									</Group>
								)}
							</Container>
						</Accordion.Panel>
					</Accordion.Item>
				</Accordion>
			</div>
		</Show>
	);
}
