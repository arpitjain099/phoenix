import React from "react";
import { IResourceComponentsProps, useUpdate } from "@refinedev/core";
import { Edit, useForm } from "@refinedev/mantine";
import CreateEditInstanceForm from "@components/forms/create_edit_instance";

export const InstanceEdit: React.FC<IResourceComponentsProps> = () => {
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
		<Edit
			saveButtonProps={{ ...saveButtonProps, onClick: handleSave }}
			canDelete={false}
		>
			<CreateEditInstanceForm getInputProps={getInputProps} />
		</Edit>
	);
};

export default InstanceEdit;
