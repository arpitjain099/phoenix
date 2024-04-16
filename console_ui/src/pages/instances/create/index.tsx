import CreateEditInstanceForm from "@components/forms/create-edit-instance";
import { IResourceComponentsProps } from "@refinedev/core";
import { Create, useForm } from "@refinedev/mantine";
import React from "react";

export const InstanceCreate: React.FC<IResourceComponentsProps> = () => {
	const {
		getInputProps,
		saveButtonProps,
		refineCore: { formLoading },
	} = useForm({
		initialValues: {
			name: "",
			description: "",
			environment_id: "",
			pi_deleted_after_days: 183,
			delete_after_days: 183,
			expected_usage: "",
		},
		validate: {
			name: (value) => (value.length <= 0 ? "Name is required" : null),
			environment_id: (value) =>
				value.length <= 0 ? "Environment is required" : null,
			pi_deleted_after_days: (value) =>
				value === undefined
					? "Required"
					: value < 183 || value > 365
						? "Value needs to fall between 183 - 365 days"
						: null,
			delete_after_days: (value) =>
				value === undefined
					? "Required"
					: value < 183 || value > 365
						? "Value needs to fall between 183 - 365 days"
						: null,
		},
	});

	return (
		<Create isLoading={formLoading} saveButtonProps={saveButtonProps}>
			<CreateEditInstanceForm getInputProps={getInputProps} />
		</Create>
	);
};

export default InstanceCreate;
