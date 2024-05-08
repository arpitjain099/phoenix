/* eslint-disable @typescript-eslint/no-use-before-define */
/* eslint-disable @typescript-eslint/no-unused-vars */
import {
	IResourceComponentsProps,
	useCreate,
	useTranslate,
} from "@refinedev/core";
import { Create, useForm, useSelect } from "@refinedev/mantine";
import { Select, Textarea, Tooltip } from "@mantine/core";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { IconInfoCircle } from "@tabler/icons";
import GatherInputs from "@components/inputs/gather-inputs";
import CreateCommentsGatherForm, {
	getCommentValidationRules,
} from "@components/forms/gather/create-comments-gather";
import CreatePostsGatherForm, {
	getPostValidationRules,
} from "@components/forms/gather/create-posts-gather";
import BreadcrumbsComponent from "@components/breadcrumbs";

export const GatherCreate: React.FC<IResourceComponentsProps> = () => {
	const today = new Date();
	const tomorrow = new Date(today);
	tomorrow.setDate(tomorrow.getDate() + 1);
	const { mutate } = useCreate();
	const translate = useTranslate();
	const router = useRouter();
	const { projectid } = router.query;
	const [inputList, setInputList] = useState<string[]>([]);

	const breadcrumbs = [
		{ title: translate("projects.projects"), href: "/projects" },
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
		input: {
			type: "",
			data: [] as string[],
		},
		start_date: today,
		end_date: tomorrow,
		limit_posts_per_account: 1000,
		limit_comments_per_post: 1000,
		comment_replies: false,
		sort_comments_by: "facebook_defaults",
	};

	const {
		getInputProps,
		saveButtonProps,
		values: formValues,
		setFieldValue,
		validate,
		isValid,
		errors,
		reset,
		refineCore: { formLoading },
	} = useForm({
		clearInputErrorOnChange: true,
		initialValues: initialFormValues,
		validate: (values) => getValidationRules(values),
	});

	// Define separate validation rules based on data type
	function getValidationRules(values: any): any {
		const commonRules = {
			source: values.source.length <= 0 ? "Required" : null,
			platform: values.platform.length <= 0 ? "Required" : null,
			data_type: values.data_type.length <= 0 ? "Required" : null,
			input:
				values.input.type.length > 0 && values.input.data.length > 0
					? null
					: {
							type: values.input.type.length <= 0 ? "Required" : null,
							data: values.input.data.length <= 0 ? "Required" : null,
						},
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
				const { source, ...filteredValues } = formValues; // Exclude 'source' from values
				if (source === "apify") {
					if (formValues.data_type === "posts") {
						const {
							limit_comments_per_post,
							comment_replies,
							sort_comments_by,
							...data
						} = filteredValues; // Exclude attributes for data_type=comment from values
						mutate(
							{
								resource: `projects/${formValues.project_id}/gathers/apify`,
								values: data,
							},
							{
								onSuccess: async () => {
									await Promise.all([setInputList([]), reset()]);
									setTimeout(() => {
										router.push(`/projects/${formValues.project_id}/gathers`);
									}, 2000);
								},
							}
						);
					} else if (formValues.data_type === "comments") {
						const { start_date, end_date, limit_posts_per_account, ...data } =
							filteredValues; // Exclude attributes for data_type=posts from values
						mutate(
							{
								resource: `projects/${formValues.project_id}/gathers/apify`,
								values: data,
							},
							{
								onSuccess: async () => {
									await Promise.all([setInputList([]), reset()]);
									setTimeout(() => {
										router.push(`/projects/${formValues.project_id}/gathers`);
									}, 2000);
								},
							}
						);
					}
				}
			}
		} else {
			validate();
		}
	};

	useEffect(() => {
		if (formValues.data_type === "posts") {
			setFieldValue("input.type", "account_url_list");
		}
		if (formValues.data_type === "comments") {
			setFieldValue("input.type", "post_url_list");
		}
	}, [formValues.data_type, setFieldValue]);

	useEffect(() => {
		setFieldValue("input.data", inputList);
	}, [inputList, setFieldValue]);

	useEffect(() => {
		setFieldValue("project_id", Number(projectid));
	}, [projectid, setFieldValue]);

	return (
		<Create
			breadcrumb={<BreadcrumbsComponent breadcrumbs={breadcrumbs} />}
			isLoading={formLoading}
			saveButtonProps={{ ...saveButtonProps, onClick: handleSave }}
		>
			<Select
				mt="lg"
				withAsterisk
				label={translate("gathers.fields.source")}
				data={[
					{ label: translate("inputs.select"), value: "" },
					{ label: "Apify", value: "apify" },
				]}
				{...getInputProps("source")}
			/>
			<Select
				mt="lg"
				withAsterisk
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
						<span className="text-red-500 ml-1">*</span>
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
				withAsterisk
				label={translate("gathers.fields.project_id")}
				{...getInputProps("project_id")}
				{...projectSelectProps}
			/>
			{formValues.data_type === "posts" && (
				<CreatePostsGatherForm getInputProps={getInputProps} />
			)}
			{formValues.data_type === "comments" && (
				<CreateCommentsGatherForm getInputProps={getInputProps} />
			)}
			<Textarea
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.info.description")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.description")}
					</div>
				}
				{...getInputProps("description")}
			/>
			<GatherInputs
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.input.data_placeholder")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.input.data")}
						<span className="text-red-500 ml-1">*</span>
						{inputList.length > 0 && (
							<span className="italic ml-10">
								{inputList.length} input value{inputList.length > 1 && "s"}
							</span>
						)}
					</div>
				}
				placeholder={translate("gathers.fields.input.data_placeholder")}
				data={inputList}
				setData={setInputList}
				{...getInputProps("input.data")}
				error={(errors?.input as { data?: string })?.data}
			/>
		</Create>
	);
};

export default GatherCreate;
