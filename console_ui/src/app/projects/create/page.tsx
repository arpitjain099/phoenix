"use client";

import CreateEditProjectForm from "@components/forms/create-edit-project";
import { Create, useForm } from "@refinedev/mantine";
import React from "react";

export default function ProjectCreate(): JSX.Element {
	const {
		getInputProps,
		saveButtonProps,
		refineCore: { formLoading },
	} = useForm({
		initialValues: {
			name: "",
			description: "",
			environment_slug: "",
			pi_deleted_after_days: 183,
			delete_after_days: 183,
			expected_usage: "",
		},
		validate: {
			name: (value) => (value.length <= 0 ? "Name is required" : null),
			expected_usage: (value) =>
				value.length <= 0 ? "Expected usage is required" : null,
			environment_slug: (value) =>
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
			<CreateEditProjectForm getInputProps={getInputProps} />
		</Create>
	);
}
