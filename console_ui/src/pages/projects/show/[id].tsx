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

const PLATFORM_DOMAIN_BASE = process.env.NEXT_PUBLIC_PLATFORM_DOMAIN_BASE!;
const PLATFORM_SCHEMA_BASE = process.env.NEXT_PUBLIC_PLATFORM_SCHEMA_BASE!;

export const ProjectShow: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const { queryResult } = useShow();
	const { data, isLoading } = queryResult;

	const record = data?.data;

	const { id: idFromParams, identifier } = useResource("projects");

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
					{translate("projects.fields.name")}:
				</Title>
				<TextField value={record?.name} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.id")}:
				</Title>
				<NumberField value={record?.id ?? ""} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.environment_slug")}:
				</Title>
				<TextField value={record?.environment_slug} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.description")}:
				</Title>
				<TextField value={record?.description} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.days_until_pi_expiration")}:
				</Title>
				<NumberField value={record?.pi_deleted_after_days ?? ""} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.days_until_all_data_expiration")}:
				</Title>
				<NumberField value={record?.delete_after_days ?? ""} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.expected_usage.title")}:
				</Title>
				<TextField value={record?.expected_usage} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.created_at")}:
				</Title>
				<DateField value={record?.created_at} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.updated_at")}:
				</Title>
				<DateField value={record?.updated_at} />
			</Group>
			<Group className="mt-4 flex flex-col items-start gap-4">
				<Link
					href="/projects/[projectid]/gathers"
					as={`/projects/${idFromParams}/gathers`}
				>
					<Button>{translate("gathers.gathers")}</Button>
				</Link>
				<Link
					href="/projects/[projectid]/tabulate"
					as={`/projects/${idFromParams}/tabulate`}
				>
					<Button>{translate("tabulate.tabulate")}</Button>
				</Link>
				{PLATFORM_DOMAIN_BASE && PLATFORM_SCHEMA_BASE && (
					<Link
						href={`${PLATFORM_SCHEMA_BASE}://dashboard.${record?.environment_slug}.${PLATFORM_DOMAIN_BASE}`}
						target="_blank"
					>
						<Button leftIcon={<IconEye />}>
							{translate("projects.titles.dashboard")}
						</Button>
					</Link>
				)}
				<EditButton {...editButtonProps} />
			</Group>
		</Show>
	);
};

export default ProjectShow;
