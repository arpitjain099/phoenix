import React from "react";
import { Checkbox, NumberInput, Select, Tooltip } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { IconInfoCircle } from "@tabler/icons";
import { GetInputProps } from "@mantine/form/lib/types";
import { ProjectSchema } from "src/interfaces/interface";

interface Props {
	getInputProps: GetInputProps<ProjectSchema>;
}

const CreateCommentsGatherForm: React.FC<Props> = ({ getInputProps }) => {
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
				label={translate("gathers.fields.comment_replies")}
				{...getInputProps("comment_replies", { type: "checkbox" })}
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
					{ label: "Facebook Defaults", value: "facebook_defaults" },
					{ label: "Most Relevant", value: "most_relevant" },
					{ label: "Newest First", value: "newest_first" },
					{ label: "None-filtered", value: "none_filtered" },
				]}
			/>
		</>
	);
};

export default CreateCommentsGatherForm;
