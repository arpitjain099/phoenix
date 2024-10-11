/* eslint-disable @typescript-eslint/no-use-before-define */

"use client";

import { useCreate, useTranslate } from "@refinedev/core";
import { Create, useForm } from "@refinedev/mantine";
import { Title } from "@mantine/core";
import { useRouter, useParams } from "next/navigation";
import { useState } from "react";
import ApifyFacebookSearchPostsForm, {
	getPostValidationRules,
	initialFormValues,
} from "@components/forms/gather/apify_facebook_search_posts_form";
import { handleGatherSave } from "src/utils/constants";

export default function ApifyFacebookSearchPostCreate(): JSX.Element {
	const { mutate, isLoading: createResourceLoading } = useCreate();
	const translate = useTranslate();
	const router = useRouter();
	const { projectid } = useParams();
	const [proxyGroup, setProxyGroup] = useState("RESIDENTIAL");
	const [proxyCountry, setProxyCountry] = useState<string | null>("");
	const [inputList, setInputList] = useState<string[]>([]);
	const [formResetAfterCreateloading, setLoading] = useState<boolean>(false);

	const {
		getInputProps,
		saveButtonProps,
		values: formValues,
		isValid,
		validate,
		reset,
		refineCore: { formLoading },
	} = useForm({
		clearInputErrorOnChange: true,
		initialValues: initialFormValues,
		validate: (values) => getPostValidationRules(values, translate),
	});

	const handleSubmit = () => {
		const updatedFormValues = {
			...formValues,
			proxy: {
				use_apify_proxy: proxyGroup === "RESIDENTIAL",
				apify_proxy_groups: proxyGroup === "RESIDENTIAL" ? ["RESIDENTIAL"] : [],
				apify_proxy_country:
					proxyGroup === "RESIDENTIAL" && proxyCountry !== "anywhere"
						? proxyCountry
						: undefined,
			},
		};
		handleGatherSave(
			`projects/${projectid}/gathers/apify_facebook_search_posts`,
			`/projects/show/${projectid}?activeItem=gather`,
			isValid,
			projectid as string,
			setLoading,
			mutate,
			translate,
			updatedFormValues,
			setInputList,
			reset,
			router,
			validate
		);
	};

	return (
		<div className="form-wrapper">
			<Create
				breadcrumb={null}
				title={
					<Title order={3}>
						{translate("gathers.types.apify_facebook_search_posts.create")}
					</Title>
				}
				isLoading={
					formLoading || createResourceLoading || formResetAfterCreateloading
				}
				saveButtonProps={{
					...saveButtonProps,
					onClick: () => handleSubmit(),
				}}
			>
				<ApifyFacebookSearchPostsForm
					proxyGroup={proxyGroup}
					setProxyGroup={setProxyGroup}
					proxyCountry={proxyCountry}
					setProxyCountry={setProxyCountry}
					getInputProps={getInputProps}
				/>
			</Create>
		</div>
	);
}
