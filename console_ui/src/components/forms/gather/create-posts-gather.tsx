import React from "react";
import { NumberInput, Tooltip } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { IconInfoCircle } from "@tabler/icons";
import { GetInputProps } from "@mantine/form/lib/types";
import { ProjectSchema } from "src/interfaces/project";
import { DatePicker } from "@mantine/dates";

// Define separate validation rules for posts
export function getPostValidationRules(data: any, today: Date) {
	if (data.data_type === "posts") {
		const validationRules: any = {};

		validationRules.start_date = !data.start_date ? "Required" : null;
		validationRules.end_date = !data.end_date ? "Required" : null;
		validationRules.limit_posts_per_account =
			data.limit_posts_per_account === undefined ? "Required" : null;

		if (data.start_date && data.end_date) {
			const startDate = new Date(data.start_date);
			const endDate = new Date(data.end_date);

			if (startDate > today) {
				validationRules.start_date = "Start date cannot be in the future";
			}
			if (startDate > endDate) {
				validationRules.start_date = "Start date cannot be after end date";
				validationRules.end_date = "End date cannot be before start date";
			}
		}

		return validationRules;
	}
	return {};
}

interface Props {
	getInputProps: GetInputProps<ProjectSchema>;
}

const CreatePostsGatherForm: React.FC<Props> = ({ getInputProps }) => {
	const translate = useTranslate();
	return (
		<>
			<DatePicker
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.info.start_date")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.start_date")}
						<span className="text-red-500 ml-1">*</span>
					</div>
				}
				{...getInputProps("start_date")}
			/>
			<DatePicker
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.info.end_date")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.end_date")}
						<span className="text-red-500 ml-1">*</span>
					</div>
				}
				{...getInputProps("end_date")}
			/>
			<NumberInput
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate("gathers.fields.info.limit_posts_per_account")}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.limit_posts_per_account")}
						<span className="text-red-500 ml-1">*</span>
					</div>
				}
				{...getInputProps("limit_posts_per_account")}
			/>
		</>
	);
};

export default CreatePostsGatherForm;
