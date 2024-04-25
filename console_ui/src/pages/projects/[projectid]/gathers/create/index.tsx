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
import CreateCommentsGatherForm from "@components/forms/gather/create-comments-gather";
import CreatePostsGatherForm from "@components/forms/gather/create-posts-gather";
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

	const {
		getInputProps,
		saveButtonProps,
		values,
		setFieldValue,
		validate,
		isValid,
		reset,
		refineCore: { formLoading },
	} = useForm({
		initialValues: {
			source: "apify",
			platform: "facebook",
			project_id: Number(projectid),
			data_type: "",
			description: "",
			input: {
				type: "author_url_list",
				data: [] as string[],
			},
			start_date: today,
			end_date: tomorrow,
			limit_posts_per_account: 1000,
			limit_comments_per_post: 1000,
			comment_replies: false,
			sort_comments_by: "facebook_defaults",
		},
		validate: {
			source: (value) => (value.length <= 0 ? "Required" : null),
			platform: (value) => (value.length <= 0 ? "Required" : null),
			data_type: (value) => (value.length <= 0 ? "Required" : null),
			input: {
				type: (value) => (value.length <= 0 ? "Required" : null),
				data: (value) => (value.length <= 0 ? "Required" : null),
			},
			start_date: (value) => {
				if (values.data_type === "posts" && !value) return "Required";
				if (values.data_type === "posts") {
					const startDate = new Date(value);
					const endDate = new Date(values.end_date);
					if (startDate > today) return "Start date cannot be in the future";
					if (startDate > endDate) return "Start date cannot be after end date";
				}
				return null;
			},
			end_date: (value) => {
				if (values.data_type === "posts" && !value) return "Required";
				if (values.data_type === "posts") {
					const endDate = new Date(value);
					const startDate = new Date(values.start_date);
					if (endDate < startDate)
						return "End date cannot be before start date";
				}
				return null;
			},
			limit_posts_per_account: (value) => {
				if (values.data_type === "posts" && value === undefined)
					return "Required";
				return null;
			},
			limit_comments_per_post: (value) => {
				if (values.data_type === "comments" && value === undefined)
					return "Required";
				return null;
			},
			sort_comments_by: (value) => {
				if (values.data_type === "posts" && !value) return "Required";
				return null;
			},
		},
	});

	const { selectProps: projectSelectProps } = useSelect({
		resource: "projects",
		optionLabel: "name",
		optionValue: "id",
		defaultValue: Number(projectid),
	});

	const handleSave = async () => {
		if (isValid()) {
			if (values.project_id) {
				const { source, ...filteredValues } = values; // Exclude 'source' from values
				if (source === "apify") {
					if (values.data_type === "posts") {
						const {
							limit_comments_per_post,
							comment_replies,
							sort_comments_by,
							...data
						} = filteredValues; // Exclude attributes for data_type=comment from values
						mutate(
							{
								resource: `projects/${values.project_id}/gathers/apify`,
								values: data,
							},
							{
								onSuccess: async () => {
									await Promise.all([setInputList([]), reset()]);
									setTimeout(() => {
										router.push(`/projects/${values.project_id}/gathers`);
									}, 2000);
								},
							}
						);
					} else if (values.data_type === "comments") {
						const { start_date, end_date, limit_posts_per_account, ...data } =
							filteredValues; // Exclude attributes for data_type=posts from values
						mutate(
							{
								resource: `projects/${values.project_id}/gathers/apify`,
								values: data,
							},
							{
								onSuccess: async () => {
									await Promise.all([setInputList([]), reset()]);
									setTimeout(() => {
										router.push(`/projects/${values.project_id}/gathers`);
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
		setFieldValue("input.data", inputList);
	}, [inputList, setFieldValue]);

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
			{values.data_type === "posts" && (
				<CreatePostsGatherForm getInputProps={getInputProps} />
			)}
			{values.data_type === "comments" && (
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
			/>
		</Create>
	);
};

export default GatherCreate;
