"use client";

import DashboardLinkButton from "@components/buttons/DashboardLinkButton";
import { Anchor, Text, Title } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import React from "react";

const PHEONIX_MANUAL_VISUALISE =
	"https://howtobuildup.notion.site/Visualize-the-data-you-have-gathered-5db82b16367e455f99bda9d13b3fec04";

interface IVisualiseProps {
	info: any;
}

const VisualiseComponent: React.FC<IVisualiseProps> = ({ info }) => {
	const translate = useTranslate();
	return (
		<div className="p-4 flex flex-col gap-4">
			<Title order={3}>{translate("projects.tabs.visualise.title")}</Title>
			<Text fz="sm">
				{translate("projects.tabs.visualise.description")}{" "}
				<Anchor
					className="font-normal text-inherit hover:text-blue-500 text-sm underline"
					href={PHEONIX_MANUAL_VISUALISE}
					target="_blank"
				>
					{translate("projects.tabs.gather.description.part2.b")}
				</Anchor>
			</Text>
			<DashboardLinkButton
				workspaceSlug={info?.workspace_slug}
				dashboardId={info?.dashboard_id}
			/>
		</div>
	);
};

export default VisualiseComponent;
