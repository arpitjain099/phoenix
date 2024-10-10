"use client";

import React from "react";
import { NumberInput, Select, TextInput, Tooltip } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { IconInfoCircle } from "@tabler/icons";
import { GetInputProps } from "@mantine/form/lib/types";
import { ProjectSchema } from "src/interfaces/project";
import GatherInputs from "@components/inputs/gather-inputs";
import { TextField } from "@refinedev/mantine";
import { countryList, hashTagPostBaseLink } from "src/utils/constants";

interface FormValues {
	name: string;
	limit_posts_per_search: number;
	search_list: string[];
	proxy_country_to_gather_from: string;
}

export const initialFormValues: FormValues = {
	name: "",
	limit_posts_per_search: 100,
	search_list: [],
	proxy_country_to_gather_from: "None",
};

// Define separate validation rules for posts
export function getPostValidationRules(data: any, translate: any) {
	const validationRules: any = {};

	validationRules.name =
		data.name.length <= 0
			? translate(
					"gathers.types.apify_tiktok_tiktok_posts.fields.validation.required"
				)
			: null;
	validationRules.search_list =
		data.search_list.length <= 0
			? translate(
					"gathers.types.apify_tiktok_tiktok_posts.fields.validation.required"
				)
			: null;
	validationRules.limit_posts_per_search =
		data.limit_posts_per_search === undefined
			? translate(
					"gathers.types.apify_tiktok_tiktok_posts.fields.validation.required"
				)
			: null;
	validationRules.proxy_country_to_gather_from =
		!data.proxy_country_to_gather_from
			? translate(
					"gathers.types.apify_tiktok_tiktok_posts.fields.validation.required"
				)
			: null;

	return validationRules;
}

interface Props {
	getInputProps: GetInputProps<ProjectSchema>;
	inputList: string[];
	setInputList: any;
}

const ApifyTiktokSearchesPostsForm: React.FC<Props> = ({
	getInputProps,
	inputList,
	setInputList,
}) => {
	const translate = useTranslate();
	return (
		<>
			<TextField
				value={translate(
					"gathers.types.apify_tiktok_searches_posts.create_description"
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
			<NumberInput
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate(
								"gathers.types.apify_tiktok_searches_posts.fields.info.limit_posts_per_search"
							)}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate(
							"gathers.types.apify_tiktok_searches_posts.fields.limit_posts_per_search"
						)}
					</div>
				}
				{...getInputProps("limit_posts_per_search")}
			/>
			<Select
				mt="lg"
				searchable
				clearable
				data={countryList}
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate(
								"gathers.types.apify_tiktok_searches_posts.fields.info.proxy_country_to_gather_from"
							)}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate(
							"gathers.types.apify_tiktok_searches_posts.fields.proxy_country_to_gather_from"
						)}
					</div>
				}
				{...getInputProps("proxy_country_to_gather_from")}
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
							"gathers.types.apify_tiktok_searches_posts.fields.input.url_list"
						)}
						{inputList.length > 0 && (
							<span className="italic ml-10">
								{inputList.length}{" "}
								{translate(`gathers.fields.source.input_values`)}
							</span>
						)}
					</div>
				}
				placeholder={translate("gathers.fields.input.data_placeholder")}
				data={inputList}
				setData={setInputList}
				template_url_for_input={hashTagPostBaseLink}
				{...getInputProps("search_list")}
			/>
		</>
	);
};

export default ApifyTiktokSearchesPostsForm;
