/* eslint-disable @typescript-eslint/no-use-before-define */

"use client";

import { useCreate, useTranslate } from "@refinedev/core";
import { Create, useForm } from "@refinedev/mantine";
import { Title } from "@mantine/core";
import { useRouter, useParams } from "next/navigation";
import { useEffect, useState } from "react";
import ApifyFacebookPostsForm, {
	getPostValidationRules,
	initialFormValues,
} from "@components/forms/gather/apify_facebook_posts_form";
import { handleGatherSave } from "src/utils/constants";

export default function ApifyFacebookPostCreate(): JSX.Element {
	const { mutate, isLoading: createResourceLoading } = useCreate();
	const translate = useTranslate();
	const router = useRouter();
	const { projectid } = useParams();
	const [inputList, setInputList] = useState<string[]>([]);
	const [formResetAfterCreateloading, setLoading] = useState<boolean>(false);

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

	useEffect(() => {
		// Updating the "account_url_list" with values from local state
		setFieldValue("account_url_list", inputList);
	}, [inputList, setFieldValue]);

	return (
		<div className="form-wrapper">
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
				saveButtonProps={{
					...saveButtonProps,
					onClick: () =>
						handleGatherSave(
							`projects/${projectid}/gathers/apify_facebook_posts`,
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
		</div>
	);
}
