/* eslint-disable react/require-default-props */
import { Tooltip } from "@mantine/core";
import { IconInfoCircle, IconX } from "@tabler/icons";
import React, { useState, ChangeEvent, FormEvent, KeyboardEvent } from "react";

interface Props {
	required?: boolean;
	label: string;
	placeholder: string;
	data: string[];
	setData: React.Dispatch<React.SetStateAction<string[]>>;
}

const GatherInputs: React.FC<Props> = ({
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

	const handleInputSubmit = (e: FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		if (inputValue.trim() !== "") {
			const inputs = inputValue
				.split(",")
				.map((input) => input.trim())
				.filter((input) => input !== "");
			setData((prevInputs) => [...prevInputs, ...inputs]);
			setInputValue("");
		}
	};

	const handleRemoveInput = (input: string) => {
		setData((prevInputs) => prevInputs.filter((e) => e !== input));
	};

	const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
		if (e.key === "Enter") {
			handleInputSubmit(e as any);
		} else if (e.key === " ") {
			handleInputSubmit(e as any);
		}
	};

	return (
		<div className="mt-3">
			<form onSubmit={handleInputSubmit}>
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
					<div className="flex flex-col p-4 rounded outline-none border border-solid focus-within:shadow-active focus-within:border-[#228BE6] border-[#ced4da]">
						<div
							className={`flex flex-wrap gap-1 ${data.length > 0 && "mb-3"}`}
						>
							{data.map((input: string) => (
								<div
									key={input}
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
							placeholder={placeholder}
							className="w-full text-sm font-normal border-0 rounded-lg focus:outline-none text-neutral-700"
						/>
					</div>
				</div>
			</form>
		</div>
	);
};

export default GatherInputs;
