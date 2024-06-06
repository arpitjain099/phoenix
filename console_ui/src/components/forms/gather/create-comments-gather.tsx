import React from "react";
import { Checkbox, NumberInput, Select, Tooltip } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { IconInfoCircle } from "@tabler/icons";
import { GetInputProps } from "@mantine/form/lib/types";
import { ProjectSchema } from "src/interfaces/project";
import GatherInputs from "@components/inputs/gather-inputs";

// Define form fields for submit
export const commentFieldsToKeep = [
	"source",
	"platform",
	"project_id",
	"data_type",
	"description",
	"post_url_list",
	"limit_comments_per_post",
	"sort_comments_by",
	"include_comment_replies",
];

// Define separate validation rules for comments
export function getCommentValidationRules(data: any) {
	if (data.data_type === "comments") {
		return {
			post_url_list: data.post_url_list.length <= 0 ? "Required" : null,
			limit_comments_per_post:
				data.limit_comments_per_post === undefined ? "Required" : null,
			sort_comments_by: !data.sort_comments_by ? "Required" : null,
		};
	}
	return {};
}

interface Props {
	getInputProps: GetInputProps<ProjectSchema>;
	inputList: string[];
	setInputList: any;
}

const CreateCommentsGatherForm: React.FC<Props> = ({
	getInputProps,
	inputList,
	setInputList,
}) => {
	const translate = useTranslate();
	return (
		<>
			<NumberInput
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate("gathers.fields.info.limit_comments_per_post")}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.limit_comments_per_post")}
						<span className="text-red-500 ml-1">*</span>
					</div>
				}
				{...getInputProps("limit_comments_per_post")}
			/>
			<Checkbox
				mt="sm"
				label={translate("gathers.fields.include_comment_replies")}
				{...getInputProps("include_comment_replies", { type: "checkbox" })}
			/>
			<Select
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.info.sort_comments_by")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.sort_comments_by")}
						<span className="text-red-500 ml-1">*</span>
					</div>
				}
				{...getInputProps("sort_comments_by")}
				data={[
					{ label: translate("inputs.select"), value: "" },
					{ label: "Facebook Default", value: "facebook_default" },
					{ label: "Most Relevant", value: "most_relevant" },
					{ label: "Newest First", value: "newest_first" },
					{ label: "Non-filtered", value: "non_filtered" },
				]}
			/>
			<GatherInputs
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.input.data_placeholder")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.input.facebook_post_url_list")}
						<span className="text-red-500 ml-1">*</span>
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
				{...getInputProps("post_url_list")}
			/>
		</>
	);
};

export default CreateCommentsGatherForm;
