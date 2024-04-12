import CreateEditInstanceForm from "@components/forms/create_edit_instance";
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
			<CreateEditInstanceForm getInputProps={getInputProps} />
		</Create>
	);
};

export default InstanceCreate;
