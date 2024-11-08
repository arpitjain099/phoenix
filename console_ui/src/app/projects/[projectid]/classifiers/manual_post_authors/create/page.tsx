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
	ScrollArea,
	Group,
} from "@mantine/core";
import {
	IconTrash,
	IconPlus,
	IconArrowLeft,
	IconDeviceFloppy,
} from "@tabler/icons";
import { useState, ChangeEvent, useCallback, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { useBack, useTranslate } from "@refinedev/core";
import { classifierService } from "src/services";
import { showNotification } from "@mantine/notifications";
import PaginationComponent from "@components/table/pagination";
import { Author } from "../model";

// Define types for class and keyword group structures
interface ClassData {
	id?: number;
	tempId?: number;
	name: string;
	description: string;
}

const CreateManualPostClassifier: React.FC = () => {
	const back = useBack();
	const router = useRouter();
	const translate = useTranslate();
	const { projectid } = useParams();
	// State to manage classes and keyword groups
	const [classifierName, setClassifierName] = useState();
	const [classifierDescription, setClassifierDescription] = useState();
	const [classes, setClasses] = useState<ClassData[]>([
		{ name: "", description: "" },
	]);
	const [loading, setLoading] = useState(false);
	const [authors, setAuthors] = useState<Author[]>([]);
	const [totalAuthors, setTotalAuthors] = useState(0);
	const [activePage, setActivePage] = useState(1);
	const authorsPerPage = 10; // Set the number of authors to show per page

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
		try {
			setClasses(classes.filter((_, i) => i !== index));
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
			const res = await classifierService.createManualPostClassifier(
				{
					project_id: projectid,
				},
				{
					name: classifierName,
					description: classifierDescription,
					intermediatory_classes: classes.filter(
						(cls) => cls.name && cls.name.trim() !== ""
					),
				}
			);
			const { data } = res;
			showNotification({
				title: translate("status.success"),
				message: translate("classifiers.success.success"),
			});
			router.push(
				`/projects/${projectid}/classifiers/${data?.type}/${data.id}`
			);
		} catch (error: any) {
			showNotification({
				title: translate("status.error"),
				color: "red",
				message: error?.response?.data?.message || "An Error Occured",
			});
			console.error("Error creating/updating class", error);
		} finally {
			setLoading(false);
		}
	};

	// Fetch initial data on mount
	const fetchData = useCallback(
		async (page: number) => {
			const start = (page - 1) * authorsPerPage;
			const end = start + authorsPerPage;
			try {
				const authorsResponse =
					await classifierService.getRefreshManualPostAuthors({
						project_id: projectid as string,
						params: { start, end },
					});
				setAuthors(authorsResponse?.data?.authors);
				setTotalAuthors(authorsResponse?.data?.meta?.total_count);
			} catch (error) {
				console.error("Error fetching classifier data", error);
			}
		},
		[projectid, setAuthors]
	);

	useEffect(() => {
		if (projectid) {
			fetchData(activePage);
		}
	}, [projectid, activePage, fetchData]);

	return (
		<div className="p-8 bg-white min-h-screen">
			<h1 className="flex items-center gap-2 text-2xl font-semibold">
				<ActionIcon onClick={back}>
					<IconArrowLeft />
				</ActionIcon>
				{translate("classifiers.types.manual_post_authors.create")}
			</h1>
			<p className="mb-2">
				{translate("classifiers.types.manual_post_authors.create_description")}
			</p>
			<p className="mb-4">
				{translate(
					"classifiers.types.manual_post_authors.create_description_2"
				)}
			</p>

			<Space h="md" />
			<div>
				<Divider
					my="sm"
					label={translate(
						"classifiers.types.manual_post_authors.view.accordion.basic_setup"
					)}
				/>
				<TextInput
					label="Name"
					placeholder={translate("classifiers.fields.name_placeholder")}
					value={classifierName}
					onChange={(e) => {
						setClassifierName(e.target.value);
					}}
					required
				/>
				<Space h="sm" />
				<TextInput
					label="Description"
					placeholder={translate("classifiers.fields.description_placeholder")}
					value={classifierDescription}
					onChange={(e) => {
						setClassifierDescription(e.target.value);
					}}
					required
				/>
			</div>
			<Space h="lg" />

			{/* Classes Section */}
			<Divider
				my="sm"
				label={translate(
					`classifiers.types.manual_post_authors.fields.create.class_section`
				)}
			/>
			<Table highlightOnHover withBorder>
				<thead>
					<tr>
						<th>{translate("classifiers.fields.class_name")}</th>
						<th>{translate("projects.fields.description")}</th>
						<th>{translate("table.actions")}</th>
					</tr>
				</thead>
				<tbody>
					{classes?.map((classItem, classIndex) => (
						<tr key={classIndex}>
							<td>
								<TextInput
									placeholder={translate(
										"classifiers.fields.class_name_placeholder"
									)}
									value={classItem.name}
									onChange={(event: ChangeEvent<HTMLInputElement>) =>
										handleClassChange(classIndex, "name", event.target.value)
									}
								/>
							</td>
							<td>
								<TextInput
									placeholder={translate(
										"classifiers.fields.class_description_placeholder"
									)}
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
					<Button
						leftIcon={<IconPlus size={16} />}
						variant="subtle"
						mt="sm"
						onClick={handleAddClass}
					>
						{translate("buttons.add_class")}
					</Button>
				</tbody>
			</Table>

			<Space h="lg" />

			{/* Authors Section */}
			<Divider
				my="sm"
				label={translate(
					`classifiers.types.manual_post_authors.fields.create.authors_section`
				)}
			/>
			<ScrollArea>
				<Table highlightOnHover withBorder>
					<thead>
						<tr>
							<th className="!text-gray-400">
								{translate(
									"classifiers.types.manual_post_authors.fields.classes"
								)}
							</th>
							<th className="!text-gray-400">
								{translate(
									"classifiers.types.manual_post_authors.fields.author_name"
								)}
							</th>
							<th className="!text-gray-400">
								{translate(
									"classifiers.types.manual_post_authors.fields.no_of_posts"
								)}
							</th>
							<th className="!text-gray-400">
								{translate(
									"classifiers.types.manual_post_authors.fields.author_platform"
								)}
							</th>
							<th className="!text-gray-400">
								{translate(
									"classifiers.types.manual_post_authors.fields.author_anon_id"
								)}
							</th>
							<th className="!text-gray-400">{translate("table.actions")}</th>
						</tr>
					</thead>
					<tbody>
						{authors.map((author) => (
							<tr key={author.phoenix_platform_message_author_id}>
								<td>
									<div className="flex flex-wrap">
										{author.intermediatory_author_classes.map((cls) => (
											<span
												key={cls.class_id}
												className="mr-2 mb-2 px-2 py-1 bg-gray-200 rounded text-sm sm:text-base"
											>
												{cls.class_name}
											</span>
										))}
									</div>
								</td>
								<td className="!text-gray-400">
									{author.pi_platform_message_author_name}
								</td>
								<td className="!text-gray-400">{author.post_count}</td>
								<td className="capitalize !text-gray-400">{author.platform}</td>
								<td className="!text-gray-400">
									{author.pi_platform_message_author_id}
								</td>
								<td>
									<Group spacing="xs">
										<Button size="xs" variant="default" disabled>
											{translate("buttons.edit")}
										</Button>
									</Group>
								</td>
							</tr>
						))}
					</tbody>
				</Table>
			</ScrollArea>
			<br />
			<PaginationComponent
				pages={Math.ceil(totalAuthors / authorsPerPage)}
				_activeIndex={activePage}
				_setActiveIndex={setActivePage}
			/>

			<Space h="lg" />
			<div className="flex justify-end gap-2 w-full">
				<Button
					leftIcon={<IconDeviceFloppy size={16} />}
					mt="sm"
					// fullWidth
					loading={loading}
					disabled={!classifierName}
					onClick={handleSave}
				>
					{translate("buttons.create_edit")}
				</Button>
			</div>
		</div>
	);
};

export default CreateManualPostClassifier;
