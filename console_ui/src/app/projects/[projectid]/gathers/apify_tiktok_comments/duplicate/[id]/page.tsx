"use client";

import { useCreate, useOne, useTranslate } from "@refinedev/core";
import { Create, useForm } from "@refinedev/mantine";
import { Title } from "@mantine/core";
import { useRouter, useParams } from "next/navigation";
import { useEffect, useState } from "react";
import ApifyFacebookPostsForm, {
	getCommentValidationRules,
	initialFormValues,
} from "@components/forms/gather/apify_tiktok_comments_form";
import { handleGatherSave } from "src/utils/constants";

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
		validate: (values) => getCommentValidationRules(values, translate),
	});

	const projectsData = data?.data;

	useEffect(() => {
		// Updating the "post_url_list" with values from local state
		if (projectsData?.post_url_list) {
			setInputList(projectsData.post_url_list);
		}
		// Setting the value for "limit_comments_per_post" with value from API call
		setFieldValue(
			"limit_comments_per_post",
			projectsData?.limit_comments_per_post
		);
		setFieldValue(
			"include_comment_replies",
			projectsData?.include_comment_replies
		);
	}, [projectsData, setFieldValue]);

	useEffect(() => {
		setFieldValue("post_url_list", inputList);
	}, [inputList, setFieldValue]);

	return (
		<Create
			breadcrumb={null}
			title={
				<Title order={3}>
					{translate("gathers.types.apify_tiktok_comments.create")}
				</Title>
			}
			isLoading={
				formLoading || createResourceLoading || formResetAfterCreateloading
			}
			saveButtonProps={{
				...saveButtonProps,
				onClick: () =>
					handleGatherSave(
						`projects/${projectid}/gathers/apify_tiktok_comments`,
						`/projects/show/${projectid}?activeItem=gather`,
						isValid,
						projectid as string,
						setLoading,
						mutate,
						translate,
						formValues,
						setInputList,
						reset,
						router,
						validate
					),
			}}
		>
			<ApifyFacebookPostsForm
				getInputProps={getInputProps}
				inputList={inputList}
				setInputList={setInputList}
			/>
		</Create>
	);
}
