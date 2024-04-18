import React from "react";
import { IResourceComponentsProps, useUpdate } from "@refinedev/core";
import { Edit, useForm } from "@refinedev/mantine";
import CreateEditProjectForm from "@components/forms/create-edit-project";

export const ProjectEdit: React.FC<IResourceComponentsProps> = () => {
	const { mutate } = useUpdate();
	const {
		getInputProps,
		saveButtonProps,
		values,
		refineCore: { queryResult },
	} = useForm({
		initialValues: {
			name: "",
			environment_slug: "",
			description: "",
			pi_deleted_after_days: "",
			delete_after_days: "",
			expected_usage: "",
		},
	});

	const projectsData = queryResult?.data?.data;

	const handleSave = async () => {
		if (projectsData?.id)
			mutate({
				resource: "projects",
				id: projectsData.id,
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
			<CreateEditProjectForm getInputProps={getInputProps} />
		</Edit>
	);
};

export default ProjectEdit;
