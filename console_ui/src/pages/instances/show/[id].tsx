import {
	IResourceComponentsProps,
	useResource,
	useShow,
	useTranslate,
} from "@refinedev/core";
import {
	Show,
	TextField,
	NumberField,
	DateField,
	EditButtonProps,
	EditButton,
} from "@refinedev/mantine";
import { Button, Group, Title } from "@mantine/core";
import { IconEye } from "@tabler/icons";
import Link from "next/link";

export const InstanceShow: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const { queryResult } = useShow();
	const { data, isLoading } = queryResult;

	const record = data?.data;

	const { id: idFromParams, identifier } = useResource("instances");

	const editButtonProps: EditButtonProps = {
		...(isLoading ? { disabled: true } : {}),
		color: "primary",
		variant: "filled",
		resource: identifier,
		recordItemId: idFromParams,
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
					{translate("instances.fields.environment_slug")}:
				</Title>
				<TextField value={record?.environment_slug} />
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
					{translate("instances.fields.expected_usage.title")}:
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
				<Link
					href={{
						pathname: `/instances/[instanceid]/gathers`,
						query: { instanceid: idFromParams },
					}}
				>
					<Button>Gathers</Button>
				</Link>
				{record?.status !== "pending" && (
					<Button leftIcon={<IconEye />}>Go to Visualisation</Button>
				)}
				{record?.status !== "pending" && <EditButton {...editButtonProps} />}
			</Group>
		</Show>
	);
};

export default InstanceShow;
