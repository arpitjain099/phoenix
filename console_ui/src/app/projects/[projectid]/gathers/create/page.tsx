"use client";

import { useCreate, useTranslate } from "@refinedev/core";
import { Create, useForm, useSelect } from "@refinedev/mantine";
import { Select, Textarea, Tooltip } from "@mantine/core";
import { useRouter, useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { IconInfoCircle } from "@tabler/icons";
import CreateCommentsGatherForm, {
	commentFieldsToKeep,
	getCommentValidationRules,
} from "@components/forms/gather/create-comments-gather";
import CreatePostsGatherForm, {
	getPostValidationRules,
	postFieldsToKeep,
} from "@components/forms/gather/create-posts-gather";
import BreadcrumbsComponent from "@components/breadcrumbs";

export default function GatherCreate(): JSX.Element {
	const today = new Date();
	const tomorrow = new Date(today);
	tomorrow.setDate(tomorrow.getDate() + 1);
	const { mutate, isLoading: createResourceLoading } = useCreate();
	const translate = useTranslate();
	const router = useRouter();
	const { projectid } = useParams();
	const [inputList, setInputList] = useState<string[]>([]);
	const [formResetAfterCreateloading, setLoading] = useState<boolean>(false);

	const breadcrumbs = [
		{ title: translate("projects.projects"), href: "/projects" },
		{
			title: projectid as string,
			href: `/projects/show/${projectid}`,
			replaceWithProjectName: true,
		},
		{ title: translate("gathers.gathers"), href: "../gathers" },
		{ title: translate("actions.create"), href: "create" },
	];

	// Define initial values for useForm hook
	const initialFormValues = {
		source: "apify",
		platform: "facebook",
		project_id: Number(projectid),
		data_type: "",
		description: "",
		account_url_list: [] as string[],
		only_posts_older_than: today,
		only_posts_newer_than: tomorrow,
		limit_posts_per_account: 1000,
		limit_comments_per_post: 1000,
		include_comment_replies: false,
		sort_comments_by: "facebook_defaults",
		post_url_list: [] as string[],
	};

	const {
		getInputProps,
		saveButtonProps,
		values: formValues,
		setFieldValue,
		validate,
		isValid,
		reset,
		refineCore: { formLoading },
	} = useForm({
		clearInputErrorOnChange: true,
		initialValues: initialFormValues,
		// validate: (values) => getValidationRules(values),
	});

	// Define separate validation rules based on data type
	function getValidationRules(values: any): any {
		const commonRules = {
			source: values.source.length <= 0 ? "Required" : null,
			platform: values.platform.length <= 0 ? "Required" : null,
			data_type: values.data_type.length <= 0 ? "Required" : null,
		};
		if (values && values.data_type === "posts") {
			return {
				...commonRules,
				...getPostValidationRules(values, today),
			};
		}
		if (values && values.data_type === "comments") {
			return {
				...commonRules,
				...getCommentValidationRules(values),
			};
		}
		return commonRules;
	}

	const { selectProps: projectSelectProps } = useSelect({
		resource: "projects",
		optionLabel: "name",
		optionValue: "id",
		defaultValue: Number(projectid),
	});

	const handleSave = async () => {
		if (isValid()) {
			if (formValues.project_id) {
				const { source } = formValues; // Exclude 'source' from values
				if (source === "apify") {
					// Define the list of fields to keep based on data_type
					let fieldsToKeep: string[] = [];
					if (formValues.data_type === "posts") {
						fieldsToKeep = [...postFieldsToKeep];
					} else if (formValues.data_type === "comments") {
						fieldsToKeep = [...commentFieldsToKeep];
					}
					// Filter out unnecessary fields
					const filteredRequiredFields = Object.fromEntries(
						Object.entries(formValues).filter(([key, _]) =>
							fieldsToKeep.includes(key)
						)
					);
					setLoading(true);
					mutate(
						{
							resource: `projects/${formValues.project_id}/gathers/${formValues.source}_${formValues.platform}_${formValues.data_type}`,
							values: filteredRequiredFields,
							errorNotification: (res) => {
								let message = "Something went wrong while creating";
								if (res?.response?.data?.detail[0]?.msg) {
									message = res.response.data.detail[0].msg;
								}
								return {
									message,
									description: "Error",
									type: "error",
								};
							},
						},
						{
							onSuccess: async () => {
								await Promise.all([setInputList([]), reset()]);
								setTimeout(() => {
									router.push(`/projects/${formValues.project_id}/gathers`);
								}, 1000);
							},
							onError: () => {
								setLoading(false);
							},
						}
					);
				}
			}
		} else {
			validate();
		}
	};

	useEffect(() => {
		if (formValues.data_type === "posts") {
			setFieldValue("account_url_list", inputList);
		}
		if (formValues.data_type === "comments") {
			setFieldValue("post_url_list", inputList);
		}
	}, [formValues.data_type, inputList, setFieldValue]);

	useEffect(() => {
		setFieldValue("project_id", Number(projectid));
	}, [projectid, setFieldValue]);

	return (
		<Create
			breadcrumb={
				<BreadcrumbsComponent
					breadcrumbs={breadcrumbs}
					projectid={projectid as string}
				/>
			}
			isLoading={
				formLoading || createResourceLoading || formResetAfterCreateloading
			}
			saveButtonProps={{ ...saveButtonProps, onClick: handleSave }}
		>
			<Select
				mt="lg"
				label={translate("gathers.fields.source")}
				data={[
					{ label: translate("inputs.select"), value: "" },
					{ label: "Apify", value: "apify" },
				]}
				{...getInputProps("source")}
			/>
			<Select
				mt="lg"
				label={translate("gathers.fields.platform")}
				data={[
					{ label: translate("inputs.select"), value: "" },
					{ label: "Facebook", value: "facebook" },
				]}
				{...getInputProps("platform")}
			/>
			<Select
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.info.data_type")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.data_type")}
					</div>
				}
				{...getInputProps("data_type")}
				data={[
					{ label: translate("inputs.select"), value: "" },
					{ label: "Posts", value: "posts" },
					{ label: "Comments", value: "comments" },
				]}
			/>
			<Select
				mt="lg"
				disabled
				label={translate("gathers.fields.project_id")}
				{...getInputProps("project_id")}
				{...projectSelectProps}
			/>
			<Textarea
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.info.description")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.input.description")}
					</div>
				}
				{...getInputProps("description")}
			/>
			{formValues.data_type === "posts" && (
				<CreatePostsGatherForm
					getInputProps={getInputProps}
					inputList={inputList}
					setInputList={setInputList}
				/>
			)}
			{formValues.data_type === "comments" && (
				<CreateCommentsGatherForm
					getInputProps={getInputProps}
					inputList={inputList}
					setInputList={setInputList}
				/>
			)}
		</Create>
	);
}
