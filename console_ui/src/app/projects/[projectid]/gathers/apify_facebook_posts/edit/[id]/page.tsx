/* eslint-disable @typescript-eslint/no-use-before-define */

"use client";

import { useParsed, useTranslate, useUpdate } from "@refinedev/core";
import { Edit, useForm } from "@refinedev/mantine";
import { Title } from "@mantine/core";
import { useRouter, useParams } from "next/navigation";
import { useEffect, useState } from "react";
import BreadcrumbsComponent from "@components/breadcrumbs";
import ApifyFacebookPostsForm, {
	getPostValidationRules,
	initialFormValues,
} from "@components/forms/gather/apify_facebook_posts_form";

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

	const {
		getInputProps,
		saveButtonProps,
		values: formValues,
		setFieldValue,
		isValid,
		validate,
		refineCore: { formLoading, queryResult },
	} = useForm({
		refineCoreProps: {
			resource: `projects/${projectid}/gathers`,
			action: "edit",
			id,
		},
		clearInputErrorOnChange: true,
		initialValues: initialFormValues,
		validate: (values) => getPostValidationRules(values, translate),
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
							setTimeout(() => {
								router.push(
									`/projects/${projectid}/gathers/${projectsData?.child_type}/${projectsData?.id}`
								);
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
		setFieldValue(
			"posts_created_before",
			new Date(projectsData?.posts_created_before)
		);
		setFieldValue(
			"posts_created_after",
			new Date(projectsData?.posts_created_after)
		);
	}, [projectsData, setFieldValue]);

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
			<ApifyFacebookPostsForm
				getInputProps={getInputProps}
				inputList={inputList}
				setInputList={setInputList}
			/>
		</Edit>
	);
}
