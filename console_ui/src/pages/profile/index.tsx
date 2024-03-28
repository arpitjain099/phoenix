import React from "react";
import {
	Paper,
	Button,
	Container,
	Text,
	TextInput,
	Select,
	Divider,
} from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { useForm } from "@refinedev/mantine";

const ProfilePage: React.FC = () => {
	const translate = useTranslate();
	const { getInputProps } = useForm({
		initialValues: {
			name: "",
			email: "",
			role: "",
		},
		validate: {},
	});
	return (
		<Paper shadow="sm" radius="md" p="lg">
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
				<Text size="lg" weight={700}>
					John Doe
				</Text>
				<Text size="sm" color="gray">
					Admin
				</Text>
				<Text size="sm" color="gray" className="mt-4">
					{translate("pages.profile.email")}: john@example.com
				</Text>
				<Text size="sm" color="gray">
					{translate("pages.profile.created_at")}: 22/02/2024
				</Text>
			</div>
			<Divider my="sm" />
			<Container className="h-[100vh] mx-0 flex flex-col">
				<h2 className="text-xl font-semibold mb-4">
					{translate("pages.profile.title")}
				</h2>
				<div className="flex flex-col">
					<TextInput
						mt="sm"
						withAsterisk
						label={translate("pages.profile.fields.name")}
						{...getInputProps("name")}
					/>
					<TextInput
						mt="sm"
						withAsterisk
						label={translate("pages.profile.fields.email")}
						{...getInputProps("email")}
					/>
					<Select
						mt="sm"
						withAsterisk
						label={translate("pages.profile.fields.role")}
						{...getInputProps("role")}
						data={[
							{ label: translate("inputs.select"), value: "" },
							{ label: "Admin", value: "admin" },
							{ label: "User", value: "user" },
						]}
					/>
				</div>
				<div className="flex gap-4 items-center mt-4">
					<Button>{translate("buttons.save")}</Button>
					<Button variant="outline">{translate("buttons.cancel")}</Button>
				</div>
			</Container>
		</Paper>
	);
};

export default ProfilePage;
