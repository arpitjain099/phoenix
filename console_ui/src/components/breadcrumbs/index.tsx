/* eslint-disable react/require-default-props */

"use client";

import React, { useEffect, useState } from "react";
import { Group, Anchor, Breadcrumbs } from "@mantine/core";
import { useOne } from "@refinedev/core";

interface BreadcrumbItem {
	title: string;
	href: string;
	replaceWithProjectName?: boolean;
}

interface BreadcrumbsProps {
	breadcrumbs: BreadcrumbItem[];
	projectid?: string;
}

const BreadcrumbsComponent: React.FC<BreadcrumbsProps> = ({
	breadcrumbs,
	projectid,
}) => {
	const [updatedBreadcrumbs, setUpdatedBreadcrumbs] =
		useState<BreadcrumbItem[]>(breadcrumbs);

	const { data: projectData } = useOne({
		resource: "projects",
		id: projectid as string,
		queryOptions: {
			enabled: !!projectid,
		},
	});

	useEffect(() => {
		if (projectData?.data?.name) {
			const newBreadcrumbs = breadcrumbs.map((breadcrumb) => {
				if (breadcrumb?.replaceWithProjectName && projectid) {
					return { ...breadcrumb, title: projectData.data.name };
				}
				return breadcrumb;
			});
			setUpdatedBreadcrumbs(newBreadcrumbs);
		}
	}, [projectData?.data?.name, breadcrumbs, projectid]);

	return (
		<Breadcrumbs>
			{updatedBreadcrumbs.map((item) => (
				<Group key={item.title}>
					<Anchor color="gray" size="sm" href={item.href}>
						{item.title}
					</Anchor>
				</Group>
			))}
		</Breadcrumbs>
	);
};

export default BreadcrumbsComponent;
