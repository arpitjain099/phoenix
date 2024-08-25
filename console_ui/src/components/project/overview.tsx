"use client";

import { Anchor, Checkbox, Group, Text, Title } from "@mantine/core";
import { useTranslate, useUpdate } from "@refinedev/core";
import React from "react";
import { PHEONIX_MANUAL_URL } from "src/utils";

interface IOverviewProps {
	info: any;
	setActiveTab: any;
}

const OverviewComponent: React.FC<IOverviewProps> = ({
	info,
	setActiveTab,
}) => {
	const { mutate } = useUpdate();
	const translate = useTranslate();
	const handleUpdate = async (values: any) => {
		if (info?.id)
			mutate(
				{
					resource: "projects",
					id: info.id,
					values,
					meta: {
						method: "put",
					},
					errorNotification: false,
					successNotification: false,
				},
				{
					onSuccess: async () => {},
				}
			);
	};
	return (
		<div className="p-4">
			<div className="flex flex-col gap-4">
				<Title order={3}>{translate("projects.tabs.overview.title")}</Title>
				<Text fz="sm">
					{translate("projects.tabs.overview.description.part1.a")}
					<span className="font-bold">
						{translate("projects.tabs.overview.description.part1.b")}
					</span>
				</Text>
				<Text fz="sm">
					{translate("projects.tabs.overview.description.part2.a")}
					<Anchor
						className="font-normal text-inherit hover:text-blue-500 text-sm underline"
						href={PHEONIX_MANUAL_URL}
						target="_blank"
					>
						{translate("projects.tabs.overview.description.part2.b")}
					</Anchor>
				</Text>
				<Text fz="sm" mt={4}>
					{translate("projects.tabs.overview.description.part3")}
				</Text>
			</div>
			<div className="my-4 relative z-10">
				<div className="flex flex-col gap-2 text-left font-medium text-lg leading-none border-blue-200 divide-y divide-blue-200">
					<Group spacing="xs">
						{/* <span className="ml-5 mr-2.5 w-1 h-7 bg-blue-500 rounded-r-md" /> */}
						<Checkbox
							checked={info?.checked_problem_statement || false}
							onChange={(event) =>
								handleUpdate({
									checked_problem_statement: event.currentTarget.checked,
								})
							}
							size="xs"
							className="cursor-pointer"
						/>
						<Text fz="sm">
							{translate("projects.tabs.overview.problem_statement")}
						</Text>
						<Anchor
							className="font-normal text-inherit hover:text-blue-500 text-sm underline"
							href={PHEONIX_MANUAL_URL}
							target="_blank"
						>
							({translate("projects.tabs.overview.tips.manual")})
						</Anchor>
					</Group>
					<Group spacing="xs">
						<Checkbox
							checked={info?.checked_sources || false}
							onChange={(event) =>
								handleUpdate({
									checked_sources: event.currentTarget.checked,
								})
							}
							size="xs"
							className="cursor-pointer"
						/>
						<Text fz="sm">{translate("projects.tabs.overview.source")}</Text>
						<Anchor
							className="font-normal text-inherit hover:text-blue-500 text-sm underline"
							href={PHEONIX_MANUAL_URL}
							target="_blank"
						>
							({translate("projects.tabs.overview.tips.manual")})
						</Anchor>
					</Group>
					<Group spacing="xs">
						<Checkbox
							checked={info?.checked_gather || false}
							onChange={(event) =>
								handleUpdate({
									checked_gather: event.currentTarget.checked,
								})
							}
							size="xs"
							className="cursor-pointer"
						/>
						<Text fz="sm">{translate("projects.tabs.overview.gather")}</Text>
						<Anchor
							component="button"
							type="button"
							className="font-normal text-inherit hover:text-blue-500 text-sm underline"
							onClick={() => setActiveTab("gather")}
							aria-hidden="true"
						>
							({translate("projects.tabs.overview.tips.gather")})
						</Anchor>
					</Group>
					<Group spacing="xs">
						<Checkbox
							checked={info?.checked_classify || false}
							onChange={(event) =>
								handleUpdate({
									checked_classify: event.currentTarget.checked,
								})
							}
							size="xs"
							className="cursor-pointer"
						/>
						<Text fz="sm">{translate("projects.tabs.overview.classify")}</Text>
						<Anchor
							component="button"
							type="button"
							className="font-normal text-inherit hover:text-blue-500 text-sm underline"
							onClick={() => setActiveTab("classify")}
							aria-hidden="true"
						>
							({translate("projects.tabs.overview.tips.classify")})
						</Anchor>
					</Group>
					<Group spacing="xs">
						<Checkbox
							checked={info?.checked_visualise || false}
							onChange={(event) =>
								handleUpdate({
									checked_visualise: event.currentTarget.checked,
								})
							}
							size="xs"
							className="cursor-pointer"
						/>
						<Text fz="sm">{translate("projects.tabs.overview.visualise")}</Text>
						<Anchor
							component="button"
							type="button"
							className="font-normal text-inherit hover:text-blue-500 text-sm underline"
							onClick={() => setActiveTab("visualise")}
							aria-hidden="true"
						>
							({translate("projects.tabs.overview.tips.visualise")})
						</Anchor>
					</Group>
					<Group spacing="xs">
						<Checkbox
							checked={info?.checked_explore || false}
							onChange={(event) =>
								handleUpdate({
									checked_explore: event.currentTarget.checked,
								})
							}
							size="xs"
							className="cursor-pointer"
						/>
						<Text fz="sm">{translate("projects.tabs.overview.insights")}</Text>
						<Anchor
							className="font-normal text-inherit hover:text-blue-500 text-sm underline"
							href={PHEONIX_MANUAL_URL}
							target="_blank"
						>
							({translate("projects.tabs.overview.tips.manual")})
						</Anchor>
					</Group>
				</div>
			</div>
		</div>
	);
};

export default OverviewComponent;
