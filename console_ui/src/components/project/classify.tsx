"use client";

import { Title } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import React from "react";

interface IClassifyProps {}

const ClassifyComponent: React.FC<IClassifyProps> = () => {
	const translate = useTranslate();
	return (
		<div className="p-4">
			<Title order={3}>{translate("projects.tabs.classify.coming_soon")}</Title>
		</div>
	);
};

export default ClassifyComponent;
