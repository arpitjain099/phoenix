"use client";

import { Container, Group, Title } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { DateField, NumberField, TextField } from "@refinedev/mantine";
import React from "react";

interface IAboutProps {
	info: any;
}

const AboutComponent: React.FC<IAboutProps> = ({ info }) => {
	const translate = useTranslate();
	return (
		<Container className="mx-0 flex flex-col my-4">
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.environment_slug")}:
				</Title>
				<TextField value={info?.environment_slug} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.id")}:
				</Title>
				<NumberField value={info?.id ?? ""} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.days_until_pi_expiration")}:
				</Title>
				<NumberField value={info?.pi_deleted_after_days ?? ""} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.days_until_all_data_expiration")}:
				</Title>
				<NumberField value={info?.delete_after_days ?? ""} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.expected_usage.title")}:
				</Title>
				<TextField value={info?.expected_usage} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.updated_at")}:
				</Title>
				<DateField format="LLL" value={info?.updated_at} />
			</Group>
		</Container>
	);
};

export default AboutComponent;
