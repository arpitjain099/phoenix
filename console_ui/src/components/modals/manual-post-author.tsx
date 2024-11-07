import React, { useEffect, useState } from "react";
import { Modal, Button, MultiSelect, Text, Group, Loader } from "@mantine/core";
import { showNotification } from "@mantine/notifications";
import {
	Author,
	ClassData,
} from "@pages/projects/[projectid]/classifiers/manual_post_authors/model";
import { classifierService } from "src/services";
import { useTranslate } from "@refinedev/core";

interface ClassifyAuthorModalProps {
	authorIdx: number;
	authorsCount: number;
	goToNext: (idx: number) => void;
	isOpen: boolean;
	onClose: () => void;
	author: Author;
	projectId: string;
	classifierId: string;
	availableClasses: Array<ClassData>;
}

const ClassifyAuthorModal: React.FC<ClassifyAuthorModalProps> = ({
	authorIdx,
	authorsCount,
	goToNext,
	isOpen,
	onClose,
	author,
	projectId,
	classifierId,
	availableClasses,
}) => {
	const translate = useTranslate();
	const [isLoading, setIsLoading] = useState(false);
	const [selectedClasses, setSelectedClasses] = useState(
		author.intermediatory_author_classes.map((c) => c.class_id.toString())
	);

	const addClassMutation = async (classId: string) => {
		setIsLoading(true);
		try {
			await classifierService.addClassToManualPostAuthorClassifier(
				{
					project_id: projectId,
					classifier_id: classifierId,
				},
				{
					class_id: Number(classId),
					phoenix_platform_message_author_id:
						author.phoenix_platform_message_author_id,
				}
			);
		} catch (error: any) {
			showNotification({
				title: "Error",
				color: "red",
				message: error?.response?.data?.message || "Failed to add class",
			});
		} finally {
			setIsLoading(false);
		}
	};

	const removeClassMutation = async (classId: string) => {
		setIsLoading(true);
		try {
			const classAuthor = author.intermediatory_author_classes.find(
				(item) => item.class_id === Number(classId)
			);
			if (classAuthor?.id)
				await classifierService.removeClassToManualPostAuthorClassifier({
					project_id: projectId,
					classifier_id: classifierId,
					classified_post_author_id: classAuthor.id,
				});
		} catch (error: any) {
			showNotification({
				title: "Error",
				color: "red",
				message: error?.response?.data?.message || "Failed to remove class",
			});
		} finally {
			setIsLoading(false);
		}
	};

	// Handle class selection changes
	const handleClassChange = (newSelectedClasses: string[]) => {
		// Find added classes
		const addedClasses = newSelectedClasses.filter(
			(id) => !selectedClasses.includes(id)
		);
		// Find removed classes
		const removedClasses = selectedClasses.filter(
			(id) => !newSelectedClasses.includes(id)
		);

		// Add newly selected classes
		addedClasses.forEach((classId) => {
			addClassMutation(classId);
		});

		// Remove unselected classes
		removedClasses.forEach((classId) => {
			removeClassMutation(classId);
		});

		// Update selected classes in state
		setSelectedClasses(newSelectedClasses);
	};

	useEffect(() => {
		setSelectedClasses(
			author.intermediatory_author_classes.map((c) => c.class_id.toString())
		);
	}, [author]);

	return (
		<Modal opened={isOpen} onClose={onClose} size="lg">
			<div className="font-medium flex flex-col px-8 pb-8">
				<Text size="xl" weight={500} className="mb-2">
					{translate("classifiers.types.manual_post_authors.author_edit.title")}
				</Text>
				<Text size="sm" color="dimmed" className="mb-4">
					{translate(
						"classifiers.types.manual_post_authors.author_edit.instruction"
					)}
				</Text>

				<Text size="sm" color="dimmed" className="mb-4">
					{translate("classifiers.types.manual_post_authors.author_edit.count")}
					{` ${authorIdx + 1} of ${authorsCount}`}
				</Text>
				<div>
					<div className="w-full flex mb-5 p-1">
						<div className="w-1/2 flex flex-col">
							<Text className="font-medium text-lg capitalize">
								{author.pi_platform_message_author_name}
							</Text>
							<Text className="text-base text-neutral-500 font-normal">
								{translate(
									"classifiers.types.manual_post_authors.fields.author_name"
								)}
							</Text>
						</div>
						<div className="w-1/2 flex flex-col">
							<Text className="font-medium text-lg capitalize">
								{author.phoenix_platform_message_author_id}
							</Text>
							<Text className="text-base text-neutral-500 font-normal">
								{translate(
									"classifiers.types.manual_post_authors.fields.author_link"
								)}
							</Text>
						</div>
					</div>
					<div className="w-full flex mb-5 p-1">
						<div className="w-1/2 flex flex-col">
							<Text className="font-medium text-lg capitalize">
								{author.post_count}
							</Text>
							<Text className="text-base text-neutral-500 font-normal">
								{translate(
									"classifiers.types.manual_post_authors.fields.no_of_posts"
								)}
							</Text>
						</div>
						<div className="w-1/2 flex flex-col">
							<Text className="font-medium capitalize text-lg">
								{author.platform}
							</Text>
							<Text className="text-base text-neutral-500 font-normal">
								{translate(
									"classifiers.types.manual_post_authors.fields.author_platform"
								)}
							</Text>
						</div>
					</div>
					<div className="w-full flex mb-5 p-1">
						<div className="w-1/2 flex flex-col">
							<Text className="font-medium text-lg">
								{author.pi_platform_message_author_id}
							</Text>
							<Text className="text-base text-neutral-500 font-normal">
								{translate(
									"classifiers.types.manual_post_authors.fields.author_anon_id"
								)}
							</Text>
						</div>
					</div>
					<MultiSelect
						label={translate(
							"classifiers.types.manual_post_authors.fields.classes"
						)}
						placeholder="Select classes"
						data={(availableClasses || []) // Ensure availableClasses is defined
							.filter((c) => c?.id && c?.name)
							.map((c) => ({
								value: c?.id?.toString() || "",
								label: c.name,
							}))}
						value={selectedClasses}
						onChange={handleClassChange}
						searchable
						clearable
						disabled={isLoading}
					/>
				</div>

				{isLoading && (
					<Group position="center" mt="md">
						<Loader size="sm" />
						<Text>
							{translate(
								"classifiers.types.manual_post_authors.author_edit.processing"
							)}
							...
						</Text>
					</Group>
				)}

				<Group position="right" mt="lg">
					<Button variant="outline" onClick={onClose}>
						{translate("buttons.close")}
					</Button>
					<Button
						onClick={() => goToNext(authorIdx)}
						disabled={authorIdx + 1 >= authorsCount}
					>
						{translate(
							"classifiers.types.manual_post_authors.author_edit.go_to_next"
						)}
					</Button>
				</Group>
			</div>
		</Modal>
	);
};

export default ClassifyAuthorModal;
