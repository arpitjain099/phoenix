import React from "react";
import {
	IResourceComponentsProps,
	useTranslate,
	useUpdate,
} from "@refinedev/core";
import { Edit, useForm } from "@refinedev/mantine";
import {
	TextInput,
	NumberInput,
	Select,
	Textarea,
	Alert,
	Tooltip,
} from "@mantine/core";
import { IconInfoCircle } from "@tabler/icons";

export const InstanceEdit: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const { mutate } = useUpdate();
	const {
		getInputProps,
		saveButtonProps,
		values,
		refineCore: { queryResult },
	} = useForm({
		initialValues: {
			name: "",
			environment_id: "",
			description: "",
			pi_deleted_after_days: "",
			delete_after_days: "",
			expected_usage: "",
		},
	});

	const instancesData = queryResult?.data?.data;

	const handleSave = async () => {
		if (instancesData?.id)
			mutate({
				resource: "instances",
				id: instancesData.id,
				values,
				meta: {
					method: "put",
				},
			});
	};

	return (
		<Edit saveButtonProps={{ ...saveButtonProps, onClick: handleSave }}>
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
				data={[
					{ label: translate("inputs.select"), value: "" },
					{ label: "Main", value: "main" },
				]}
				{...getInputProps("environment_id")}
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
				label={translate("instances.fields.expected_usage")}
				data={[
					{ label: translate("inputs.select"), value: "" },
					{ label: "One off analysis", value: "one_off" },
					{ label: "Monthly", value: "monthly" },
					{ label: "Weekly", value: "weekly" },
					{ label: "Daily", value: "daily" },
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
		</Edit>
	);
};

export default InstanceEdit;
