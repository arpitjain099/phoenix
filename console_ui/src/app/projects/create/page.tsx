"use client";

import CreateEditProjectForm from "@components/forms/create-edit-project";
import { useTranslate } from "@refinedev/core";
import { Create, useForm } from "@refinedev/mantine";
import React from "react";

export default function ProjectCreate(): JSX.Element {
	const translate = useTranslate();
	const {
		getInputProps,
		saveButtonProps,
		refineCore: { formLoading },
	} = useForm({
		initialValues: {
			name: "",
			description: "",
			environment_slug: "",
			pi_deleted_after_days: 90,
			delete_after_days: 90,
			expected_usage: "",
		},
		validate: {
			name: (value) =>
				value.length <= 0
					? translate("projects.fields.validation.required")
					: null,
			expected_usage: (value) =>
				value.length <= 0
					? translate("projects.fields.validation.required")
					: null,
			environment_slug: (value) =>
				value.length <= 0
					? translate("projects.fields.validation.required")
					: null,
			pi_deleted_after_days: (value) =>
				value === undefined
					? translate("projects.fields.validation.required")
					: value < 90 || value > 365
						? translate("projects.fields.validation.days_until_pi_expiration")
						: null,
			delete_after_days: (value) =>
				value === undefined
					? translate("projects.fields.validation.required")
					: value < 90 || value > 365
						? translate(
								"projects.fields.validation.days_until_all_data_expiration"
							)
						: null,
		},
	});

	return (
		<Create isLoading={formLoading} saveButtonProps={saveButtonProps}>
			<CreateEditProjectForm getInputProps={getInputProps} />
		</Create>
	);
}
