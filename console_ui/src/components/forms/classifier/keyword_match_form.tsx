"use client";

import React from "react";
import { NumberInput, TextInput, Tooltip } from "@mantine/core";
import { useGetLocale, useTranslate } from "@refinedev/core";
import { IconInfoCircle } from "@tabler/icons";
import { GetInputProps } from "@mantine/form/lib/types";
import { ProjectSchema } from "src/interfaces/project";
import { DatePicker } from "@mantine/dates";
import GatherInputs from "@components/inputs/gather-inputs";
import { TextField } from "@refinedev/mantine";

const today = new Date();
const tomorrow = new Date(today);
tomorrow.setDate(tomorrow.getDate() + 1);

export const initialFormValues = {
	name: "",
	limit_posts_per_account: 1000,
	account_url_list: [] as string[],
	posts_created_after: today,
	posts_created_before: tomorrow,
};

// Define separate validation rules for posts
export function getPostValidationRules(data: any, translate: any) {
	const validationRules: any = {};

	validationRules.name =
		data.name.length <= 0
			? translate(
					"gathers.types.apify_facebook_posts.fields.validation.required"
				)
			: null;
	validationRules.account_url_list =
		data.account_url_list.length <= 0
			? translate(
					"gathers.types.apify_facebook_posts.fields.validation.required"
				)
			: null;
	validationRules.limit_posts_per_account =
		data.limit_posts_per_account === undefined
			? translate(
					"gathers.types.apify_facebook_posts.fields.validation.required"
				)
			: null;
	validationRules.posts_created_after = !data.posts_created_after
		? translate("gathers.types.apify_facebook_posts.fields.validation.required")
		: null;
	validationRules.posts_created_before = !data.posts_created_before
		? translate("gathers.types.apify_facebook_posts.fields.validation.required")
		: null;

	if (data.posts_created_after && data.posts_created_before) {
		const startDate = new Date(data.posts_created_after);
		const endDate = new Date(data.posts_created_before);

		if (startDate > today) {
			validationRules.posts_created_after = translate(
				"gathers.types.apify_facebook_posts.fields.validation.posts_created_after.less_than_today"
			);
		}
		if (startDate > endDate) {
			validationRules.posts_created_after = translate(
				"gathers.types.apify_facebook_posts.fields.validation.posts_created_after.less_than_end"
			);
			validationRules.posts_created_before = translate(
				"gathers.types.apify_facebook_posts.fields.validation.posts_created_before.greater_than_start"
			);
		}
	}

	return validationRules;
}

interface Props {
	getInputProps: GetInputProps<ProjectSchema>;
	inputList: string[];
	setInputList: any;
}

const KeywordMatchForm: React.FC<Props> = ({
	getInputProps,
	inputList,
	setInputList,
}) => {
	const translate = useTranslate();
	const locale = useGetLocale();
	const currentLocale = locale();
	return (
		<>
			<TextField
				value={translate(
					"gathers.types.apify_facebook_posts.create_description"
				)}
			/>
			<TextInput
				mt="sm"
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.info.name")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.input.name")}
					</div>
				}
				{...getInputProps("name")}
			/>
			<DatePicker
				mt="lg"
				locale={currentLocale}
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate(
								"gathers.types.apify_facebook_posts.fields.info.posts_created_after"
							)}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate(
							"gathers.types.apify_facebook_posts.fields.posts_created_after"
						)}
					</div>
				}
				{...getInputProps("posts_created_after")}
			/>
			<DatePicker
				mt="lg"
				locale={currentLocale}
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate(
								"gathers.types.apify_facebook_posts.fields.info.posts_created_before"
							)}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate(
							"gathers.types.apify_facebook_posts.fields.posts_created_before"
						)}
					</div>
				}
				{...getInputProps("posts_created_before")}
			/>
			<NumberInput
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate(
								"gathers.types.apify_facebook_posts.fields.info.limit_posts_per_account"
							)}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate(
							"gathers.types.apify_facebook_posts.fields.limit_posts_per_account"
						)}
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
						{translate(
							"gathers.types.apify_facebook_posts.fields.input.url_list"
						)}
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
				split_regex={/[,\s]+/}
				{...getInputProps("account_url_list")}
			/>
		</>
	);
};

export default KeywordMatchForm;
