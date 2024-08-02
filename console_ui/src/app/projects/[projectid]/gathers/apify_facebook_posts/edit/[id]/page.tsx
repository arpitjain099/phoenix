/* eslint-disable @typescript-eslint/no-use-before-define */

"use client";

import { useParsed, useTranslate, useUpdate } from "@refinedev/core";
import { Edit, TextField, useForm } from "@refinedev/mantine";
import { NumberInput, TextInput, Title, Tooltip } from "@mantine/core";
import { useRouter, useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { IconInfoCircle } from "@tabler/icons";
import BreadcrumbsComponent from "@components/breadcrumbs";
import { DatePicker } from "@mantine/dates";
import GatherInputs from "@components/inputs/gather-inputs";

export default function ApifyFacebookPostEdit(): JSX.Element {
	const today = new Date();
	const tomorrow = new Date(today);
	tomorrow.setDate(tomorrow.getDate() + 1);
	const { mutate, isLoading: editResourceLoading } = useUpdate();
	const translate = useTranslate();
	const router = useRouter();
	const { projectid } = useParams();
	const { id } = useParsed();
	const [inputList, setInputList] = useState<string[]>([]);

	const breadcrumbs = [
		{ title: translate("projects.projects"), href: "/projects" },
		{
			title: projectid as string,
			href: `/projects/show/${projectid}`,
			replaceWithProjectName: true,
		},
		{
			title: translate("gathers.gathers"),
			href: `/projects/show/${projectid}?activeItem=gather`,
		},
		{ title: translate("actions.edit"), href: "" },
	];

	const initialFormValues = {
		name: "",
		limit_posts_per_account: 1000,
		account_url_list: [] as string[],
		only_posts_older_than: today,
		only_posts_newer_than: tomorrow,
	};

	const {
		getInputProps,
		saveButtonProps,
		values: formValues,
		setFieldValue,
		isValid,
		validate,
		reset,
		refineCore: { formLoading, queryResult },
	} = useForm({
		refineCoreProps: {
			resource: `projects/${projectid}/gathers`,
			action: "edit",
			id,
		},
		clearInputErrorOnChange: true,
		initialValues: initialFormValues,
		validate: {
			name: (value) => (value.length <= 0 ? "Required" : null),
			only_posts_older_than: (value) => {
				if (!value) return "Required";
				const startDate = new Date(value);
				const endDate = new Date(formValues.only_posts_newer_than);
				if (startDate > today) return "Start date cannot be in the future";
				if (startDate > endDate) return "Start date cannot be after end date";
				return null;
			},
			only_posts_newer_than: (value) => {
				if (!value) return "End date is required";
				const endDate = new Date(value);
				const startDate = new Date(formValues.only_posts_older_than);
				if (endDate < startDate) return "End date cannot be before start date";
				return null;
			},
			limit_posts_per_account: (value) =>
				value === undefined ? "Required" : null,
			account_url_list: (value) => (value.length <= 0 ? "Required" : null),
		},
	});

	const projectsData = queryResult?.data?.data;

	const handleSave = async () => {
		if (isValid()) {
			if (projectid && projectsData?.id) {
				mutate(
					{
						resource: `projects/${projectid}/gathers/apify_facebook_posts`,
						id: projectsData.id,
						values: formValues,
						meta: {
							method: "patch",
						},
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
								router.push(`/projects/show/${projectid}?activeItem=gather`);
							}, 1000);
						},
						onError: () => {},
					}
				);
			}
		} else {
			validate();
		}
	};

	useEffect(() => {
		if (projectsData?.account_url_list) {
			setInputList(projectsData.account_url_list);
		}
	}, [projectsData]);

	useEffect(() => {
		setFieldValue("account_url_list", inputList);
	}, [inputList, setFieldValue]);

	return (
		<Edit
			breadcrumb={
				<BreadcrumbsComponent
					breadcrumbs={breadcrumbs}
					projectid={projectid as string}
				/>
			}
			title={
				<Title order={3}>
					{translate("gathers.types.apify_facebook_posts.edit")}
				</Title>
			}
			isLoading={formLoading || editResourceLoading}
			headerButtons={() => null}
			saveButtonProps={{ ...saveButtonProps, onClick: handleSave }}
		>
			<TextField
				value={translate("gathers.types.apify_facebook_posts.edit_description")}
			/>
			<TextInput
				mt="sm"
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.info.name")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.input.name")}
					</div>
				}
				{...getInputProps("name")}
			/>
			<DatePicker
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate("gathers.fields.info.only_posts_older_than")}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.only_posts_older_than")}
					</div>
				}
				{...getInputProps("only_posts_older_than")}
			/>
			<DatePicker
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate("gathers.fields.info.only_posts_newer_than")}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.only_posts_newer_than")}
					</div>
				}
				{...getInputProps("only_posts_newer_than")}
			/>
			<NumberInput
				mt="lg"
				label={
					<div className="flex items-center">
						<Tooltip
							label={translate("gathers.fields.info.limit_posts_per_account")}
						>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.limit_posts_per_account")}
					</div>
				}
				{...getInputProps("limit_posts_per_account")}
			/>
			<GatherInputs
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.input.data_placeholder")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.input.facebook_account_url_list")}
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
				{...getInputProps("account_url_list")}
			/>
		</Edit>
	);
}
