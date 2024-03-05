import { IResourceComponentsProps, useTranslate } from "@refinedev/core";
import { Create, useForm } from "@refinedev/mantine";
import { TextInput, NumberInput, Select, Textarea, Alert } from "@mantine/core";
import React, { useEffect } from "react";

export const InstanceCreate: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const {
		getInputProps,
		saveButtonProps,
		setFieldValue,
		values,
		refineCore: { formLoading },
	} = useForm({
		initialValues: {
			id: "",
			name: "",
			description: "",
			environment_id: "",
			days_until_pi_expiration: undefined,
			days_until_all_data_expiration: undefined,
		},
		validate: {
			id: (value) =>
				value.length <= 0
					? "ID is required"
					: value.length < 2
						? "ID is too short"
						: null,
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

	useEffect(() => {
		setFieldValue("id", values.name);
	}, [setFieldValue, values.name]);

	return (
		<Create isLoading={formLoading} saveButtonProps={saveButtonProps}>
			<TextInput
				mt="sm"
				withAsterisk
				label={translate("instances.fields.name")}
				{...getInputProps("name")}
			/>
			<TextInput
				mt="sm"
				withAsterisk
				disabled
				label={translate("instances.fields.id")}
				{...getInputProps("id")}
			/>
			<Select
				mt="sm"
				withAsterisk
				label={translate("instances.fields.environment_id")}
				{...getInputProps("environment_id")}
				data={[
					{ label: "Select", value: "" },
					{ label: "Environment 1", value: "env1" },
					{ label: "Environment 2", value: "env2" },
					{ label: "Environment 3", value: "env3", disabled: true },
					{ label: "Environment 4", value: "env4" },
				]}
			/>
			<NumberInput
				mt="sm"
				min={183}
				max={365}
				withAsterisk
				label={translate("instances.fields.days_until_pi_expiration")}
				{...getInputProps("days_until_pi_expiration")}
			/>
			<NumberInput
				mt="sm"
				min={183}
				max={365}
				label={translate("instances.fields.days_until_all_data_expiration")}
				{...getInputProps("days_until_all_data_expiration")}
			/>
			<Select
				mt="sm"
				label={translate("instances.fields.lookup_frequency")}
				data={[
					{ label: "Select", value: "" },
					{ label: "One off analysis", value: "env1" },
					{ label: "Monthly", value: "env2" },
					{ label: "Weekly", value: "env3" },
					{ label: "Daily", value: "env4" },
				]}
			/>
			<Textarea
				mt="sm"
				label={translate("instances.fields.description")}
				{...getInputProps("description")}
			/>
			<Alert mt="lg" title="Note!" color="red">
				{translate("instances.warnings.create")}
			</Alert>
		</Create>
	);
};

export default InstanceCreate;
