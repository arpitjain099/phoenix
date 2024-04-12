import { IResourceComponentsProps, useTranslate } from "@refinedev/core";
import { Create, useForm } from "@refinedev/mantine";
import {
	TextInput,
	NumberInput,
	Select,
	Textarea,
	Alert,
	Tooltip,
} from "@mantine/core";
import React from "react";
import { IconInfoCircle } from "@tabler/icons";

export const InstanceCreate: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const {
		getInputProps,
		saveButtonProps,
		refineCore: { formLoading },
	} = useForm({
		initialValues: {
			name: "",
			description: "",
			environment_id: "",
			days_until_pi_expiration: 183,
			days_until_all_data_expiration: 183,
			expected_usage: "",
		},
		validate: {
			name: (value) => (value.length <= 0 ? "Name is required" : null),
			environment_id: (value) =>
				value.length <= 0 ? "Environment is required" : null,
			days_until_pi_expiration: (value) =>
				value === undefined
					? "Required"
					: value < 183 || value > 365
						? "Value needs to fall between 183 - 365 days"
						: null,
			days_until_all_data_expiration: (value) =>
				value === undefined
					? "Required"
					: value < 183 || value > 365
						? "Value needs to fall between 183 - 365 days"
						: null,
		},
	});

	return (
		<Create isLoading={formLoading} saveButtonProps={saveButtonProps}>
			<TextInput
				mt="sm"
				withAsterisk
				label={translate("instances.fields.name")}
				{...getInputProps("name")}
			/>
			<Select
				mt="sm"
				withAsterisk
				label={translate("instances.fields.environment_id")}
				{...getInputProps("environment_id")}
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
				{...getInputProps("days_until_pi_expiration")}
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
				{...getInputProps("days_until_all_data_expiration")}
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
		</Create>
	);
};

export default InstanceCreate;
