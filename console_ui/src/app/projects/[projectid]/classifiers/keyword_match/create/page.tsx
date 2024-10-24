"use client";

/* eslint-disable react/no-array-index-key */

import {
	TextInput,
	Button,
	Table,
	Tooltip,
	ActionIcon,
	Space,
	Divider,
} from "@mantine/core";
import { IconTrash, IconPlus, IconCheck, IconInfoCircle } from "@tabler/icons";
import { useState, ChangeEvent } from "react";
import { useParams, useRouter } from "next/navigation";
import { useTranslate } from "@refinedev/core";
import { classifierService } from "src/services";
import { showNotification } from "@mantine/notifications";

// Define types for class and keyword group structures
interface ClassData {
	id?: number;
	tempId?: number;
	name: string;
	description: string;
}

interface KeywordGroup {
	id?: number; // Will exist for existing configurations, undefined for new ones
	tempId?: number;
	class_id: number;
	musts: string;
	nots?: string;
	class_name?: string;
}

const CreateKeywordClassifier: React.FC = () => {
	const router = useRouter();
	const translate = useTranslate();
	const { projectid, id } = useParams();
	// State to manage classes and keyword groups
	const [classifierName, setClassifierName] = useState("");
	const [classes, setClasses] = useState<ClassData[]>([
		{ name: "", description: "" },
	]);
	const [keywordGroups, setKeywordGroups] = useState<KeywordGroup[]>([]);

	// Input change handlers
	const handleClassChange = (
		index: number,
		field: "name" | "description",
		value: string
	): void => {
		const updatedClasses = classes.map((cls, i) =>
			i === index ? { ...cls, [field]: value } : cls
		);
		setClasses(updatedClasses);
	};

	const handleAddClass = (): void => {
		setClasses([
			...classes,
			{ tempId: Math.random(), name: "", description: "" },
		]);
	};

	const handleRemoveClass = async (index: number): Promise<void> => {
		const classToRemove = classes[index];
		try {
			setClasses(classes.filter((_, i) => i !== index));
			setKeywordGroups(
				keywordGroups.filter((group) => group.class_id !== classToRemove.tempId)
			);
		} catch (error: any) {
			showNotification({
				title: "Error",
				color: "red",
				message: error?.response?.data?.message || "An Error Occured",
			});
			console.error("Error removing class", error);
		}
	};

	const handleSubmitClass = async (classIndex: number): Promise<void> => {
		const classToAdd = classes[classIndex];
		try {
			await classifierService.createClassifierClassData(
				{
					project_id: projectid,
					classifier_id: id,
				},
				{
					name: classToAdd.name,
					description: classToAdd.description,
				}
			);
			// todo redirect out
		} catch (error: any) {
			showNotification({
				title: "Error",
				color: "red",
				message: error?.response?.data?.message || "An Error Occured",
			});
			console.error("Error creating class", error);
		}
	};

	const handleSave = async (): Promise<void> => {
		try {
			classes.map(async (_, idx) => await handleSubmitClass(idx));
			showNotification({
				title: "success",
				message: translate("classifiers.success.success"),
			});
		} catch (error: any) {
			showNotification({
				title: "Error",
				color: "red",
				message: error?.response?.data?.message || "An Error Occured",
			});
			console.error("Error creating/updating class", error);
		}
	};

	return (
		<div className="p-8 bg-white min-h-screen">
			<h1 className="text-2xl font-semibold">
				{translate("classifiers.types.keyword_match.create")}
			</h1>
			<p className="mb-2">
				{translate("classifiers.types.keyword_match.create_description")}
			</p>
			<p className="mb-4">
				{translate("classifiers.types.keyword_match.create_description_2")}
			</p>

			<Space h="md" />
			<div>
				<Divider my="sm" label="Basic Setup" />
				<TextInput
					label="Name"
					placeholder="My classifier"
					value={classifierName}
					onChange={(e) => {
						setClassifierName(e.target.value);
					}}
					required
				/>
			</div>
			<Space h="lg" />

			{/* Classes Section */}
			<Divider my="sm" label="Classes" />
			<Table highlightOnHover withBorder>
				<thead>
					<tr>
						<th>{translate("classifiers.fields.class_name")}</th>
						<th>{translate("projects.fields.description")}</th>
						<th className="flex items-center">
							{translate("classifiers.fields.keywords")}
							<Tooltip label={translate("classifiers.info.create_keywords")}>
								<span className="flex">
									<IconInfoCircle size={12} />
								</span>
							</Tooltip>
						</th>
						<th>{translate("table.actions")}</th>
					</tr>
				</thead>
				<tbody>
					{classes?.map((classItem, classIndex) => (
						<tr key={classIndex}>
							<td>
								<TextInput
									placeholder="Class name"
									value={classItem.name}
									onChange={(event: ChangeEvent<HTMLInputElement>) =>
										handleClassChange(classIndex, "name", event.target.value)
									}
								/>
							</td>
							<td>
								<TextInput
									placeholder="Class description"
									value={classItem.description}
									onChange={(event: ChangeEvent<HTMLInputElement>) =>
										handleClassChange(
											classIndex,
											"description",
											event.target.value
										)
									}
								/>
							</td>
							<td />
							<td>
								<div className="w-full h-full flex gap-1 items-center justify-center">
									<Tooltip
										label={translate(
											"classifiers.actions.tooltips.delete_class"
										)}
									>
										<ActionIcon
											color="red"
											variant="light"
											onClick={() => handleRemoveClass(classIndex)}
										>
											<IconTrash size={16} />
										</ActionIcon>
									</Tooltip>
								</div>
							</td>
						</tr>
					))}
				</tbody>
			</Table>
			<div className="flex gap-2 w-full">
				<Button
					leftIcon={<IconPlus size={16} />}
					variant="outline"
					mt="sm"
					onClick={handleAddClass}
				>
					Add Class
				</Button>
				<Button
					rightIcon={<IconCheck size={16} />}
					mt="sm"
					// fullWidth
					onClick={handleSave}
				>
					Save
				</Button>
			</div>
		</div>
	);
};

export default CreateKeywordClassifier;
