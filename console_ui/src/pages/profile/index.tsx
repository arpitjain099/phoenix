import React from "react";
import {
	Paper,
	Button,
	Container,
	Text,
	TextInput,
	Divider,
	Accordion,
	Badge,
	Group,
} from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { useForm } from "@refinedev/mantine";

interface AccordionLabelProps {
	label: string;
	description: string;
}

function AccordionLabel({ label, description }: AccordionLabelProps) {
	return (
		<Group noWrap>
			<div>
				<h2 className="text-xl font-semibold my-0">{label}</h2>
				<Text size="sm" color="dimmed" weight={400}>
					{description}
				</Text>
			</div>
		</Group>
	);
}

const ProfilePage: React.FC = () => {
	const translate = useTranslate();
	const { getInputProps } = useForm({
		initialValues: {
			name: "",
		},
		validate: {},
	});

	return (
		<Paper className="h-[100vh]" shadow="sm" radius="md" p="lg">
			<div className="flex flex-col p-4">
				{/* <div className="relative w-32 h-32 mb-4">
						<Image
							src="/profile-picture.jpg"
							alt="Profile Picture"
							layout="fill"
							objectFit="cover"
							className="rounded-full"
						/>
					</div> */}
				<h2 className="text-xxl font-bold my-0">John Doe</h2>
				<Badge className="w-max">Admin</Badge>
				<Text size="sm" className="mt-4">
					{translate("pages.profile.email")}: <strong>john@example.com</strong>
				</Text>
				<Text size="sm">
					{translate("pages.profile.created_at")}: <strong>22/02/2024</strong>
				</Text>
			</div>
			<Divider my="sm" />
			<Accordion
				styles={{
					item: {
						"&[data-active]": {
							backgroundColor: "none",
						},
					},
				}}
			>
				<Accordion.Item value="profile-settings">
					<Accordion.Control>
						<AccordionLabel
							label={translate("pages.profile.settings.title")}
							description={translate("pages.profile.settings.description")}
						/>
					</Accordion.Control>
					<Accordion.Panel>
						<Container className="mx-0 flex flex-col my-4">
							<div className="flex flex-col">
								<TextInput
									mt="sm"
									withAsterisk
									label={translate("pages.profile.fields.name")}
									{...getInputProps("display_name")}
								/>
							</div>
							<div className="flex gap-4 items-center mt-4">
								<Button>{translate("buttons.save")}</Button>
								<Button variant="outline">{translate("buttons.cancel")}</Button>
							</div>
						</Container>
					</Accordion.Panel>
				</Accordion.Item>
			</Accordion>
		</Paper>
	);
};

export default ProfilePage;
