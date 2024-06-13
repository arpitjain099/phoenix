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
import {
	Accordion,
	Button,
	Container,
	Divider,
	Group,
	Title,
} from "@mantine/core";
import Link from "next/link";
import DashboardLinkButton from "@components/buttons/DashboardLinkButton";

export const ProjectShow: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const { queryResult } = useShow();
	const { data, isLoading } = queryResult;

	const record = data?.data;

	const { id: idFromParams, identifier } = useResource("projects");

	const editButtonProps: EditButtonProps = {
		...(isLoading ? { disabled: true } : {}),
		// color: "primary",
		variant: "outline",
		resource: identifier,
		recordItemId: idFromParams,
	};

	return (
		<Show
			title={<Title order={3}>{record?.name}</Title>}
			isLoading={isLoading}
			headerButtons={() => <EditButton {...editButtonProps} />}
		>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.description")}:
				</Title>
				<TextField value={record?.description} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.environment_slug")}:
				</Title>
				<TextField value={record?.environment_slug} />
			</Group>
			<Group>
				<Title my="xs" order={5}>
					{translate("projects.fields.created_at")}:
				</Title>
				<DateField format="LLL" value={record?.created_at} />
			</Group>
			<Divider mt="sm" />
			<Accordion
				styles={{
					control: {
						paddingLeft: 0,
					},
					item: {
						"&[data-active]": {
							backgroundColor: "none",
						},
					},
				}}
			>
				<Accordion.Item value="details">
					<Accordion.Control>
						<Title order={5}>{translate("projects.more_info")}</Title>
					</Accordion.Control>
					<Accordion.Panel>
						<Container className="mx-0 flex flex-col my-4">
							<Group>
								<Title my="xs" order={5}>
									{translate("projects.fields.id")}:
								</Title>
								<NumberField value={record?.id ?? ""} />
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
									{translate("projects.fields.updated_at")}:
								</Title>
								<DateField format="LLL" value={record?.updated_at} />
							</Group>
						</Container>
					</Accordion.Panel>
				</Accordion.Item>
			</Accordion>

			<Group className="mt-4 flex flex-col sm:flex-row items-start gap-4">
				<Link
					href="/projects/[projectid]/gathers"
					as={`/projects/${idFromParams}/gathers`}
				>
					<Button>{translate("projects.titles.gathers")}</Button>
				</Link>
				<Link
					href="/projects/[projectid]/tabulate"
					as={`/projects/${idFromParams}/tabulate`}
				>
					<Button>{translate("projects.titles.tabulates")}</Button>
				</Link>
				<DashboardLinkButton environmentSlug={record?.environment_slug} />
			</Group>
		</Show>
	);
};

export default ProjectShow;
