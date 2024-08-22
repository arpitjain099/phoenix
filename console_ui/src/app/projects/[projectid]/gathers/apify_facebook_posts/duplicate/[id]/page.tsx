/* eslint-disable @typescript-eslint/no-use-before-define */

"use client";

import { useCreate, useOne, useTranslate } from "@refinedev/core";
import { Create, useForm } from "@refinedev/mantine";
import { Title } from "@mantine/core";
import { useRouter, useParams } from "next/navigation";
import { useEffect, useState } from "react";
import ApifyFacebookPostsForm, {
	getPostValidationRules,
	initialFormValues,
} from "@components/forms/gather/apify_facebook_posts_form";

export default function ApifyFacebookPostDuplicate(): JSX.Element {
	const { mutate, isLoading: createResourceLoading } = useCreate();
	const translate = useTranslate();
	const router = useRouter();
	const { projectid, id } = useParams();
	const [inputList, setInputList] = useState<string[]>([]);
	const [formResetAfterCreateloading, setLoading] = useState<boolean>(false);
	const { data } = useOne({
		resource: `projects/${projectid}/gathers`,
		id: id as string,
	});

	const {
		getInputProps,
		saveButtonProps,
		values: formValues,
		setFieldValue,
		isValid,
		validate,
		reset,
		refineCore: { formLoading },
	} = useForm({
		clearInputErrorOnChange: true,
		initialValues: initialFormValues,
		validate: (values) => getPostValidationRules(values, translate),
	});

	const projectsData = data?.data;

	const handleSave = async () => {
		if (isValid()) {
			if (projectid) {
				setLoading(true);
				mutate(
					{
						resource: `projects/${projectid}/gathers/apify_facebook_posts`,
						values: formValues,
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
						onError: () => {
							setLoading(false);
						},
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
			"limit_posts_per_account",
			projectsData?.limit_posts_per_account
		);
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
		<Create
			breadcrumb={null}
			title={
				<Title order={3}>
					{translate("gathers.types.apify_facebook_posts.create")}
				</Title>
			}
			isLoading={
				formLoading || createResourceLoading || formResetAfterCreateloading
			}
			saveButtonProps={{ ...saveButtonProps, onClick: handleSave }}
		>
			<ApifyFacebookPostsForm
				getInputProps={getInputProps}
				inputList={inputList}
				setInputList={setInputList}
			/>
		</Create>
	);
}
