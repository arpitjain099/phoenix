import { useTranslate } from "@refinedev/core";
import React from "react";
import BreadcrumbsComponent from ".";

interface Props {
	projectid: string;
	record: any;
}

const GatherViewBreadcrumb: React.FC<Props> = ({ projectid, record }) => {
	const translate = useTranslate();
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
		<BreadcrumbsComponent
			breadcrumbs={breadcrumbs}
			projectid={projectid as string}
		/>
	);
};

export default GatherViewBreadcrumb;
