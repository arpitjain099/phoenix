import React from "react";
import { Container, Text, Button } from "@mantine/core";

const ProfilePage: React.FC = () => (
	<Container className="h-[100vh] flex items-center justify-center">
		<div className="flex flex-col items-center">
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
				Email: john@example.com
			</Text>
			<Text size="sm" color="gray">
				Created At: 22/02/2024
			</Text>
			<Button className="mt-4">Edit Profile</Button>
		</div>
	</Container>
);

export default ProfilePage;
