/* eslint-disable react/no-array-index-key */
/* eslint-disable react/require-default-props */
import { Text, Tooltip } from "@mantine/core";
import { IconInfoCircle, IconX } from "@tabler/icons";
import React, { useState, ChangeEvent, KeyboardEvent } from "react";

interface Props {
	error?: string;
	required?: boolean;
	label: string;
	placeholder: string;
	data: string[];
	setData: React.Dispatch<React.SetStateAction<string[]>>;
}

const GatherInputs: React.FC<Props> = ({
	error,
	required = false,
	label,
	placeholder,
	data,
	setData,
}) => {
	const [inputValue, setInputValue] = useState<string>("");

	const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
		setInputValue(e.target.value);
	};

	const handleInputSubmit = () => {
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

	const handleRemoveInput = (input: string) => {
		setData((prevInputs) => prevInputs.filter((e) => e !== input));
	};

	const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
		if (e.key === "Enter" || e.key === " ") {
			handleInputSubmit();
		}
	};

	const handleBlur = () => {
		handleInputSubmit();
	};

	return (
		<div className="mt-3">
			<div className="input">
				<div className="text-[#212529] font-medium inline-block text-sm">
					<label htmlFor="input" className="flex items-center">
						<Tooltip label={placeholder}>
							<span className="flex">
								<IconInfoCircle size={12} />
							</span>
						</Tooltip>
						{label}
						<span className="text-red-500 ml-1">{required && "*"}</span>
					</label>
				</div>
				<div
					className={`min-h-20 flex flex-col p-4 rounded outline-none border border-solid focus-within:shadow-active focus-within:border-[#228BE6] ${error ? "border-[#fa5252]" : "border-[#ced4da]"}`}
				>
					<div className={`flex flex-wrap gap-1 ${data.length > 0 && "mb-3"}`}>
						{data.map((input: string, idx: number) => (
							<div
								key={idx}
								className="flex items-center gap-3 bg-neutral-100 rounded-lg py-1 px-2 text-neutral-800 font-medium text-sm"
							>
								<span>{input}</span>
								<IconX
									size={12}
									className="cursor-pointer"
									onClick={() => handleRemoveInput(input)}
								/>
							</div>
						))}
					</div>
					<input
						type="text"
						value={inputValue}
						onChange={handleInputChange}
						onKeyDown={handleKeyDown}
						onBlur={handleBlur}
						placeholder={placeholder}
						className="w-full text-sm font-normal border-0 rounded-lg focus:outline-none text-neutral-700"
					/>
				</div>
				<Text fz="xs" color="red">
					{error && error}
				</Text>
			</div>
		</div>
	);
};

export default GatherInputs;
