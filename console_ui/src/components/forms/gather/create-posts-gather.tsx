import React from "react";
import { NumberInput, Tooltip } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { IconInfoCircle } from "@tabler/icons";
import { GetInputProps } from "@mantine/form/lib/types";
import { ProjectSchema } from "src/interfaces/interface";
import { DatePicker } from "@mantine/dates";

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
