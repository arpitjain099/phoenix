"use client";

import React, { Dispatch, SetStateAction } from "react";
import {
	Checkbox,
	Group,
	NumberInput,
	Radio,
	Select,
	TextInput,
	Tooltip,
} from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { IconInfoCircle } from "@tabler/icons";
import { GetInputProps } from "@mantine/form/lib/types";
import { ProjectSchema } from "src/interfaces/project";
import { TextField } from "@refinedev/mantine";
import { countryList } from "src/utils/constants";

const today = new Date();
const tomorrow = new Date(today);
tomorrow.setDate(tomorrow.getDate() + 1);

export const initialFormValues = {
	name: "",
	search_query: "",
	limit_posts: 0,
	limit_retries: 0,
	recent_posts: true,
};

// Define separate validation rules for posts
export function getPostValidationRules(data: any, translate: any) {
	const validationRules: any = {};

	validationRules.name =
		data.name.length <= 0
			? translate(
					"gathers.types.apify_facebook_search_posts.fields.validation.required"
				)
			: null;
	validationRules.search_query =
		data.search_query.length <= 0
			? translate(
					"gathers.types.apify_facebook_search_posts.fields.validation.required"
				)
			: null;
	validationRules.limit_posts =
		data.limit_posts === undefined
			? translate(
					"gathers.types.apify_facebook_search_posts.fields.validation.required"
				)
			: null;
	validationRules.limit_retries =
		data.limit_retries === undefined
			? translate(
					"gathers.types.apify_facebook_search_posts.fields.validation.required"
				)
			: null;

	return validationRules;
}

interface Props {
	proxyGroup: string;
	setProxyGroup: Dispatch<SetStateAction<string>>;
	proxyCountry: string | null;
	setProxyCountry: Dispatch<SetStateAction<string | null>>;
	getInputProps: GetInputProps<ProjectSchema>;
}

const ApifyFacebookSearchPostsForm: React.FC<Props> = ({
	getInputProps,
	proxyGroup,
	setProxyGroup,
	proxyCountry,
	setProxyCountry,
}) => {
	const translate = useTranslate();
	return (
		<>
			<TextField
				value={translate(
					"gathers.types.apify_facebook_search_posts.create_description"
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
			<TextInput
				mt="sm"
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate(
								"gathers.types.apify_facebook_search_posts.fields.info.search_query"
							)}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate(
							"gathers.types.apify_facebook_search_posts.fields.search_query"
						)}
					</div>
				}
				{...getInputProps("search_query")}
			/>
			<NumberInput
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate(
								"gathers.types.apify_facebook_search_posts.fields.info.limit_posts"
							)}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate(
							"gathers.types.apify_facebook_search_posts.fields.limit_posts"
						)}
					</div>
				}
				{...getInputProps("limit_posts")}
			/>
			<NumberInput
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate(
								"gathers.types.apify_facebook_search_posts.fields.info.limit_retries"
							)}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate(
							"gathers.types.apify_facebook_search_posts.fields.limit_retries"
						)}
					</div>
				}
				{...getInputProps("limit_retries")}
			/>
			<Checkbox
				mt="sm"
				label={translate(
					"gathers.types.apify_facebook_search_posts.fields.recent_posts"
				)}
				{...getInputProps("recent_posts", { type: "checkbox" })}
			/>
			<div>
				<Group spacing="lg" mt="sm">
					<Radio.Group
						value={proxyGroup}
						onChange={setProxyGroup}
						orientation="vertical"
						label={
							<div className="flex items-center">
								{translate(
									"gathers.types.apify_facebook_search_posts.fields.proxy_groups"
								)}
							</div>
						}
						description={translate(
							"gathers.types.apify_facebook_search_posts.fields.info.proxy_groups"
						)}
					>
						<Radio
							value="RESIDENTIAL"
							label={translate(
								"gathers.types.apify_facebook_search_posts.fields.residential_proxies"
							)}
						/>
						<Radio
							value="no_proxy"
							label={translate(
								"gathers.types.apify_facebook_search_posts.fields.no_proxy"
							)}
						/>
					</Radio.Group>
					{proxyGroup !== "no_proxy" && (
						<Select
							label={translate(
								"gathers.types.apify_facebook_search_posts.fields.proxy_country"
							)}
							value={proxyCountry || ""}
							onChange={setProxyCountry}
							data={[
								{
									value: "",
									label: translate(
										"gathers.types.apify_facebook_search_posts.fields.anywhere"
									),
								},
								...countryList.filter((country) => country.value !== "None"),
							]}
						/>
					)}
				</Group>
			</div>
		</>
	);
};

export default ApifyFacebookSearchPostsForm;
