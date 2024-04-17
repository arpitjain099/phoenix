import {
	IResourceComponentsProps,
	useCreate,
	useTranslate,
} from "@refinedev/core";
import { Create, useForm, useSelect } from "@refinedev/mantine";
import {
	Select,
	NumberInput,
	Textarea,
	Tooltip,
	Group,
	Anchor,
	Breadcrumbs,
} from "@mantine/core";
import { DatePicker } from "@mantine/dates";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import GatherInputs from "@components/gather-inputs";
import { IconInfoCircle } from "@tabler/icons";

const breadcrumbs = [
	{ title: "Instances", href: "/instances" },
	{ title: "Gathers", href: "../gathers" },
	{ title: "Create", href: "create" },
].map((item) => (
	<Group key={item.title}>
		<Anchor color="gray" size="sm" href={item.href}>
			{item.title}
		</Anchor>
	</Group>
));

export const GatherCreate: React.FC<IResourceComponentsProps> = () => {
	const today = new Date();
	const tomorrow = new Date(today);
	tomorrow.setDate(tomorrow.getDate() + 1);
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
			start_date: today,
			end_date: tomorrow,
			platform: "facebook",
			data_type: "",
			input: {
				type: "author_url_list",
				data: [] as string[],
			},
			instance_id: Number(instanceid),
			limit_messages: 1000,
		},
		validate: {
			data_type: (value) => (value.length <= 0 ? "Required" : null),
			platform: (value) => (value.length <= 0 ? "Required" : null),
			start_date: (value) => {
				if (!value) return "Start date is required";
				const startDate = new Date(value);
				const endDate = new Date(values.end_date);
				if (startDate > today) return "Start date cannot be in the future";
				if (startDate > endDate) return "Start date cannot be after end date";
				return null;
			},
			end_date: (value) => {
				if (!value) return "End date is required";
				const endDate = new Date(value);
				const startDate = new Date(values.start_date);
				if (endDate < startDate) return "End date cannot be before start date";
				return null;
			},
			limit_messages: (value) => (value === undefined ? "Required" : null),
			input: {
				type: (value) => (value.length <= 0 ? "Required" : null),
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
						onSuccess: async () => {
							await Promise.all([setInputList([]), reset()]);
							setTimeout(() => {
								router.push(`/instances/${values.instance_id}/gathers`);
							}, 2000);
						},
					}
				);
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
			breadcrumb={<Breadcrumbs>{breadcrumbs}</Breadcrumbs>}
			isLoading={formLoading}
			saveButtonProps={{ ...saveButtonProps, onClick: handleSave }}
		>
			<Select
				mt="sm"
				withAsterisk
				label={translate("gathers.fields.platform")}
				data={[
					{ label: translate("inputs.select"), value: "" },
					{ label: "Facebook", value: "facebook" },
				]}
				{...getInputProps("platform")}
			/>
			<Select
				mt="sm"
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
				]}
			/>
			<Select
				mt="sm"
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.info.input.type")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.input.type")}
						<span className="text-red-500 ml-1">*</span>
					</div>
				}
				data={[
					{ label: translate("inputs.select"), value: "" },
					{ label: "Accounts List", value: "author_url_list" },
				]}
				{...getInputProps("input.type")}
			/>
			<GatherInputs
				required
				label={translate("gathers.fields.input.data")}
				placeholder={translate("gathers.fields.input.data_placeholder")}
				data={inputList}
				setData={setInputList}
				{...getInputProps("input.data")}
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
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.info.start_date")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.start_date")}
						<span className="text-red-500 ml-1">*</span>
					</div>
				}
				{...getInputProps("start_date")}
			/>
			<DatePicker
				mt="sm"
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.info.end_date")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.end_date")}
						<span className="text-red-500 ml-1">*</span>
					</div>
				}
				{...getInputProps("end_date")}
			/>
			<NumberInput
				mt="sm"
				label={
					<div className="flex items-center">
						<Tooltip label={translate("gathers.fields.info.limit_messages")}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{translate("gathers.fields.limit_messages")}
						<span className="text-red-500 ml-1">*</span>
					</div>
				}
				{...getInputProps("limit_messages")}
			/>
			<Textarea
				mt="sm"
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
		</Create>
	);
};

export default GatherCreate;
