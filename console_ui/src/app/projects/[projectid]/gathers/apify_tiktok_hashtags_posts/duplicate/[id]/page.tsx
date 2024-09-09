/* eslint-disable @typescript-eslint/no-use-before-define */

"use client";

import { useCreate, useOne, useTranslate } from "@refinedev/core";
import { Create, useForm } from "@refinedev/mantine";
import { Title } from "@mantine/core";
import { useRouter, useParams } from "next/navigation";
import { useEffect, useState } from "react";
import ApifyTiktokHashtagsPostsForm, {
	getPostValidationRules,
	initialFormValues,
} from "@components/forms/gather/apify_tiktok_hashtags_posts_form";
import { handleGatherSave } from "src/utils/constants";

export default function ApifyTiktokHashtagsPostDuplicate(): JSX.Element {
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

	useEffect(() => {
		// Updating the "hashtag_list" with values from local state
		if (projectsData?.hashtag_list) {
			setInputList(projectsData.hashtag_list);
		}
		// Setting the value for "limit_posts_per_hashtag" with value from API call
		setFieldValue(
			"limit_posts_per_hashtag",
			projectsData?.limit_posts_per_hashtag
		);
		// Setting the value for "proxy_country_to_gather_from" with value from API call
		setFieldValue(
			"proxy_country_to_gather_from",
			projectsData?.proxy_country_to_gather_from
		);
	}, [projectsData, setFieldValue]);

	useEffect(() => {
		setFieldValue("hashtag_list", inputList);
	}, [inputList, setFieldValue]);

	return (
		<Create
			breadcrumb={null}
			title={
				<Title order={3}>
					{translate("gathers.types.apify_tiktok_hashtags_posts.create")}
				</Title>
			}
			isLoading={
				formLoading || createResourceLoading || formResetAfterCreateloading
			}
			saveButtonProps={{
				...saveButtonProps,
				onClick: () =>
					handleGatherSave(
						`projects/${projectid}/gathers/apify_tiktok_hashtags_posts`,
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
			<ApifyTiktokHashtagsPostsForm
				getInputProps={getInputProps}
				inputList={inputList}
				setInputList={setInputList}
			/>
		</Create>
	);
}
