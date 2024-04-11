import {
	IResourceComponentsProps,
	useGo,
	useResource,
	useShow,
	useToPath,
	useTranslate,
} from "@refinedev/core";
import {
	Show,
	TextField,
	NumberField,
	DateField,
	EditButtonProps,
	DeleteButtonProps,
	EditButton,
	DeleteButton,
} from "@refinedev/mantine";
import { Button, Group, Title } from "@mantine/core";
import { IconEye } from "@tabler/icons";

export const InstanceShow: React.FC<IResourceComponentsProps> = () => {
	const go = useGo();
	const translate = useTranslate();
	const { queryResult } = useShow();
	const { data, isLoading } = queryResult;

	const record = data?.data;

	const { resource, id: idFromParams, identifier } = useResource("instances");

	const goListPath = useToPath({
		resource,
		action: "list",
	});

	const editButtonProps: EditButtonProps = {
		...(isLoading ? { disabled: true } : {}),
		color: "primary",
		variant: "filled",
		resource: identifier,
		recordItemId: idFromParams,
	};
	const deleteButtonProps: DeleteButtonProps = {
		...(isLoading ? { disabled: true } : {}),
		resource: identifier,
		recordItemId: idFromParams,
		onSuccess: () => go({ to: goListPath }),
	};

	return (
		<Show isLoading={isLoading} canDelete={false} canEdit={false}>
			<Group>
				<Title my="xs" order={5}>
					{translate("instances.fields.name")}:
				</Title>
				<TextField value={record?.name} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("instances.fields.id")}:
				</Title>
				<NumberField value={record?.id ?? ""} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("instances.fields.environment_id")}:
				</Title>
				<TextField value={record?.environment_id} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("instances.fields.description")}:
				</Title>
				<TextField value={record?.description} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("instances.fields.days_until_pi_expiration")}:
				</Title>
				<NumberField value={record?.pi_deleted_after_days ?? ""} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("instances.fields.days_until_all_data_expiration")}:
				</Title>
				<NumberField value={record?.delete_after_days ?? ""} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("instances.fields.expected_usage")}:
				</Title>
				<TextField value={record?.expected_usage} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("instances.fields.created_at")}:
				</Title>
				<DateField value={record?.created_at} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("instances.fields.updated_at")}:
				</Title>
				<DateField value={record?.updated_at} />
			</Group>
			<Group className="mt-4 flex flex-col items-start gap-4">
				{record?.status !== "pending" && (
					<Button leftIcon={<IconEye />}>Go to Visualisation</Button>
				)}
				{record?.status !== "pending" && <EditButton {...editButtonProps} />}
				{record?.status !== "pending" && (
					<DeleteButton {...deleteButtonProps} />
				)}
			</Group>
		</Show>
	);
};

export default InstanceShow;
