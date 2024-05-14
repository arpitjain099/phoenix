import React from "react";
import { Group, Anchor, Breadcrumbs } from "@mantine/core";

interface BreadcrumbItem {
	title: string;
	href: string;
}

interface BreadcrumbsProps {
	breadcrumbs: BreadcrumbItem[];
}

const BreadcrumbsComponent: React.FC<BreadcrumbsProps> = ({ breadcrumbs }) => (
	<Breadcrumbs>
		{breadcrumbs.map((item) => (
			<Group key={item.title}>
				<Anchor color="gray" size="sm" href={item.href}>
					{item.title}
				</Anchor>
			</Group>
		))}
	</Breadcrumbs>
);

export default BreadcrumbsComponent;
