/* eslint-disable @typescript-eslint/no-use-before-define */

"use client";

import { useParsed, useTranslate, useUpdate } from "@refinedev/core";
import { Edit, useForm } from "@refinedev/mantine";
import { Title } from "@mantine/core";
import { useRouter, useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { handleGatherSave } from "src/utils/constants";
import ApifyTiktokAccountsPostsForm, {
	getPostValidationRules,
	initialFormValues,
} from "@components/forms/gather/apify_tiktok_accounts_posts_form";

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
	const [formResetAfterEditloading, setLoading] = useState<boolean>(false);

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
		validate: (values) => getPostValidationRules(values, translate),
	});

	const projectsData = queryResult?.data?.data;

	useEffect(() => {
		// Updating the "account_username_list" with values from local state
		if (projectsData?.account_username_list) {
			setInputList(projectsData.account_username_list);
		}
		// Setting the value for "posts_created_after" with value from API call
		setFieldValue(
			"posts_created_after",
			projectsData?.posts_created_after
				? new Date(projectsData.posts_created_after)
				: null
		);
	}, [projectsData, setFieldValue]);

	useEffect(() => {
		setFieldValue("account_username_list", inputList);
	}, [inputList, setFieldValue]);

	return (
		<Edit
			breadcrumb={null}
			title={
				<Title order={3}>
					{translate("gathers.types.apify_tiktok_accounts_posts.edit")}
				</Title>
			}
			isLoading={
				formLoading || editResourceLoading || formResetAfterEditloading
			}
			headerButtons={() => null}
			saveButtonProps={{
				...saveButtonProps,
				onClick: () =>
					handleGatherSave(
						`projects/${projectid}/gathers/apify_tiktok_accounts_posts`,
						`/projects/${projectid}/gathers/${projectsData?.child_type}/${projectsData?.id}`,
						isValid,
						projectid as string,
						setLoading,
						mutate,
						translate,
						formValues,
						setInputList,
						reset,
						router,
						validate,
						projectsData?.id as string
					),
			}}
		>
			<ApifyTiktokAccountsPostsForm
				getInputProps={getInputProps}
				inputList={inputList}
				setInputList={setInputList}
			/>
		</Edit>
	);
}
