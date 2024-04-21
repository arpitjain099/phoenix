/* eslint-disable react/require-default-props */
/* eslint-disable react/no-array-index-key */
import React, {
	ChangeEvent,
	KeyboardEvent,
	ReactNode,
	useEffect,
	useState,
} from "react";
import { Button, Text, TextInput, List, Group } from "@mantine/core";
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

	const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
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

	const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
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
			<TextInput
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
				<>
					<div className="flex items-center">
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
					<List spacing="md">
						{filteredItems.map((item: string, idx: number) => (
							<List.Item key={item}>
								{editIndex === idx ? (
									<TextInput
										label="Edit item"
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
									<Group position="left" align="center">
										<Text>{item}</Text>
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
								)}
							</List.Item>
						))}
					</List>
				</>
			)}
		</div>
	);
};

export default GatherInputs;
