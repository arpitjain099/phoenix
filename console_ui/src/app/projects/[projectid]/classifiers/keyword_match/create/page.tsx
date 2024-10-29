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
import {
	IconTrash,
	IconPlus,
	IconCheck,
	IconInfoCircle,
	IconArrowLeft,
	IconDeviceFloppy,
} from "@tabler/icons";
import { useState, ChangeEvent } from "react";
import { useParams, useRouter } from "next/navigation";
import { useBack, useTranslate } from "@refinedev/core";
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
	const back = useBack();
	const router = useRouter();
	const translate = useTranslate();
	const { projectid, id } = useParams();
	// State to manage classes and keyword groups
	const [classifierName, setClassifierName] = useState("");
	const [classifierDescription, setClassifierDescription] = useState("");
	const [classes, setClasses] = useState<ClassData[]>([
		{ name: "", description: "" },
	]);
	const [loading, setLoading] = useState(false);
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

	const handleSave = async (): Promise<void> => {
		setLoading(true);
		try {
			const res = await classifierService.createKeywordClassifier(
				{
					project_id: projectid,
				},
				{
					name: classifierName,
					description: classifierDescription,
					intermediatory_classes: classes,
				}
			);
			const { data } = res;
			showNotification({
				title: "success",
				message: translate("classifiers.success.success"),
			});
			router.push(
				`/projects/${projectid}/classifiers/${data?.type}/${data.id}`
			);
		} catch (error: any) {
			showNotification({
				title: "Error",
				color: "red",
				message: error?.response?.data?.message || "An Error Occured",
			});
			console.error("Error creating/updating class", error);
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="p-8 bg-white min-h-screen">
			<h1 className="flex items-center gap-2 text-2xl font-semibold">
				<ActionIcon onClick={back}>
					<IconArrowLeft />
				</ActionIcon>
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
				<Space h="sm" />
				<TextInput
					label="Description"
					placeholder="Classifier Description"
					value={classifierDescription}
					onChange={(e) => {
						setClassifierDescription(e.target.value);
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
							<Tooltip
								label={translate("classifiers.info.create_keywords")}
								width={200}
							>
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
							<td>
								<TextInput placeholder="Keyword1 kewyord2" disabled />
							</td>
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
					rightIcon={<IconDeviceFloppy size={16} />}
					mt="sm"
					// fullWidth
					loading={loading}
					disabled={!classifierName}
					onClick={handleSave}
				>
					Create
				</Button>
			</div>
		</div>
	);
};

export default CreateKeywordClassifier;
