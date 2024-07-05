"use client";

import DashboardLinkButton from "@components/buttons/DashboardLinkButton";
import { Text, Title } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import React from "react";

interface IVisualiseProps {
	info: any;
}

const VisualiseComponent: React.FC<IVisualiseProps> = ({ info }) => {
	const translate = useTranslate();
	return (
		<div className="p-4 flex flex-col gap-4">
			<Title order={3}>{translate("projects.tabs.visualise.title")}</Title>
			<Text fz="sm" c="dimmed">
				{translate("projects.tabs.visualise.description")}
			</Text>
			<DashboardLinkButton
				environmentSlug={info?.environment_slug}
				dashboardId={info?.dashboard_id}
			/>
		</div>
	);
};

export default VisualiseComponent;
