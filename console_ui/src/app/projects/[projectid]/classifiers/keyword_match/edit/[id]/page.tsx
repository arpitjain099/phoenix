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
	IconChevronDown,
	IconChevronUp,
} from "@tabler/icons";
import { useState, useEffect, ChangeEvent, useCallback } from "react";
import { useParams } from "next/navigation";
import { useTranslate } from "@refinedev/core";
import { classifierService } from "src/services";
import { showNotification } from "@mantine/notifications";
import ClassifierViewBreadcrumb from "@components/breadcrumbs/classifierView";

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

const EditKeywordClassifier: React.FC = () => {
	const translate = useTranslate();
	const { projectid, id } = useParams();
	// State to manage classes and keyword groups
	const [classifierName, setClassifierName] = useState("");
	const [classifierDescription, setClassifierDescription] = useState("");
	const [classifier, setClassifier] = useState();
	const [classes, setClasses] = useState<ClassData[]>([]);
	const [keywordGroups, setKeywordGroups] = useState<KeywordGroup[]>([]);
	const [isModified, setIsModified] = useState<boolean>(false);
	const [refetch, setRefetch] = useState<boolean>(true);
	const [openRows, setOpenRows] = useState<{ [key: number]: boolean }>({});

	const showRow = (index: number) => {
		setOpenRows((prev) => ({ ...prev, [index]: true }));
	};

	const toggleRow = (index: number) => {
		setOpenRows((prev) => ({ ...prev, [index]: !prev[index] }));
	};

	// Fetch initial data on mount
	const fetchData = useCallback(async () => {
		try {
			const response = await classifierService.getClassifierData({
				project_id: projectid as string,
				classifier_id: id as string,
			});
			const { data } = response;
			setClassifier(data);
			setClassifierName(data?.name);
			setClassifierDescription(data?.description);
			// Set classes and keyword groups from API response
			setClasses(data.intermediatory_classes);
			setKeywordGroups(data.intermediatory_class_to_keyword_configs);
			setRefetch(false);
		} catch (error) {
			console.error("Error fetching classifier data", error);
		}
	}, [id, projectid]);

	useEffect(() => {
		if (id && projectid && refetch) {
			fetchData();
		}

		// Warn user on exit without saving
		window.onbeforeunload = isModified ? () => true : null;

		return () => {
			window.onbeforeunload = null;
		};
	}, [isModified, id, projectid, fetchData, refetch]);

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
		setIsModified(true);
	};

	const handleKeywordChange = (groupId: number, value: string): void => {
		const updatedKeywordGroups = keywordGroups.map((group) =>
			group.id === groupId || group.tempId === groupId
				? {
						...group,
						musts: value,
					}
				: group
		);
		setKeywordGroups(updatedKeywordGroups);
		setIsModified(true);
	};

	const handleUpdateBasicInfo = async () => {
		try {
			await classifierService.updateClassifierBasicData(
				{
					project_id: projectid,
					classifier_id: id,
				},
				{
					name: classifierName,
					description: classifierDescription,
				}
			);
			showNotification({
				title: "Success",
				message: translate("classifiers.success.success"),
			});
		} catch (error) {
			console.error("Error applying classifier", error);
		}
	};

	const handleAddKeywordGroup = (class_id: number): void => {
		setKeywordGroups([
			...keywordGroups,
			{
				tempId: Math.random(),
				class_id,
				musts: "",
			},
		]);
		setIsModified(true);
	};

	const handleRemoveKeywordGroup = async (groupId: number): Promise<void> => {
		const groupToRemove = keywordGroups.find(
			(group) => group.id === groupId || group.tempId === groupId
		);
		if (groupToRemove?.id) {
			try {
				await classifierService.removeKeywordClassifierConfig({
					project_id: projectid,
					classifier_id: id,
					config_id: groupToRemove.id,
				});
				setIsModified(true);
				setRefetch(true);
			} catch (error) {
				console.error("Error removing keyword group", error);
			}
		} else {
			try {
				setKeywordGroups(
					keywordGroups.filter((item) => item.tempId !== groupId)
				);
				setIsModified(true);
			} catch (error) {
				console.error("Error removing keyword group", error);
			}
		}
	};

	const handleAddClass = (): void => {
		setClasses([
			...classes,
			{ tempId: Math.random(), name: "", description: "" },
		]);
		setIsModified(true);
	};

	const handleRemoveClass = async (index: number): Promise<void> => {
		const classToRemove = classes[index];
		if (classToRemove?.id) {
			try {
				await classifierService.removeClassifierClassData({
					project_id: projectid,
					classifier_id: id,
					class_id: classToRemove.id,
				});
				setIsModified(true);
				setRefetch(true);
			} catch (error) {
				console.error("Error removing class", error);
			}
		} else {
			try {
				setClasses(classes.filter((_, i) => i !== index));
				setKeywordGroups(
					keywordGroups.filter(
						(group) => group.class_id !== classToRemove.tempId
					)
				);
				setIsModified(true);
			} catch (error: any) {
				showNotification({
					title: "Error",
					color: "red",
					message: error?.response?.data?.message || "An Error Occured",
				});
				console.error("Error removing class", error);
			}
		}
	};

	const onSubmitKeyword = async (
		class_id: number,
		group: KeywordGroup
	): Promise<void> => {
		try {
			if (group?.id) {
				await classifierService.updateKeywordClassifierConfig(
					{
						project_id: projectid,
						classifier_id: id,
						config_id: group.id,
					},
					{
						musts: group.musts,
						nots: group.nots || "",
					}
				);
				setIsModified(true);
			} else {
				await classifierService.createKeywordClassifierConfig(
					{
						project_id: projectid,
						classifier_id: id,
						config_id: group.id,
					},
					{
						class_id,
						musts: group.musts,
						nots: group.nots || "",
					}
				);
				setIsModified(true);
			}
		} catch (error) {
			console.error("Error removing class", error);
		}
	};

	const handleSubmitKeywords = async (
		classId: number,
		dataId?: number
	): Promise<void> => {
		const updatedKeywordGroups = keywordGroups.filter(
			(group) => group.class_id === classId
		);
		updatedKeywordGroups.map(
			async (group) => await onSubmitKeyword(dataId || classId, group)
		);
	};

	const handleSubmitClass = async (classIndex: number): Promise<void> => {
		const classToAdd = classes[classIndex];
		try {
			if (classToAdd?.id) {
				await classifierService.updateClassifierClassData(
					{
						project_id: projectid,
						classifier_id: id,
						class_id: classToAdd.id,
					},
					{
						name: classToAdd.name,
						description: classToAdd.description,
					}
				);
				await handleSubmitKeywords(classToAdd.id);
			} else if (classToAdd?.tempId) {
				const res = await classifierService.createClassifierClassData(
					{
						project_id: projectid,
						classifier_id: id,
					},
					{
						name: classToAdd.name,
						description: classToAdd.description,
					}
				);
				const { data } = res;
				await handleSubmitKeywords(classToAdd.tempId, data.id);
			}
			setRefetch(true);
			setIsModified(true);
		} catch (error: any) {
			showNotification({
				title: "Error",
				color: "red",
				message: error?.response?.data?.message || "An Error Occured",
			});
			console.error("Error creating/updating class", error);
		}
	};

	const handleSaveAll = async (): Promise<void> => {
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
			<ClassifierViewBreadcrumb
				record={classifier}
				projectid={projectid as string}
			/>
			<h1 className="text-2xl font-semibold">
				{translate("classifiers.types.keyword_match.edit")}
			</h1>
			<p className="mb-4">
				{translate("classifiers.types.keyword_match.edit_description")}
			</p>

			<Space h="md" />
			<div>
				<Divider my="sm" label="Basic Setup" />
				<TextInput
					label="Name"
					placeholder="My classifier"
					value={classifierName}
					onChange={(e) => {
						setIsModified(true);
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
				<Space h="sm" />
				<div className="flex justify-end">
					<Button
						leftIcon={<IconCheck size={16} />}
						mt="sm"
						onClick={handleUpdateBasicInfo}
					>
						Update Basic Info
					</Button>
				</div>
			</div>
			<Space h="lg" />

			{/* Classes Section */}
			<Divider my="sm" label="Configuration" />
			<Table highlightOnHover withBorder>
				<thead>
					<tr>
						<th aria-label="Accordion Control" />
						<th>{translate("classifiers.fields.class_name")}</th>
						<th>{translate("projects.fields.description")}</th>
						<th className="flex items-center justify-center">
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
							<td className="align-baseline">
								<ActionIcon
									color="dark"
									variant="light"
									onClick={() => toggleRow(classIndex)}
								>
									{openRows[classIndex] ? (
										<IconChevronUp size={16} />
									) : (
										<IconChevronDown size={16} />
									)}
								</ActionIcon>
							</td>
							<td className="align-baseline">
								<TextInput
									placeholder="Class name"
									value={classItem.name}
									onChange={(event: ChangeEvent<HTMLInputElement>) =>
										handleClassChange(classIndex, "name", event.target.value)
									}
								/>
							</td>
							<td className="align-baseline">
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
							<td className="!pt-0">
								<Table>
									<tbody className="flex flex-col items-center">
										{openRows[classIndex]
											? keywordGroups
													?.filter(
														(group) =>
															group.class_id === classItem?.id ||
															group.class_id === classItem?.tempId
													)
													.map((keywordGroup, keywordIndex) => (
														<>
															<tr key={keywordIndex}>
																<td>
																	<TextInput
																		placeholder="e.g Keyword1 keyword2"
																		value={keywordGroup.musts}
																		onChange={(
																			event: ChangeEvent<HTMLInputElement>
																		) => {
																			if (keywordGroup?.id) {
																				handleKeywordChange(
																					keywordGroup.id,
																					event.target.value
																				);
																			} else if (keywordGroup?.tempId) {
																				handleKeywordChange(
																					keywordGroup.tempId,
																					event.target.value
																				);
																			}
																		}}
																	/>
																</td>
																<td>
																	<Tooltip
																		label={translate(
																			"classifiers.actions.tooltips.delete_keyword"
																		)}
																	>
																		<ActionIcon
																			color="red"
																			variant="light"
																			onClick={() => {
																				if (keywordGroup?.id) {
																					handleRemoveKeywordGroup(
																						keywordGroup.id
																					);
																				} else if (keywordGroup?.tempId) {
																					handleRemoveKeywordGroup(
																						keywordGroup.tempId
																					);
																				}
																			}}
																		>
																			<IconTrash size={16} />
																		</ActionIcon>
																	</Tooltip>
																</td>
															</tr>
															{keywordGroups.length > 0 &&
																keywordIndex <
																	keywordGroups.filter(
																		(group) =>
																			group.class_id === classItem?.id ||
																			group.class_id === classItem?.tempId
																	).length -
																		1 && <td className="text-center">or</td>}
														</>
													))
											: `${
													keywordGroups?.filter(
														(group) =>
															group.class_id === classItem?.id ||
															group.class_id === classItem?.tempId
													).length
												} added`}
										<Tooltip
											label={translate(
												"classifiers.actions.tooltips.add_keyword"
											)}
										>
											<ActionIcon
												color="blue"
												variant="light"
												onClick={() => {
													showRow(classIndex);
													if (classItem?.tempId) {
														return handleAddKeywordGroup(classItem.tempId);
													}
													if (classItem?.id) {
														return handleAddKeywordGroup(classItem.id);
													}
													return null;
												}}
											>
												<IconPlus size={16} />
											</ActionIcon>
										</Tooltip>
									</tbody>
								</Table>
							</td>
							<td className="align-baseline">
								<div className="w-full h-full flex gap-1 items-center justify-center">
									<Tooltip
										label={translate("classifiers.actions.tooltips.save_class")}
									>
										<ActionIcon
											color="green"
											variant="light"
											onClick={() => handleSubmitClass(classIndex)}
										>
											<IconCheck size={16} />
										</ActionIcon>
									</Tooltip>
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
					onClick={handleSaveAll}
				>
					Save All
				</Button>
			</div>
		</div>
	);
};

export default EditKeywordClassifier;
