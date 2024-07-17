"use client";

import React from "react";
import { NumberInput, Tooltip } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { IconInfoCircle } from "@tabler/icons";
import { GetInputProps } from "@mantine/form/lib/types";
import { ProjectSchema } from "src/interfaces/project";
import { DatePicker } from "@mantine/dates";
import GatherInputs from "@components/inputs/gather-inputs";

// Define form fields for submit
export const postFieldsToKeep = [
	"source",
	"platform",
	"project_id",
	"data_type",
	"name",
	"account_url_list",
	"posts_created_after",
	"only_posts_newer_than",
	"limit_posts_per_account",
];

// Define separate validation rules for posts
export function getPostValidationRules(data: any, today: Date) {
	if (data.data_type === "posts") {
		const validationRules: any = {};

		validationRules.account_url_list =
			data.account_url_list.length <= 0 ? "Required" : null;
		validationRules.posts_created_after = !data.posts_created_after
			? "Required"
			: null;
		validationRules.only_posts_newer_than = !data.only_posts_newer_than
			? "Required"
			: null;
		validationRules.limit_posts_per_account =
			data.limit_posts_per_account === undefined ? "Required" : null;

		if (data.posts_created_after && data.only_posts_newer_than) {
			const startDate = new Date(data.posts_created_after);
			const endDate = new Date(data.only_posts_newer_than);

			if (startDate > today) {
				validationRules.posts_created_after =
					"Start date cannot be in the future";
			}
			if (startDate > endDate) {
				validationRules.posts_created_after =
					"Start date cannot be after end date";
				validationRules.only_posts_newer_than =
					"End date cannot be before start date";
			}
		}

		return validationRules;
	}
	return {};
}

interface Props {
	getInputProps: GetInputProps<ProjectSchema>;
	inputList: string[];
	setInputList: any;
}

const CreatePostsGatherForm: React.FC<Props> = ({
	getInputProps,
	inputList,
	setInputList,
}) => {
	const translate = useTranslate();
	return (
		<>
			<DatePicker
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate("gathers.fields.info.posts_created_after")}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.posts_created_after")}
					</div>
				}
				{...getInputProps("posts_created_after")}
			/>
			<DatePicker
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate("gathers.fields.info.only_posts_newer_than")}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.only_posts_newer_than")}
					</div>
				}
				{...getInputProps("only_posts_newer_than")}
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
					</div>
				}
				{...getInputProps("limit_posts_per_account")}
			/>
			<GatherInputs
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.input.data_placeholder")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.input.facebook_account_url_list")}
						{inputList.length > 0 && (
							<span className="italic ml-10">
								{inputList.length} input value{inputList.length > 1 && "s"}
							</span>
						)}
					</div>
				}
				placeholder={translate("gathers.fields.input.data_placeholder")}
				data={inputList}
				setData={setInputList}
				{...getInputProps("account_url_list")}
			/>
		</>
	);
};

export default CreatePostsGatherForm;
