"use client";

import { Container, Group, Title } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { DateField, TextField } from "@refinedev/mantine";
import React from "react";

interface Props {
	record: any;
}

const ClassifierViewGeneral: React.FC<Props> = ({ record }) => {
	const translate = useTranslate();
	return (
		<Container className="mx-0 flex flex-col my-4">
			<Group>
				<Title my="xs" order={5}>
					{translate("gathers.fields.name")}:
				</Title>
				<TextField className="capitalize" value={record?.name} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.description")}:
				</Title>
				<TextField className="capitalize" value={record?.description} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("gathers.fields.created_at")}:
				</Title>
				{record?.created_at ? (
					<DateField format="LLL" value={record?.created_at} />
				) : (
					"-"
				)}
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("classifiers.fields.latest_version_applyed_at")}:
				</Title>
				{record?.latest_version?.created_at ? (
					<DateField format="LLL" value={record?.latest_version?.created_at} />
				) : (
					"-"
				)}
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("classifiers.fields.latest_edits_made_at")}:
				</Title>
				{record?.last_edited_at ? (
					<DateField format="LLL" value={record?.last_edited_at} />
				) : (
					"-"
				)}
			</Group>
		</Container>
	);
};

export default ClassifierViewGeneral;
