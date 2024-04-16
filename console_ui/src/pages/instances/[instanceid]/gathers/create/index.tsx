import {
	IResourceComponentsProps,
	useCreate,
	useTranslate,
} from "@refinedev/core";
import { Create, useForm, useSelect } from "@refinedev/mantine";
import { Select, NumberInput, Checkbox, Textarea } from "@mantine/core";
import { DatePicker } from "@mantine/dates";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import GatherInputs from "@components/gather-inputs";

export const GatherCreate: React.FC<IResourceComponentsProps> = () => {
	const { mutate } = useCreate();
	const translate = useTranslate();
	const router = useRouter();
	const { instanceid } = router.query;
	const [inputList, setInputList] = useState<string[]>([]);
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
			description: "",
			start_date: "",
			end_date: "",
			platform: "facebook",
			data_type: "",
			input: {
				type: "author_url_list",
				data: [] as string[],
			},
			instance_id: Number(instanceid),
			limit_messages: 1000,
			limit_replies: 100,
			nested_replies: false,
		},
		validate: {
			data_type: (value) => (value.length <= 0 ? "Required" : null),
			platform: (value) => (value.length <= 0 ? "Required" : null),
			start_date: (value) => (value.length <= 0 ? "Required" : null),
			end_date: (value) => (value.length <= 0 ? "Required" : null),
			limit_messages: (value) => (value === undefined ? "Required" : null),
			limit_replies: (value) => (value === undefined ? "Required" : null),
			input: {
				data: (value) => (value.length <= 0 ? "Required" : null),
			},
		},
	});

	const { selectProps: instanceSelectProps } = useSelect({
		resource: "instances",
		optionLabel: "name",
		optionValue: "id",
		defaultValue: Number(instanceid),
	});

	const handleSave = async () => {
		if (isValid()) {
			if (values.instance_id) {
				mutate(
					{
						resource: `instances/${values.instance_id}/gathers/apify`,
						values,
					},
					{
						onSuccess: () => {
							reset();
						},
					}
				);
			}
		} else {
			validate();
		}
	};

	useEffect(() => {
		const input = {
			type: "author_url_list",
			data: inputList,
		};
		setFieldValue("input", input);
	}, [inputList, setFieldValue]);

	return (
		<Create
			isLoading={formLoading}
			saveButtonProps={{ ...saveButtonProps, onClick: handleSave }}
		>
			<Select
				mt="sm"
				withAsterisk
				label={translate("gathers.fields.platform")}
				{...getInputProps("platform")}
				data={[
					{ label: translate("inputs.select"), value: "" },
					{ label: "Facebook", value: "facebook" },
				]}
			/>
			<Select
				mt="sm"
				withAsterisk
				label={translate("gathers.fields.data_type")}
				{...getInputProps("data_type")}
				data={[
					{ label: translate("inputs.select"), value: "" },
					{ label: "Posts", value: "posts" },
					{ label: "Messages", value: "messages" },
				]}
			/>
			<GatherInputs
				required
				label={translate("gathers.fields.inputs.title")}
				placeholder={translate("gathers.fields.inputs.placeholder")}
				data={inputList}
				setData={setInputList}
			/>
			<Select
				mt="sm"
				disabled
				withAsterisk
				label={translate("gathers.fields.instance_id")}
				{...getInputProps("instance_id")}
				{...instanceSelectProps}
			/>
			<DatePicker
				mt="sm"
				withAsterisk
				label={translate("gathers.fields.start_date")}
				{...getInputProps("start_date")}
			/>
			<DatePicker
				mt="sm"
				withAsterisk
				label={translate("gathers.fields.end_date")}
				{...getInputProps("end_date")}
			/>
			<Textarea
				mt="sm"
				label={translate("gathers.fields.description")}
				{...getInputProps("description")}
			/>
			<NumberInput
				mt="sm"
				label={translate("gathers.fields.limit_messages")}
				{...getInputProps("limit_messages")}
			/>
			<NumberInput
				mt="sm"
				label={translate("gathers.fields.limit_replies")}
				{...getInputProps("limit_replies")}
			/>
			<Checkbox
				mt="sm"
				label={translate("gathers.fields.nested_replies")}
				{...getInputProps("nested_replies", { type: "checkbox" })}
			/>
		</Create>
	);
};

export default GatherCreate;
