import React from "react";
import {
	TextInput,
	NumberInput,
	Select,
	Textarea,
	Alert,
	Tooltip,
} from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { IconInfoCircle } from "@tabler/icons";
import { GetInputProps } from "@mantine/form/lib/types";
import { InstanceSchema } from "src/interfaces/interface";

interface Props {
	getInputProps: GetInputProps<InstanceSchema>;
}

const CreateEditInstanceForm: React.FC<Props> = ({ getInputProps }) => {
	const translate = useTranslate();
	return (
		<>
			<TextInput
				mt="sm"
				withAsterisk
				label={translate("instances.fields.name")}
				{...getInputProps("name")}
			/>
			<Select
				mt="sm"
				withAsterisk
				label={translate("instances.fields.environment_slug")}
				{...getInputProps("environment_slug")}
				data={[
					{ label: translate("inputs.select"), value: "" },
					{ label: "Main", value: "main" },
				]}
			/>
			<NumberInput
				mt="sm"
				min={183}
				max={365}
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate("instances.warnings.days_until_pi_expiration")}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("instances.fields.days_until_pi_expiration")}
						<span className="text-red-500">*</span>
					</div>
				}
				{...getInputProps("pi_deleted_after_days")}
			/>
			<NumberInput
				mt="sm"
				min={183}
				max={365}
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate(
								"instances.warnings.days_until_all_data_expiration"
							)}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("instances.fields.days_until_all_data_expiration")}
						<span className="text-red-500">*</span>
					</div>
				}
				{...getInputProps("delete_after_days")}
			/>
			<Select
				mt="sm"
				label={translate("instances.fields.expected_usage.title")}
				data={[
					{ label: translate("inputs.select"), value: "" },
					{
						label: translate("instances.fields.expected_usage.options.one_off"),
						value: "one_off",
					},
					{
						label: translate("instances.fields.expected_usage.options.monthly"),
						value: "monthly",
					},
					{
						label: translate("instances.fields.expected_usage.options.weekly"),
						value: "weekly",
					},
					{
						label: translate("instances.fields.expected_usage.options.daily"),
						value: "daily",
					},
				]}
				{...getInputProps("expected_usage")}
			/>
			<Textarea
				mt="sm"
				label={translate("instances.fields.description")}
				{...getInputProps("description")}
			/>
			<Alert mt="lg" title={translate("note")} color="gray">
				{translate("instances.warnings.create")}
			</Alert>
		</>
	);
};

export default CreateEditInstanceForm;
