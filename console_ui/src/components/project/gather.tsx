"use client";

import React, { useState } from "react";
import { useTranslate, useList } from "@refinedev/core";
import { Group, Button, Text, Title, Anchor } from "@mantine/core";
import TableComponent from "@components/table";
import { IconSquarePlus } from "@tabler/icons";
import GatherRunModal from "@components/modals/gather-run";
import GatherDeleteModal from "@components/modals/delete-gather";
import { GatherResponse } from "src/interfaces/gather";
import Link from "next/link";
import GatherRow from "@components/project/gather-row";

const PHEONIX_MANUAL_GATHER =
	"https://howtobuildup.notion.site/Decide-where-you-will-get-data-from-167f039d54874316be086734be194654";
const PHEONIX_MANUAL_GATHER_MORE =
	"https://howtobuildup.notion.site/Understanding-platform-credits-3f749bc6ebdf4ca68ba44447bc0dd4cc";

interface IGatherProps {
	projectid: any;
}

const GatherComponent: React.FC<IGatherProps> = ({ projectid }) => {
	const translate = useTranslate();
	const [opened, setOpened] = useState(false);
	const [deleteModalOpen, setDeleteModalOpen] = useState(false);
	const [selected, setSelected] = useState(null);

	const apiResponse = useList({
		resource: projectid ? `projects/${projectid}/gathers` : "",
		pagination: {
			mode: "off",
		},
	});

	return (
		<>
			<div className="p-4">
				<Group className="mb-4">
					<div className="flex flex-col gap-4">
						<Title order={3}>{translate("projects.tabs.gather.title")}</Title>
						<Text fz="sm">
							{translate("projects.tabs.gather.description.part1.a")}
							<Anchor
								className="font-normal text-inherit hover:text-blue-500 text-sm underline"
								href={PHEONIX_MANUAL_GATHER}
								target="_blank"
							>
								{translate("projects.tabs.gather.description.part1.b")}
							</Anchor>
							{translate("projects.tabs.gather.description.part1.c")}
						</Text>
						<Text fz="sm">
							{translate("projects.tabs.gather.description.part2.a")}
							<Anchor
								className="font-normal text-inherit hover:text-blue-500 text-sm underline"
								href={PHEONIX_MANUAL_GATHER_MORE}
								target="_blank"
							>
								{translate("projects.tabs.gather.description.part2.b")}
							</Anchor>
							{translate("projects.tabs.gather.description.part2.c")}
						</Text>
					</div>
					<Link href={`/projects/${projectid}/gathers/select_type`}>
						<Button leftIcon={<IconSquarePlus />}>
							{translate("actions.create")}
						</Button>
					</Link>
				</Group>
				<TableComponent>
					<thead>
						<tr>
							<th>{translate("gathers.fields.name")}</th>
							<th>{translate("gathers.fields.started_run_at")}</th>
							<th>{translate("gathers.fields.completed_at")}</th>
							<th>{translate("projects.fields.status")}</th>
							<th>{translate("table.actions")}</th>
						</tr>
					</thead>
					<tbody>
						{(apiResponse.data?.data || []).map((gather: GatherResponse) => (
							<GatherRow
								key={gather.id}
								row={gather}
								setSelected={setSelected}
								setOpened={setOpened}
								setDeleteModalOpen={setDeleteModalOpen}
								translate={translate}
							/>
						))}
					</tbody>
				</TableComponent>
			</div>
			<GatherRunModal
				opened={opened}
				setOpened={setOpened}
				gatherDetail={selected}
				handleRefresh={handleGatherRefresh}
			/>
			<GatherDeleteModal
				opened={deleteModalOpen}
				setOpened={setDeleteModalOpen}
				gatherDetail={selected}
				handleUpdate={handleGatherUpdate}
			/>
		</>
	);
};

export default GatherComponent;
