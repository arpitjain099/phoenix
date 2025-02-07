"use client";

import React, { useState, useEffect } from "react";
import { useResource, useShow, useTranslate } from "@refinedev/core";
import {
	Show,
	TextField,
	DateField,
	EditButtonProps,
	EditButton,
} from "@refinedev/mantine";
import { Group, Loader, Tabs, Text, Title } from "@mantine/core";
import OverviewComponent from "@components/project/overview";
import AboutComponent from "@components/project/about";
import VisualiseComponent from "@components/project/visualise";
import GatherComponent from "@components/project/gather";
import ClassifyComponent from "@components/project/classify";
import { useRouter, useSearchParams } from "next/navigation";

export default function ProjectShow(): JSX.Element {
	const translate = useTranslate();
	const { queryResult } = useShow();
	const router = useRouter();
	const searchParams = useSearchParams();
	const activeItem = searchParams.get("activeItem");
	const { refetch, data, isLoading } = queryResult;

	const record = data?.data;

	const { id: idFromParams, identifier } = useResource("projects");
	const [activeTab, setActiveTab] = useState<string | null>(
		activeItem || "overview"
	);

	const editButtonProps: EditButtonProps = {
		...(isLoading ? { disabled: true } : {}),
		// color: "primary",
		variant: "outline",
		resource: identifier,
		recordItemId: idFromParams,
	};
	useEffect(() => {
		if (activeItem) {
			setActiveTab(activeItem);
		}
	}, [activeItem]);
	return (
		<Show
			title={<Title order={3}>{record?.name}</Title>}
			isLoading={isLoading}
			headerButtons={() => <EditButton {...editButtonProps} />}
		>
			<TextField value={record?.description} />

			<Group>
				<Title my="xs" order={5}>
					{translate("projects.dataset_last_update")}:
				</Title>
				{record?.last_job_run_completed_at ? (
					<DateField format="LLL" value={record?.last_job_run_completed_at} />
				) : (
					<Text>-</Text>
				)}
				{record?.latest_job_run && !record?.latest_job_run?.completed_at && (
					<Loader size="xs" />
				)}
			</Group>
			<Tabs
				value={activeTab}
				onTabChange={(value) =>
					router.replace(`/projects/show/${idFromParams}?activeItem=${value}`)
				}
			>
				<Tabs.List>
					<Tabs.Tab value="overview">Overview</Tabs.Tab>
					<Tabs.Tab value="gather">Gather</Tabs.Tab>
					<Tabs.Tab value="classify">Classify</Tabs.Tab>
					<Tabs.Tab value="visualise">Visualise</Tabs.Tab>
					<Tabs.Tab value="about">About</Tabs.Tab>
				</Tabs.List>

				<Tabs.Panel value="overview" pt="xs">
					<OverviewComponent setActiveTab={setActiveTab} info={record} />
				</Tabs.Panel>

				<Tabs.Panel value="gather" pt="xs">
					<GatherComponent projectid={idFromParams} refetch={refetch} />
				</Tabs.Panel>

				<Tabs.Panel value="classify" pt="xs">
					<ClassifyComponent projectid={idFromParams} refetch={refetch} />
				</Tabs.Panel>

				<Tabs.Panel value="visualise" pt="xs">
					<VisualiseComponent info={record} />
				</Tabs.Panel>

				<Tabs.Panel value="about" pt="xs">
					<AboutComponent info={record} />
				</Tabs.Panel>
			</Tabs>
		</Show>
	);
}
