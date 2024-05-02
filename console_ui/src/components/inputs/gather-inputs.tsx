/* eslint-disable react/require-default-props */
/* eslint-disable react/no-array-index-key */
import React, {
	ChangeEvent,
	KeyboardEvent,
	ReactNode,
	useEffect,
	useState,
} from "react";
import {
	Button,
	Text,
	TextInput,
	Group,
	Textarea,
	Box,
	Divider,
} from "@mantine/core";
import {
	IconCircleCheck,
	IconExternalLink,
	IconPencil,
	IconSearch,
	IconTrash,
	IconX,
} from "@tabler/icons";
import { useTranslate } from "@refinedev/core";

interface Props {
	error?: string;
	label: ReactNode;
	placeholder: string;
	data: string[];
	setData: React.Dispatch<React.SetStateAction<string[]>>;
}

const GatherInputs: React.FC<Props> = ({
	error,
	label,
	placeholder,
	data,
	setData,
}) => {
	const translate = useTranslate();
	const [inputValue, setInputValue] = useState<string>("");
	const [searchQuery, setSearchQuery] = useState<string>("");
	const [editIndex, setEditIndex] = useState<number | null>(null);
	const [editedValue, setEditedValue] = useState<string>("");

	const handleInputChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
		setInputValue(e.target.value);
	};

	const handleAddInput = () => {
		if (inputValue.trim() !== "") {
			const inputs = inputValue
				.split(/[,\s]+/) // Split by commas and spaces
				.map((input) => input.trim())
				.filter((input) => input !== "");

			// Create a Set to store unique inputs
			const uniqueInputs = new Set([...data, ...inputs]);

			// Convert Set back to an array
			setData(Array.from(uniqueInputs));

			setInputValue("");
		}
	};

	const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
		if (e.key === "Enter") {
			handleAddInput();
		}
	};

	const handleRemoveInput = (input: string) => {
		setData((prevInputs) => prevInputs.filter((e) => e !== input));
	};

	const handleEditItem = (index: number, newValue: string) => {
		setEditedValue(newValue);
		setEditIndex(index);
	};

	const handleSaveItem = () => {
		if (editedValue.trim() !== "") {
			setData((prevItems) =>
				prevItems.map((item, index) =>
					index === editIndex ? editedValue : item
				)
			);
		}
		setEditIndex(null);
	};

	const filteredItems = data.filter((item) =>
		item.toLowerCase().includes(searchQuery.toLowerCase())
	);

	useEffect(() => {
		setEditIndex(null);
	}, [searchQuery]);

	return (
		<div>
			<Textarea
				mt="lg"
				mb="sm"
				label={label}
				value={inputValue}
				onChange={handleInputChange}
				onKeyDown={handleKeyDown}
				placeholder={placeholder}
				error={error}
			/>
			<Button onClick={handleAddInput} variant="light" mb="md">
				{translate("gathers.fields.input.button_text")}
			</Button>
			{data.length > 0 && (
				<Box
					py={16}
					sx={{
						border: "1px solid rgba(0, 0, 0, 0.1)",
						maxWidth: "fit-content",
					}}
				>
					<div className="flex items-center p-4">
						<TextInput
							mb="sm"
							value={searchQuery}
							onChange={(e) => setSearchQuery(e.currentTarget.value)}
							icon={<IconSearch size={16} />}
							placeholder={translate("gathers.fields.input.search_placeholder")}
							rightSection={
								<IconX
									size={16}
									className="cursor-pointer"
									onClick={() => setSearchQuery("")}
								/>
							}
						/>
					</div>
					{filteredItems.map((item: string, idx: number) => (
						<div key={item} className="pt-2">
							{editIndex === idx ? (
								<TextInput
									mx={16}
									label={translate("gathers.fields.input.edit_input_label")}
									value={editedValue}
									onChange={(e) => setEditedValue(e.currentTarget.value)}
									rightSection={
										<IconCircleCheck
											color="green"
											className="cursor-pointer"
											onClick={handleSaveItem}
										/>
									}
									placeholder={translate(
										"gathers.fields.input.edit_input_label"
									)}
									autoFocus
								/>
							) : (
								<div className="flex items-center justify-between gap-10 px-4">
									<Text>{item}</Text>
									<Group>
										<Button
											p={0}
											variant="subtle"
											onClick={() => handleEditItem(idx, item)}
										>
											<IconPencil color="black" size={16} />
										</Button>
										<Button
											component="a"
											href={item}
											target="_blank"
											rel="noopener noreferrer"
											p={0}
											variant="subtle"
										>
											<IconExternalLink size={16} />
										</Button>
										<Button
											p={0}
											color="red"
											variant="subtle"
											onClick={() => handleRemoveInput(item)}
										>
											<IconTrash
												size={16}
												color="red"
												className="cursor-pointer"
											/>
										</Button>
									</Group>
								</div>
							)}
							{idx < filteredItems.length - 1 && <Divider className="mt-2" />}
						</div>
					))}
				</Box>
			)}
		</div>
	);
};

export default GatherInputs;
