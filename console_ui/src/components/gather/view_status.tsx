import { Container, Group, Title } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { DateField, TextField } from "@refinedev/mantine";
import React from "react";
import { statusTextStyle } from "src/utils";

interface Props {
	record: any;
}

const GatherViewStatus: React.FC<Props> = ({ record }) => {
	const translate = useTranslate();
	return (
		<Container className="mx-0 flex flex-col my-4">
			<Group>
				<Title my="xs" order={5}>
					{translate("gathers.fields.status")}:
				</Title>
				<span className={`${statusTextStyle(record?.latest_job_run?.status)}`}>
					{record?.latest_job_run?.status
						? translate(`status.${record.latest_job_run.status}`)
						: "-"}
				</span>
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("gathers.fields.started_processing_at")}:
				</Title>
				{record?.latest_job_run?.started_processing_at ? (
					<DateField
						format="LLL"
						value={record?.latest_job_run.started_processing_at}
					/>
				) : (
					"-"
				)}
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("gathers.fields.completed_at")}:
				</Title>
				{record?.latest_job_run?.completed_at ? (
					<DateField format="LLL" value={record?.latest_job_run.completed_at} />
				) : (
					"-"
				)}
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("buttons.delete")} {translate("projects.fields.status")}:
				</Title>
				{record?.delete_job_run ? (
					<TextField
						className={`capitalize ${statusTextStyle(record?.delete_job_run?.status === "completed_successfully" ? "deleted" : record?.delete_job_run?.status)}`}
						value={translate(
							`status.delete_status.${record.delete_job_run.status}`
						)}
					/>
				) : (
					"-"
				)}
			</Group>
		</Container>
	);
};

export default GatherViewStatus;
